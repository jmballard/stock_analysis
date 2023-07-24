# project_title

## Table of contents

- [Motivations](#motivations)
- [Project description](#description)
- [Data used](#data)
- [Visuals](#visuals)
- [Packages used](#packages_used)
- [Instructions](#instructions)
- [Files](#files)
- [Possible improvements](#improvements)
- [Credits](#credits)
- [License](#license)
- [Links](#links)
- [Status](#status)

## Motivations <a name="motivations"></a>

What was your motivation?
Why did you build this project?
What problem does it solve?

## Project description <a name="description"></a>

A good one takes advantage of the opportunity to explain and showcase:

What your application does,
Why you used the technologies you used,
Some of the challenges you faced and features you hope to implement in the future.

- step by step of pipeline / modelling
- summary on data (unless in section below)

## Data used (if any) <a name="data"></a>

Description of the public data used in this Project

## Visuals <a name="visuals"></a>

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos).

```text
To link to pictures:
![Alt text](relative/path/to/img.jpg?raw=true "Title")
```

## Packages used <a name="packages_used"></a>

For the analysis:

- os
- sys
- numpy
- pandas
- re
- matplotlib
- pickle
- sqlalchemy
- logging
- nltk
- sklearn
- json
- plotly
- flask
- pathlib

For code quality:

- pre-commit
- black
- flake8
- isort (In GitHub actions only)
- nbstripout
- pydocstyle
- sqlstuff
- mdformat
- yesqa

For more information: read the requirements.txt file.

## Instructions <a name="instructions"></a>

### Prerequisites

You need to have Python, Make and Poetry installed on your machine.

To install python: [Official website](https://www.python.org/downloads/)

To install Make: first install [Chocolatey](https://chocolatey.org/install), then use it to install [make](https://community.chocolatey.org/packages/make).

To install Poetry: [Official website](https://python-poetry.org/docs/#installing-with-the-official-installer)

### Initial set-up

You can clone this repository by opening Git Bash and the command line

```text
git clone https://github.com/jmballard/NAME_OF_REPO.git
```

Copy the local clone (without the `.git` folder) to the new project’s repo (which has its own `.git`).

### Set up with Make

Make sure you don’t have any virtual environment activated in the CLI. In a command prompt, run setup target using make: `make setup`.

`make` looks for a Makefile in the project’s root that contains a set of rules to run. Each rule has 3 parts: a target, a list of prerequisites, and a recipe in the following format:

```bash
target: prerequisites
    recipes
```

The setup target on the template Makefile in line 8 doesn’t have any recipes but rather 3 prerequisites, which are 3 make targets (a target that runs other targets).

Let’s have a look at these 3 targets that the current Makefile contains:

1. It will install an isolated `.venv` in the project's library.

The venv target in Makefile > line 10 has one prerequisite $(GLOBAL_PYTHON) which is the value of a variable defined earlier in Makefile > line 4. The variable GLOBAL_PYTHON grabs the full path to the python interpreter which we installed earlier. If the prerequisite interpreter path doesn’t exist, you will get an error when running the venv target

Makefile > line 12 is where poetry creates an isolated .venv folder in the project’s root using the interpreter full path. To make sure .venv is created in the root directory of the project, the following configuration is added in the poetry.toml 📃 (where all poetry configurations go):

```text
[virtualenvs]
in-project = true
```

2. It will install some packages in the `.venv`.

The install target in Makefile > line 14 has one prerequisite $(LOCAL_PYTHON) which is the value of a variable defined earlier in Makefile > line 5. The variable LOCAL_PYTHON checks if there is a path to a python interpreter in .venv. If the prerequisite interpreter path doesn’t exist, you will get an error when running the install target

Makefile > line 16 is where poetry installs the projects’ dependencies found in the pyproject.toml file.

Poetry separates packages into dependencies pyproject.toml > line 7 and development dependencies pyproject.toml > line 11. When Poetry has finished installing all packages in .venv, it writes their exact versions to a poetry.lock file that you should commit to the project’s repo 🔗 so that the team working on the project is locked to the same versions of dependencies 🔗

Our packages have different version constraints. For example "\*" means latest, while "^1" means >=1.0.0 \<2.0.0.

3. It will install the pre-commit hooks.

The hooks currently used are:

1. Black for formatting codes
1. flake8 for linting
1. isort to sort imports
1. nbstripout to strip all notebooks output
1. pydocstyle to check doc style is complaint with Google docstrings format
1. check-ast to check files parse as valid python
1. end-of-file-fixer to check files end in a newline and only a newline
1. trailing-whitespace to check there are no trailing whitespace

The clean target in Makefile > line 20 cleans up your project by:

- Removing the directory .git\\hooks if it exists
- Removing the directory .venv if it exists
- Removing the file poetry.lock if it exists

### Managing packages

To add a package to the project’s dependencies or dev dependencies:

```bash
poetry add <package>
poetry add <package> --dev
```

To remove a package from the project’s dependencies or dev dependencies:

```bash
poetry remove <package>
poetry remove <package> --dev
```

These commands will automatically update the pyproject.toml and the poetry.lock files

### VSCode integration

If the IDE used is VSCode, you can integrate some of the dev packages to run automatically on your code on save.

To do this, add the setting.json values to the workspace settings. Whenever you save a script (ctrl + s), it will be formatted with black, linted with flake8, and packages sorted with isort

## Files <a name="files"></a>

Here is the content of this repo:

```bash
.
├── config
│   ├── connections.py
│   └── parameters.py
├── data
│   ├── processed
│   │   └── v1
│   └── raw
│       └── v1
├── deploy
│   ├── scripts
│   └── tests
├── develop
│   ├── artifacts
│   ├── eda
│   ├── notebooks
│   ├── scripts
│   │   ├── eda.py
│   │   └── load.py
│   └── main.py
├── label
├── train
├── visualise
├── .flake8
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── Makefile
├── poetry.toml
├── pyproject.toml
└── README.md
```

## Possible improvements on this project: <a name="improvements"></a>

List of possible improvements

## Credits <a name="credits"></a>

If you worked on the project as a team or an organization, list your collaborators/team members. You should also include links to their GitHub profiles and social media too.

Also, if you followed tutorials or referenced a certain material that might help the user to build that particular project, include links to those here as well.

## License <a name="license"></a>

MIT License

Copyright (c) \[2022\] \[Julie Ballard\]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Links <a name="links"></a>

Documentation about the setup: (Medium article)\[https://drgabrielharris.medium.com/python-how-using-poetry-make-and-pre-commit-hooks-to-setup-a-repo-template-for-your-ds-team-15b5a77d0e0f\]

Other links if needed

## Project status  <a name="status"></a>

If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
