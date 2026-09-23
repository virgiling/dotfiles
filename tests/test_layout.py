import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (("common", "darwin"), ("common", "linux"), ("macos", "darwin"), ("linux", "linux"))


@unittest.skipUnless(shutil.which("chezmoi"), "chezmoi is required for layout checks")
class LayoutTests(unittest.TestCase):
    def archive(self, source, operating_system):
        with tempfile.TemporaryDirectory() as directory:
            scratch = Path(directory)
            config = scratch / "chezmoi.toml"
            config.write_text("")
            destination = scratch / "home"
            destination.mkdir()
            result = subprocess.run(
                [
                    "chezmoi", "--config", str(config),
                    "--source", str(source), "--working-tree", str(ROOT),
                    "--destination", str(destination),
                    "--persistent-state", str(scratch / "state.boltdb"),
                    "--cache", str(scratch / "cache"),
                    "--override-data", json.dumps({"chezmoi": {"os": operating_system}}),
                    "archive", "--format", "tar",
                ],
                capture_output=True, timeout=30,
            )
            self.assertEqual(list(destination.iterdir()), [], "Archive must not deploy files")
            return result

    def archive_contents(self, source, operating_system):
        result = self.archive(source, operating_system)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        with tarfile.open(fileobj=io.BytesIO(result.stdout), mode="r:") as archive:
            return {item.name: archive.extractfile(item).read() for item in archive if item.isfile()}

    def test_each_source_renders_only_its_own_files(self):
        for directory, os_name in SOURCES:
            with self.subTest(source=directory, os=os_name):
                source = ROOT / directory
                actual = self.archive_contents(source, os_name)
                expected = {}
                for path in source.rglob("*"):
                    if path.is_file() and path.name != ".chezmoiignore":
                        parts = list(path.relative_to(source).parts)
                        self.assertTrue(parts[0].startswith("dot_"))
                        parts = ["." + part[4:] if part.startswith("dot_") else part for part in parts]
                        expected["/".join(parts)] = path.read_bytes()
                self.assertEqual(actual, expected)

    def test_shared_agents_and_disjoint_sources(self):
        mac_common = self.archive_contents(ROOT / "common", "darwin")
        linux_common = self.archive_contents(ROOT / "common", "linux")
        self.assertEqual(mac_common, linux_common)
        for target in (".agents/AGENTS.md", ".agents/.skill-lock.json", ".agents/skills/research/SKILL.md"):
            self.assertIn(target, mac_common)
        for directory, os_name in (("macos", "darwin"), ("linux", "linux")):
            with self.subTest(source=directory):
                names = set(self.archive_contents(ROOT / directory, os_name))
                self.assertTrue(set(mac_common).isdisjoint(names))
                for target in (".zshrc", ".zprofile", ".profile", ".tmux.conf"):
                    self.assertNotIn(target, names)
        self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in mac_common))

    def test_agents_generated_files_are_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            shutil.copytree(ROOT / "common", source)
            generated = (
                "skills/research/__pycache__/example.pyc",
                "skills/research/example.pyo",
                "skills/research/.DS_Store",
                "skills/research/.git/config",
                "skills/research/node_modules/example/index.js",
            )
            for name in generated:
                path = source / "dot_agents" / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"generated test data")
            names = self.archive_contents(source, "darwin")
            for name in generated:
                self.assertNotIn(".agents/" + name, names)
            self.assertIn(".agents/skills/research/SKILL.md", names)

    def test_project_guidance_is_not_deployed(self):
        self.assertTrue((ROOT / "AGENTS.md").is_file())
        for name in ("maintain-dotfiles", "sync"):
            self.assertTrue((ROOT / f".agents/skills/{name}/SKILL.md").is_file())
        self.assertFalse((ROOT / ".agents").is_symlink())
        for directory, os_name in SOURCES:
            with self.subTest(source=directory, os=os_name):
                names = self.archive_contents(ROOT / directory, os_name)
                self.assertNotIn("AGENTS.md", names)
                for skill in ("maintain-dotfiles", "sync"):
                    self.assertFalse(any(name.startswith(f".agents/skills/{skill}/") for name in names))

    def test_sequential_apply_keeps_shared_and_system_files(self):
        for directory, os_name, relative in (
            ("macos", "darwin", ".config/ghostty/config"),
            ("linux", "linux", ".config/kitty/kitty.conf"),
        ):
            with self.subTest(system=directory), tempfile.TemporaryDirectory() as name:
                scratch = Path(name)
                config = scratch / "chezmoi.toml"
                config.write_text("")
                home = scratch / "home"
                home.mkdir()
                shared = home / ".agents/AGENTS.md"
                system = home / relative
                for source, target in (("common", shared), (directory, system)):
                    result = subprocess.run(
                        [
                            "chezmoi", "--config", str(config),
                            "--source", str(ROOT / source), "--working-tree", str(ROOT),
                            "--destination", str(home),
                            "--persistent-state", str(scratch / "state.boltdb"),
                            "--cache", str(scratch / "cache"),
                            "--override-data", json.dumps({"chezmoi": {"os": os_name}}),
                            "apply", *([str(home / ".agents")] if source == "common" else []),
                        ],
                        capture_output=True, text=True, timeout=30,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(shared.read_bytes(), (ROOT / "common/dot_agents/AGENTS.md").read_bytes())
                expected = ROOT / directory / "dot_config" / Path(relative).relative_to(".config")
                self.assertEqual(system.read_bytes(), expected.read_bytes())

    def test_source_files_are_not_git_ignored(self):
        files = [str(path.relative_to(ROOT)) for directory in ("common", "macos", "linux")
                 for path in (ROOT / directory).rglob("*") if path.is_file()]
        result = subprocess.run(
            ["git", "-C", str(ROOT), "check-ignore", "--no-index", "--stdin"],
            input="\n".join(files) + "\n", text=True, capture_output=True, timeout=10,
        )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)

    def test_root_is_not_a_deployment_source(self):
        result = self.archive(ROOT, "darwin")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"Repository root is not a chezmoi source", result.stderr)

    def test_wrong_os_is_rejected(self):
        for directory, os_name in (("linux", "darwin"), ("macos", "linux"), ("common", "windows")):
            with self.subTest(source=directory, os=os_name):
                result = self.archive(ROOT / directory, os_name)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(b"error calling fail", result.stderr)


if __name__ == "__main__":
    unittest.main()
