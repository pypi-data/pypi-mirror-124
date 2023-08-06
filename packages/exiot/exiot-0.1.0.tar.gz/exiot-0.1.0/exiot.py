#! /usr/bin/env python3
"""
Executable I/O Testing Tool (exiot),

The "exiot" is a testing tool to test the executable STDIN, STDOUT, STDERR, and many more.
Tool is parsing provided test scenarios using multiple parsers.

Authors:
- Peter Stanko <peter.stanko0@gmail.com>
"""
import abc
import argparse
import base64
import collections.abc
import copy
import enum
import inspect
import json
import logging
import logging.config
import os
import re
import shlex
import shutil
import string
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional, List, Union, Set, TypeVar, Type, Mapping, Callable, Tuple

##
# Global Definitions
##

PYTHON_REQUIRED = "3.7"
APP_NAME = "exiot"
APP_VERSION = "0.0.1-alpha.3"
APP_DESC = f"""
Executable I/O Testing Tool ({APP_NAME})
is a testing tool to test the executable STDIN, STDOUT, STDERR, and many more.
Tool is parsing provided test scenarios using multiple parsers.
"""

LOG = logging.getLogger(APP_NAME)
FILE_EXTENSIONS = ('.in', '.out', '.err', '.files', '.args', '.exit', '.env')

DParams = Dict[str, Any]

# Logging specific

TRACE = 5
logging.addLevelName(TRACE, 'TRACE')


def log_trace(self, msg, *args, **kwargs):
    self.log(TRACE, msg, args, **kwargs)


logging.Logger.trace = log_trace


##
# Definitions
##


class AsDict:
    """Helper class for the "nicer" serialization - converting objects to the dictionaries
    """

    def as_dict(self, params: Dict = None) -> Dict:
        data = obj_get_props_dict(self)
        if params:
            data.update(params)
        return data

    def d_serialize(self) -> Dict:
        return dict_serialize(self.as_dict())

    def __str__(self) -> str:
        return str(self.d_serialize())

    def __repr__(self):
        return self.__str__()


class RunParams(AsDict):
    def __init__(self, data: DParams):
        tests = data.get('tests_dir', Path.cwd())
        ws = data.get('ws')
        executable = data.get('executable')
        data.update({
            'executable': Path(executable) if executable else None,
            'tests_dir': Path(tests) if tests else Path.cwd(),
            'ws': Path(ws) if ws else Path(tempfile.mkdtemp(prefix=APP_NAME + "-")),
            'timeout': data.get('timeout', 10),
            'valgrind': to_bool(data.get('valgrind', False)),
            'devel_mode': to_bool(data.get('devel_mode', False)),
        })
        self.raw = data

    # paths
    @property
    def executable(self) -> Optional[Path]:
        exe = self.get('executable')
        return Path(exe).resolve() if exe else None

    @property
    def tests_dir(self) -> Path:
        return Path(self.get('tests_dir', Path.cwd()))

    @property
    def ws(self) -> Path:
        return self.raw.get('ws')

    # Runtime config
    @property
    def timeout(self) -> int:
        return int(self.get('timeout', 10))

    @property
    def valgrind(self) -> bool:
        return to_bool(self.get('valgrind', False))

    @property
    def devel_mode(self) -> bool:
        return to_bool(self.get('devel_mode', False))

    def get(self, key: str, default: Any = None) -> Any:
        return self.raw.get(key, default)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def merge(self, other: Union[Mapping, 'RunParams'], override: bool = True) -> 'RunParams':
        if not other:
            return self
        data = other.raw if isinstance(other, RunParams) else other
        new_data = copy.deepcopy(self.raw)
        for key, val in data.items():
            if key in new_data and not override:
                continue
            new_data[key] = val

        return RunParams(new_data)

    def as_dict(self, params: Dict = None) -> Dict:
        return dict_serialize(self.raw)


class EntityNamespace:
    def __init__(self, parent: Optional['EntityNamespace'], current: str):
        # pylint: disable=E0601
        self.parent: Optional['EntityNamespace'] = parent
        self.current: str = current

    @property
    def parts(self) -> List[str]:
        if self.parent is None:
            return [self.current]
        return [*self.parent.parts, self.current]

    def str(self, sep='/') -> str:
        return sep.join(self.parts)

    def __str__(self) -> str:
        return self.str()


EntityDfType = TypeVar('EntityDfType', bound='_EntityDf')


class _EntityDf(AsDict):
    KIND: str = None

    def __init__(self, name: str, desc: str, params: DParams,
                 parent: Optional[EntityDfType]) -> None:
        self.id: str = normalize_string(name, sep='_')
        self.name: str = name
        self.desc: str = desc if desc is not None else name
        self.params: DParams = params or {}
        self._parent: Optional[EntityDfType] = parent
        self._namespace = None

    @property
    def kind(self) -> str:
        return self.KIND

    @property
    def parent(self) -> 'EntityDfType':
        return self._parent

    @parent.setter
    def parent(self, value: 'EntityDfType'):
        self._parent = value
        self._namespace = None

    @property
    def nm(self) -> 'EntityNamespace':
        if self._namespace is None:
            parent = self.parent.nm if self.parent else None
            self._namespace = EntityNamespace(parent, self.id)
        return self._namespace

    def as_dict(self, params: Dict = None) -> Dict[str, Any]:
        params = params if params else {}
        return dict_serialize({
            'kind': self.kind,
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'nm': self.nm.str(),
            'params': self.params,
            **params
        })


class ProjectDf(_EntityDf):
    KIND = 'project'

    @classmethod
    def parse_df(cls, data: Dict[str, Any]) -> 'ProjectDf':
        return cls(name=data['name'], desc=data.get('desc'), params=data.get('params', {}))

    def __init__(self, name: str, desc: str, params: DParams = None):
        super().__init__(name, desc, params, parent=None)
        self._suites: List['SuiteDf'] = []

    @property
    def suites(self) -> List['SuiteDf']:
        return self._suites

    def add_suite(self, *suite: 'SuiteDf') -> None:
        for df in suite:
            df.parent = self
            self.suites.append(df)

    def find_suite(self, sel: str) -> Optional['SuiteDf']:
        for suite in self.suites:
            if sel in (suite.id, suite.name):
                return suite
        return None

    def as_dict(self, params: Dict = None) -> Dict:
        return super().as_dict({'suites': self.suites})


class SuiteDf(_EntityDf):
    KIND = 'suite'

    def __init__(self, name: str, desc: str, stage: List[str] = None,
                 params: DParams = None, parent: Optional[EntityDfType] = None):
        super().__init__(name, desc, params, parent)
        self._stage = stage or []
        self.tests: List['TestDf'] = []

    @property
    def stage(self) -> List[str]:
        return self._stage

    @property
    def project(self) -> Optional['ProjectDf']:
        return self.parent

    def add_test(self, *test: 'TestDf') -> None:
        for tst in test:
            tst.parent = self
            self.tests.append(tst)

    def find_test(self, sel: str) -> Optional['TestDf']:
        for test in self.tests:
            if sel in (test.id, test.name):
                return test
        return None

    def as_dict(self, params: Dict = None) -> Dict:
        return super().as_dict({'tests': self.tests})


class TestDf(_EntityDf):
    KIND = 'test'

    def __init__(self, name: str, desc: str, params: DParams = None, stage: List[str] = None,
                 action: 'ActionDf' = None, parent: Optional[EntityDfType] = None):
        super().__init__(name, desc, params, parent)
        self._preconditions: List['ActionDf'] = []
        self._stage = stage or []
        self._validations: List['ActionDf'] = []
        self._action: Optional['ActionDf'] = None
        self.action = action

    @property
    def suite(self) -> Optional[SuiteDf]:
        return self.parent

    @property
    def stage(self) -> List[str]:
        return self._stage

    @property
    def action(self) -> 'ActionDf':
        return self._action

    @action.setter
    def action(self, act: 'ActionDf'):
        act.parent = self
        self._action = act

    @property
    def preconditions(self) -> List['ActionDf']:
        return self._preconditions

    def add_precondition(self, *preconditions):
        for cond in preconditions:
            cond.parent = self
            self._preconditions.append(cond)

    @property
    def validations(self) -> List['ActionDf']:
        return self._validations

    def add_validation(self, *validations):
        for vld in validations:
            if vld is None:
                continue
            vld.parent = self
            self.validations.append(vld)

    def as_dict(self, params: Dict = None) -> Dict:
        return super().as_dict({
            'preconditions': self.preconditions,
            'action': self.action,
            'validations': self.validations,
        })


