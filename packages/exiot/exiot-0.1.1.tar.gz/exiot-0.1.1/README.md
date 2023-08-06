# Executable I/O Testing Tool (exiot)

![Exiot Tests Pipeline](https://github.com/pestanko/exiot/actions/workflows/tests.yml/badge.svg)

The (`exiot`) is a testing tool to test the executable `STDIN`, `STDOUT`, `STDERR`, and many more.

You can take a look to the (man/architecture.md)[Architecture] `man` documentation.

## Getting Started

This tool requires [unix's ``diff``](https://man7.org/linux/man-pages/man1/diff.1.html) - to compare file's content.

If you would like to use the ``--build=cmake`` you would need: [`cmake`](https://cmake.org/),
[`make`](https://man7.org/linux/man-pages/man1/make.1.html) and
[`gcc`](https://gcc.gnu.org/) or [`clang`](https://clang.llvm.org/)

In order to use this tool on MS Windows, you need to use the [`wsl`](https://docs.microsoft.com/en-us/windows/wsl/install).


### Installation

In order to install the latest "stable" version of the tool you can use
the [pip](https://packaging.python.org/tutorials/installing-packages/).

```shell
pip install exiot
```

In order to get latest version of the tool you can just clone the repository:

```shell
git clone https://github.com/pestanko/exiot.git
```

and then use the [poetry](https://python-poetry.org/docs/) to install dependencies, or just install them manually (
dependencies are optional).

```shell
cd exiot
poetry install
```

Optional dependencies:

- ``junitparser`` - to produce the junit report
- ``pyyaml`` - to parse yaml schemas and generate yaml reports

You can install them manually if you do not want to use the poetry

```shell
pip install junitparser pyyaml
```

## Usage

Show help:

```shell
$ python -m exiot --help
```

### Parse the tests

Parse the tests - show all available tests:

```shell
python -m exiot parse [-o OUTPUT_FORMAT] [-p PARSER] <TEST_DIR>
# Example:
python -m exiot parse examples/single_fail
```

Parse the tests - show all available tests, dump them as `json` or `yaml` (if `pyyaml` installed):

```shell
# Examples:
python -m exiot parse -o json examples/single_fail
# or yaml if PyYAML installed
python -m exiot parse -o yaml examples/single_fail
```

#### Supported parsers

Tool is currently supporting these parsers:

- [``minihw``](man/minihw_def.md) - MiniHomework parser for _MUNI FI:PB071_ course (`examples/minihw_not_impl`)
- [``dir``](man/directory_def.md) - Directory parser (`examples/single`, `examples/single_fail`)
- [``scenario``](man/scenario_def.md) - Scenario parser, this is most advanced parser, and it is the preferred way to
  write tests
- ``auto`` - Autodetect parser - automatically detect which parser to use based on the root tests structure

### Run the tests

Run tests in directory:

```shell
python -m exiot -Linfo exec -E <EXECUTABLE> <TESTS_DIR>
# Example:
python -m exiot -Linfo exec -E ./myexec ./tests
# Example with cmake build
python -m exiot -Linfo exec --build=cmake <PATH_TO_TESTS>
```

Run Mini Homeworks:

```shell
# -p parameters specifies the "parser" - minihw is special parser for parsing the mini homeworks for FI:PB071
python -m exiot -Linfo exec -p minihw <PATH_TO_MINIHW>
# Example:
python -m exiot -Linfo exec -p minihw examples/minihw_not_impl
# Example to run the solution
python -m exiot -Linfo exec -D="target: solution" <PATH_TO_MINIHW>
# Example with cmake build
python -m exiot -Linfo exec --build=cmake <PATH_TO_MINIHW>
```

The build support is currently experimental, it requires ``cmake``, `make`, `gcc/clang`.
The cmake build will create new directory in the ``TESTS_DIR`` and runs `cmake/make` there.

How it might looks like:

```shell
cmake -B build
make -k -C build
```

## Supported execution parameters

To provide/override parameters you can use ``params`` property for definitions or pass it as command line parameter
using: `-D` or `--define` option.

- `valgrind` (not implemented)
- `executable` - do not use directly from command line (use `-E` or `--executable` param)
- `timeout` - Timeout - max execution time
- `devel_mode` - Enable development mode, only for test development, not for "production"
- `target` - for minihw you can toggle between `source|solution` executable testing (default: `source`)
- `diff_params` - `diff` executable additional params
- `junit_dump` - Print out the JUNIT dump at the end of the execution

## Examples

For examples - take a look at the ``examples`` directory.

- ``minihw_not_impl`` - Mini Homework format for FI:PB071, the minihw `source.c` is not implemented
- ``proj_def_yml`` - Passing project definition - all tests should be passing
- ``proj_def_fail_yml`` - Failing project def. - all tests should be failing
- ``single`` - Single directory with tests - files based tests definition, all should be passing
- ``single_fail`` - Single directory with tests - files based tests definition, all tests should be failing
- ``echocat.c`` - reference implementation for the testing binary `echocat` (used in tests)

## TODOs

- [ ] Definition support templates (parametrized tests)
- [ ] Valgrind Support
- [ ] More tests
- [ ] Support more parsers (ex. `kontr`)
- [ ] Support tests generation
