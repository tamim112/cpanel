import datetime
import urllib
db = DAL('mysql://access_management:TJ544#20&^bdsjy@34.143.171.140/access_management', decode_credentials=True)
date_fixed=datetime.datetime.now()+datetime.timedelta(hours=6)

session.connect(request, response, db, migrate=False)

# this is for change trucking file without restart the server
from gluon.custom_import import track_changes
track_changes(True)
