# httpservermock

`httpservermock` provides a HTTP server mock that can be used to test code that needs to interact with an HTTP server.

```bash
pip install httpservermock
# or
poetry add --dev httpservermock
```

Example usage:

```python
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from httpservermock import MethodName, MockHTTPResponse, ServedBaseHTTPServerMock


def test_example() -> None:
    with ServedBaseHTTPServerMock() as httpmock:
        httpmock.responses[MethodName.GET].append(
            MockHTTPResponse(404, "Not Found", b"gone away", {})
        )
        httpmock.responses[MethodName.GET].append(
            MockHTTPResponse(200, "OK", b"here it is", {})
        )

        # send a request to get the first response
        with pytest.raises(HTTPError) as raised:
            urlopen(f"{httpmock.url}/bad/path")
        assert raised.value.code == 404

        # get and validate request that the mock received
        req = httpmock.requests[MethodName.GET].pop(0)
        assert req.path == "/bad/path"

        # send a request to get the second response
        resp = urlopen(f"{httpmock.url}/")
        assert resp.status == 200
        assert resp.read() == b"here it is"

        httpmock.responses[MethodName.GET].append(
            MockHTTPResponse(404, "Not Found", b"gone away", {})
        )
        httpmock.responses[MethodName.GET].append(
            MockHTTPResponse(200, "OK", b"here it is", {})
        )
```
