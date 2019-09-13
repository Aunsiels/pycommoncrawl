import gzip
import os
import re
import unittest

import progressbar

from pycommoncrawl.utils import get_raw_html_page, download, BASE


class UnknownResourceName(Exception):

    def __init__(self, resources_available):
        super().__init__("Available resources: " + ", ".join(resources_available))


def get_destination(url):
    destination = url.split('/')[-1]
    return destination


class CommonCrawlDataAccessor(object):

    def __init__(self, url, clean_after=True):
        self.url = url
        self.clean_after = clean_after
        self.base = "/".join(url.split("/")[:-1])
        self.raw_info_page = get_raw_html_page(url)
        self.resources = dict(zip(self.get_part_names(), self.get_urls()))

    def get_part_names(self):
        regex = re.compile(r"<td>(?P<name>(\w|\s|\.|-)*)</td>")
        return [x.group("name") for x in regex.finditer(self.raw_info_page)]

    def get_urls(self):
        regex = re.compile(r'<td><a href="(?P<url>[^"]*)">[^<]*</a></td>')
        return [self.base + x.group("url")[1:] for x in regex.finditer(self.raw_info_page)]

    def get_number_files(self, resource_name):
        self.check_if_legal_resource(resource_name)
        return sum(self.apply_on_each_line(resource_name, lambda x: 1))

    def apply_on_each_line(self, resource_name, function):
        url = self.resources[resource_name]
        yield from self.apply_on_each_line_url(url, function)

    def apply_on_each_line_url(self, url, function):
        destination = get_destination(url)
        download(url, destination)
        with gzip.open(destination, 'rb') as f:
            for line in f:
                yield function(line.decode("utf-8"))
        if self.clean_after:
            os.remove(destination)

    def check_if_legal_resource(self, resource_name):
        if resource_name not in self.resources:
            raise UnknownResourceName(self.resources.keys())

    def get_raw_resource_data(self, resource_name, min_file_number=0, max_file_number=-1):
        self.check_if_legal_resource(resource_name)
        urls = list(self.apply_on_each_line(resource_name, lambda x: BASE + x.strip()))
        if max_file_number == -1:
            urls = urls[min_file_number:]
        else:
            urls = urls[min_file_number:max_file_number]
        bar = progressbar.ProgressBar(
            max_value=len(urls),
            widgets=[
                ' [', progressbar.Timer(), '] ',
                progressbar.Bar(),
                ' ',
                ' (', progressbar.ETA(), ') ',
                progressbar.Counter(format='%(value)02d/%(max_value)d'),
            ]
        )
        for i, url in enumerate(urls):
            bar.update(i)
            yield from self.apply_on_each_line_url(url, lambda x: x)
        bar.finish()

    def get_raw_resource_data_per_block(self, resource_name, min_file_number=0, max_file_number=-1):
        buffer = []
        n_empty_line = 0
        for line in self.get_raw_resource_data(resource_name, min_file_number, max_file_number):
            if n_empty_line == 3:
                yield "\n".join(buffer)
                buffer = []
            line = line.strip()
            if line:
                n_empty_line = 0
            else:
                n_empty_line += 1
            buffer.append(line)
        yield "\n".join(buffer)


class TestCommonCrawlDataAccessor(unittest.TestCase):

    def setUp(self) -> None:
        self.common_crawl_data_accessor = CommonCrawlDataAccessor("https://commoncrawl.s3.amazonaws.com/crawl-data/"
                                                                  "CC-MAIN-2019-35/index.html", False)

    def test_part_names(self):
        self.assertIn("Segments", self.common_crawl_data_accessor.get_part_names())
        self.assertIn("URL index files", self.common_crawl_data_accessor.get_part_names())
        self.assertEqual(7, len(self.common_crawl_data_accessor.get_part_names()))

    def test_get_urls(self):
        self.assertEqual(7, len(self.common_crawl_data_accessor.get_urls()))
        self.assertIn("https://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-35/segment.paths.gz",
                      self.common_crawl_data_accessor.get_urls())

    def test_number_files(self):
        self.assertEqual(56000, self.common_crawl_data_accessor.get_number_files("WAT"))
        with self.assertRaises(UnknownResourceName):
            self.common_crawl_data_accessor.get_number_files("WTF")

    def test_raw_resource_data(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data("WAT", 0, 1):
            counter += 1
        self.assertEqual(1768135, counter)

    def test_raw_resource_data_block(self):
        counter = 0
        for _ in self.common_crawl_data_accessor.get_raw_resource_data_per_block("WAT", 0, 1):
            counter += 1
        self.assertEqual(160739, counter)


if __name__ == '__main__':
    unittest.main()
