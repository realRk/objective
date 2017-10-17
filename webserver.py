from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class Haandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path.endswith("/hello"):
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()

            msg = ""
            msg += "<html><head>Hello Rk</head></html>"
            self.wfile.write(msg)
            print msg
            return
        else:
            self.send_error(404,"file not found")




def main():
    try:
        port = 8080
        server = HTTPServer(('',port),Haandler)
        print "server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "server shutting down"
        server.socket.close()

if __name__ == "__main__":
    main()
