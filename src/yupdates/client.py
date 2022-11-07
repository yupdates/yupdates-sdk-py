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

from . import normalize_item_time
from .models import InputItem, FeedItem

import dataclasses
import json
import logging
import os
import urllib.parse
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

        GET $base_url/ping/
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

        POST $base_url/items/

        Parameters
        ----------
        items : list of models.InputItem
            You can send up to 10 at a time. See notes below for chunked example. Sending zero
            items is legal (you might want to verify the credential is authorized for this call, or
            you might want to get the matching `feed_id` returned without adding an item).

        Raises
        ------
        urllib.error.HTTPError

        Notes
        -----
        To send a list larger than 10, chunk them into separate calls of 10 or fewer items.
        For example, given the list `items` and YupdatesClient `yc`:

            chunk_size = 10
            list_chunked = [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]
            for chunk in list_chunked:
                yc.new_items(chunk)
                print(f"Added {len(chunk)} item(s)")
                time.sleep(0.2)  # Preempt being throttled
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

    def read_items(self, feed_id, max_items=10, include_item_content=False, item_time_after=None,
                   item_time_before=None):
        """Read items from a feed.

        GET $base_url/feeds/$feed_id

        Parameters
        ----------
        feed_id : str
            The feed to read from, an ID like '02fb24a4478462a4491067224b66d9a8b2338dada2737'
        max_items : int, optional
            The number of items to return, must be 1 <= N <= 50. Default is 10. May not be more
            than 10 if `include_item_content` is True.
        include_item_content : bool
            If True, populate each FeedItem with the full item content.
        item_time_after : str or int, optional
            Only return items that come after this item time (non-inclusive). See notes.
        item_time_before : str or int, optional
            Only return items that come before this item time (non-inclusive). See notes.

        Returns
        -------
        items : list of models.FeedItem

        Raises
        ------
        ValueError
        urllib.error.HTTPError

        Notes
        -----
        If you don't supply `item_time_after` or `item_time_before`, the latest items are queried.
        You cannot supply `item_time_after` and `item_time_before` at the same time.

        An item time is a unix epoch millisecond with an optional 5 digit suffix. In practice, you
        would only use the suffix form if you got that as the item time string from the service.
        Examples: 1234, 1661564013555, "1661564013555", "1661564013555.00003"
        """
        if not feed_id:
            raise ValueError("`feed_id` is missing")
        feed_id = str(feed_id).strip()

        # Validation to catch basic issues, full validation is server-side
        if len(feed_id) != 45:
            raise ValueError("`feed_id` expected to be 45 characters")
        if include_item_content and not 1 <= max_items <= 10:
            raise ValueError("`max_items` must be 1 to 10 when `include_item_content` is True")
        if not 1 <= max_items <= 50:
            raise ValueError("`max_items` must be 1 to 50")

        params = {'max_items': max_items, 'include_item_content': include_item_content}

        if item_time_after is not None:
            params['item_time_after'] = normalize_item_time(item_time_after)
        if item_time_before is not None:
            params['item_time_before'] = normalize_item_time(item_time_before)
        if item_time_after and item_time_before:
            raise ValueError("cannot simultaneously query `item_time_after` and `item_time_before`")

        encoded_params = urllib.parse.urlencode(params)
        url = f"{self.base_url}feeds/{feed_id}/?{encoded_params}"
        req = ur.Request(url, headers=self._headers())
        with ur.urlopen(req) as response:
            json_str = response.read()
            data_dict = json.loads(json_str)
            feed_item_dicts = data_dict['feed_items']
            return _map_dicts_to_dataclasses(feed_item_dicts, FeedItem)


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


def _map_dicts_to_dataclasses(dict_list, klass):
    dc_list = []
    for data_dict in dict_list:
        dc = klass(**data_dict)
        dc_list.append(dc)
    return dc_list
