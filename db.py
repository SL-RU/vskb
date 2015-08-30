import sqlite3 as lite
import json
import os

def GetSQLTypeFromColumnType(type):
    if type in ["text", "str", "tags", "select"]:
        return "TEXT"
    elif type in ["rate", "int", "check"]:
        return "INTEGER"
    elif type in ["image"]:
        return "BLOB"
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
    #Тип столбца.
    columnType = dict()
    #Аргументы к типу колонки(например список опций у комбобокса и тд)
    columnTypeArg = dict()
    #Кэш столбцов. Используется некоторыми типами столбцов, например тэгами для словаря тэгов. Сохраняется и загружается.
    columnsCache = dict()
    #Колонки, которые будут отображатся на странице базы данных
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

    def update(self, id, data):
        vls = ""
        print(data)
        for n,v in data:
            if n in self.columns:
                vls += n + "="
                tp = GetSQLTypeFromColumnType(self.columnType[n])
                if tp is "TEXT":
                    vls += "'" + str(v) + "',"
                else:
                    vls += str(v) + ","
                self.process_val(v, n)
        print("UPDATE " + self.DBID + " SET " + vls[:-1] + " WHERE ID=" + id)
        self.db.execute("UPDATE " + self.DBID + " SET " + vls[:-1] + " WHERE ID=" + id)
        self.db.commit()

        
    def add(self, args):
        if(len(args) != len(self.columns)):
            print("Wrong data! Arg count wrong! Data:", args)
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
            #Process vals for smth...
            self.process_val(args[i], cl)
        comm = "INSERT INTO " + self.DBID + "(" + cols[:-2] + ") VALUES (" + vals[:-2] + ");"
        print(comm)
        self.db.execute(comm)
        self.db.commit()    


    def process_val(self, val, name):
        tp = self.columnType[name]    
        if tp == "tags":
            tgs = val.split(",")
            for i in tgs:
                i = i.rstrip().lstrip()
                if name in self.columnsCache:
                    if i not in self.columnsCache[name]:
                        self.columnsCache[name].append(i)
                        print("Tag " + i + " added in column " + name + "'s cache'")
                else:
                    self.columnsCache[name] = [i,]
                    print("Tag " + i + " added in column " + name + "'s cache'")
        
        
        
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
            self.columnTypeArg = dt["columnTypeArg"]
            self.previewColumns = dt["previewColumns"]
            if "cache" in dt:
                self.columnsCache = dt["cache"]
            fl.close()
        pass
            
    def save(self):
        dt = {}
        with open(self.ConfigPath, "r") as fl:
            dt  = json.load(fl)
            fl.close()         
        dt["cache"] = self.columnsCache
        with open(self.ConfigPath, "w") as fl:
            json.dump(dt, fl)
            fl.close()
        
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

 #####   #######  #        #     #  #     #  #     #    
#     #  #     #  #        #     #  ##   ##  ##    #    
#        #     #  #        #     #  # # # #  # #   #    
#        #     #  #        #     #  #  #  #  #  #  #    
#        #     #  #        #     #  #     #  #   # #    
#     #  #     #  #        #     #  #     #  #    ##    
 #####   #######  #######   #####   #     #  #     #    

#######  #     #  ######   #######  
   #      #   #   #     #  #        
   #       # #    #     #  #        
   #        #     ######   #####    
   #        #     #        #        
   #        #     #        #        
   #        #     #        #######  
        
#######  #     #  #     #   #####   #######  ###  #######  #     #   #####   
#        #     #  ##    #  #     #     #      #   #     #  ##    #  #     #  
#        #     #  # #   #  #           #      #   #     #  # #   #  #        
#####    #     #  #  #  #  #           #      #   #     #  #  #  #   #####   
#        #     #  #   # #  #           #      #   #     #  #   # #        #  
#        #     #  #    ##  #     #     #      #   #     #  #    ##  #     #  
#         #####   #     #   #####      #     ###  #######  #     #   #####   

    def get_all_tags(self, name):
        if name in self.columnsCache:
            return self.columnsCache[name]
        else:
            return []

    