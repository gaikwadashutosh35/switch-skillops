import unittest

from profile_settings import initials, save_profile


class ProfileTest(unittest.TestCase):
    def test_initials(self):
        self.assertEqual(initials("Ada Lovelace"), "AL")

    def test_save_profile_with_display_name(self):
        store = {}
        saved = save_profile(store, "u1", "ada@example.com", " Ada Lovelace ")
        self.assertEqual(saved["display_name"], "Ada Lovelace")
        self.assertEqual(store["u1"]["initials"], "AL")


if __name__ == "__main__":
    unittest.main()
