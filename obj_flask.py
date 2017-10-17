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
    message = ""
    message +="<h1>hello world</h1>"
    message +="<input type = 'submit' value = 'list' action = '/list' >"
    return message

@app.route("/list")
def list():
    rest = session.query(Restaurant).all()
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

    return message

@app.route("/listmenu")
def listmenu():
    rest = session.query(MenuItem).all()
    messgae = ""
    message = "<html><body>"
    message += "<a href = '/restaurants/new'>Make new</a></br>"
    for rst in rest:
        message += rst.id
        message += "</br>"
        message += "<a href ='/Edit'>Edit</a>"
        message += "</br>"
        message += "<a href = #>Delete</a>"
        message += "</br>"
    message += "</body></html>"

    return message



@app.route("/details")
def details():
    rest = session.query(Restaurant).one()
    message = ""
    message += "<html><body>"
    message += rest.id
    message +="</br>"

    return message



@app.route("/deta")
def deta():
    rest = session.query(Restaurant).first()
    men = session.query(MenuItem).filter_by(id = rest.id)
    message = ""
    for mn in men:
        message += men.name
        message += "</br>"

    return message

@app.route("/check")
def check():

    restaurants = session.query(Restaurant).first()
    return restaurants.id

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0',port = 8000)
