import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('configure', Path(__file__).resolve().parents[1] / 'scripts/configure.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class InstallTests(unittest.TestCase):
    def test_repeat_install_preserves_user_config_and_links(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {}, clear=True):
            home = Path(directory)
            (home / '.bashrc').write_text('export MY_SETTING=yes\n')
            config = home / '.config'
            config.mkdir()
            (config / 'starship.toml').write_text('old config\n')
            module.configure(home, True)
            first = (home / '.bashrc').read_bytes()
            module.configure(home, True)
            self.assertEqual(first, (home / '.bashrc').read_bytes())
            self.assertEqual((home / '.bashrc').read_text().count(module.START), 1)
            self.assertIn('export MY_SETTING=yes', first.decode())
            self.assertEqual((config / 'starship.toml.pre-dotfiles').read_text(), 'old config\n')
            self.assertEqual(len(list(config.glob('starship.toml.pre-dotfiles*'))), 1)
            self.assertEqual((config / 'starship.toml').resolve(), module.REPO / 'config/starship.toml')
            self.assertTrue((home / 'Library/Application Support/iTerm2/DynamicProfiles/andrew-dotfiles.json').is_symlink())

    def test_xdg_and_zdotdir(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            with patch.dict(os.environ, {'XDG_CONFIG_HOME': str(home / 'config'), 'ZDOTDIR': str(home / 'zsh')}, clear=True):
                module.configure(home, False)
                self.assertTrue((home / 'config/starship.toml').is_symlink())
                self.assertTrue((home / 'zsh/.zshrc').exists())
                self.assertFalse((home / '.zshrc').exists())

if __name__ == '__main__':
    unittest.main()
