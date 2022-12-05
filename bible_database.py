import os, psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL', None)

class BibleDB:
    def __init__(self) -> None:
        self.con = None
    
    def connect(self, dbname="./data/longKou-market-linebot.db"):
        try:
            # self.con = sqlite3.connect(dbname, check_same_thread=False)
            self.con = psycopg2.connect(DATABASE_URL)
            return True
        except:
            return False
    
    def close(self):
        self.con.close()
    
    def create_userlog_table(self):
        cur = self.con.cursor()
        # listOfTables = cur.execute(
        # f"""SELECT name FROM sqlite_master WHERE type='table'
        # AND name='UserLog'; """).fetchall()
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS UserLog(UserID VARCHAR(255), CurStoryID int, Finished int, LoginCount int, RetryCount int);""")
        self.con.commit()
        print('UserLog table created')
        
        # if len(listOfTables) == 0:
        #     print(f'UserLog table not found!')
        #     cur.execute(
        #     f"""CREATE TABLE IF NOT EXISTS UserLog(UserID VARCHAR(255), CurStoryID int, Finished int, LoginCount int, RetryCount int);""")
        #     self.con.commit()
        #     print('UserLog table created')
        # else:
        #     print('UserLog Table found!')
    
    def drop_table(self):
        cur = self.con.cursor()
        cur.execute("DROP TABLE UserLog")
        self.con.commit()
        print('Dropped UserLog Table!')
    
    def execute(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data

    def get_storyid_by_userid(self, useid):
        """Get user current story id

        :param str user_id: User ID
        :return int: current story id, return 0 if not found this user id
        """
        cur = self.con.cursor()
        users = cur.execute(
        f"""SELECT CurStoryID, Finished FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            return users[0][0]
        else:
            print(f'UserID {useid} not found')
            return 0

    def get_finished_by_userid(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT Finished FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            return users[0][0] == 1
        else:
            print(f'UserID {useid} not found')
            return False

    def add_new_user(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) == 0:
            sql = ''' INSERT INTO UserLog(UserID,CurStoryID,Finished,LoginCount,RetryCount)
              VALUES(%s,%s,%s,%s,%s) '''
            cur.execute(sql, (useid, 0, 0, 1,0))
            self.con.commit()
            return 1
        else:
            print(f'UserID {useid} existed! Not allow to add new one')
            login_count = self.update_login_count(useid)
            return login_count

    def delete_user(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""DELETE FROM UserLog WHERE UserID='{useid}'; """)
        self.con.commit()

    def check_user_exist(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        return len(users) > 0

    def update_login_count(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT LoginCount FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            login_count = users[0][0]
            sql = ''' UPDATE UserLog
              SET LoginCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (login_count+1,useid))
            self.con.commit()
            return login_count+1

    def update_story_id(self, useid, storyid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = ''' UPDATE UserLog
              SET CurStoryID = %s
              WHERE UserID = %s'''
            cur.execute(sql, (storyid,useid))
            self.con.commit()

    def update_finished(self, useid, finished:int):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = ''' UPDATE UserLog
              SET Finished = %s
              WHERE UserID = %s'''
            cur.execute(sql, (finished,useid))
            self.con.commit()

    def get_retry_count_by_userid(self, useid):
        """Get retry counts for this user_id

        :param str user_id: User ID
        :return int: current retry_count, return 0 if not found this user id
        """
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT RetryCount, Finished FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            return users[0][0]
        else:
            print(f'UserID {useid} not found')
            return 0

    def clear_retry_count(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            sql = ''' UPDATE UserLog
              SET RetryCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (0,useid))
            self.con.commit()

    def increase_1_retry_count(self, useid):
        cur = self.con.cursor()
        cur.execute(
        f"""SELECT * FROM UserLog WHERE UserID='{useid}'; """)
        users = cur.fetchall()
        if len(users) > 0:
            cur_retry = self.get_retry_count_by_userid(useid)
            sql = ''' UPDATE UserLog
              SET RetryCount = %s
              WHERE UserID = %s'''
            cur.execute(sql, (cur_retry+1,useid))
            self.con.commit()

def test_db():
    mydb = BibleDB()
    mydb.connect()
    mydb.create_userlog_table()
    mydb.add_new_user('ony_for_test')
    mydb.get_storyid_by_userid('ony_for_test')
    mydb.close()

db = BibleDB()
db.connect()
try:
    # db.drop_table()
    pass
except:
    pass
db.create_userlog_table()

if __name__=='__main__':
    test_db()

