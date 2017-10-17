from db_setup import Base, Restaurant, MenuItem
import cgi

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///restaurentmenu.db")
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()


class server_Handler_class(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                rest = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                messgae = ""
                message = "<html><body>"
                message += "<a href = '/restaurants/new'>Make new</a></br>"
                for rst in rest:
                    message += rst.name
                    message += "</br>"
                    message += "<a href ='restaurants/%s/edit'>Edit</a>" % rst.id
                    message += "</br>"
                    message += "<a href = 'restaurants/%s/delete'>Delete</a>" %rst.id
                    message += "</br>"
                message += "</body></html>"
                self.wfile.write(message)


            if self.path.endswith("/edit"):
                restIDPath = self.path.split("/")[2]
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                myrstqr = session.query(Restaurant).filter_by(id = restIDPath).one()
                if myrstqr !=[]:
                    message = ""
                    message += "<html><body>"
                    message += "<form method ='POST' enctype = 'multipart/form-data' action='/restaurant/%s/edit'>" % restIDPath
                    message += "<input type ='text' placeholder='new name' name = 'newName'>"
                    message += "<input type= 'submit' value = 'update'>"
                    message += "</form>"
                    message += "</body></html>"

                self.wfile.write(message)


            if self.path.endswith("/delete"):
                restIDPath = self.path.split("/")[2]
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                myrstqr = session.query(Restaurant).filter_by(id = restIDPath).one()
                if myrstqr !=[]:
                    message = ""
                    message += "<html><body>"
                    message += "<form method = 'POST' enctype = 'multipart/form-data' action='/restaurant/%s/delete'>" % restIDPath
                    message += "<h1>Are you sure, you want to delete this!!!</h1>"
                    message += "<input type= 'submit' value = 'delete'>"
                    message += "</form>"
                    message += "</body></html>"

                self.wfile.write(message)


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                message = ""
                message = "<html><body>"
                message += "<h1>Make new Restaurants here</h1>"
                message += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurants/new'>"
                message += "<input type = 'text' name = 'newRestaurantName' placeholder = 'new Restaurants Name'>"
                message += "<input type = 'submit' value = 'create'>"
                message += "</form>"
                message += "</body></html>"

                self.wfile.write(message)


        except IOError:
            self.send_response(404)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                #getting the new name from form
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    #getting data from the pdict ie a dictionary
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    #getting new name from the fields using .get
                    name_update = fields.get('newName')

                    rest_id = self.path.split("/")[2]
                    #whole database with given condition is assigned to the rest_query
                    rest_query = session.query(Restaurant).filter_by(id = rest_id).one()

                    if rest_query!= []:
                        rest_query.name = name_update[0]
                        session.add(rest_query)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type','text/html')
                        self.send_header('Location','/restaurants')
                        self.end_headers()


            if self.path.endswith("/delete"):
                rest_id = self.path.split("/")[2]
                rest_query = session.query(Restaurant).filter_by(id = rest_id).one()

                if rest_query != []:
                    session.delete(rest_query)
                    session.commit()


                self.send_response(301)
                self.send_header('Content-type','text/html')
                self.send_header('Location','/restaurants')
                self.end_headers()




            if self.path.endswith("/restaurants/new"):
                ctype,pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile,pdict)
                    messg = fields.get('newRestaurantName')


                    newRest = Restaurant(name=messg[0])
                    session.add(newRest)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('',port),server_Handler_class)
        print 'server is running on port %s' % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "keybord interuption occured"
        server.socket.close()

if __name__ == '__main__':
    main()
