import sqlite3 as lite
import json
import os

def GetSQLTypeFromColumnType(type):
    if type in ["text", "str", "tags"]:
        return "TEXT"
    elif type in ["rate", "int"]:
        return "INTEGER"
    else:
        return "TEXT"
        
    

class DB(object):
    """Interface for sqlite db"""
    def __init__(self, configpath, dbpath=None):
        if dbpath is None:
            dbpath = configpath[:-4] + "db"
        self.ConfigPath = configpath    
        self.DBPath = dbpath
        self.load_config()
        if not os.path.exists(dbpath):
            self.db = lite.connect(dbpath, check_same_thread=False) 
            self.createDB()
        else:         
            self.db = lite.connect(dbpath, check_same_thread=False)
            print("DB connected")


    db = None
    DBPath = ""
    DBID = ""
    DBName = ""
    ConfigPath = ""
    columns = list()
    columnNames = dict()
    #searchColumns = list()
    columnType = dict()
    previewColumns = list()

    def all(self):
        rt = list()
        for row in self.db.execute('SELECT * FROM ' + self.DBID):
            rt.append(row)
        return rt

    def all_preview(self):
        rt = list()
        cl = "ID, "
        for i in self.previewColumns:
            cl += i + ","
        for row in self.db.execute('SELECT ' + cl[:-1] + ' FROM ' + self.DBID):
            rt.append(row)
        return rt

    def get_by_id(self, id):
        return self.db.execute("SELECT * FROM " + self.DBID + " WHERE ID = " + str(id)).fetchone()

    def search(self, pattern):
        pass

    def add(self, args):
        cols = "ID, "
        vals = str(self.count()) + ", "
        for i in range(len(args)):
            cl = self.columns[i]
            tp = GetSQLTypeFromColumnType(self.columnType[cl])
            cols += cl + ", "
            if tp is "TEXT":
                vals += "'" + str(args[i])  + "', "
            else:
                vals += str(args[i]) + ", "
        comm = "INSERT INTO " + self.DBID + "(" + cols[:-2] + ") VALUES (" + vals[:-2] + ");"
        print(comm)
        self.db.execute(comm)
        self.db.commit()    

    def count(self):
        return self.db.execute("SELECT COUNT(*) FROM " + self.DBID).fetchone()[0]
        
    def load_config(self):
        with open(self.ConfigPath, "r") as fl:
            dt  = json.load(fl)
            self.DBID = dt["dbid"]
            self.columns = dt["columns"]
            self.columnNames = dt["columnNames"]
            #self.searchColumns = dt["searchColumns"]
            self.columnType = dt["columnType"]
            self.DBName = dt["name"]
            self.previewColumns = dt["previewColumns"]
        pass
#    def TestConf(self):
#        self.DBID = "test"
#        self.DBName = "Тестовая"
#        self.columns = ["name", "year", "genres", "descr", "rate", "comment", "tags"]
#        self.columnNames = ["Имя", "Год", "Жанры", "Описание", "Оценка", "Комментарий", "Тэги"]
#        #self.searchColumns = ["name", "year", "genres", "tags", "comment"]
#        self.columnType = ["str", "int", "tags", "text", "rate", "text", "tags"]
#        self.previewColumns = ["name", "year", "genres", "tags"]
    
    def createDB(self):
        types = ""
        for i in self.columns:
            print(i)
            print(self.columns.index(i))
            types += i + " " + GetSQLTypeFromColumnType(self.columnType[i]) + ", "
        print(types[:-2])
        self.db.execute("CREATE TABLE " + self.DBID + "\n" +
                        "(ID INT PRIMARY KEY NOT NULL," +
                        types[:-2] + ");")
        self.db.commit()
        print("DB created")