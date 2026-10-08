#!/usr/bin/env bash
set -euo pipefail
REPO_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKIP_PACKAGES=false
case "${1:-}" in
  --skip-packages) SKIP_PACKAGES=true ;;
  '') ;;
  *) echo "Usage: ./install.sh [--skip-packages]" >&2; exit 2 ;;
esac
if ! "$SKIP_PACKAGES"; then
  case "$(uname -s)" in
    Darwin)
      if ! command -v brew >/dev/null 2>&1; then
        for brew_path in /opt/homebrew/bin/brew /usr/local/bin/brew; do
          if [ -x "$brew_path" ]; then eval "$("$brew_path" shellenv)"; break; fi
        done
      fi
      if ! command -v brew >/dev/null 2>&1; then
        echo 'Installing Homebrew (may request your macOS password)...'
        brew_installer="$(mktemp)"
        curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh -o "$brew_installer"
        /bin/bash "$brew_installer"
        rm -f "$brew_installer"
        if [ -x /opt/homebrew/bin/brew ]; then
          eval "$(/opt/homebrew/bin/brew shellenv)"
        else
          eval "$(/usr/local/bin/brew shellenv)"
        fi
      fi
      brew bundle --file="$REPO_DIR/Brewfile"
      ;;
    Linux)
      . /etc/os-release
      if [ "${ID:-}" != ubuntu ]; then echo 'Supported platforms: macOS and Ubuntu.' >&2; exit 1; fi
      if ! command -v python3 >/dev/null || ! command -v curl >/dev/null; then
        if [ "$(id -u)" -eq 0 ]; then
          apt-get update && apt-get install -y python3 curl ca-certificates
        else
          sudo apt-get update && sudo apt-get install -y python3 curl ca-certificates
        fi
      fi
      if ! command -v starship >/dev/null && [ ! -x "$HOME/.local/bin/starship" ]; then
        mkdir -p "$HOME/.local/bin"
        starship_installer="$(mktemp)"
        curl -fsSL https://starship.rs/install.sh -o "$starship_installer"
        sh "$starship_installer" --yes --bin-dir "$HOME/.local/bin"
        rm -f "$starship_installer"
      fi
      ;;
    *) echo 'Supported platforms: macOS and Ubuntu.' >&2; exit 1 ;;
  esac
fi
python3 "$REPO_DIR/scripts/configure.py"
echo 'Done. Open a new terminal to load your prompt.'
