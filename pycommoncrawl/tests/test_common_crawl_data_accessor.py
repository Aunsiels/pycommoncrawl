import os
import unittest
from shutil import copyfile

from pycommoncrawl.common_crawl_data_accessor import UnknownResourceName, CommonCrawlDataAccessor


class CommonCrawlDataAccessorTest(CommonCrawlDataAccessor):

    def download(self, url, destination):
        if "wat.paths.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/wat.paths.gz", destination)
        elif "file0.warc.wat.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file0.warc.wat.gz", destination)
        elif "file1.warc.wat.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file1.warc.wat.gz", destination)
        elif "warc.paths.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/warc.paths.gz", destination)
        elif "file0.warc.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file0.warc.gz", destination)
        elif "file1.warc.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file1.warc.gz", destination)
        elif "wet.paths.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/wet.paths.gz", destination)
        elif "file0.warc.wet.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file0.warc.wet.gz", destination)
        elif "file1.warc.wet.gz" in url:
            copyfile(os.path.dirname(os.path.realpath(__file__)) + "/data/file1.warc.wet.gz", destination)



class TestCommonCrawlDataAccessor(unittest.TestCase):

    def setUp(self) -> None:
        self.common_crawl_data_accessor = CommonCrawlDataAccessorTest("https://commoncrawl.s3.amazonaws.com/crawl-data/"
                                                                      "CC-MAIN-2019-35/index.html", False)

    def test_part_names(self):
        self.assertIn("Segments", self.common_crawl_data_accessor.get_part_names())
        self.assertIn("URL index files", self.common_crawl_data_accessor.get_part_names())
        self.assertEqual(7, len(self.common_crawl_data_accessor.get_part_names()))

    def test_get_urls(self):
        self.assertEqual(7, len(self.common_crawl_data_accessor.get_urls()))
        self.assertIn("https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-35/segment.paths.gz",
                      self.common_crawl_data_accessor.get_urls())

    def test_number_files_wat(self):
        self.assertEqual(2, self.common_crawl_data_accessor.get_number_files("WAT"))
        with self.assertRaises(UnknownResourceName):
            self.common_crawl_data_accessor.get_number_files("WTF")

    def test_raw_resource_data(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data("WAT"):
            counter += 1
        self.assertEqual(92, counter)

    def test_raw_resource_data_block(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data_per_block("WAT"):
            counter += 1
        self.assertEqual(8, counter)

    def test_raw_resource_data_warc(self):
        for warc in self.common_crawl_data_accessor.get_raw_resource_data_per_warc("WAT"):
            self.assertNotEqual(0, warc["Content-Length"])
            self.assertNotEqual("0", warc["Content-Length"])

    def test_number_files_warc(self):
        self.assertEqual(2, self.common_crawl_data_accessor.get_number_files("WARC"))

    def test_raw_resource_data_block_warc(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data_per_block("WARC"):
            counter += 1
        self.assertEqual(5, counter)

    def test_raw_resource_data_warc_warc(self):
        for warc in self.common_crawl_data_accessor.get_raw_resource_data_per_warc("WARC"):
            self.assertNotEqual(0, warc["Content-Length"])
            self.assertNotEqual("0", warc["Content-Length"])

    def test_number_files_wet(self):
        self.assertEqual(2, self.common_crawl_data_accessor.get_number_files("WET"))

    def test_raw_resource_data_block_wet(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data_per_block("WET"):
            counter += 1
        self.assertEqual(3, counter)

    def test_raw_resource_data_warc_wet(self):
        for warc in self.common_crawl_data_accessor.get_raw_resource_data_per_warc("WET"):
            self.assertNotEqual(0, warc["Content-Length"])
            self.assertNotEqual("0", warc["Content-Length"])


if __name__ == '__main__':
    unittest.main()
