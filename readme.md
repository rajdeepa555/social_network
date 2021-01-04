# App:Social Network
	//Description
	
# Configuration

	//Configure the environment variables for the bot in /bot/bot.env
	BACKEND_HOST=#
	BACKEND_PORT=#
	BACKEND_SCHEME=#

	//Configure the Bot variables in /bot/config.yaml
	number_of_users: #
	max_posts_per_user: #
	max_likes_dislikes_per_user: #

### Build
	//building the app
	sudo docker-compose build
	
	//building the bot
	sudo docker build -t bot .

### Run
	//running the app
	sudo docker-compose up
	
	//running the bot 
	sudo docker run bot config.yaml

