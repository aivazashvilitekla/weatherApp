import sqlite3


class DBConnect():
    def connect():
        try:
            sqliteConnection = sqlite3.connect('../../../weatherDB.db')
            return sqliteConnection

        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")