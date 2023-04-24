import psycopg2

';delete from posts;'
class Database:

    def __init__(self, DBURL: str):
        self.connection = psycopg2.connect(DBURL)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
    
    def __del__(self):
        self.cursor.close()
        self.connection.close()

    def add_channel(self, channel_info):
        try:
            self.cursor.execute("INSERT INTO channels VALUES(%s, %s, %s, %s)", channel_info)

        except Exception as e:
            print(e)

    def delete_channel(self, channel_username: str):
        try:
            self.cursor.execute("SELECT id FROM channels WHERE username=%s", (channel_username,))
            channel_id = self.cursor.fetchone()

            self.cursor.execute("DELETE FROM channels WHERE username=%s", (channel_username,))
            self.cursor.execute("DELETE FROM posts WHERE channel_id=%s", (channel_id[0],))

        except Exception as e:
            print(e)

    def get_channels(self, skip: int = 0, limit: int = 100):
        try:
            self.cursor.execute("SELECT * FROM channels LIMIT %s OFFSET %s", (limit, skip,))
            channels = self.cursor.fetchall()
            return [{"id": c[0], "username": c[1], "title": c[2], "description": c[3]} for c  in channels]

        except Exception as e:
            print(e)

    def add_post(self, post_info):
        try:
            self.cursor.execute("INSERT INTO posts(post_id, channel_id, date, message, media_url) VALUES(%s, %s, %s, %s, %s)", post_info)

        except Exception as e:
            print(e)

    def add_posts(self, posts):
        for post in posts:
            self.add_post(post)

    def get_posts(self, skip: int = 0, limit: int = 100, like: str = ""):
        posts = []
        try:
            self.cursor.execute("SELECT posts.id, channel_id, date, username, title, message, media_url FROM posts\
                JOIN channels ON posts.channel_id=channels.id \
                WHERE message LIKE %s \
                ORDER BY date DESC \
                LIMIT %s OFFSET %s",
                (f"%{like}%", limit, skip,))
            print(self.cursor.query)

            for row in self.cursor.fetchall():
                posts.append({
                    "id": row[0], "channel_id": row[1], "date": row[2], "username": row[3], 
                    "title": row[4], "message": row[5], "media_url": row[6]})

            return posts
            
        except Exception as e:
            print(e)
