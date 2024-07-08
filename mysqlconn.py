import pymysql


class DbAction:
    def __init__(self, host='localhost', user='root', password='',
                 database=None, port=3306, charset='utf8mb4'):
        """
        初始化数据库连接参数
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        连接到数据库
        """
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset
            )
            self.cursor = self.connection.cursor()
            # print('mysql连接成功')
            return True
        except pymysql.Error as e:
            # print('未连接上数据库！' + str(e))
            return False

    def execute_query(self, query, params=None):
        """
        执行SQL查询
        :param query: SQL查询语句
        :param params: 查询参数元组，默认为None
        :return: 查询结果，如果有结果的话
        """
        if not self.connection:
           self.connect()
        try:
            # with self.connection:
            #     with self.cursor as cursor:
            self.cursor.execute(query, params)
            self.connection.commit()
            # print(f'执行{query}')
        except pymysql.Error as e:
            # print(f"执行查询时发生错误: {e}")
            self.connection.rollback()

    def select_query(self, query, params=None):
        """
        执行SQL查询
        :param query: SQL查询语句
        :param params: 查询参数元组，默认为None
        :return: 查询结果，如果有结果的话
        """
        if not self.connection:
            conn = self.connect()
        try:
            # with self.connection:
            #     with self.cursor as cursor:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except pymysql.Error as e:
            # print(f"执行查询时发生错误: {e}")
            self.connection.rollback()

    def close(self):
        """
        关闭数据库连接
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        # print("数据库连接已关闭。")
