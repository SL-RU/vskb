import cherrypy
import os
import simplejson
import json
from mako.template import Template

class DBInterface(object):
    def __init__(self, db):
        self.db = db

    db = None
    
    def index(self):
        return "<a href='./all'>" + self.db.DBName + "</a>"

    @cherrypy.tools.json_out()
    def get_all(self, _=0):
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        dt = self.db.all_preview()
        s = {'data': dt}
        #print (s)
        return s

    @cherrypy.tools.json_in()
    def add_item(self):
        i = cherrypy.request.json
        print(i)
        #self.db.add(n, y, g, d, r, c, t)
        return ""

    @cherrypy.tools.json_out()
    def get_db_info(self):
        db = self.db
        sc = list()
        for i in self.db.previewColumns:
            sc.append(db.columnNames[i])
        return {"showColumns" : sc,
                "name": db.DBName,
                "id" : db.DBID,
                "columns" : db.columns,
                "columnNames":db.columnNames}

    def all(self):
        db = self.db
        sc = list()
        for i in self.db.previewColumns:
            sc.append(db.columnNames[i])
        return Template(filename="/home/sl_ru/b/vskb/html/db.html").render(clmns=sc)

    def edit(self):
        return Template(filename="/home/sl_ru/b/vskb/html/edit_item.html").render(clms= self.db.columns, cln=self.db.columnNames, clt=self.db.columnType)

    @cherrypy.tools.json_in()
    def add_item(self):
        i = cherrypy.request.json
        z = list()
        for j in i:
            z.append(j['value'])
        print(z)
        self.db.add(z)

        
        
    all.exposed = True
    edit.exposed = True
    add_item.exposed = True
    get_db_info.exposed = True
    add_item.exposed = True
    index.exposed = True
    get_all.exposed = True


        
class MainPage(object):
    def __init__(self, core):
        self.core=core
        

    core = None
    
    def index(self):
        s = ""
        for i in self.core.dbs:
            s += "<a href='" + i.DBID  + "'>" + i.DBName + "</a><br>"
        return s

    @cherrypy.tools.json_in()
    def add_new_db(self):
        i = cherrypy.request.json
        self.core.create_db(i)
        return ""


    index.exposed = True
    add_new_db.exposed = True    


def start(core):
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    conf = os.path.join(os.path.dirname(__file__), 'web.conf')
    root = MainPage(core)
    cherrypy.tree.mount(root, config=conf)
    print("CP added core")
    cherrypy.server.socket_host = "0.0.0.0"
    cherrypy.engine.start()

def addPage(page, addr):
    conf = os.path.join(os.path.dirname(__file__), 'page.conf')
    cherrypy.tree.mount(page, addr, config=conf)