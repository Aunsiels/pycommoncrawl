# PyCommonCrawl

A python interface for [Common Crawl](https://commoncrawl.org/).

## INSTALL

TODO

## USAGE

```python
from pycommoncrawl.common_crawl_data_accessor import CommonCrawlDataAccessor

common_crawl_data_accessor = CommonCrawlDataAccessor()

# Iterate by line
for line in common_crawl_data_accessor.get_raw_resource_data("WAT"):
    print(line)

# Iterate by WARC bloc
for warc in common_crawl_data_accessor.get_raw_resource_data_per_warc("WAT"):
    print(warc["Content-Length"])
```
