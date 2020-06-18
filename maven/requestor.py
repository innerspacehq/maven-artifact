import base64

from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

UTF_8 = 'utf-8'


class Requestor(object):
    def __init__(self, username=None, password=None, user_agent="Maven Artifact Downloader/1.0"):
        self.user_agent = user_agent
        self.username = username
        self.password = password

    def request(self, url, on_fail, on_success):
        headers = {"User-Agent": self.user_agent}
        if self.username and self.password:
            auth_header = base64.b64encode(bytes('{}:{}'.format(self.username, self.password), UTF_8)).decode(UTF_8)
            headers["Authorization"] = "Basic " + auth_header
        req = Request(url, None, headers)
        try:
            response = urlopen(req)
        except HTTPError as e:
            on_fail(url, e)
        except URLError as e:
            on_fail(url, e)
        else:
            return on_success(response)


class RequestException(Exception):
    def __init__(self, msg):
        self.msg = msg
