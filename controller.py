from flask import jsonify , request 
from config import db
from model import User
import jwt 
import datetime

import re , os 

def sign_up():

    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")
    profile = request.form.get("profile")

    reg = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"

    if not firstname or not lastname or not email or not password :
        return jsonify({"message" : "All Field Must Be Filled" , "success" : False})
    
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])[A-Za-z]+$" , firstname):
        print (os.getenv("name"))
        return jsonify({"message" : 'Your First Name Must Contain Upper And Lower Case Characters' , "success" : False})

    if not re.match(os.getenv("name") , lastname) :
        return jsonify({"message" : "Your Last Name Must Contain Lower And Upper Case Characters" , "success" : False})
    
    if not re.match(reg, email) :
        return jsonify({"message" : "Your Email Address Is Invalid" , "success" : False})
    
    if not len(password) > 3 :
        return jsonify({"message" : "Your Password Must Contain Atleast 3 Characters" , "success" : False})
    
    user = User.query.filter_by(email=email).first()

    if user :
        return jsonify({"message" : "A User Of The Same Detaills Exist Already" , "success" : False})
    
    us = User(firstname = firstname, lastname = lastname , email = email , password = password) 

    try:
        db.session.add(us) 
        db.session.commit()
        return jsonify({"message" : f"User: {firstname} Saved With Success", "success" : True})
    except:
        db.session.rollback()
        return jsonify({"message" : "Database Went Wrong" , "success" : False })

def test() :
    a = User.query.all()
    b = list(map(lambda x : x.to_json() , a))
    return jsonify({"data" : b})

def login():
    email = request.form.get("email")
    password = request.form.get('password')

    reg = r"^[a-zA-Z0-9._+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$"

    if not password or not email :
        return jsonify({'message' : "Please Fill In All Gaps" , "success" : False})

    if not re.match(reg , email) :
        return jsonify({"message" : "Invalid Email Addresss" , "success" : False})
    
    if not len(password) > 3 :
        return jsonify({"message" : "password Must be Atleast 3 Characters" , "success" : False})
    
    user = User.query.filter_by(email=email).first()

    if not user.password == password :
        return jsonify({"message" : "Please That Is A Wrong Password Try Again" , "success" : False})
    
    if not user :
        return jsonify({"message" : "No Such user Exist" , "success" : False})
    
    token = jwt.encode({"userid" : user.id , "exp" : datetime.datetime.utcnow() + datetime.timedelta(days=7) }, os.getenv("jwt") , algorithm='HS256' )

    return jsonify({"message" : f"Login Successful, Name: {user.firstname}", "token" : token , "success" : True})

def profile(cu) :
    cc = cu.to_json()
    return jsonify({"messsage" : f"User: {cu} , GEt Successfull" ,"data" : cc , "success" : False})