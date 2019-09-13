import unittest

from pycommoncrawl.version_getter import get_version_html_page, VersionGetter, InvalidVersion, read_version_date


class TestVersionReader(unittest.TestCase):

    def test_get_page(self):
        page = get_version_html_page()
        self.assertIsNotNone(page)

    def test_contains_cc_main(self):
        page = get_version_html_page()
        self.assertIn("CC-MAIN", page)

    def test_get_index_version(self):
        version_getter = VersionGetter()
        date_check = read_version_date("August 2019")
        self.assertIn(date_check, version_getter.get_versions())
        self.assertEqual(version_getter.get_url(date_check),
                         "https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-35/index.html")

    def test_fake_date(self):
        version_getter = VersionGetter()
        fake_date = read_version_date("August 1999")
        with self.assertRaises(InvalidVersion):
            version_getter.get_url(fake_date)

    def test_get_latest_version(self):
        version_getter = VersionGetter()
        latest_version_date, _ = version_getter.get_latest_version()
        date_check = read_version_date("August 2019")
        self.assertTrue(date_check <= latest_version_date)


if __name__ == '__main__':
    unittest.main()
