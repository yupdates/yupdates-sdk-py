# Yupdates Python SDK

The Yupdates Python SDK lets you easily use the Yupdates API from your own software and scripts.

Also see the [Yupdates Rust SDK](https://github.com/yupdates/yupdates-sdk-rs).

### Getting started

First, obtain an API token from the application. Navigate to "Settings" and then "API".

The examples will start with read-only operations, so you can use the general, read-only token to get started.

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
set +o history
export YUPDATES_API_TOKEN="1a7814fc25:c38bb526..."
set -o history
```

During the preview, you also need to set the URL. This won't be necessary once there is a default endpoint.
```shell
export YUPDATES_API_URL="https://..."
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

### Getting help

You can create a [GitHub issue](https://github.com/yupdates/yupdates-sdk-py/issues) on this repository for bugs and feature requests.

The fastest way to get help is to create a support ticket from the Yupdates application. Or email `support@yupdates.com`. Especially if you need help that is not specific to this SDK.

### License

The SDK is distributed under the MIT license, please see [LICENSE](https://github.com/yupdates/yupdates-sdk-py/blob/main/LICENSE) for more information.

This covers the source code and examples, but it does not cover related items like the Yupdates logo or API documentation which is not hosted here.
