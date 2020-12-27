import yaml

with open('config.yaml') as file:
    bot_configuration = yaml.load(file, Loader=yaml.FullLoader)
    print(bot_configuration)