# Yupdates Python SDK

The Yupdates Python SDK lets you easily use the Yupdates API from your own software and scripts.

This is [hosted on GitHub](https://github.com/yupdates/yupdates-sdk-py). There is also a [Yupdates Rust SDK](https://github.com/yupdates/yupdates-sdk-rs).

### Requirements

The Python SDK has *zero external dependencies*. It is written so that you can easily drop it into your scripts, Lambda functions, and bigger projects without any dependency needs or conflicts.

It requires Python 3.7 or higher.

You will need an API token from the application. Navigate to "Settings" and then "API".

The examples below start with read-only operations, so you can use the general, read-only token to get started.

### Installation

Before running the following commands, we assume you have set up your environment (pyenv, virtualenv, etc.).

Install the SDK via [pip](https://pip.pypa.io).

```shell
$ pip install yupdates
```

Or, install from source:
```shell
$ git clone git://github.com/yupdates/yupdates-sdk-py.git
$ cd yupdates-sdk-py
$ pip install .
```

Set the API token environment variable:
```shell
$ set +o history
$ export YUPDATES_API_TOKEN="1a7814fc25:c38bb526..."
$ set -o history
```

Now test the connection and authentication. This will work from a Python shell or script:
```python
from yupdates import yapi
print(yapi.ping())
```

If there is anything but a 200 response, it will throw an exception. Otherwise, this will print out the JSON response which is returned from the `ping` function deserialized into a Python dict.

The `ping` operation is helpful to run in the beginning of your scripts to make sure there are no setup issues.

Another way to use the SDK is to instantiate a client once and use it repeatedly:
```python
from yupdates.client import yupdates_client
yup = yupdates_client()
print(yup.ping())
```

### Read items from a feed

```python
from yupdates import yapi

feed_id = '02fb24a4478462a4491067224b66d9a8b2338dada2737'
feed_items = yapi.read_items(feed_id)  # See client.py for optional parameters

for feed_item in feed_items:
    print(feed_item.title)  # See models.py and API docs for field descriptions
```

### Write items to a feed

To write items, you cannot use the read-only API token anymore. Obtain a token with write privileges by adding an API input to a feed in the app, and set the `YUPDATES_API_TOKEN` environment variable as you did above.

```python
from yupdates.client import yupdates_client
from yupdates.models import InputItem

yc = yupdates_client()
item = InputItem("a title", "some content", "https://www.example.com/something")
yc.new_items([item])
```

The API token is feed-specific, which is why there is no other configuration needed. You make one configuration (the API token) and Yupdates figures out the rest on the server side.

That is for convenience, but it also means there's only one permission to reason about, and a small blast radius if it's exposed. The token is authorized to add items to one, single feed, and it cannot do anything else (not even read items). You're not dropping a master key into a cronjob script or Lambda function or wherever it's going to run.

In the future, it will be possible to obtain a token with wider writer privileges, so you can add items to multiple feeds.

### Getting help

You can create a [GitHub issue](https://github.com/yupdates/yupdates-sdk-py/issues) on this repository for bugs and feature requests.

The fastest way to get help is to create a support ticket from the Yupdates application. Or email `support@yupdates.com`. Especially if you need help that is not specific to this SDK, or if you would like more hands-on setup and troubleshooting advice.

### Conventions

This library follows the [Numpy docstring conventions](https://numpydoc.readthedocs.io/en/stable/format.html#docstring-standard).

### License

The SDK is distributed under the MIT license, please see [LICENSE](https://github.com/yupdates/yupdates-sdk-py/blob/main/LICENSE) for more information.

This covers the source code and examples, but it does not cover related items like the Yupdates logo or API documentation which is not hosted here.
