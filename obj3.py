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
                    message += "<a href ='/Edit'>Edit</a>"
                    message += "</br>"
                    message += "<a href = #>Delete</a>"
                    message += "</br>"
                message += "</body></html>"
                self.wfile.write(message)

            if self.path.endswith("/Edit"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                message = "<html><body>"
                message += "<form method = 'POST' action ='/Edit' enctype = 'multipart/form-data'>"
                message += "<input type = 'text' placeholder = 'new Name' name = 'newRestaurantName'>"
                message += "<input type = 'submit' value = 'change'>"
                message += "</form>"
                message += "</html></body>"

                self.wfile.write(message)



            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                messgae = ""
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
