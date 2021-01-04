import yaml
import json
import sys
from bot import BOT
import random
from dotenv import load_dotenv
import os
import logging

dotenv_path="bot.env"
load_dotenv(dotenv_path)

logging.basicConfig(level=logging.INFO)

arg_list = eval(str(sys.argv))
with open(arg_list[1]) as file:
    bot_configuration = yaml.load(file, Loader=yaml.FullLoader)
    NUMBER_OF_USERS = bot_configuration['number_of_users']
    MAX_POST = bot_configuration['max_posts_per_user']
    MAX_LIKE_DISLIKE = bot_configuration['max_likes_dislikes_per_user']

    bot_params = {
        'BACKEND_SCHEME' : os.environ.get('BACKEND_SCHEME'),
        'BACKEND_HOST' : os.environ.get('BACKEND_HOST'),
        'BACKEND_PORT' : os.environ.get('BACKEND_PORT')
    }

    logging.info('Bot will create {} user(s)'.format(NUMBER_OF_USERS))
    bot = BOT(**bot_params)
    for i in range(NUMBER_OF_USERS):
        logging.info('=====================================================================================================')
        logging.info('Bot is creating {}/{} user'.format(i+1, NUMBER_OF_USERS))
        username, password = bot.signup_user()
        logging.info('User {} created with username - {} password - {}'.format(i+1, username, password))
        login_data = {
            'username':username,
            'password':password
        }
        login_response = bot.login_user(login_data)
        bot.set_access_token(login_response.get("access"))

        NUMBER_OF_POSTS = random.randint(1, MAX_POST)
        logging.info('Bot will create {} post(s) for user {}. {}'.format(NUMBER_OF_POSTS, i+1, username))
        for j in range(NUMBER_OF_POSTS):
            logging.info('\t\t=====================================================================================')
            logging.info('Bot is creating {}/{} post'.format(j+1, NUMBER_OF_POSTS))
            id, title, content = bot.create_a_post()
            logging.info('Post {} created with id - {} title - {}'.format(j+1, id, title))

            NUMBER_OF_LIKE_DISLIKE = random.randint(1,MAX_LIKE_DISLIKE)
            logging.info('Bot will like/dislike post {} with id - {}, title - {} {} times'.format(j+1, id, title, NUMBER_OF_LIKE_DISLIKE))
            for k in range(NUMBER_OF_LIKE_DISLIKE):
                action_type = random.randint(1,2)
                response = bot.take_an_action(id, action_type)
                if action_type == 1:
                    logging.info('Bot liked post {} with id - {}, title - {} {}/{}'.format(j+1, id, title, k+1, NUMBER_OF_LIKE_DISLIKE))
                else:
                    logging.info('Bot disliked post {} with id - {}, title - {} {}/{}'.format(j+1, id, title, k+1, NUMBER_OF_LIKE_DISLIKE))
                print("post_response",response)
            logging.info('\t\t=====================================================================================')
        logging.info('=====================================================================================================')