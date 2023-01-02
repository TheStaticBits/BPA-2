import sqlite3
import logging

class DatabaseHandler:
    """ Handles a database file and commands through it """
    def __init__(self, file):
        self.log = logging.getLogger(__name__)
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
    

    def createTable(self, name, content):
        """ Tests if the table already exists, if it does not, creates it """
        tables = self.cursor.execute("SELECT name FROM sqlite_master")
        tables = tables.fetchone() # Returns tuple of all table names in the database

        if tables is None:
            self.cursor.execute(f"CREATE TABLE {name} ({content})")
            self.log.info(f"Creating table {name} with content: {content}")
            

    def findValue(self, tableName, columnName, keyColumn, key):
        """ Finds item inside columnName where valueColumn is value """
        self.log.info(f"Finding value in column: {columnName}, where {keyColumn} is {key} in table: {tableName}")
        return self.cursor.execute(f"SELECT {columnName} FROM {tableName} WHERE {keyColumn}='{key}'").fetchone()
    

    def modify(self, tableName, keyName, key, valueName, value):
        """ Sets valueName to value in tableName where keyName is key """
        self.log.info(f"Setting {valueName} to {value} where {keyName} is {key} in table, {tableName}")
        self.cursor.execute(f"UPDATE {tableName} SET {valueName} = ? WHERE {keyName} = ?", (value, key))
        self.commit()
    
    
    def insert(self, tableName, key, value):
        """ Inserts key and value into the table """
        self.log.info(f"Inserting ({key}, {value}) into table, {tableName}")
        self.cursor.execute(f"INSERT INTO {tableName} VALUES (?, ?)", (key, value))
        self.commit()


    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()