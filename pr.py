from flask import Flask, render_template, request, jsonify,redirect
import firebase_admin
from firebase_admin import credentials,db,initialize_app

cred = credentials.Certificate("essai-2-45770-firebase-adminsdk-fdyn8-e402afc0ba.json")
initialize_app(cred, {
    'databaseURL': 'https://essai-2-45770-default-rtdb.firebaseio.com/'
})

ref = db.reference("/")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login_1.html')


@app.route('/home')
def home():
     return render_template('index.html')


@app.route('/login')
def loginpage():
     return render_template('login_1.html')

@app.post('/login')
def checkuser():
    username = request.form['username']
    user_data = ref.child('userslist').order_by_child('username').equal_to(username).get()
    
    if user_data:
        for key, value in user_data.items():
            if value.get('username') == username:
                password = value.get('password')
                if(password==request.form['password']):
                    return redirect('/home')
    return redirect("/")


@app.route('/signup')
def signup():
     return render_template('login_2.html')

@app.post('/signup')
def adduser():
        new_data = {"username":request.form['username'],"password":request.form['password'],"email":request.form['email']}
        ref.child("userslist").push(new_data)
        return render_template('login_1.html',prompt_message='user created')

   
@app.route('/forgotpassword')
def update_data():
     return jsonify({'text': ""})

if __name__ == '__main__':
    app.run(debug=True)