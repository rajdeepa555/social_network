import yaml
from bot import signup_user
import json
import sys


arg_list = eval(str(sys.argv))
with open(arg_list[1]) as file:
    bot_configuration = yaml.load(file, Loader=yaml.FullLoader)
    MAX_USER = bot_configuration['number_of_users']
    MAX_POST = bot_configuration['max_posts_per_user']
    MAX_LIKE = bot_configuration['max_likes_per_user']
    MAX_UNLIKE = bot_configuration['max_unlikes_per_user']
    signup_user(MAX_USER, MAX_POST, MAX_LIKE, MAX_UNLIKE)