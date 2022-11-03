"""
You can instantiate `YupdatesClient` directly or call the top-level `yupdates_client()` function
for convenience.

Examples
--------
    from yupdates.client import yupdates_client
    from yupdates.models import InputItem
    import urllib

    yc = yupdates_client()
    yc.ping()

    try:
        # The error should complain about the missing URL:
        item = InputItem("a title", "some content", "")
        yc.new_items([item])
    except urllib.error.HTTPError as e:
        print(e.read())

    item = InputItem("a title", "some content", "https://www.example.com/something")
    yc.new_items([item])
"""

from .models import InputItem

import dataclasses
import json
import logging
import os
import urllib.request as ur

logger = logging.getLogger(__name__)

DEFAULT_YUPDATES_API_URL = "https://feeds.yupdates.com/api/v0/"


class YupdatesClient:
    """A client that lets you invoke each API operation.

    If you want to set all the configuration values explicitly, you can instantiate this class
    manually. Alternatively, use `yupdates_client()` which will look for the default environment
    variables and let you override just one configuration as needed.

    Or just call the functions in the `yapi` module to always use the default client which only
    needs the YUPDATES_API_TOKEN environment variable to be set.

    The `quiet` setting lets you get error-only logging without needing to configure logging
    levels. But setting logging levels will work, too.
    """
    def __init__(self, token, base_url, quiet):
        self.token = str(token)
        self.quiet = bool(quiet)
        s = str(base_url)
        if s.endswith("/"):
            self.base_url = s
        else:
            self.base_url = s + "/"

    def _headers(self):
        return {"X-Auth-Token": self.token}

    def ping(self):
        """Test the connection and authentication by calling ping.

        Returns the JSON response as a Python dict. There will be an exception if there is an issue.
        """
        url = f"{self.base_url}ping/"
        req = ur.Request(url, headers=self._headers())
        with ur.urlopen(req) as response:
            json_str = response.read()
            return json.loads(json_str)

    def ping_bool(self):
        """Test the connection and authentication by calling ping and returning True/False.

        Returns True if it worked, False if there is an issue. Convenience wrapper around ping().
        """
        try:
            self.ping()
            return True
        except Exception as e:
            logger.error(f"Issue pinging the API: {repr(e)}")
            return False

    def new_items(self, items):
        """Add new items to a feed.

        Returns the JSON response as a Python dict. There will be an exception if there is an issue.

        Parameters
        ----------
        items : list of models.InputItem

        Raises
        ------
        urllib.error.HTTPError
        """
        if not items:
            if not self.quiet:
                logger.warning("call to add new items - but there were no items?")
            return
        payload = {"items": _map_dataclasses_to_dicts(items, InputItem)}
        json_payload = json.dumps(payload).encode('utf-8')
        url = f"{self.base_url}items/"
        req = ur.Request(url, headers=self._headers(), method="POST", data=json_payload)
        with ur.urlopen(req) as response:
            json_str = response.read()
            return json.loads(json_str)


def yupdates_client(token=None, base_url=None, quiet=False):
    """Instantiate an instance of YupdatesClient, consulting environment variables when needed.

    This will look for the default environment variables and let you override just the
    configurations you want to set directly. Also see `YupdatesClient` for direct instantiation.

    Or call the functions in the `yapi` module to always use the default client which only needs
    the YUPDATES_API_TOKEN environment variable to be set.

    The `quiet` setting lets you get error-only logging without needing to configure logging
    levels. But setting logging levels will work, too.

    Parameters
    ----------
    token : str, optional
        API token. If None, the YUPDATES_API_TOKEN environment variable is required.
    base_url : str, optional
        Override the API URL. If None, the YUPDATES_API_URL environment variable will be used it
        is set. Otherwise, the default API URL will be used.
    quiet : bool, optional
        If True, all calls made with this client will log errors only, no matter the log level
        settings.

    Returns
    -------
    YupdatesClient

    Raises
    ------
    ValueError
        If the API token is missing
    """
    if token is None:
        token = os.environ.get('YUPDATES_API_TOKEN')
        if token is None:
            raise ValueError("API token is missing: set YUPDATES_API_TOKEN")
    if base_url is None:
        base_url = os.environ.get('YUPDATES_API_URL')
        if base_url is None:
            base_url = DEFAULT_YUPDATES_API_URL
    return YupdatesClient(token, base_url, quiet)


def _map_dataclasses_to_dicts(dc_list, klass):
    dict_list = []
    for dc in dc_list:
        if not isinstance(dc, klass):
            raise ValueError(f"expected list of {klass}")
        dict_list.append(dataclasses.asdict(dc))
    return dict_list
