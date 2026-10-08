#!/usr/bin/env python3
"""Link shared configuration and maintain one shell startup block."""
import os
from pathlib import Path
import re
import sys

REPO = Path(__file__).resolve().parent.parent
START = '# >>> andrew-dotfiles >>>'
END = '# <<< andrew-dotfiles <<<'


def backup(path):
    candidate = path.with_name(path.name + '.pre-dotfiles')
    index = 1
    while candidate.exists() or candidate.is_symlink():
        candidate = path.with_name(path.name + f'.pre-dotfiles.{index}')
        index += 1
    path.rename(candidate)
    print(f'Backed up {path} to {candidate}')


def link(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink() and target.resolve() == source.resolve():
        return
    if target.exists() or target.is_symlink():
        backup(target)
    target.symlink_to(source)
    print(f'Linked {target}')


def configure(home, mac):
    config = Path(os.environ.get('XDG_CONFIG_HOME') or home / '.config')
    link(REPO / 'config/starship.toml', config / 'starship.toml')
    link(REPO / 'shell/init.sh', config / 'andrew-dotfiles/init.sh')
    block = START + '\n' + '''case $- in
  *i*) [ ! -f "${XDG_CONFIG_HOME:-$HOME/.config}/andrew-dotfiles/init.sh" ] || . "${XDG_CONFIG_HOME:-$HOME/.config}/andrew-dotfiles/init.sh" ;;
esac
''' + END
    # Zsh honors ZDOTDIR; Bash uses ~/.bashrc.
    zsh_dir = Path(os.environ.get('ZDOTDIR') or home)
    for rc in (home / '.bashrc', zsh_dir / '.zshrc'):
        text = rc.read_text() if rc.exists() else ''
        if text.count(START) != text.count(END):
            raise RuntimeError(f'Unbalanced dotfiles markers in {rc}; fix them before rerunning.')
        clean = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', text, flags=re.S)
        updated = clean.rstrip('\n') + '\n\n' + block + '\n'
        if updated != text:
            rc.parent.mkdir(parents=True, exist_ok=True)
            if rc.exists():
                # Copy rather than rename: preserve symlinked startup files.
                import shutil
                saved = rc.with_name(rc.name + '.pre-dotfiles')
                if not saved.exists():
                    shutil.copy2(rc, saved)
            rc.write_text(updated)
            print(f'Updated {rc}')
    if mac:
        link(REPO / 'iterm/dotfiles.json', home / 'Library/Application Support/iTerm2/DynamicProfiles/andrew-dotfiles.json')
        print('iTerm2: select the "Dotfiles — Mocha" profile; set it as default in Settings → Profiles if desired.')


if __name__ == '__main__':
    configure(Path.home(), sys.platform == 'darwin')
