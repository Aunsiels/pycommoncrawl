import unittest

from pycommoncrawl.warc_string_record import WARCStringRecord

test_string = """
WARC/1.0
WARC-Type: metadata
WARC-Target-URI: http://0084xg.com/qpqf/56651/index.html
WARC-Date: 2019-08-26T12:01:52Z
WARC-Record-ID: <urn:uuid:59c7bb9c-8fcb-4008-93f0-f7849c59cc3e>
WARC-Refers-To: <urn:uuid:ecd48def-1234-41e0-b0af-9526f351b5de>
Content-Type: application/json
Content-Length: 1429

{"Container":{"Filename":"CC-MAIN-20190817203056-20190817225056-00000.warc.gz","Compressed":true,"Offset":"479","Gzip-Metadata":{"Deflate-Length":"466","Header-Length":"10","Footer-Length":"8","Inflated-CRC":"-629352379","Inflated-Length":"676"}},"Envelope":{"Payload-Metadata":{"Actual-Content-Type":"application/http; msgtype=request","HTTP-Request-Metadata":{"Request-Message":{"Method":"GET","Path":"/qpqf/56651/index.html","Version":"HTTP/1.1"},"Headers-Length":"312","Headers":{"User-Agent":"CCBot/2.0 (https://commoncrawl.org/faq/)","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"en-US,en;q=0.5","If-Modified-Since":"Fri, 24 May 2019 07:10:57 GMT","Host":"0084xg.com","Connection":"Keep-Alive","Accept-Encoding":"gzip"},"Entity-Length":"0","Entity-Digest":"sha1:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ","Entity-Trailing-Slop-Length":"0"},"Actual-Content-Length":"314","Block-Digest":"sha1:5YSAPEQVLJTWB32MYPD6CZHUDI6B7G2P","Trailing-Slop-Length":"4"},"Format":"WARC","WARC-Header-Length":"358","WARC-Header-Metadata":{"WARC-Type":"request","WARC-Date":"2019-08-17T20:58:30Z","WARC-Record-ID":"<urn:uuid:ecd48def-1234-41e0-b0af-9526f351b5de>","Content-Length":"314","Content-Type":"application/http; msgtype=request","WARC-Warcinfo-ID":"<urn:uuid:47046f65-c301-4c0b-b60f-7a1e6679a355>","WARC-IP-Address":"107.165.103.19","WARC-Target-URI":"http://0084xg.com/qpqf/56651/index.html"}}}

"""


class TestWARCString(unittest.TestCase):

    def test_get_record(self):
        warc_string = WARCStringRecord(test_string)
        self.assertIsNotNone(warc_string.get_content())

    def test_correct_record(self):
        warc_string = WARCStringRecord(test_string)
        self.assertIn('WARC-Target-URI', warc_string)
        self.assertIn('WARC-Type', warc_string)


if __name__ == '__main__':
    unittest.main()
