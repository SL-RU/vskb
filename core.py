import db
import web
import os
import json
from threading import Thread

class Core(object):
    def __init__(self):
        #t = Thread(target=self.startWeb)
        #t.setDaemon(True)
        #t.start()
        self.loadConfig()
        self.startWeb()

    configPath = "vskb.json"
    dbs = list()
    mainPage = None
    dbPages = list()
    defaultDBpath = "~/vskb"

    def startWeb(self):
        web.start(self)
        
    def loadConfig(self):
        if os.path.exists(self.configPath):
            with open(self.configPath, "r") as fl:
                dt = json.load(fl)
                self.defaultDBpath = dt["defaultpath"]
                for i in dt["dbs"]:
                    v = db.DB(i)
                    self._add_db(v)
                fl.close()
        else:
            self.saveConfig()

    def saveConfig(self):
        with open(self.configPath, "w") as fl:
            dt = {}
            dt["defaultpath"] = self.defaultDBpath
            dt["dbs"] = list()
            for i in self.dbs:
                i.save()
                dt["dbs"].append(i.ConfigPath)
            json.dump(dt, fl)
            fl.close()
        print("Config saved")

    def _add_db(self, d):
        self.dbs.append(d)
        web.addPage(web.DBInterface(d), "/" + d.DBID)

    def create_db(self, data):
        cls = list()
        cln = dict()
        clt = dict()
        clp = list()
        clarg = dict()
        for i in data["columns"]:
            cls.append(i[0])
            cln[i[0]] = i[1]
            clt[i[0]] = i[2]
            clarg[i[0]] = i[3]
            if i[4] == 1:
                clp.append(i[0])
        path =  os.path.join(self.defaultDBpath, data["id"] + ".conf")
        dt = {
            "dbid" : data["id"],
            "name" : data["name"],
            "columns": cls,
            "columnNames": cln,
            "columnType" : clt,
            "previewColumns": clp,
            "columnTypeArg" : clarg
        }
        with open(path, "w") as fl:
            json.dump(dt, fl)
            fl.close()

        self._add_db(db.DB(path))
        self.saveConfig()
        

    
core = Core()
