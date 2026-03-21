# prediup

`prediup` is the one-command installer for the fully local PrediHermes edition.

It bootstraps:
- the `geopolitical-market-sim` Hermes skill
- WorldOSINT headless
- MiroFish backend in local graph mode
- Ollama-backed local simulation defaults

It does not replace the existing full / legacy PrediHermes mode. It just installs the local edition cleanly.

## Install

### pipx from GitHub

```bash
pipx install git+https://github.com/nativ3ai/prediup.git
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
prediup verify
prediup status
```

## Common options

```bash
prediup install --ollama-model qwen2.5:3b
prediup install --with-video-transcriber
prediup install --repo-root ~/src/hermes-geopolitical-market-sim --stack-home ~/predihermes
```

## What install does

- clones `https://github.com/nativ3ai/hermes-geopolitical-market-sim.git` if missing
- runs `install.sh --bootstrap-local`
- points MiroFish at local Ollama
- keeps `GRAPH_BACKEND=local`
- generates local helper launchers under `~/predihermes/bin`

## Verification targets

`prediup verify` checks for:
- the installed Hermes skill
- `predihermes-local-up`
- `predihermes-local-health`
- the generated local MiroFish `.env`
