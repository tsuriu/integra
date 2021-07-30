import requests


class http(object):
    """This class must to be the http request module."""

    def __init__(self, base_url, headers=None):
        """Start method."""
        self.base_url = base_url    
        if headers is not None:
            self.headers = headers

    def get(self, endpoint=None, output=None, payload=None):
        """Get method."""
        if endpoint is not None:
            url = self.base_url+endpoint

        try:
            res = requests.get(url, data=payload, headers=self.headers)
            if output == "json":
                res =  res.json()
            if output == "file":
                res = res.content
            else:
                print("Fail to define output!")

        except requests.exceptions.RequestException as error:
            res = error

        return res

    def post(self, endpoint=None, output=None, payload=None):
        """Post method."""
        if endpoint is not None:
            url = self.base_url+endpoint

        try:
            res = requests.post(url, data=payload, headers=self.headers)

            if output == "json":
                res =  res.json()
            elif output == "file":
                res = res.content
            else:
                print("Fail to define output!")
        except requests.exceptions.RequestException as error:
            res = error

        return res