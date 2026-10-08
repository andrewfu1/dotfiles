# Dotfiles

A minimal Pure-inspired Starship prompt in Catppuccin Mocha, for macOS and Ubuntu.

```text
~/code/training  main  12m 8s
❯
```

Shows the directory, Git branch, and elapsed time for commands taking at least 10 seconds. SSH sessions also show the user and hostname. The arrow turns red after a failed command. No language versions, Git change counts, or Powerline segments. Duration appears when a command finishes, not while it runs.

## Install

Run this on **both your Mac and your Ubuntu dev machine**, separately:

```sh
git clone https://github.com/andrewfu1/dotfiles.git ~/dotfiles
cd ~/dotfiles
./install.sh
```

If Git is missing on Ubuntu, run `sudo apt-get update && sudo apt-get install -y git` first. On a fresh Mac, `xcode-select --install` supplies Git and the tools Homebrew needs; finish that installation first.

- **macOS:** installs Homebrew if missing, Starship, iTerm2, and JetBrainsMono Nerd Font. Links an iTerm2 dynamic profile with Mocha colors and a 14pt font.
- **Ubuntu:** installs Python/curl if missing (may request sudo), then Starship into `~/.local/bin` if needed. Uses your existing Bash or Zsh; does not change your login shell.
- **Both:** links the shared config and adds one managed block to `.bashrc` and `.zshrc`, preserving your existing settings. Honors `XDG_CONFIG_HOME` and `ZDOTDIR`.

Open a new terminal. On macOS, choose **Profiles → Dotfiles — Mocha** in iTerm2, then optionally make it the default in **Settings → Profiles**. Your local iTerm2 font and colors also render SSH sessions; Ubuntu needs no font installation.

Bash login sessions must source `.bashrc` from `.bash_profile` or `.profile`; Ubuntu does this by default. If you use a custom login file, ensure it includes that source. Existing prompt frameworks should be disabled if they override Starship after our startup block.

## Update

On each machine:

```sh
cd ~/dotfiles
git pull --ff-only
./install.sh
```

Repeated installs do not duplicate startup blocks or profiles. Existing files replaced by links are moved to `.pre-dotfiles` backups (numbered if necessary). Shell startup files get an initial `.pre-dotfiles` backup. Config files are symlinked, so edits pulled from Git take effect without copying them again; open a new shell to reload the prompt. Keep this checkout in place.

To link configs without installing packages:

```sh
./install.sh --skip-packages
```

This still updates your shell startup files and links configs. Starship must already be installed. Package installation ensures dependencies exist; it does not force Starship upgrades on Ubuntu. To upgrade there, rerun the official Starship installer explicitly.

## Customize

- `config/starship.toml`: prompt layout, colors, and duration threshold.
- `shell/init.sh`: shared interactive shell setup.
- `Brewfile`: macOS packages.
- `iterm/dotfiles.json`: iTerm2 dynamic profile; font size is in `Normal Font`.

Machine-specific aliases and settings can stay in your existing shell startup files. This repo does not install ML tools or coding agents.

## Verify

```sh
bash -n install.sh shell/init.sh
python3 -m unittest discover -s tests
```

## Credits

Layout inspired by [Starship's Pure preset](https://starship.rs/presets/pure-preset). Prompt colors use the [Catppuccin Mocha palette](https://github.com/catppuccin/starship). The vendored [Catppuccin iTerm2 theme](https://github.com/catppuccin/iterm) is distributed under its included MIT license.
