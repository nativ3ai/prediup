# prediup

`prediup` is the one-command installer and in-place updater for the fully local PrediHermes edition.

It bootstraps:
- the `geopolitical-market-sim` Hermes skill
- WorldOSINT headless
- MiroFish backend in local graph mode
- Ollama-backed local simulation defaults

It does not replace the existing full / legacy PrediHermes mode. It installs the local edition cleanly and leaves the main repo available for the richer companion-stack workflow.

Source repo:
- https://github.com/nativ3ai/hermes-geopolitical-market-sim

What the local edition means:
- local SQLite graph backend
- local Ollama model for simulation
- headless WorldOSINT usage
- backend-only MiroFish usage
- no Zep requirement
- no external LLM API key requirement

## Install

### Homebrew

```bash
brew tap nativ3ai/prediup
brew install predihermes
```

Or directly:

```bash
brew install nativ3ai/prediup/predihermes
```

### pipx from GitHub

```bash
pipx install git+https://github.com/nativ3ai/prediup.git
```

### plain pip from GitHub

```bash
python3 -m pip install --user git+https://github.com/nativ3ai/prediup.git
```

### local clone

```bash
git clone https://github.com/nativ3ai/prediup.git
cd prediup
pipx install .
```

## Usage

```bash
prediup doctor
prediup install
prediup update
prediup verify
prediup status
```

Recommended first run:

```bash
prediup doctor
prediup install
prediup update
prediup verify
prediup status
```

## Common options

```bash
prediup install --ollama-model qwen2.5:3b
prediup update --ollama-model qwen2.5:7b
prediup install --with-video-transcriber
prediup install --repo-root ~/src/hermes-geopolitical-market-sim --stack-home ~/predihermes
```

## What install does

- clones `https://github.com/nativ3ai/hermes-geopolitical-market-sim.git` if missing
- runs `install.sh --bootstrap-local`
- points MiroFish at local Ollama
- keeps `GRAPH_BACKEND=local`
- generates local helper launchers under `~/predihermes/bin`

By default the main repo installer will also:
- start or install Ollama when needed on macOS with Homebrew
- pull the requested Ollama model if it is missing
- write the local stack pointers into `~/.hermes/.env`

## What update does

`prediup update` is the forward path after the first install.

It will:
- fetch and rebase the local `hermes-geopolitical-market-sim` checkout to the selected repo ref
- rerun the local installer in place
- refresh the installed skill copy, helper launchers, and local companion wiring

It will stop if the checked-out repo has local uncommitted changes.

## Verification targets

`prediup verify` checks for:
- the installed Hermes skill
- `predihermes-local-up`
- `predihermes-local-health`
- the generated local MiroFish `.env`

`prediup status` prints the resolved local profile values from the generated MiroFish `.env`, including:
- `LLM_BASE_URL`
- `LLM_MODEL_NAME`
- `GRAPH_BACKEND`

## Runtime after install

Typical next commands:

```bash
~/predihermes/bin/predihermes-local-up
~/predihermes/bin/predihermes-local-status
~/predihermes/bin/predihermes-local-health
hermes -s geopolitical-market-sim
```

If you want the full companion-stack mode instead of the local edition, use the main repo directly:

```bash
git clone https://github.com/nativ3ai/hermes-geopolitical-market-sim.git
cd hermes-geopolitical-market-sim
./install.sh --bootstrap-stack
```
