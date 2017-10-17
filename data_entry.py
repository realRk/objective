from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base,Restaurant,MenuItem


engine = create_engine('sqlite:///restaurentmenu.db')


Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()


myFirstRestaurant = Restaurant(name = "pizza palace")
session.add(myFirstRestaurant)
session.commit()
session.query(MenuItem).all()

mySecondRestaurant = Restaurant(name = "royal gardens")
session.add(myFirstRestaurant)
session.commit()
session.query(MenuItem).all()
