from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InventoryTests(unittest.TestCase):
    def test_macos_manifest_contains_selected_managers(self):
        with (ROOT / "macos.toml").open("rb") as source:
            inventory = tomllib.load(source)
        self.assertEqual(set(inventory), {"brew", "cask", "npm", "cargo", "uvx", "manual"})
        self.assertTrue(all(inventory.values()))
        for packages in inventory.values():
            self.assertIsInstance(packages, dict)
            for name, version in packages.items():
                self.assertIsInstance(name, str)
                self.assertIsInstance(version, str)
        self.assertEqual(set(inventory["uvx"]), {"lic-cli"})
        self.assertEqual(
            set(inventory["manual"]),
            {"com.colliderli.iina", "fr.imag.iihm.blanch.osx-presentation"},
        )
        self.assertIn("zoom", inventory["cask"])
        self.assertNotIn("zoom", inventory["manual"])

    def test_linux_manifest_is_an_empty_placeholder(self):
        path = ROOT / "linux.toml"
        self.assertEqual(path.read_bytes(), b"")
        self.assertEqual(tomllib.loads(path.read_text()), {})


if __name__ == "__main__":
    unittest.main()
