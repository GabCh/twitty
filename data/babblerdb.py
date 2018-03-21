import pymysql.cursors


class BabblerDB(object):

    def __init__(self, app):
        self.connection = pymysql.connect(host=app.config['DB_HOST'],
                                          user=app.config['DB_USER'],
                                          password=app.config['DB_PASSWORD'],
                                          db=app.config['DB_NAME'],
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def add_babbler(self, username, publicName, password):
        sql = """
            INSERT INTO Babblers (username, publicName, password)
            VALUES ( %s , %s , %s);"""
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (username, publicName, password))
        except Exception as e:
            print(e)
        print('Inserted ' + username + ' into table babblers!')

    def add_babble(self, id, username, message, time_s, tags):
        sql = """
            INSERT INTO Babbles (id, username, message, time_s)
            VALUES (%s, %s, %s, %s);"""
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (id, username, message, time_s))
        except Exception as e:
            print(e)
        self.add_tags(id, tags)

    def add_tags(self, id, tags):
        for t in tags:
            sql = """
                INSERT INTO Tag (id, tag)
                VALUES (%s, %s);"""
            try:
                with self.connection.cursor() as cursor:
                    self.cursor.execute(sql, (id, t))
            except Exception as e:
                print(e)

    def add_follower(self, follower, followed):
        sql = """
            INSERT INTO Follows (follower, followed)
            VALUES (%s, %s);"""
        try:
            with self.connection.cursor() as cursor:
                self.cursor.execute(sql, (follower, followed))
        except Exception as e:
            print(e)


    def read_table(self, table, keyword, attribute):
        try:
            keyword = '%' + keyword + '%'
            with self.connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT username, message, time_s FROM {} WHERE {} LIKE %s".format(table, attribute)
                print(sql)
                cursor.execute(sql, (keyword,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{:%d %b %Y}".format(result['time_s'])
                return results
        except Exception as e:
            print(e)


    def get_babbles_from_followed_babblers(self, username):
        try:
            username = '%' + username + '%'
            with self.connection.cursor() as cursor:
                sql = """
                    SELECT B.username, B.message, B.time_s
                    FROM Babbles B, Follows F
                    WHERE F.follower = %s AND F.followed = B.username
                    GROUP BY B.time_s DESC;"""
                cursor.execute(sql, (username,))
                results = cursor.fetchall()
                for result in results:
                    result['time_s'] = "{:%d %b %Y}".format(result['time_s'])
                return results
        except Exception as e:
            print(e)


    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        finally:
            self.connection.close()



