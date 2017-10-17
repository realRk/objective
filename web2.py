from BaseHTTPServer import BaseHTTPRequestHandler ,HTTPServer
import cgi

class WebHandler(BaseHTTPRequestHandler):



    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>hello</h1>"
                '''enctype describes the encoding type of your form'''
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                '''enctype describes the encoding type of your form'''
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404,"file isn't found")

    def do_POST(self):
        self.send_response(301)
        self.send_header('Content-type','text/html')
        self.end_headers()
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            # fields is where the actual message is transfered to the backend as {'message': ['ljnvlklv']}
            fields = cgi.parse_multipart(self.rfile, pdict)
            print fields
            messagecontent = fields.get('message')

        output = ""
        output += "<html><body>"
        output += "<h1>%s</h1>" % messagecontent[0]
        '''enctype describes the encoding type of your form'''
        output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
        output += "</body></html>"
        self.wfile.write(output)
        print output



def main():
    try:
        port = 8080
        server = HTTPServer(('',port),WebHandler)
        print "server is running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        server.socket.close()



if __name__ == "__main__":
    main()
