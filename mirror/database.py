import psycopg2


POSTS_SCHEME = """
CREATE TABLE IF NOT EXISTS posts(
    id          SERIAL PRIMARY KEY,
    post_id     INT,
    channel_id  INT,
    date        TIMESTAMP,
    message     TEXT,
    media_url   TEXT
)
"""

CHANNELS_SCHEME = """
CREATE TABLE IF NOT EXISTS channels(
    id            INT PRIMARY KEY,
    username      TEXT UNIQUE,
    title         TEXT,
    description   TEXT
)
"""

class Database:

    def __init__(self, DBURL: str):
        self.connection = psycopg2.connect(DBURL)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

        self.cursor.execute(POSTS_SCHEME)
        self.cursor.execute(CHANNELS_SCHEME)
    

    def __del__(self):
        self.cursor.close()
        self.connection.close()


    def create_post(self, post_info):
        try:
            self.cursor.execute("INSERT INTO posts(post_id, channel_id, date, message, media_url) VALUES(%s, %s, %s, %s, %s)", post_info)

        except Exception as e:
            print(e)


    def create_channel(self, channel_info):
        try:
            self.cursor.execute("INSERT INTO channels VALUES(%s, %s, %s, %s)", channel_info)

        except Exception as e:
            print(e)

        
    def get_posts(self, skip: int = 0, limit: int = 100, like: str = ""):
        posts = []
        try:
            self.cursor.execute(f"""
                SELECT posts.id, channel_id, date, username, title, message, media_url FROM posts 
                JOIN channels ON posts.channel_id=channels.id
                WHERE message LIKE '%{like}%'
                ORDER BY date DESC
                LIMIT {limit} OFFSET {skip}""")

            for row in self.cursor.fetchall():
                posts.append({
                    "id": row[0], "channel_id": row[1], "date": row[2], "username": row[3], 
                    "title": row[4], "message": row[5], "media_url": row[6]})

            return posts
            
        except Exception as e:
            print(e)
