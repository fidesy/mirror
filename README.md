# mirror
aggregator of news and posts from multiple platforms, currently only support telegram, website: https://mirror.fidesy.xyz

## Features
* [x] Listen to new posts from telegram and save them
* [x] Web interface
* [x] Search by keywords 
* [ ] ...



## Installation
1. clone the repository
```
git clone https://github.com/fidesy/mirror.git
```

2. Create .env file with all variables from .env.example. Find api_id and api_hash from your telegram account [(guide)](https://core.telegram.org/api/obtaining_api_id)

3. set env variable for the correct installation, build and run docker app containers
```
export DOCKER_DEFAULT_PLATFORM=linux/amd64
docker compose up -d
```
now website is available at localhost:3000

4. activate python environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

5. Fill in channels.txt (mirror/data/channels.txt) file with your list of telegram channel usernames (each username on a new line) 

6. Run the parser script to initialize database and fill in information about channels and latest posts
```
python mirror/parser.py
```

7. Since you parsed the data about channels, you need to build the web-mirror container again to transfer the profile photos.
```
docker rm -f web-mirror
docker rmi mirror_web
docker compose up -d
``` 

8. Run the script to join channels to be able to listen to new posts.
```
python mirror/script/join_channels.py
```

9. Run the app to listen to new posts
```
python mirror/listen_posts.py
```