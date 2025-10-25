from config import app , db 
from controller import sign_up , test , login , profile
from flask import request , jsonify 
from functools import wraps
import os ,jwt
from model import User

@app.route("/api/signup" , methods=["POST"])
def signup() :
    return sign_up()

@app.route("/api/test" , methods=["GET"])
def tes() : 
    return test()

@app.route("/api/login" , methods=["POST"]) 
def log():
    return login()

def token_required(f) :
    @wraps(f) 
    def decorated(*args, **kwargs) :
        token = request.headers.get("Authorization").split(" ")[1]

        print (token)

        if not token: 
            return jsonify({"message" : "Token is Missing"})
        
        try:
            data = jwt.decode(token, os.getenv("jwt") , algorithms=["HS256"])
            print (data.get("userid"))
            current_user = User.query.get(data["userid"])
        except jwt.ExpiredSignatureError :
            return jsonify({"message" : "Token expired"}) 
        except jwt.InvalidTokenError :
            return jsonify({"message" : "Invalid token"})
    
        return f(current_user , *args, **kwargs)
    
    return decorated

@app.route("/api/profile") 
@token_required 
def profil(cu) :
    return profile(cu)

if __name__ == "__main__" :
    with app.app_context() :
        db.create_all() 
    app.run(debug=True , port=5000)