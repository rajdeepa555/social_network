import requests
import string 
import random 
import logging
from dotenv import load_dotenv
import os

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

    def take_an_action(self, post_id, action_type):
        action_data = {
            'post': post_id,
            'action': action_type
        }

        response = self._make_a_request("/api/posts/preference/",action_data)
        return response.json()
