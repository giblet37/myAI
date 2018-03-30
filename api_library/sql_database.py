

import settings
import sqlite3
from classes.api import Api
from sqlite3 import Error


INTEGER = 'INTEGER'

class SQLDatabaseApi(Api):

    def __init__(self):
        self.conn = sqlite3.connect(settings.DATABASE_FILE, check_same_thread = False)
        super(SQLDatabaseApi, self).__init__('sql')

    def create_table(self, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
            self.conn.commit()
        except Error as e:
            print(e)

    def run_sql(self, sqlstring):
        try:
            c = self.conn.cursor()
            c.execute(sqlstring)
            self.conn.commit()
        except Error as e:
            print(e)

    def get_all_records(self, table_name):
        rows = []
        try:
            c = self.conn.cursor()
            c.execute("SELECT * FROM {tn}". \
                      format(tn=table_name))
            rows = c.fetchall()
        except Error as e:
            print(e)
        finally:
            return rows

    def sql_select(self,sql_str):
        rows = []
        try:
            c = self.conn.cursor()
            c.execute(sql_str)
            rows = c.fetchall()
        except Error as e:
            print(e)
        finally:
            return rows

    def insert_item(self, table, items):
        try:
            cols = ', '.join('"{}"'.format(col) for col in items.keys())
            vals = ', '.join(':{}'.format(col) for col in items.keys())
            sql = 'INSERT INTO "{0}" ({1}) VALUES ({2})'.format(table, cols, vals)
            self.conn.cursor().execute(sql, items)
            self.conn.commit()
        except Error as e:
            print(e)

    def delete_item(self, table_name, column_name, id):
        """
        Delete a task by task id
        :param conn:  Connection to the SQLite database
        :param id: id of the task
        :return:
        """
        try:
            sql = 'DELETE FROM "{0}" WHERE {1}=?'.format(table_name, column_name, id)
            cur = self.conn.cursor()
            cur.execute(sql, (id,))
            self.conn.commit()
        except Error as e:
            print(e)