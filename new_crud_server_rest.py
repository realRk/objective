#importing crud operations
from db_setup import Base,Restaurant,MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BaseHTTPServer import BaseHTTPRequestHandler ,HTTPServer

engine = create_engine('sqlite:///restaurentmenu.db')
#binds the engine with the base class ie Base
Base.metadata.bind = engine
#creates a class named DBSession which is configured
DBSession = sessionmaker(bind = engine)
#create a session object of class DBSession
#session object is used to hold data in between data transfer
session = DBSession()

class HandlerClass(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content=type','text/html')
        self.end_headers()

        rst = session.query(Restaurant).all()
        msg = ""
        msg +="<html><body>"
        for nm in rst:
            msg += nm.name
            msg += "</br></br>"
            msg += "<a href = '@'>Edit</a>"
            msg += "</br></br>"
            msg += "<a href= '@'>Delete</a>"
            msg +="</br></br>"

        msg +="</body></html>"
        self.wfile.write(msg)
        print msg
        return







if __name__ =="__main__":
    try:
        port = 8080
        server = HTTPServer(('',port),HandlerClass)
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()
