
# Bugtest | GKE Failure
-----------------------

## Overview
Reproduction code for GKE failed state bug


## Development Bootstrapping

### Configure shell environment

Ensure that a GitGuardian API key is available in shell context under `GITGUARDIAN_API_KEY`, such as in `~/.zshenv`

### Install dependencies:

```
brew install \
  commitizen \
  ggshield \
  pre-commit \
  pulumi \
  python \
  pipx
```

### Install pre-commit hooks

```
pre-commit install --hook-type commit-msg --hook-type pre-commit
```

If you are using GitKraken, manually update hook scripts to load proper shell context.
For example, in zsh add:

```
source ~/.zshenv
```

To the install files:

```
vi .git/hooks/commit-msg
vi .git/hooks/pre-commit
```

### Install Poetry

```
pipx install poetry
```

### Install Python dependencies

```
poetry install
```
