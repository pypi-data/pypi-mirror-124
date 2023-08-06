# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['httpservermock']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'httpservermock',
    'version': '0.1.0',
    'description': 'A python library that provides a http server mock that can be used for testing code that should interact with an http server',
    'long_description': '# httpservermock\n\n`httpservermock` provides a HTTP server mock that can be used to test code that needs to interact with an HTTP server.\n\n```bash\npip install httpservermock\n# or\npoetry add --dev httpservermock\n```\n\nExample usage:\n\n```python\nfrom urllib.error import HTTPError\nfrom urllib.request import urlopen\n\nimport pytest\n\nfrom httpservermock import MethodName, MockHTTPResponse, ServedBaseHTTPServerMock\n\n\ndef test_example() -> None:\n    with ServedBaseHTTPServerMock() as httpmock:\n        httpmock.responses[MethodName.GET].append(\n            MockHTTPResponse(404, "Not Found", b"gone away", {})\n        )\n        httpmock.responses[MethodName.GET].append(\n            MockHTTPResponse(200, "OK", b"here it is", {})\n        )\n\n        # send a request to get the first response\n        with pytest.raises(HTTPError) as raised:\n            urlopen(f"{httpmock.url}/bad/path")\n        assert raised.value.code == 404\n\n        # get and validate request that the mock received\n        req = httpmock.requests[MethodName.GET].pop(0)\n        assert req.path == "/bad/path"\n\n        # send a request to get the second response\n        resp = urlopen(f"{httpmock.url}/")\n        assert resp.status == 200\n        assert resp.read() == b"here it is"\n\n        httpmock.responses[MethodName.GET].append(\n            MockHTTPResponse(404, "Not Found", b"gone away", {})\n        )\n        httpmock.responses[MethodName.GET].append(\n            MockHTTPResponse(200, "OK", b"here it is", {})\n        )\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
