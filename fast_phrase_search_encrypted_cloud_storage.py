from flask import Flask, render_template, request
from DBConnection import Db

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('LOGIN.html')

@app.route('/user',methods=['get','post'])
def user():
    if request.method=="POST":
        name=request.form['textfield']
        dob=request.form['textfield8']
        place=request.form['textfield2']
        post=request.form['textfield3']
        pin=request.form['textfield4']
        phone=request.form['textfield5']
        email=request.form['textfield6']
        image=request.files['fileField']
        password=request.form['textfield9']
        db=Db()
        g=db.insert("insert into login VALUES ('','"+email+"','"+password+"','user')")
        g=db.insert("insert into user VALUES ('','"+name+"','"+dob+"','"+place+"','"+post+"','"+pin+"','"+phone+"','"+email+"','"+image+"')")


    return render_template('USER/user.html')

@app.route('/file')
def file():
    return render_template('USER/file.html')

@app.route('/view_profile')
def view_profile():
    db = Db()
    ss = db.selectOne("select * from user,login WHERE user.login_id=login.login_id")
    return render_template('USER/view profile.html',data=ss)



@app.route('/user_home')
def user_home():
    return render_template('USER/USER HOME.html')


@app.route('/search_files')
def search_files():
    db = Db()
    ss = db.select("select * from file")
    return render_template('USER/search files.html',data=ss)

@app.route('/download_files')
def download_files():
    db = Db()
    ss = db.select("select * from file")
    return render_template('USER/download files.html',data=ss)

if __name__ == '__main__':
    app.run()
