from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


@unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is required for add checks")
class ChezmoiAddTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name)
        self.source = self.scratch / "source"
        self.home = self.scratch / "home"
        self.source.mkdir()
        self.home.mkdir()
        # Keep chezmoi's protected config directory separate from fake home.
        self.config = self.scratch / "config/chezmoi.toml"
        self.config.parent.mkdir()
        self.config.write_text("")

    def add(self, *targets):
        result = subprocess.run(
            [
                "chezmoi", "--config", str(self.config),
                "--source", str(self.source), "--destination", str(self.home),
                "--working-tree", str(self.source),
                "--persistent-state", str(self.config.with_name("state.boltdb")),
                "--cache", str(self.scratch / "cache"),
                "add", *map(str, targets),
            ],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_regular_file_is_copied_without_live_sync(self):
        target = self.home / ".example"
        target.write_text("original\n")
        self.add(target)
        saved = self.source / "dot_example"
        self.assertFalse(target.is_symlink())
        self.assertFalse(saved.is_symlink())
        self.assertEqual(saved.read_text(), "original\n")
        target.write_text("local edit\n")
        self.assertEqual(saved.read_text(), "original\n")
        saved.write_text("source edit\n")
        self.assertEqual(target.read_text(), "local edit\n")
        self.add(target)
        self.assertEqual(saved.read_text(), "local edit\n")

    def test_directory_add_is_recursive_and_scoped(self):
        directory = self.home / ".example"
        (directory / "nested").mkdir(parents=True)
        (directory / "nested/settings.txt").write_text("settings\n")
        (self.home / "unrelated.txt").write_text("unrelated\n")
        self.add(directory)
        self.assertEqual(
            (self.source / "dot_example/nested/settings.txt").read_text(), "settings\n"
        )
        self.assertFalse((self.source / "unrelated.txt").exists())

    def test_symlink_add_records_link_by_default(self):
        target = self.home / "target.txt"
        target.write_text("target contents\n")
        link = self.home / ".link"
        link.symlink_to("target.txt")
        self.add(link)
        self.assertTrue(link.is_symlink())
        self.assertEqual((self.source / "symlink_dot_link").read_text().strip(), "target.txt")
        self.assertFalse((self.source / "target.txt").exists())

    def test_follow_add_copies_symlink_target(self):
        target = self.home / "target.txt"
        target.write_text("target contents\n")
        link = self.home / ".link"
        link.symlink_to("target.txt")
        self.add("--follow", link)
        self.assertTrue(link.is_symlink())
        saved = self.source / "dot_link"
        self.assertFalse(saved.is_symlink())
        self.assertEqual(saved.read_text(), "target contents\n")


if __name__ == "__main__":
    unittest.main()
