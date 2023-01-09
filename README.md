# mirror
aggregator of news and posts from multiple platforms, currently only support telegram, website: https://mirror.fidesy.xyz

## Features
* [x] Listen to new posts from telegram and save them
* [x] Web interface
* [x] Search by keywords 
* [ ] ...


## Installation
todo
1. clone the repository
```
git clone https://github.com/fidesy/mirror.git
```

2. download and run PostgreSQL image
```
docker pull postgres
docker run --name mirrordb -e POSTGRES_PASSWORD=postgres -dp 5432:5432 postgres
```

3. activate python environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. find api_id and api_hash from your telegram channel and paste in .env file. [(guide)](https://core.telegram.org/api/obtaining_api_id)

5. Fill in channels.txt (mirror/data/channels.txt) file with your list of telegram channel usernames (each username on a new line) 

6. Run the parser script to initialize database and fill in information about channels and latest posts
```
python mirror/parser.py
```

7. Run the script to join channels to be able to listen to new posts.
```
python mirror/script/join_channels.py
```

8. Run the app to listen to new posts
```
python mirror/listen_posts.py
```

9. run fastapi application
```
python -m uvicorn mirror.main:app --reload
```

10. install interface dependecies and run it
```
cd interface
npm i
npm start
```