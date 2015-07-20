import cherrypy
import os
import simplejson
import json

class DBInterface(object):
    def __init__(self, db):
        self.db = db

    db = None
    
    def index(self):
        return self.db.DBName

    @cherrypy.tools.json_out()
    def get_all(self, _=0):
        #cherrypy.response.headers['Content-Type'] = 'application/json'
        dt = self.db.all()
        d = list()
        for i in dt:
            d.append(i)
        s = {'data':d}
        print (s)
        return s

    #@cherrypy.tools.json_in()
    def add_item(self, n, y, g, d, r, c, t):
#        i = cherrypy.request.json
        #print(p, n, t)
        self.db.add(n, y, g, d, r, c, t)
        return ""
        
    add_item.exposed = True
    index.exposed = True
    get_all.exposed = True




def start(db):
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    tutconf = os.path.join(os.path.dirname(__file__), 'web.conf')
    root = DBInterface(db)
    cherrypy.quickstart(root, config=tutconf)
    cherrypy.engine.start()
