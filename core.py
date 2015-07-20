import db
import web


d = db.DB("/home/sl_ru/tmp/tstDB.db")
print(d.count())
print(d.all())
print ( "")
print(d.get_by_id(3))

web.start(d)