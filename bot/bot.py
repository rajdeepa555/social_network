import requests
from requests.auth import AuthBase

class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['X-TokenAuth'] = f'{self.token}'  # Python 3.6+
        return r





def signup_user():
    pass

def like_unlike_post():
    pass

def create_a_post():
    pass


if __name__=="__main__":
    # requests.get('http://13.237.55.246:8000/hello/?format=json', auth=TokenAuth('12345abcde-token'))
    response = requests.get('http://13.237.55.246:8000/hello/?format=json')
    print("response",dir(response))
    print("json",response.json())

