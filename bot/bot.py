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

if __name__=="__main__":
    # requests.get('http://13.237.55.246:8000/hello/?format=json', auth=TokenAuth('12345abcde-token'))
    response = requests.get('http://13.237.55.246:8000/hello/?format=json')
    print("response",dir(response))
    print("json",response.json())