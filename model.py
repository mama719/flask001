from config import db 
from datetime import datetime 
from uuid import uuid4
import os , re  
from sqlalchemy.orm import validates 

class User(db.Model) :
    id = db.Column(db.String(36) , primary_key=True , default=lambda: str(uuid4()) , unique=True , nullable=False)
    firstname = db.Column(db.String(40) , nullable=False , unique=False) 
    lastname = db.Column(db.String(40) , nullable=False , unique=False) 
    email = db.Column(db.String(80) , nullable=False , unique=True) 
    password = db.Column(db.String(40) , nullable=False , unique=False )
    createdat = db.Column(db.DateTime , default=datetime.utcnow , nullable=False , unique=False) 
    updatedat = db.Column(db.DateTime , default=datetime.utcnow , onupdate=datetime.utcnow , nullable=False , unique=False)


    @validates(firstname)
    def fn(self , key, vv) :
        if not vv.isalpha() :
            raise ValueError("First name Must Contain Alphabats Only")
        return vv
    
    @validates(lastname) 
    def ln(self , key , vv) :
        if not vv.isalpha() :
            raise ValueError("Last Name Must Contain Alphabets Only") 
        return vv 
    
    @validates(email) 
    def e(self , key , vv) :
        reg = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"
        if re.match(reg , vv) :
            return vv 
        raise ValueError("Invalid Email Address") 
    
    def __repr__(self) :
        return f"<User {self.email}>"

    def to_json(self) :
        return {
            "id" : self.id ,
            "firstName" : self.firstname ,
            "lastName" : self.lastname ,
            "email" : self.email , 
            "password" : self.password ,
        }