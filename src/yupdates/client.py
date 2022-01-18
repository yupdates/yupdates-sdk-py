"""
You can instantiate `YupdatesClient` directly or call the top-level `yupdates_client()` function
for convenience.

Example:
    from yupdates.client import yupdates_client

    yup = yupdates_client()
    yup.ping()
"""

import json
import logging
import os
import urllib.request as ur

logger = logging.getLogger(__name__)

# This must be set by environment variable during preview. The default will be here in the future.
DEFAULT_YUPDATES_API_URL = "coming soon"


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


def yupdates_client(token=None, base_url=None, quiet=False):
    """Instantiate an instance of YupdatesClient, consulting environment variables when needed.

    This will look for the default environment variables and let you override just the
    configurations you want to set directly. Also see `YupdatesClient` for direct instantiation.

    Or just call the functions in the `yapi` module to always use the default client which only
    needs the YUPDATES_API_TOKEN environment variable to be set.

    The `quiet` setting lets you get error-only logging without needing to configure logging
    levels. But setting logging levels will work, too.

    :param token: If None, the YUPDATES_API_TOKEN environment variable is required.
    :param base_url: If None, the YUPDATES_API_URL environment variable will be used it is set.
    Otherwise, the default API URL will be used.
    :param quiet: If True, all calls made with this client will log errors only, no matter the
    log level settings.
    :return: Instance of `YupdatesClient`
    """
    if token is None:
        token = os.environ.get('YUPDATES_API_TOKEN')
        if token is None:
            raise ValueError("API token is missing: set YUPDATES_API_TOKEN")
    if base_url is None:
        base_url = os.environ.get('YUPDATES_API_URL')
        if base_url is None:
            base_url = DEFAULT_YUPDATES_API_URL
            if base_url == "coming soon":
                raise ValueError("Sorry, during the preview you also need to set YUPDATES_API_URL")
    return YupdatesClient(token, base_url, quiet)
