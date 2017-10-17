from flask import Flask
from db_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi


engine = create_engine('sqlite:///restaurentmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

app = Flask(__name__)

@app.route("/")
def index():
    rest = session.query(Restaurant).all()
    message = ""
    for r in rest:
        message += r.name
        message += "</br>"
        message += str(r.id)
        message += "</br>"

    return message


@app.route("/menuitem")
def menuitem():
    menu = session.query(MenuItem).all()
    message = ""
    for m in menu:
        message += m.name
        message += "</br>"
        message += str(m.id)
        message += "</br>"
        message += str(m.price)
        message += "</br>"
        message += m.course
        message += "</br>"
        message += m.description
        message += "</br>"
        message += "</br></br>"

    return message


@app.route("/for_each")
def for_each():
    rest = session.query(Restaurant).all()
    message = ""
    for r in rest:
        menu = session.query(MenuItem).filter_by(restaurant_id = r.id).all()
        for m in menu:
            message += "<h1>%s</h1>" % r.name
            message += m.name
            message += "</br>"
            message += str(m.id)
            message += "</br>"
            message += str(m.price)
            message += "</br>"
            message += m.course
            message += "</br>"
            message += m.description
            message += "</br>"
            message += "</br></br>"

    return message


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port = 8000)
