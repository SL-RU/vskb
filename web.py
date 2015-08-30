import cherrypy
import os
import json
from mako.template import Template

class DBInterface(object):
    def __init__(self, db):
        self.db = db

    db = None
    
    def index(self):
        return "<a href='./all'>View db</a><br/>"

    @cherrypy.tools.json_out()
    def get_all(self, _=0):
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        dt = self.db.all_preview()
        s = {'data': dt}
        #print (s)
        return s

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

    @cherrypy.tools.json_out()
    def get_item_data(self, id):
        return {"d" : self.db.get_by_id(id)}

    def all(self):
        db = self.db
        sc = list()
        for i in self.db.previewColumns:
            sc.append(db.columnNames[i])
        return Template(filename=os.path.join(os.getcwd(), "html/db.html")).render(clmns=sc)

    def edit(self, id):
        return Template(filename=os.path.join(os.getcwd(), "html/edit_item.html")).render(clms= self.db.columns, cln=self.db.columnNames, clt=self.db.columnType, ctarg=self.db.columnTypeArg, new_item=0, id=id)

    def add(self):
        return Template(filename=os.path.join(os.getcwd(), "html/edit_item.html")).render(clms= self.db.columns, cln=self.db.columnNames, clt=self.db.columnType, ctarg=self.db.columnTypeArg, new_item=1)

    def view(self, id):
        return Template(filename=os.path.join(os.getcwd(), "html/view_item.html")).render(clms= self.db.columns, cln=self.db.columnNames, clt=self.db.columnType, ctarg=self.db.columnTypeArg, id=id)

    @cherrypy.tools.json_in()
    def add_item(self):
        """IN: list like that: [{value: 45, name: id}, {value: dsfdsfads, name: text}], where columns goes in oder"""
        i = cherrypy.request.json
        print(i)
        z = list()
        for j in i:
            if j["name"] != 'id' and j["name"] in self.db.columns:
                z.insert(self.db.columns.index(j["name"]), j['value'])
        print(z)
        self.db.add(z)
        #save cache        
        self.db.save()
        return "1"

    @cherrypy.tools.json_in()
    def edit_item(self):
        i = cherrypy.request.json
        id = ""
        z = list()
        for j in i:
            print(j)
            if j["name"] == 'id':
                id = j["value"]
                print("ID " + id)
            else:
                z.append((j["name"], j['value']))
        self.db.update(id, z)
        #save cache        
        self.db.save()
        return "1"

        
    @cherrypy.tools.json_out()
    def get_tags(self, column):
        return self.db.get_all_tags(column)

    @cherrypy.tools.json_out()
    def get_options(self, column):
        return self.db.get_all_tags(column)

    
    all.exposed = True
    edit.exposed = True
    add.exposed = True
    view.exposed = True
    add_item.exposed = True
    get_db_info.exposed = True
    get_tags.exposed = True
    get_options.exposed = True
    add_item.exposed = True
    edit_item.exposed = True
    index.exposed = True
    get_all.exposed = True
    get_item_data.exposed = True


        
class MainPage(object):
    def __init__(self, core):
        self.core=core
        

    core = None
    
    def index(self):
        #s = "<a href='add'>Add new</a><br/><br/><br/>"
        #for i in self.core.dbs:
        #    s += "<a href='" + i.DBID  + "'>" + i.DBName + "</a><br/>"
        return Template(filename=os.path.join(os.getcwd(), "html/index.html"), input_encoding='utf-8').render()

    @cherrypy.tools.json_in()
    def add_new_db(self):
        i = cherrypy.request.json
        self.core.create_db(i)
        return ""

    @cherrypy.tools.json_out()
    def get_all_dbs(self):
        d = []
        for i in self.core.dbs:
            d.append({"id": i.DBID,
                      "name": i.DBName,
                      "cids": i.columns,
                      "cnames": i.columnNames,
                      "count": i.count()
                  })
        return d

    get_all_dbs.exposed = True
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