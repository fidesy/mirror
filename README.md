# mirror
aggregator of news and posts from multiple platforms, currently only support telegram

## Features
* [x] Listen to new posts from telegram and save them
* [x] Web interface
* [x] Search by keywords 
* [ ] ...


## Screenshots
![](./docs/preview.png)

![](./docs/search.png)

## Installation
1. clone the repository
```
git clone https://github.com/fidesy/mirror.git
```

2. Rename .env.example to .env. Fill in [configs/config.yaml](./configs/config.yaml) file with your variables. Find api_id and api_hash from your telegram account [(guide)](https://core.telegram.org/api/obtaining_api_id). Channel username is the channel that posts will be forwarded to.

3. activate python environment and install dependencies
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Run the app to init telegram client. This is needed to create session file for transfer to the docker container.
```
python -m mirror.init_client
```

5. set env variable for the correct installation, build and run docker app containers
```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose up -d
```

6. Initialize database tables
```
make migrate-up
```

now website is available at localhost:3000

## Usage

You can manage your appication using the API.

Add channel and parse the latest 50 posts.
```
curl -H "X-TOKEN: YOUR_CUSTOM_ENV_TOKEN" -X POST http://localhost:8000/api/channel?username=CHANNEL_USERNAME
```

Delete the channel and all its posts.
```
curl -H "X-TOKEN: YOUR_CUSTOM_ENV_TOKEN" -X DELETE http://localhost:8000/api/channel?username=CHANNEL_USERNAME
```