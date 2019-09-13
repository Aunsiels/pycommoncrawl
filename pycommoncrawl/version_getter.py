import datetime
import hashlib
import os
import re
import time
import urllib.request

N_SECONDS_PER_DAY = 60 * 60 * 24
BASE = "https://commoncrawl.s3.amazonaws.com/crawl-data/"


class VersionGetter(object):

    def __init__(self):
        self.index_versions = get_index_versions()

    def get_latest_version(self):
        most_recent_date = None
        for key in self.index_versions:
            if most_recent_date is None:
                most_recent_date = key
            elif most_recent_date < key:
                most_recent_date = key
        return most_recent_date, self.index_versions[most_recent_date]

    def get_versions(self):
        return list(self.index_versions.keys())

    def get_url(self, version):
        if version not in self.index_versions:
            raise InvalidVersion
        return self.index_versions[version]


def get_version_html_page():
    return get_raw_html_page(BASE + "index.html")


def get_raw_html_page(url):
    cached_version = get_cached_version_if_possible(url)
    if cached_version is not None:
        return cached_version
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        save_cached_version(url, content)
        return content


def get_cached_version_if_possible(url):
    encoded_url = get_encoded_filename(url)
    if os.path.exists(encoded_url):
        creation_time = os.stat(encoded_url).st_ctime
        file_is_too_old = time.time() - creation_time > N_SECONDS_PER_DAY
        if not file_is_too_old:
            with open(encoded_url) as f:
                return f.read()
    return None


def save_cached_version(url, content):
    encoded_url = get_encoded_filename(url)
    with open(encoded_url, "w") as f:
        return f.write(content)


def get_encoded_filename(filename):
    return hashlib.sha512(filename.encode("utf-8")).hexdigest() + ".tmp"


def get_index_versions():
    page = get_version_html_page()
    regex = re.compile(r'<td><a href="(?P<url>./CC-MAIN[^"]*)">CC-MAIN-2019-35</a></td>[^<]*'
                       '<td><a href="(?P<urluseless>https?://commoncrawl.org/[^"]*)">(?P<date>[^<]*)</a></td>')
    versions = dict()
    for match in regex.finditer(page):
        versions[read_version_date(match.group("date"))] = BASE + match.group("url")[2:]
    return versions


def read_version_date(raw_date):
    return datetime.datetime.strptime(raw_date, "%B %Y")


class InvalidVersion(Exception):
    pass
