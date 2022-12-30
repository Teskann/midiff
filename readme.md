# midiff 🎹 ↔ 🎹

Compare MIDI files in a human-readable format.

[](mdtoc)
## Table of Contents

* [Features](#features)
* [Installation](#installation)
	* [Prerequisites](#prerequisites)
	* [Installation](#installation-1)
* [Usage](#usage)
	* [Examples](#examples)
	* [Documentation](#documentation)
* [Contribute](#contribute)
[](/mdtoc)

## Features

- ✅ Compare MIDI files using the diff tool you like the most
- ✅ Easy work with git

## Installation

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/) 🐍
- [Make](https://www.gnu.org/software/make/) 🔨
- [Git](https://git-scm.com/)

### Installation

```bash
git clone https://github.com/Teskann/midiff && cd midiff && make && cd .. && rm -rf midiff
```

## Usage

### Examples

View the diff of all midi files in your current git repository:
```commandline
midiff
```

Compare two files:
```commandline
midiff --diff a.mid b.mid
```

Configure VS Code as diff tool
```bash
midiff --configure-difftool "code --diff \$1 \$2"
# Disable automatic file deletion because VS Code is launched asynchronously.
midiff --configure-clear false
```
The settings are saved for your further uses of midiff.

### Documentation

```commandline
usage: midiff [-h] [--diff DIFF DIFF]
              [--configure-difftool CONFIGURE_DIFFTOOL]
              [--configure-clear CONFIGURE_CLEAR]
              [repo]

View the difference between MIDI files in a human readable format.

positional arguments:
  repo                  Path to the git repository

optional arguments:
  -h, --help            show this help message and exit
  --diff DIFF DIFF      Provide the path to 2 midi files and compare them.
  --configure-difftool CONFIGURE_DIFFTOOL
                        Give the diff tool command to use to compare files
                        with `$1` and `$2` as placeholders for the two files
                        you want to compare. Current diff tool is: `diff $1 $2`.
  --configure-clear CONFIGURE_CLEAR
                        Set to false if you want to remove the temporary files
                        when midiff is done. Clearing the files may cause
                        problems on asynchronous diff tools such as VS Code.
                        Currently set to true.
```

## Contribute

Contributions are welcome, feel free to open issues or propose pull requests.

If you don't know where to get started, here is a non-exhaustive list of
what needs to be done:

- ⬜ Add unit tests
- ⬜ CI / CD
- ⬜ Deploy on py-pi once tests are written
- ⬜ Move installer to PEP 517
- ⬜ Deliver as a plugin for some IDEs like VS Code or IntelliJ IDEs