import yaml
import json
import sys
from bot import BOT
import random


arg_list = eval(str(sys.argv))
with open(arg_list[1]) as file:
    bot_configuration = yaml.load(file, Loader=yaml.FullLoader)
    NUMBER_OF_USERS = bot_configuration['number_of_users']
    MAX_POST = bot_configuration['max_posts_per_user']
    MAX_LIKE_DISLIKE = bot_configuration['max_likes_dislikes_per_user']

    bot = BOT()
    for i in range(NUMBER_OF_USERS):
        username, password = bot.signup_user()
        login_data = {
            'username':username,
            'password':password
        }
        login_response = bot.login_user(login_data)
        bot.set_access_token(login_response.get("access"))
        
        for j in range(random.randint(1, MAX_POST)):
            post_response = bot.create_a_post()

            for k in range(random.randint(1,MAX_LIKE_DISLIKE)):
                action_type = random.randint(1,2)
                response = bot.take_an_action(post_response.get("id"), action_type)
                print("post_response",response)