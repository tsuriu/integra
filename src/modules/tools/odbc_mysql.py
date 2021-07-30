import pymysql


class mysqldb(object):
    def __init__(self, host, user, pswd, schema):
        self.host = host
        self.user = user
        self.pswd = pswd
        self.schema = schema

        self.db = pymysql.connect(host=self.host,
                                  port=3306,
                                  user=self.user,
                                  passwd=self.pswd,
                                  db=self.schema,
                                  cursorclass=pymysql.cursors.DictCursor)

        self.cur = self.db.cursor()

    def fetchOne(self, query):
        self.cur.execute(query)
        return self.cur.fetchone()

    def fetchAll(self, query):
        result = {}
        temp = []

        self.cur.execute(query)
        data = self.cur.fetchall()

        for dt in data:
            temp.append(dt)

        result['count'] = len(data)
        result['data'] = temp

        return result

    def insertCsv(self, data, table):

        return 0