class ActionDf(_EntityDf):
    KIND = 'action'

    def __init__(self, name: str, desc: str = None, params: DParams = None,
                 parent: Optional[EntityDfType] = None):
        super().__init__(name, desc, params, parent)

    @property
    def test(self) -> 'TestDf':
        return self.parent


##
# RUNTIME
##

class ResultKind(enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    SKIP = 'skip'

    def is_pass(self) -> bool:
        return self == self.PASS

    def is_fail(self) -> bool:
        return self == self.FAIL

    def is_skip(self) -> bool:
        return self == self.SKIP

    def is_ok(self) -> bool:
        return self.is_skip() or self.is_pass()

    def __str__(self) -> str:
        # pylint: disable=E1101
        return self.value.upper()

    def __repr__(self) -> str:
        return str(self)


RunResultType = TypeVar('RunResultType', bound='_RunResultBase')


class _RunResultBase(AsDict):
    def __init__(self, kind: 'ResultKind' = ResultKind.PASS, msg: str = 'OK', detail: Any = None):
        self.kind: ResultKind = kind
        self.msg: str = msg
        self.detail: Any = detail

    def is_pass(self) -> bool:
        return self.kind.is_pass()

    def is_fail(self) -> bool:
        return self.kind.is_fail()

    def is_skip(self) -> bool:
        return self.kind.is_skip()

    def is_ok(self) -> bool:
        return self.kind.is_ok()


class RunResult(_RunResultBase):
    def __init__(self, kind: 'ResultKind' = ResultKind.PASS,
                 msg: str = 'OK', detail: DParams = None,
                 df: 'EntityDfType' = None):
        super().__init__(kind, msg, detail)
        self.preconditions: List['ActionResult'] = []
        self.df: EntityDfType = df
        self.sub_results: List['RunResultType'] = []

    def add_result(self, res: 'RunResultType') -> None:
        if self.is_pass() and res.is_fail():
            self.kind = ResultKind.FAIL
            self.msg = "One of the sub-results has failed"
        self.sub_results.append(res)

    def add_precondition(self, res: 'ActionResult') -> None:
        if res.is_fail() and self.is_pass():
            self.kind = ResultKind.FAIL
            self.msg = "One of the preconditions has failed"
        self.preconditions.append(res)

    @property
    def n_failed(self) -> int:
        return len([a for a in self.sub_results if a.is_fail()])

    @property
    def n_passed(self) -> int:
        return len([a for a in self.sub_results if a.is_pass()])

    @property
    def n_skipped(self) -> int:
        return len([a for a in self.sub_results if a.is_skip()])

    @property
    def n_oks(self) -> int:
        return len([a for a in self.sub_results if a.is_ok()])

    @property
    def n_subs(self) -> int:
        return len(self.sub_results)


class ProjectResult(RunResult):
    @property
    def suites(self) -> List['SuiteResult']:
        return self.sub_results

    def find_suite(self, sel: str) -> Optional['SuiteResult']:
        for item in self.suites:
            if item.df.id == sel or item.df.name == sel:
                return item
        return None


class SuiteResult(RunResult):
    @property
    def tests(self) -> List['TestResult']:
        return self.sub_results

    def find_test(self, sel: str) -> Optional['TestResult']:
        for test in self.tests:
            if test.df.id == sel or test.df.name == sel:
                return test
        return None


class TestResult(RunResult):
    def __init__(self, kind: 'ResultKind' = ResultKind.PASS, msg: str = None,
                 detail: DParams = None, df: 'EntityDfType' = None):
        super().__init__(kind, msg, detail=detail, df=df)
        self.main_action: Optional['ActionResult'] = None
        self.cmd_res: Optional['CommandResult'] = None

    @property
    def actions(self) -> List['ActionResult']:
        return self.sub_results

    @property
    def n_actions(self) -> int:
        return self.n_subs


class ActionResult(_RunResultBase):
    def __init__(self, kind: 'ResultKind', msg: str, detail: Any = None,
                 df: 'ActionDf' = None):
        super().__init__(kind, msg, detail)
        self.df: 'ActionDf' = df

    @classmethod
    def make_fail(cls, msg: str, df: 'ActionDf', detail: Any = None):
        return ActionResult(kind=ResultKind.FAIL, msg=msg, df=df, detail=detail)

    @classmethod
    def make_pass(cls, msg: str, df: 'ActionDf', detail: Any = None):
        return ActionResult(kind=ResultKind.PASS, msg=msg, df=df, detail=detail)

    def fail_msg(self, fill: str = "") -> str:
        result = ""
        if self.msg:
            result += f"{fill}Message: {self.msg}\n"

        if not self.detail:
            return result

        if isinstance(self.detail, dict):
            for k, v in self.detail.items():
                if not k.startswith('_'):
                    result += f"{fill}{k}: {v}\n"
        return result

    def verbose(self, size: int = 0) -> Optional[str]:
        if not self.detail:
            return None
        verb_func = self.detail.get('_verbose')
        return verb_func(size) if verb_func else None


class CommandResult(AsDict):
    def __init__(self, exit_code: int, stdout: Path, stderr: Path, elapsed: int):
        self.exit: int = exit_code
        self.stdout: Path = stdout
        self.stderr: Path = stderr
        self.elapsed: int = elapsed

    def as_dict(self, params: Dict = None) -> Dict:
        return {
            'exit': self.exit,
            'stdout': str(self.stdout),
            'stderr': str(self.stderr),
            'elapsed': self.elapsed,
        }


class RunCtx:
    @classmethod
    def make_new(cls, df: 'EntityDfType', params: RunParams, parent=None) -> 'RunCtx':
        run_params = params.merge(df.params, override=True)
        return cls(df=df, params=run_params, parent=parent)

    @classmethod
    def from_parent(cls, parent: 'RunCtx', df: 'EntityDfType'):
        return cls.make_new(df, parent.params, parent=parent)

    def __init__(self, df: 'EntityDfType', params: RunParams, parent: Optional['RunCtx'] = None):
        """Creates instance of the Runtime context
        This is not intended to be called directly
        please use `for_*` class methods
        :param df: Definition
        :param params:
        """
        self._df = df
        self.params: RunParams = params
        self.parent: Optional['RunCtx'] = parent

    @property
    def project_df(self) -> Optional['ProjectDf']:
        if isinstance(self.df, ProjectDf):
            return self.df
        return self.suite_df.project if self.suite_df else None

    @property
    def suite_df(self) -> Optional['SuiteDf']:
        if isinstance(self.df, SuiteDf):
            return self.df
        return self.test_df.suite if self.test_df else None

    @property
    def test_df(self) -> Optional['TestDf']:
        return self.df if isinstance(self.df, TestDf) else None

    @property
    def df(self) -> 'EntityDfType':
        return self._df

    @property
    def ws_root_dir(self) -> Path:
        return Path(self.params.ws)

    @property
    def nm(self) -> 'EntityNamespace':
        return self.df.nm

    def ws(self, ensure: bool = False) -> Path:
        if self.suite_df:
            return self.suite_ws(ensure)
        return self.project_ws(ensure)

    def project_ws(self, ensure: bool = False) -> Path:
        path = self.ws_root_dir / self.project_df.name
        if ensure and not path.exists():
            path.mkdir(parents=True)
        return path

    def suite_ws(self, ensure: bool = False) -> Path:
        path = self.project_ws(ensure=ensure)
        if not self.suite_df:
            LOG.error("[WS] Suite not set - this should never happen!")
            assert self.suite_df is not None
        path /= self.suite_df.id
        if ensure and not path.exists():
            path.mkdir(parents=True)
        return path

    def make_result(self) -> 'RunResultType':
        if self.test_df is not None:
            return TestResult(df=self.test_df)
        if self.suite_df is not None:
            return SuiteResult(df=self.suite_df)
        return ProjectResult(df=self.project_df)

    def stage_files(self, stage_patterns: List['str']):
        suite_ws = self.suite_ws(True)
        for stage in stage_patterns:
            files = self.data_dir.glob(stage)
            for f in files:
                LOG.debug("[STAGE] File for '%s' - from '%s' to '%s'", self.nm, f, suite_ws)
                shutil.copy2(f, suite_ws)

    @property
    def tests_dir(self) -> Path:
        return self.params.tests_dir

    @property
    def data_dir(self) -> Path:
        return self.params.tests_dir / self.params.get('data_subdir', '')

    def resolve_data_file(self, exp: Path) -> Optional[Path]:
        if exp is None:
            return None
        exp = Path(exp)
        if exp.is_absolute() and exp.exists():
            return exp
        if exp.exists():
            return exp
        data = self.data_dir / exp
        if data.exists():
            return data
        data = self.tests_dir / exp
        if data.exists():
            return data
        return self.data_dir / exp


class ProjectRunner:
    def __init__(self, app_params: 'RunParams', project: ProjectDf):
        self.run_params = app_params
        self.df = project

    def run(self) -> 'ProjectResult':
        ctx = RunCtx.make_new(self.df, params=self.run_params)
        LOG.info("[RUN] Project: '%s'", ctx.nm)
        result = ctx.make_result()

        for suite in self.df.suites:
            suite_runner = SuiteRunner(suite=suite, project_ctx=ctx)
            suite_res = suite_runner.run()
            LOG.debug("[RUN] Suite '%s' result: %s", ctx.nm, suite_res)
            result.add_result(suite_res)

        return result


class SuiteRunner:
    def __init__(self, project_ctx: 'RunCtx', suite: 'SuiteDf'):
        self.df = suite
        self.project_ctx = project_ctx

    def run(self) -> 'SuiteResult':
        ctx = RunCtx.from_parent(self.project_ctx, self.df)
        LOG.info("[RUN] Suite: '%s'", ctx.nm)
        result = ctx.make_result()
        ctx.stage_files(self.df.stage)
        for test in self.df.tests:
            test_runner = TestRunner(ctx, test)
            test_result = test_runner.run()
            LOG.debug("[RUN] Test '%s' result [%s]: %s",
                      ctx.nm, test_result.kind, test_result)
            result.add_result(test_result)
        return result


class TestRunner:
    def __init__(self, suite_ctx: 'RunCtx', test: 'TestDf'):
        self.suite_ctx = suite_ctx
        self.df = test

    def run(self) -> 'TestResult':
        # pylint: disable=W0201
        ctx = RunCtx.from_parent(self.suite_ctx, self.df)
        LOG.info("[RUN] Test: '%s'", ctx.nm)
        result: TestResult = ctx.make_result()
        ctx.stage_files(self.df.stage)

        for pre in self.df.preconditions:
            pc_res = _run_action(ctx, pre, cmd_res=None)
            result.add_precondition(pc_res)

        if result.is_fail():
            LOG.warning("[RUN] Preconditions for '%s' has failed", ctx.nm)
            return result

        main_result = _run_action(ctx, self.df.action, None)
        result.main_action = main_result
        result.cmd_res = main_result.detail
        if main_result.is_fail():
            LOG.warning("Main action has failed - this should not happened")
            result.add_result(main_result)
            return result

        for validation in self.df.validations:
            validation_res = _run_action(ctx, validation, main_result.detail)
            result.add_result(validation_res)

        return result


def _run_action(ctx: 'RunCtx', action_df: 'ActionDf', cmd_res=None) -> 'ActionResult':
    register = ActionsRegister.instance()
    action = register.get(action_df.id)
    if not action:
        LOG.error("[RUN] Unable to find action: '%s'", action_df.id)
        return ActionResult.make_fail(f"Unable to find action: {action_df.id}", df=action_df)
    try:
        return action(ctx, action_df, cmd_res=cmd_res).invoke()
    except Exception as ex:
        LOG.error("ERROR: Action '%s' execution error: %s", action_df.id, ex)
        if ctx.params.get('devel_mode', False):
            raise ex
        return ActionResult.make_fail("ERROR: Action execution error", df=action_df,
                                      detail={'error': ex})


##
# ACTIONS
##

ActionType = TypeVar('ActionType', bound='GeneralAction')


class GeneralAction:
    NAME = 'nop'

    @classmethod
    def _make_df(cls, params: DParams, desc: str = None) -> 'ActionDf':
        return ActionDf(name=cls.NAME, desc=desc, params=params)

    def __init__(self, ctx: 'RunCtx', action_df: 'ActionDf',
                 cmd_res: Optional['CommandResult'] = None):
        self.ctx = ctx
        self.df = action_df
        self.cmd_res = cmd_res

    @property
    def params(self) -> DParams:
        return self.df.params

    def invoke(self) -> 'ActionResult':
        LOG.info("[RUN] Executing action '%s'", self.df.name)
        LOG.debug("[RUN] Action '%s' with params: %s", self.df.name, self.params)
        result = self._run()
        if result is None:
            result = self._make_skip("No result provided, skipping action")
        _log = LOG.debug if result.is_ok() else LOG.warning
        _log("[ACT] Action Result [%s] for '%s::%s'",
             result.kind, self.ctx.nm, self.NAME)
        LOG.trace("-> Result info: %s", result)
        return result

    def _run(self) -> 'ActionResult':
        return ActionResult.make_pass("Nothing to do", df=self.df)

    def _make_fail(self, msg: str, detail: Any = None):
        return self._make_result(False, msg=msg, detail=detail)

    def _make_skip(self, msg: str, detail: Any = None):
        return ActionResult(ResultKind.SKIP, msg=msg, df=self.df, detail=detail)

    def _make_pass(self, msg: str, detail: Any = None):
        return self._make_result(True, msg=msg, detail=detail)

    def _make_result(self, pred: bool, msg: str, detail: Any = None) -> 'ActionResult':
        kind = ResultKind.PASS if pred else ResultKind.FAIL
        return ActionResult(kind, msg=msg, df=self.df, detail=detail)


class ExecAction(GeneralAction):
    NAME = 'cmd_exec'
    """Execute Command/Executable action
    Kind: cmd_exec

    Params:
    - args(List[str]): Command Line arguments
    - env(Dict): Optional environment variables
    - stdin(Path|str|dict): Standard input

    params:
    - executable: Executable to be executed
    - timeout: Executable runtime timeout
    """

    @classmethod
    def make_df(cls, args: List[str], stdin: Union[Dict, str, Path], env: DParams) -> 'ActionDf':
        return cls._make_df({'args': args, 'stdin': stdin, 'env': env}, desc="Execute command")

    def _run(self) -> 'ActionResult':
        exe = self._get_executable()
        if not exe:
            return self._make_fail("Executable not set")
        args = self._get_args()
        stdin = self._get_stdin_dict()
        env = self._get_env()
        ws = self.ctx.ws(ensure=True)

        try:
            cmd_res = execute_cmd(
                exe,
                args=args,
                ws=ws,
                nm=self.ctx.test_df.id,
                env=env,
                cwd=ws,
                timeout=self.ctx.params.get('timeout', 5),
                **stdin,
            )
        except FileNotFoundError as ex:
            return self._make_fail(f"Command not found '{exe}': {ex}", detail=ex)

        except Exception as ex:
            return self._make_fail(f"Command failed '{exe}': {ex}", detail=ex)

        return self._make_pass("Command executed", detail=cmd_res)

    def _get_env(self) -> DParams:
        params_env = self.params.get('env')
        return params_env

    def _get_executable(self) -> str:
        return self.ctx.params.get('executable')

    def _get_args(self) -> List[str]:
        return self.params.get('args', [])

    def _get_stdin_dict(self) -> Dict:
        stdin = self.df.params.get('stdin')
        if not stdin or stdin == 'empty':
            return {'input': b''}
        if isinstance(stdin, (str, Path)):
            return {'stdin': self.ctx.resolve_data_file(stdin)}
        if isinstance(stdin, (dict, collections.abc.Mapping)):
            if 'file' in stdin:
                return {'stdin': self.ctx.resolve_data_file(stdin['file'])}
            if 'content' in stdin:
                content: str = stdin['content']
                return {'input': content.encode(encoding='utf-8')}
        return {}


class FileValidation(GeneralAction):
    NAME = 'file_validation'
    """Validate content of the file
    Kind: file_validation
    Params:
    - expected(dict): Expected file/content definition
    - selector(str): Select the "executable generated file" to compare against
        Special: @stdout, @stderr - standard output/error output files
    """

    @classmethod
    def make_df(cls, expected: Dict[str, Any], selector: str) -> ActionDf:
        return cls._make_df({
            'expected': expected,
            'selector': selector,
        }, desc=f"SELECTOR: {selector}")

    @classmethod
    def parse(cls, expected: Union[Dict, str, Path], selector: str) -> Optional['ActionDf']:
        expected = expected if expected else {'empty': True}
        if isinstance(expected, str):
            if expected == 'any':
                return None
            if expected == 'empty':
                expected = {'empty': True}
            elif expected in ['nonempty', 'non-empty']:
                expected = {'empty': False}
            else:
                expected = {'file': expected}
        return cls.make_df(expected, selector)

    def _run(self) -> 'ActionResult':
        provided = self._get_by_selector()
        exp = self.params.get('expected', {'empty': True})
        return self._resolve_dict(exp, provided)

    def _resolve_file_size(self, exp: Dict) -> str:
        empty = exp.get('empty')
        if empty is not None:
            return '== 0' if empty else '!= 0'

        size = exp.get('size')
        return f'== {int(size)}' if size is not None else None

    def _resolve_dict(self, exp: Dict, provided: Path):
        if exp.get('any'):
            return self._make_pass('Not checking file content')

        size_expr = self._resolve_file_size(exp)
        if size_expr is not None:
            return self._compare_file_size(provided, expr=size_expr)

        match = exp.get('match')
        if match is not None:
            return self._match_file_content(provided, pattern=match)

        content = self._resolve_raw_file_content(exp)

        if content is not None:
            fp = self._make_expected_output(content)
        else:
            fp = exp.get('file', exp.get('path'))

        if fp:
            return self._compare_file_content(provided, exp=Path(fp))
        return None

    def _resolve_raw_file_content(self, exp: Dict[str, Any]) -> str:
        b64cont = exp.get('base64', exp.get('b64'))
        if b64cont is not None:
            return base64.b64decode(b64cont).decode('utf-8')
        return exp.get('content', exp.get('text'))

    def _compare_file_size(self, provided: Path, expr: str):
        provided_size = os.path.getsize(str(provided))
        full_expr = f"{provided_size} {expr}"
        result = safer_eval_cond(full_expr)

        return self._make_result(result, msg="File size mismatch", detail={
            'expected': full_expr,
            'provided': provided_size,
            'provided_file': provided,
            'expr': full_expr,
            '_verbose': lambda s: _verbose_wrap('FILE CONTENT', _trunc_read(provided, s))
        })

    def _compare_file_content(self, provided: Path, exp: Path) -> 'ActionResult':
        exp = self.ctx.resolve_data_file(exp)
        diff_params: List[str] = self.ctx.params.get('diff_params', [])
        diff_params.append('--strip-trailing-cr')
        diff_exec = execute_cmd(
            'diff',
            args=['-u', *diff_params, str(exp), str(provided)],
            ws=self.ctx.ws(),
            nm=f"diff-{self.ctx.nm.current}"
        )
        detail = {
            'expected': str(exp),
            'provided': str(provided),
            'diff': str(diff_exec.stdout),
            'diff_exit': diff_exec.exit,
            'additional': diff_exec.as_dict(),
            '_verbose': lambda s: _verbose_wrap('DIFF', _trunc_read(diff_exec.stdout, s))
        }
        return self._make_result(
            diff_exec.exit == 0,
            msg="Files content is not a same!",
            detail=detail
        )

    def _get_by_selector(self) -> Path:
        selector = self.params.get('selector')
        if selector == '@stdout':
            return self.cmd_res.stdout

        if selector == '@stderr':
            return self.cmd_res.stderr

        sel_pth = Path(selector)
        if sel_pth.is_absolute():
            return sel_pth

        return self.ctx.ws() / selector

    def _make_expected_output(self, content: Union[str, bytes]) -> Path:
        selector: str = self.params.get('selector')
        selector = selector[1:] if selector.startswith('@') else selector
        tid = self.df.test.id
        full_name = "{}_{}.exp".format(normalize_string(tid, max_len=150),
                                       normalize_string(selector, max_len=70))
        pth = self.ctx.ws(True) / full_name
        if isinstance(content, bytes):
            pth.write_bytes(content)
        else:
            pth.write_text(content)
        return pth

    def _match_file_content(self, provided, pattern: str) -> 'ActionResult':
        result = re.match(pattern, provided.read_text('utf-8'))
        return self._make_result(
            bool(result),
            "File content does not match the expected pattern",
            detail={
                'expected': pattern,
                'provided': str(provided),
            }
        )


class ExitCodeValidation(GeneralAction):
    NAME = 'exit_validation'
    """Exit code validation to validate executable exit code
    Name: exit_validation
    Params:
    - expected(int): Expected exit code, special value (any) - it will not be checked
    """

    @classmethod
    def parse(cls, code: Union['str', int]) -> Optional['ActionDf']:
        if code is None:
            return cls.make_df(0)

        if isinstance(code, int):
            return cls.make_df(code)

        if code == 'any':
            return None

        return cls.make_df(int(code))

    @classmethod
    def make_df(cls, expected: int) -> ActionDf:
        return cls._make_df({
            'expected': expected,
        }, desc=f"EXIT_CODE: {expected}")

    def _run(self) -> 'ActionResult':
        exit_code = self.params.get('expected')
        provided = self.cmd_res.exit
        if exit_code == 'any':
            return self._make_pass("Exit code is not checked")
        if exit_code in ['non-zero', 'nonzero']:
            expr = f'{provided} != 0'
        else:
            expr = f'{provided} == {int(exit_code)}'
        result = safer_eval_cond(expr)
        return self._make_result(result, msg="Exit code mismatch", detail={
            'expected': exit_code,
            'provided': provided,
            'expr': expr
        })


class ActionsRegister:
    INSTANCE = None

    @classmethod
    def instance(cls) -> 'ActionsRegister':
        if cls.INSTANCE is None:
            cls.INSTANCE = cls.make()
        return cls.INSTANCE

    @classmethod
    def make(cls) -> 'ActionsRegister':
        instance = ActionsRegister()
        instance.add(ExecAction)
        instance.add(FileValidation)
        instance.add(ExitCodeValidation)
        return instance

    def __init__(self):
        self.register: Dict[str, Type[GeneralAction]] = {}

    def add(self, action: Type[ActionType]):
        self.register[action.NAME] = action

    def get(self, kind: str) -> Optional[Type[ActionType]]:
        return self.register.get(kind)


##
# PARSERS
##

class DefinitionParser:
    NAME = None

    def __init__(self, params: RunParams):
        self.params: RunParams = params
        self.log = LOG

    @property
    def tests_dir(self) -> Path:
        return self.params.tests_dir

    @abc.abstractmethod
    def parse(self) -> Optional[ProjectDf]:
        return None


class DirectoryTestsParser(DefinitionParser):
    NAME = 'dir'

    def parse(self) -> Optional['ProjectDf']:
        if not self.tests_dir.exists():
            self.log.error("[PARSE] Specified folder not found: '%s'", self.tests_dir)
            return None
        self.log.info("[PARSE] Project '%s' in folder: '%s'",
                      self.tests_dir.name, self.tests_dir)
        project = ProjectDf(name=self.tests_dir.name, desc=f'Project {self.tests_dir.name}')
        project.add_suite(*self._gather_suites())
        return project

    def _gather_suites(self) -> List['SuiteDf']:
        root_suite = self._parse_suite(self.tests_dir)
        result = [root_suite] if root_suite.tests else []
        for sub in self.tests_dir.glob("*/"):
            if self._should_exclude(sub):
                continue
            suite = self._parse_suite(sub)
            if suite.tests:
                result.append(suite)
        return result

    def _should_exclude(self, sub: Path) -> bool:
        # pylint: disable=R0201
        name = sub.name
        return not sub.is_dir() or name.startswith('.') or name.startswith('_')

    def _parse_suite(self, folder: Path) -> 'SuiteDf':
        name = folder.name
        self.log.info("[PARSE] Suite '%s' in folder: '%s'", name, folder)
        stage = _parse_lines(_resolve_file(folder, name, ext='stage'))
        if stage:
            self.log.debug("[PARSE] Suite '%s' files to stage: '%s'", name, stage)
        suite = SuiteDf(name=name, desc=f'Suite {name} for {folder}', stage=stage)
        suite.add_test(*self._gather_tests(folder))
        return suite

    def _gather_tests(self, folder: Path) -> List[TestDf]:
        names = self._gather_test_names(folder)
        return [self._parse_test(folder, name) for name in names]

    def _parse_test(self, folder: Path, name: str):
        self.log.info("[PARSE] Test '%s'", name)
        action = ExecAction.make_df(
            args=_parse_lines(_resolve_file(folder, name, ext='args')),
            stdin=_resolve_file(folder, name, ext='in'),
            env=_parse_env(_resolve_file(folder, name, ext='env'))
        )
        stage = _parse_lines(_resolve_file(folder, name, ext='stage'))
        if stage:
            self.log.debug("[PARSE] Test '%s' files to stage: %s", name, stage)
        test = TestDf(
            name=name,
            desc=f"Test Case '{name}' for '{folder.name}'",
            action=action,
            stage=stage
        )
        validations = self._parse_validations(folder, name)
        test.add_validation(*validations)
        return test

    def _parse_validations(self, folder: Path, name: str):
        def _rslv_out(pth: Optional[Path]) -> Dict[str, Any]:
            return {'file': pth} if pth else {'empty': True}

        validations = [
            # STDOUT
            FileValidation.make_df(
                _rslv_out(_resolve_file(folder, name, 'out', None)),
                selector='@stdout',
            ),
            # STDERR
            FileValidation.make_df(
                _rslv_out(_resolve_file(folder, name, 'err', None)),
                selector='@stderr',
            ),
            # EXIT CODE (the main original RETURN VALUE)
            ExitCodeValidation.parse(_parse_exit(_resolve_file(folder, name, 'exit'), 0)),
        ]

        files_map = _parse_files_map(_resolve_file(folder, name, 'files', None))
        for f_map in files_map:
            exp_path = folder / f_map['expected']
            if not exp_path.exists():
                self.log.warning("[PARSE] File mapping - '%s' does not exists!", exp_path)
                continue
            self.log.debug("[PARSE] Validation files mapping: %s", f_map)
            validations.append(
                FileValidation.make_df(
                    expected={'file': exp_path},
                    selector=f_map['provided']
                )
            )
        return validations

    def _gather_test_names(self, folder: Path) -> Set[str]:
        names = set()
        self.log.debug("Gathering tests in: '%s'", folder)
        for pth in folder.glob("*.*"):
            if pth.suffix in FILE_EXTENSIONS:
                names.add(pth.stem)
            if pth.suffix in ['.exp', '.expected']:
                # handle expected file - in format <TEST_NAME>.<OUTPUT_FILE>.exp
                parts = pth.stem.split(".")
                if len(parts) > 1:
                    names.add(parts[0])
        self.log.debug("Found tests: %s", names)
        return names


class MiniHwParser(DirectoryTestsParser):
    NAME = "minihw"

    def _should_exclude(self, sub: Path):
        return not sub.is_dir() or not sub.name.lower().startswith("task")

    def _parse_suite(self, folder: Path) -> 'SuiteDf':
        suite = super()._parse_suite(folder)
        task_name = suite.name
        target = self.params.get('target', 'source')
        task_build_dir = self.tests_dir / 'build' / task_name / f"{task_name}-{target}"
        suite.params['executable'] = task_build_dir
        return suite


class FileScenarioDefParser(DefinitionParser):
    NAME = 'scenario'

    def parse(self) -> Optional['ProjectDf']:
        proj_file = self._find_project_file() or {}
        project = self._make_project(proj_file)
        suites_prop = proj_file.get('suites', [])
        self.parse_suite_files(project, suites_prop)
        return project

    def _make_project(self, proj_file):
        proj_prop = proj_file.get('project', {})
        project = ProjectDf(
            name=proj_prop.get('name', self.tests_dir.name),
            desc=proj_prop.get('desc'),
            params=proj_file.get('params')
        )
        return project

    def _find_project_file(self) -> Optional[Dict[str, Any]]:
        files = self.tests_dir.glob('project*.*')
        if not files:
            return None
        result = []
        for proj_file in files:
            parsed = load_def_file(proj_file)
            if not parsed:
                continue
            if 'project' in parsed:
                parsed['project_file'] = proj_file
                LOG.info("[PARSE] Project File: '%s'", proj_file)
                result.append(parsed)
        if len(result) > 1:
            LOG.warning("There are multiple projects found - this should not happen. "
                        "The first one will be used: %s",
                        result[0]['project_file'])
        return result[0] if result else None

    def parse_suite_files(self, project: ProjectDf, suites_list: List[str]) -> List['SuiteDf']:
        suite_files = self._find_suite_files(suites_list)
        suites = []
        for suite_file in suite_files:
            LOG.info("[PARSE] Suite File: '%s'", suite_file)
            suite_def = load_def_file(suite_file)
            if not suite_def or 'suite' not in suite_def:
                continue
            suite = self.parse_suite(project, suite_def)
            if suite:
                suites.append(suite)

        return suites

    def _find_suite_files(self, suites_list: List[str]):
        result = []
        for pat in suites_list:
            files = self.tests_dir.glob(pat)
            if files:
                result.extend(files)
        return result

    def parse_suite(self, project: ProjectDf, sfd: Dict[str, Any]) -> 'SuiteDf':
        LOG.debug("[PARSE] Suite: '%s'", sfd)
        suite_prop = sfd['suite']
        stage_prop = sfd.get('data', sfd.get('stage'))
        suite = SuiteDf(
            name=suite_prop['name'],
            desc=suite_prop.get('desc'),
            stage=stage_prop,
            params=sfd.get('params')
        )
        project.add_suite(suite)
        tests_list = sfd.get('tests')
        for test_def in tests_list:
            self.parse_test(suite, test_def)
        return suite

    def parse_test(self, suite: SuiteDf, tdf: Dict[str, Any]) -> 'TestDf':
        params = tdf.get('params', {})
        test = TestDf(
            name=tdf['name'],
            desc=tdf.get('desc'),
            params=params,
            stage=tdf.get('data', tdf.get('stage')),
            action=self.parse_action(tdf)
        )
        vals_prop = tdf.get('validations', [])
        for val in vals_prop:
            test.add_validation(self._parse_explicit_action(val))
        self._add_default_validations(tdf, test)
        suite.add_test(test)
        return test

    def _add_default_validations(self, test_d, test: 'TestDf'):
        test.add_validation(
            FileValidation.parse(expected=test_d.get('out'), selector='@stdout'),
            FileValidation.parse(expected=test_d.get('err'), selector='@stderr'),
            ExitCodeValidation.parse(test_d.get('exit', 0)),
        )

        for f in test_d.get('files', []):
            test.add_validation(
                FileValidation.parse(
                    expected=f.get('exp', f.get('expected', f.get('e'))),
                    selector=f.get('provided', f.get('prov', f.get('p'))),
                )
            )
        self.log.trace("[PARSE] Default Validations for '%s': %s", test.nm, test.validations)

    def parse_action(self, test_df: Dict[str, Any]) -> ActionDf:
        act = test_df.get('action')
        if act:
            return self._parse_explicit_action(act)

        return ExecAction.make_df(
            args=test_df.get('args'),
            stdin=test_df.get('in'),
            env=test_df.get('env'),
        )

    def _parse_explicit_action(self, act) -> 'ActionDf':
        self.log.debug("[PARSE] Action: %s", act)
        if isinstance(act, str):
            act = {'name': act, 'desc': f'Action {act}'}
        return ActionDf(name=act['name'], desc=act.get('desc'), params=act.get('params'))


class AutoScenarioParser(DefinitionParser):
    NAME = 'auto'

    def parse(self) -> Optional[ProjectDf]:
        parser = self._select()
        return parser(self.params).parse()

    def _select(self) -> Type[DefinitionParser]:
        for ext in ('yml', 'yaml', 'json'):
            glob = list(self.tests_dir.glob(f'project*.{ext}'))
            if len(glob) > 0:
                return FileScenarioDefParser

        tests = list(self.tests_dir.glob('task*'))
        if tests:
            if (tests[0] / 'source.c').exists():
                return MiniHwParser

        return DirectoryTestsParser


PARSERS = {c.NAME: c for c in [
    MiniHwParser,
    DirectoryTestsParser,
    FileScenarioDefParser,
    AutoScenarioParser,
]}


##
# UTILITIES
##

def dict_serialize(obj, as_dict_skip: bool = False) -> Any:
    if obj is None or isinstance(obj, (str, int)):
        return obj
    if isinstance(obj, list):
        return [dict_serialize(i) for i in obj]

    if isinstance(obj, set):
        return {dict_serialize(i) for i in obj}

    if isinstance(obj, dict):
        return {k: dict_serialize(v) for k, v in obj.items()}

    if isinstance(obj, enum.Enum):
        return obj.value

    if not as_dict_skip and isinstance(obj, AsDict):
        return obj.as_dict()

    if hasattr(obj, '__dict__'):
        return {k: dict_serialize(v) for k, v in obj.__dict__.items()}

    return str(obj)


_KT = Union[str, List[str]]


def dict_set(orig: Dict[str, Any], key: _KT, value: Any, sep: str = '.') -> Dict[str, Any]:
    if not key:
        return orig
    orig = orig if orig is not None else {}
    if isinstance(key, str):
        key = key.split(sep)
    current = orig
    for idx, kpart in enumerate(key):
        if idx == (len(key) - 1):
            break
        if current is None:
            current = {kpart: {}}
        if isinstance(current, dict):
            part = current.get(kpart)
            if part is None:
                current[kpart] = {}
        if isinstance(current, list):
            kpart = int(kpart)
            part = current[kpart]
            if part is None:
                current[kpart] = {}
        current = current[kpart]
    current[key[len(key) - 1]] = value
    return orig


def dict_get(orig: Dict[str, Any], key: _KT, sep: str = '.', default: Any = None) -> Optional[Any]:
    if not orig:
        return default

    if not key:
        return orig

    if isinstance(key, str):
        key = key.split(sep)

    current = orig
    for idx, kpart in enumerate(key):
        if isinstance(current, dict):
            if kpart not in current:
                return default
        if isinstance(current, list):
            kpart = int(kpart)
            if kpart >= len(current):
                return default
        current = current[kpart]
    return current


def dict_dump_dotted(orig: Any, prefix: str = '') -> List[Tuple[str, Any]]:
    coll = None
    if isinstance(orig, dict):
        coll = orig.items()
    if isinstance(orig, list):
        coll = enumerate(orig)

    if not coll or not orig:
        return [(f'{prefix}', orig)]

    buffer = []
    for k, v in coll:
        fk = f'{prefix}.{k}' if prefix else k
        buffer += dict_dump_dotted(v, fk)
    return buffer


def dump_config(data, fmt: str = 'dot', nones=False):
    if fmt in ('json', 'j'):
        print(json.dumps(data, indent=2))
    elif fmt in ('yml', 'y', 'yaml'):
        import yaml
        print(yaml.dump(data))
    else:  # Dot format
        for k, v in dict_dump_dotted(data):
            if nones or v is not None:
                print(f"{k}: {v}" if k else v)


def dict_rec_subst(orig: Dict[str, Any], resolved=None) -> Dict[str, Any]:
    resolved = resolved if resolved else {}
    not_resolved = set(orig.keys())

    while not_resolved:
        cp = not_resolved.copy()
        for k in cp:
            if k not in not_resolved:
                continue
            v = orig[k]
            if isinstance(v, dict):
                not_resolved.remove(k)
                resolved[k] = dict_rec_subst(v)
            if not isinstance(v, str):
                not_resolved.remove(k)
                resolved[k] = v
                continue
            t = string.Template(v)
            try:
                resolved[k] = t.substitute(resolved)
                not_resolved.remove(k)
            except KeyError:
                continue
        if cp == not_resolved:
            for nrk in not_resolved:
                resolved[nrk] = orig[nrk]
            break

    return resolved


def obj_get_props_dict(obj: object) -> Dict[str, Any]:
    cls = obj.__class__
    props = inspect.getmembers(cls, lambda o: isinstance(o, property))
    res = {}
    for name, prop in props:
        res[name] = prop.fget(obj)
    return res


def dump_as_dict(dictionary, frm: str = 'json', indent: int = 4, **kwargs) -> str:
    data = dict_serialize(dictionary)
    frm = frm.lower()

    if frm in ('yaml', 'yml', 'y'):
        try:
            import yaml
            return yaml.safe_dump(data=data, **kwargs)
        except ImportError:
            LOG.error("YAML definitions require package: PyYaml")

    return json.dumps(data, indent=indent, **kwargs)


def load_def_file(file: Path) -> Optional[Dict[str, Any]]:
    if not file.exists():
        LOG.warning("Provided file '%s' not found", file.suffix)
        return None
    with file.open('r') as fd:
        if file.suffix == '.json':
            return json.load(fd)
        if file.suffix in ['.yml', '.yaml']:
            try:
                import yaml
                return yaml.safe_load(fd)
            except ImportError:
                LOG.error("YAML definitions require package: PyYaml")
                return None
        LOG.error("Unsupported file format '%s' for definition", file.suffix)
        return None


def _resolve_file(folder: Path, name: str, ext: str, default: Any = None) -> Optional[Path]:
    fpath = folder / f"{name}.{ext}"
    if fpath.exists():
        return fpath
    return default


def _parse_lines(f: Optional[Path]) -> List[str]:
    return list(f.read_text('utf-8').splitlines(keepends=False)) if f else []


def _parse_exit(f: Optional[Path], default: int = 0) -> str:
    return f.read_text("utf-8") if f else default


def _parse_files_map(file: Optional[Path]) -> List[Dict[str, str]]:
    if not file:
        return []
    result = []
    with file.open('r') as fd:
        for line in fd:
            line = line.strip()
            if not line or line.startswith("#") or ';' not in line:
                continue
            parts = line.split(';')
            result.append({'expected': parts[0].strip(), 'provided': parts[1].strip()})
    return result


def _parse_env(file: Optional[Path]) -> DParams:
    if not file:
        return {}
    env_re = re.compile(r'''^([^\s=]+)=[\s"']*(.+?)[\s"']*$''')
    result = {}
    with file.open('r') as fd:
        for line in fd:
            match = env_re.match(line)
            if match is not None:
                result[match.group(1)] = match.group(2)
    return result


def _trunc_read(provided: Path, size: int = 0):
    with provided.open('r') as fd:
        data = fd.read(size)
        if len(data) == size:
            data += "\n...TRUNCATED...\n"
        return data


def _verbose_wrap(section: str, data: str, spc='#'):
    section = section.upper()
    spc = spc * 3
    return f'{spc} {section} {spc}\n{data}\n{spc} END {section} {spc}\n'


def execute_cmd(cmd: str, args: List[str], ws: Path, stdin: Optional[Path] = None,
                stdout: Path = None, stderr: Path = None, nm: str = None,
                log: logging.Logger = None, timeout: int = 60,
                env: Dict[str, Any] = None, cwd: Union[str, Path] = None,
                **kwargs) -> 'CommandResult':
    # pylint: disable=R0914,R0913
    log = log or LOG
    log.info("[CMD] Exec: '%s' with args %s", cmd, str(args))
    log.debug(" -> [CMD] Exec STDIN: '%s'", stdin if stdin else "EMPTY")
    log.trace(" -> [CMD] Exec with timeout %d, cwd: '%s'", timeout, cwd)
    nm = nm or cmd
    stdout = stdout or ws / f'{nm}.stdout'
    stderr = stderr or ws / f'{nm}.stderr'

    full_env = {**os.environ, **(env or {})}

    with stdout.open('w') as fd_out, stderr.open('w') as fd_err:
        fd_in = Path(stdin).open('r') if stdin else None
        start_time = time.perf_counter_ns()
        try:
            exec_result = subprocess.run(
                [cmd, *args],
                stdout=fd_out,
                stderr=fd_err,
                stdin=fd_in,
                timeout=timeout,
                env=full_env,
                check=False,
                cwd=str(cwd) if cwd else None,
                **kwargs
            )
        except Exception as ex:
            log.error("[CMD] Execution '%s' failed: %s", cmd, ex)
            raise ex
        finally:
            end_time = time.perf_counter_ns()
            if fd_in:
                fd_in.close()

    log.debug("[CMD] Result[exit=%d]: %s", exec_result.returncode, str(exec_result))
    log.trace(" -> Command stdout '%s'", stdout)
    log.trace("STDOUT: %s", stdout.read_bytes())
    log.trace(" -> Command stderr '%s'", stderr)
    log.trace("STDERR: %s", stderr.read_bytes())

    return CommandResult(
        exit_code=exec_result.returncode,
        elapsed=end_time - start_time,
        stdout=stdout,
        stderr=stderr,
    )


SAFE_CHARS = string.digits + string.ascii_letters + '_!-.@'


def normalize_string(original: str, sep: str = '_', max_len: int = 0) -> str:
    spaces_removed = sep.join(original.split())
    res = "".join([c for c in spaces_removed if c in SAFE_CHARS])
    max_len = 0 if max_len is None or max_len <= 0 else max_len
    return res[:max(max_len, len(res))] if max_len > 0 else res


def to_bool(val: Any) -> bool:
    if val is None:
        return False

    if isinstance(val, str):
        return val.lower() in ('y', 'on', 'yes', 'enable', 'true', 't')

    return bool(val)


def safer_eval(expr: str, variables: Any = None) -> Any:
    # license: MIT (C) tardyp
    """
    Safely evaluate a a string containing a Python
    expression.  The string or node provided may only consist of the following
    Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
    and None. safe operators are allowed (and, or, ==, !=, not, +, -, ^, %, in, is)
    """
    import ast
    _safe_names = {'None': None, 'True': True, 'False': False}
    _safe_nodes = (
        'Add', 'And', 'BinOp', 'BitAnd', 'BitOr', 'BitXor', 'BoolOp',
        'Compare', 'Dict', 'Eq', 'Expr', 'Expression', 'For',
        'Gt', 'GtE', 'Is', 'In', 'IsNot', 'LShift', 'List',
        'Load', 'Lt', 'LtE', 'Mod', 'Name', 'Not', 'NotEq', 'NotIn',
        'Num', 'Or', 'RShift', 'Set', 'Slice', 'Str', 'Sub',
        'Tuple', 'UAdd', 'USub', 'UnaryOp', 'boolop', 'cmpop',
        'expr', 'expr_context', 'operator', 'slice', 'unaryop',
        'Constant', 'Mult', 'Pow', 'Div')
    node = ast.parse(expr, mode='eval')
    for subnode in ast.walk(node):
        subnode_name = type(subnode).__name__
        if isinstance(subnode, ast.Name):
            if subnode.id not in _safe_names and subnode.id not in variables:
                raise ValueError("Unsafe expression {}. contains {}".format(expr, subnode.id))
        if subnode_name not in _safe_nodes:
            raise ValueError("Unsafe expression {}. contains {}".format(expr, subnode_name))
    # pylint: disable=W0123
    return eval(expr, variables)


def safer_eval_cond(expr: str, variables: Any = None) -> bool:
    try:
        return safer_eval(expr, variables=variables)
    except Exception as ex:
        LOG.error("[EVL] Eval Error: '%s': %s", expr, ex)
        return False


##
# CLI AND MAIN
##

# Printers

COLORS = ('black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white')


def _clr_index(name: str) -> int:
    try:
        return COLORS.index(name.lower())
    except ValueError:
        return 0


def _clr(name: str, bright: bool = False):
    prefix = '\033['
    name = name.lower()
    if name == 'end':
        return f'{prefix}0m'
    if name == 'bold':
        return f'{prefix}1m'
    if name == 'underline':
        return f'{prefix}4m'
    mode = '9' if bright else '3'
    return f'{prefix}{mode}{_clr_index(name)}m'


class TColors:
    BLUE = '\033[34m'
    CYAN = _clr('cyan')
    GREEN = _clr('green')
    MAGENTA = _clr('magenta')
    YELLOW = _clr('yellow')
    RED = _clr('red')
    ENDC = _clr('end')
    BOLD = _clr('bold')
    UNDERLINE = _clr('underline')

    def __init__(self, colors: bool = True):
        self._colors = colors

    def fail(self, text: str) -> str:
        return self.wrap(self.RED, text)

    def passed(self, text: str) -> str:
        return self.wrap(self.GREEN, text)

    def warn(self, text: str) -> str:
        return self.wrap(self.YELLOW, text)

    def head(self, text: str) -> str:
        return self.wrap(self.MAGENTA, text)

    def wrap(self, color_prefix: str, text: str) -> str:
        if not self._colors:
            return text
        return f"{color_prefix}{text}{self.ENDC}"


def print_project_df(pdf: 'ProjectDf', colors: bool = True):
    term = TColors(colors)
    print(f"Project: '{term.wrap(term.GREEN, pdf.id)}' :: {pdf.desc}")
    for sdf in pdf.suites:
        print(f"\tSuite: '{term.wrap(term.GREEN, sdf.id)}'", "::", sdf.desc)
        for test in sdf.tests:
            print(f"\t- Test: '{term.wrap(term.CYAN, test.id)}' :: {test.desc} "
                  f"(Actions: {len(test.validations)})")
            if test.action:
                act = test.action
                print(f"\t\t ->  Main '{term.wrap(term.MAGENTA, act.id)}': {act.desc}")
            for action in test.validations:
                print(f"\t\t * Action '{term.wrap(term.MAGENTA, action.id)}': {action.desc}")
        print()


class Reporter:
    def __init__(self, cfg: 'RunParams'):
        self.cfg: 'RunParams' = cfg

    @abc.abstractmethod
    def report(self, res: 'ProjectResult', **kwargs) -> Optional[Path]:
        pass


class ConsoleReporter(Reporter):
    def __init__(self, cfg: 'RunParams'):
        super().__init__(cfg)
        self.tcol: TColors = TColors(not cfg.get('no_color', False))

    def _prk(self, r: 'RunResultType') -> str:
        color = self.tcol.RED if r.kind.is_fail() else self.tcol.GREEN
        return self.tcol.wrap(color, f"[{r.kind.value.upper()}]")

    def report(self,
               res: 'ProjectResult',
               with_actions: bool = False,
               verbose_size: int = 0,
               **kwargs) -> Optional[Path]:

        def _p(r: 'RunResultType', kind: str):
            line = f"{self._prk(r)} {kind.capitalize()}: " \
                   f"({r.df.name}) :: {r.df.desc}"
            if isinstance(r, RunResult):
                line += f" (All: {r.n_subs}; Failed: {r.n_failed}; " \
                        f"Passed: {r.n_passed}; Skipped: {r.n_skipped})"
            return line

        def _echo(*args, **kw):
            print(*args, **kw)

        _echo(_p(res, 'Project'))
        for s_res in res.suites:
            _echo(">>>", _p(s_res, 'Suite'))
            for t_res in s_res.tests:
                _echo(f"\t - {_p(t_res, 'Test')} ")
                if t_res.is_fail():
                    if t_res.msg:
                        _echo(f"\t\t Message: {t_res.msg}")
                pad = "\t\t*"
                for pre_cond in t_res.preconditions:
                    if not pre_cond.is_ok() or with_actions:
                        _echo(f"{pad} {_p(pre_cond, 'Pre-condition')}")
                if t_res.main_action.is_fail() or with_actions:
                    _echo(f"{pad} {_p(t_res.main_action, 'Main')}")
                for act_res in t_res.actions:
                    if not act_res.is_ok() or with_actions:
                        _echo(f"{pad} {_p(act_res, 'Validate')}")

                    if act_res.kind.is_pass():
                        continue

                    _echo(act_res.fail_msg("\t\t  [info] "))
                    if verbose_size:
                        vrb = act_res.verbose(verbose_size)
                        if vrb:
                            _echo(vrb)
            _echo()

        _echo(f"\nOVERALL RESULT: {self._prk(res)}\n")
        return None


class JUnitReporter(Reporter):
    def report(self,
               res: 'ProjectResult',
               report_name: str = 'junit_report',
               **kwargs) -> Optional[Path]:
        try:
            import junitparser
        except ImportError:
            LOG.warning("No JUNIT generated - junit parser is not installed")
            return None
        report_path = self._make_report_path(res.df.id, report_name=report_name)
        LOG.info("[REPORT] Generating JUNIT report: %s", report_path)
        junit_suites = junitparser.JUnitXml(res.df.name)
        for s_res in res.suites:
            unit_suite = junitparser.TestSuite(name=s_res.df.name)
            for test_res in s_res.tests:
                junit_case = self.__make_junit_case(test_res)
                unit_suite.add_testcase(junit_case)
            junit_suites.add_testsuite(unit_suite)

        junit_suites.write(str(report_path))
        return report_path

    @classmethod
    def __make_junit_case(cls, test_res: 'TestResult'):
        import junitparser  # This will always succeed
        jcase = junitparser.TestCase(
            name=test_res.df.desc,
            classname=test_res.df.nm.str(),
            time=test_res.cmd_res.elapsed / 1000000.0 if test_res.cmd_res else 0
        )
        if test_res.kind.is_pass():
            return jcase

        jcase.result = [cls._make_tc_fail(act) for act in test_res.actions]
        if test_res.cmd_res:
            jcase.system_out = str(test_res.cmd_res.stdout)
            jcase.system_err = str(test_res.cmd_res.stderr)
        return jcase

    @classmethod
    def _make_tc_fail(cls, act):
        import junitparser  # This will always succeed
        fail = junitparser.Failure(act.msg)
        fail.text = "\n" + act.fail_msg()
        return fail

    def _make_report_path(self, project_id: str, report_name: str):
        report_dir = self.cfg.ws / project_id
        if not report_dir.exists():
            report_dir.mkdir(parents=True)
        report_path = report_dir / f'{report_name}.xml'
        return report_path


def cli_parse(args: argparse.Namespace):
    cfg = _app_get_cfg(args)
    p_def = _app_parse_project(cfg, args)
    if args.output in ['json', 'j', 'yml', 'yaml', 'y']:
        print(dump_as_dict(p_def.d_serialize(), frm=args.output))
    else:
        print_project_df(p_def)
    return True


def cli_exec(args: argparse.Namespace):
    cfg = _app_get_cfg(args)
    project_df = _app_parse_project(cfg, args)
    if project_df is None:
        raise AssertionError("No project definition found in test dir: ", cfg.tests_dir)
    runner = ProjectRunner(cfg, project=project_df)
    result = runner.run()
    with_actions = args.with_actions
    cons_rep = ConsoleReporter(cfg)
    cons_rep.report(result, with_actions=with_actions)
    junit_reporter = JUnitReporter(cfg)
    report = junit_reporter.report(
        result,
        report_name=f'report_{project_df.id}'
    )
    if report:
        print("JUNIT REPORT:", report)
        if cfg.get('junit_dump', False):
            try:
                print("\nJUNIT REPORT CONTENT: \n")
                print(pretty_print_xml(report))
            except Exception as ex:
                LOG.error("Unable to pretty print XML JUnit Report: ", ex)

    return result.is_pass()


def make_cli_parser() -> argparse.ArgumentParser:
    parser_names = "|".join(PARSERS.keys())

    def _shared_options(sub):
        sub.add_argument('-E', '--executable', type=str, default=None,
                         help="Location of the executable you would like to df")
        sub.add_argument('-T', '--test', type=str, help='Location of the df files',
                         default='./tests')
        sub.add_argument('-W', '--workspace', type=str,
                         help='Location of the testing workspace - outputs/artifacts',
                         default=None)
        sub.add_argument('-p', '--parser', type=str,
                         help=f'Use specific parser ({parser_names}), default is "auto"',
                         default=None)
        sub.add_argument('-D', '--define', action='append',
                         help='Define/override parameter (format: \'-D "var:value"\')')
        sub.add_argument('--no-color', action='store_true', default=False,
                         help='Print output without color')
        sub.add_argument('tests', type=str, help='Test files location')

    parser = argparse.ArgumentParser(APP_NAME, description=APP_DESC)
    parser.set_defaults(func=None)
    parser.add_argument('--version', action='version', version=f'{APP_NAME}: {APP_VERSION}')
    parser.add_argument("-L", "--log-level", type=str,
                        help="Set log level (DEBUG|INFO|WARNING|ERROR)", default=None)
    subs = parser.add_subparsers(title="Available ")
    # Parse
    sub_parse = subs.add_parser("parse", help="Parse and print the test scenario")
    sub_parse.add_argument("-o", "--output", help="Output format (console|json|yaml)",
                           default="console")
    _shared_options(sub_parse)
    sub_parse.set_defaults(func=cli_parse)

    # Exec
    sub_exec = subs.add_parser("exec", help="Execute the unit file")
    _shared_options(sub_exec)
    sub_exec.add_argument('--with-actions', action='store_true', default=False,
                          help='Print out also report about all the actions')
    sub_exec.set_defaults(func=cli_exec)
    return parser


def main(args: Optional[List['str']] = None) -> int:
    parser = make_cli_parser()
    args = parser.parse_args(args)
    if not args.func:
        parser.print_help()
        return 0

    try:
        if not args.func(args):
            print("\nExecution failed!")
            return 1
        return 0
    except Exception as e:
        print(f"\nExecution Failed: {e}", file=sys.stderr)
        return 2


def pretty_print_xml(path: Path) -> str:
    import xml.dom.minidom

    dom = xml.dom.minidom.parse(str(path))
    return dom.toprettyxml()


def _get_log_level(args):
    log_level = args.log_level
    if not log_level:
        log_level = os.getenv('LOG_LEVEL', 'error')
    return log_level


DEFAULT_TCS: Dict[str, Callable[[str], Any]] = {
    '@bool': to_bool,
    '@path': Path,
    '@int': int,
    '@float': float,
    '@none': lambda _: None,
    '@true': lambda _: True,
    '@false': lambda _: False,
    '@id': lambda x: x[4:]
}


class ParamParser:
    _DEFAULT = None

    @classmethod
    def default(cls) -> 'ParamParser':
        if cls._DEFAULT is None:
            cls._DEFAULT = cls()
        return cls._DEFAULT

    def __init__(self, delim: str = ':', tcs: Dict[str, Callable[[str], Any]] = None):
        self._delim: str = delim
        self._tc: Dict[str, Callable[[str], Any]] = tcs if tcs else DEFAULT_TCS

    def parse(self, params: List[str]) -> Dict[str, Any]:
        result = {}
        for param in params:
            (key, val) = self._parse_param(param)
            if not key:
                continue
            dict_set(result, key, val)
        return result

    def _parse_param(self, param: str) -> Tuple[str, Any]:
        if not param:
            return '', ''
        parts = param.split(self._delim, maxsplit=1)
        LOG.debug('[PARSE] Parse param "%s": %s', param, parts)
        key = parts[0].strip()

        val = self.parse_value(parts[1].strip() if len(parts) > 1 else None)
        return key, val

    def parse_value(self, val: str) -> Any:
        if not val:
            return True
        for (cvt_name, fn) in self._tc.items():
            if val.startswith(cvt_name):
                return fn(val[len(cvt_name):].lstrip())
        return val


def _app_get_cfg(args: argparse.Namespace) -> 'RunParams':
    app_cfg = dict(
        tests_dir=args.tests,
        executable=args.executable,
        ws=args.workspace,
        no_color=args.no_color
    )

    app_cfg.update(_parse_environ_params('EX'))
    defn = args.define
    if defn:
        parser = ParamParser.default()
        app_cfg.update(parser.parse(defn))

    app_cfg['diff_params'] = shlex.split(app_cfg.get('diff_params', ''))
    params = RunParams(app_cfg)

    load_logger(_get_log_level(args), log_file=(params.ws / 'tests.log'))

    LOG.info("[PATHS] Executable: %s", params.executable)
    LOG.info("[PATHS] Test dir: %s", params.tests_dir)
    LOG.info("[PATHS] Workspace: %s", params.ws)
    return params


def _parse_environ_params(prefix: str = '') -> Dict[str, Any]:
    parser = ParamParser.default()
    prefix = f"{prefix}_" if prefix else ''
    result = {}
    for key, val in os.environ.items():
        if key.startswith(prefix):
            name = key[len(prefix):].lower()
            result[name] = parser.parse_value(val)
    return result


def _app_parse_project(cfg: RunParams, args) -> Optional[ProjectDf]:
    if not cfg.tests_dir.exists():
        LOG.error("Tests files directory does not exists")
        return None
    # Extract to registry

    parser = PARSERS.get(args.parser, AutoScenarioParser)
    parser_instance = parser(cfg)
    return parser_instance.parse()


def load_logger(level: str = 'INFO', log_file: Optional[Path] = None, file_level: str = None):
    level = level.upper()
    file_level = file_level.upper() if file_level else level
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
            },
            'single': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'TRACE',
                'class': 'logging.StreamHandler',
                'formatter': 'single'
            },
        },
        'loggers': {
            APP_NAME: {
                'handlers': ['console'],
                'level': level,
            }
        }
    }
    if log_file and log_file.parent.exists():
        log_config['handlers']['file'] = {
            'level': file_level,
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': str(log_file)
        }
        log_config['loggers'][APP_NAME]['handlers'].append('file')
    logging.config.dictConfig(log_config)


if __name__ == '__main__':
    sys.exit(main())
