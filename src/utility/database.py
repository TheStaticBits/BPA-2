import sqlite3

class DatabaseHandler:
    """ Handles a database file and commands through it """
    def __init__(self, file):
        self.connection = sqlite3.connect(file)
        self.cursor = self.connection.cursor()
    

    def createTable(self, name, content):
        """ Tests if the table already exists, if it does not, creates it """
        tables = self.cursor.execute("SELECT name FROM sqlite_master")
        tables = tables.fetchone() # Returns tuple of all table names in the database

        if name not in tables:
            self.cursor.execute(f"CREATE TABLE {name} ({content})")
    
    
    def contains(self, tableName, columnName, value, valueColumn):
        """ Tests if value is in the column of the table given """
        find = self.cursor.execute(f"SELECT {columnName} FROM {tableName} WHERE {valueColumn}='{value}'")
        return find.fetchone() is None
    

    def modify(self, tableName, keyName, key, valueName, value):
        """ Sets valueName to value in tableName where keyName is key """
        self.cursor.execute(f"UPDATE {tableName} SET {valueName} = ? FROM {keyName} = ?", (value, key))
        self.commit()
    
    
    def insert(self, tableName, key, value):
        """ Inserts key and value into the table """
        self.cursor.execute(f"INSERT INTO {tableName} VALUES (?, ?)", (key, value))
        self.commit()
    

    def findValue(self, tableName, columnName, value, valueColumn):
        """ Finds item inside columnName where valueColumn is value """
        return self.cursor.execute(f"SELECT {columnName} FROM {tableName} WHERE {valueColumn}='{value}'").fetchone()


    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()