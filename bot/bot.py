import requests
from requests.auth import AuthBase
import string 
import random 
import logging
from dotenv import load_dotenv
import os

class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        """Attach an API token to a custom auth header."""
        r.headers['X-TokenAuth'] = f'{self.token}'  # Python 3.6+
        return r

def get_environement_var():
    load_dotenv(dotenv_path='environment.env')
    BACKEND_HOST = os.getenv("BACKEND_HOST")
    BACKEND_PORT = os.getenv("BACKEND_PORT")
    return BACKEND_HOST, BACKEND_PORT

def get_random_post_details():
    N = random.randint(10, 50)
    title = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    N = random.randint(50, 200)
    content = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    return title, content

def get_random_user_details():
    N = random.randint(8, 20)
    username = ''.join(random.choices(string.ascii_letters + string.digits, k = N))
    email = username + "@gmail.com"
    password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k = N))
    first_name = ''.join(random.choices(string.ascii_uppercase, k = N))
    last_name = ''.join(random.choices(string.ascii_uppercase, k = N))
    return username, password, email, first_name, last_name

def like_unlike_post(access_token, post_id, max_like, max_unlike):
    BACKEND_HOST, BACKEND_PORT = get_environement_var()
    M = random.randint(1, max_like)
    logging.info('We are going to like Post having id- {} for {} times'.format(post_id,M))
    i=0
    while i < M:
        post_data = {
            'post': post_id,
            'action': 1
        }
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        logging.info('We are requesting to like the post having id- {} {}/{} times'.format(post_id, i+1, M))
        response = requests.post('http://' + BACKEND_HOST + ':'+ BACKEND_PORT +'/api/posts/preference/', data=post_data, headers=headers)
        if response.status_code != 400 and response.status_code != 500:
            logging.info('Post having id- {} liked {}/{} times'.format(post_id, i+1,M))
            i += 1
    N = random.randint(1, max_unlike)
    logging.info('We are going to dislike Post having id- {} for {} times'.format(post_id,N))
    i=0
    while i < N:
        post_data = {
            'post': post_id,
            'action': 2
        }
        headers = {
            'Authorization': 'Bearer ' + access_token
        }
        logging.info('We are requesting to dislike the post having id- {} {}/{} times'.format(post_id, i+1, N))
        response = requests.post('http://' + BACKEND_HOST + ':'+ BACKEND_PORT +'/api/posts/preference/', data=post_data, headers=headers)
        if response.status_code != 400 and response.status_code != 500:
            logging.info('Post having id- {} disliked {}/{} times'.format(post_id, i+1,N))
            i += 1

def create_a_post(access_token, max_post, max_like, max_unlike, usercount, username):
    try:
        BACKEND_HOST, BACKEND_PORT = get_environement_var()
        M = random.randint(1, max_post)
        logging.info('We are going to create {} posts for user {} having username- {}'.format(M, usercount, username))
        i=0
        while i < M:
            title, content = get_random_post_details()
            post_data = {
                'title': title,
                'content': content
            }
            headers = {
                'Authorization': 'Bearer ' + access_token
            }
            logging.info('\t\t\t==============================================================')
            logging.info('We are requesting to create post {}/{} for user {} having username- {}'.format(i+1, M, usercount, username))
            print('title: ', title, '\ncontent: ', content)
            response = requests.post('http://' + BACKEND_HOST + ':'+ BACKEND_PORT +'/api/posts/', data=post_data, headers=headers)
            print(response)
            post_id = response.json()['id']
            if response.status_code != 400 and response.status_code != 500:
                logging.info('Post {} for user {} having username- {} created with id-{}, title-{}'.format(i+1, usercount, username, post_id, title))
                like_unlike_post(access_token, post_id, max_like, max_unlike)
                i += 1
    except Exception as e:
        print(e)

def signup_user(max_user, max_post, max_like, max_unlike):
    BACKEND_HOST, BACKEND_PORT = get_environement_var()
    logging.info('We are going to create {} users'.format(max_user))
    i = 0
    while i < max_user:
        username, password, email, first_name, last_name = get_random_user_details()
        user_data = {
            'username': username,
            'password': password,
            'password2': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name
        }
        logging.info('==================================================================================================')
        logging.info('We are requesting to create user {}/{}'.format(i+1, max_user))
        response = requests.post('http://' + BACKEND_HOST + ':'+ BACKEND_PORT +'/api/auth/register/', user_data)
        if response.status_code != 400 and response.status_code != 500:
            logging.info('User {} created with username- {}, Email- {}, Password- {}'.format(i+1, username, email, password))
            
            login_data = {
                'username': username,
                'password': password
            }
            response = requests.post('http://' + BACKEND_HOST + ':'+ BACKEND_PORT +'/api/auth/login/', login_data)
            # refresh_token = response.json()['refresh']
            access_token = response.json()['access']
            print('username: ', username, '\npassword: ', password, '\naccess_token: ', access_token)
            create_a_post(access_token, max_post, max_like, max_unlike, i+1, username)
            logging.info('==================================================================================================')
            i += 1



class BOT:

    def __init__(self, **kwargs):
        self.BACKEND_SCHEME = "http"
        self.BACKEND_HOST = "35.178.183.18"
        self.BACKEND_PORT = 8000
        self.access_token = None

    def _get_backend_url(self,url_end_point):
        return f"{self.BACKEND_SCHEME}://{self.BACKEND_HOST}:{self.BACKEND_PORT}{url_end_point}"

    def _get_random_string(self,min_len=8,max_len=20):
        return ''.join(random.choices(string.ascii_letters, k = random.randint(min_len, max_len)))

    def _get_fake_user(self):
        password = self._get_random_string()
        user_data = {
            'username': self._get_random_string(),
            'password': password,
            'password2': password,
            'email': f'{self._get_random_string()}@gmail.com',
            'first_name': self._get_random_string(),
            'last_name': self._get_random_string()
        }
        return user_data

    def _get_fake_post(self):
        post_data = {
            'title':self._get_random_string(min_len=10,max_len=50),
            'content':self._get_random_string(min_len=50,max_len=200)
        }
        return post_data

    def set_access_token(self,access_token):
        self.access_token = access_token

    def _get_headers(self):
        headers = {}
        if self.access_token:
            headers["Authorization"] = f'Bearer {self.access_token}'
        return headers

    def _make_a_request(self,url_end_point,form_data):
        return requests.post(self._get_backend_url(url_end_point), data= form_data, headers= self._get_headers())

    def signup_user(self):
        fake_user = self._get_fake_user()
        response = self._make_a_request("/api/auth/register/",fake_user)
        response_json = response.json()
        return response_json.get("username"), fake_user.get("password")


    def login_user(self,login_data):
        response = self._make_a_request("/api/auth/login/",login_data)
        return response.json()
    
    def create_a_post(self):
        fake_post = self._get_fake_post()
        response = self._make_a_request("/api/posts/",fake_post)
        return response.json()

    
        
if __name__=="__main__":
    bot = BOT()
    for i in range(2):
        username, password = bot.signup_user()
        login_data = {
            'username':username,
            'password':password
        }
        login_response = bot.login_user(login_data)
        print("login_response",login_response)