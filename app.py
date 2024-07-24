from flask import Flask , render_template , request
import mysql.connector

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('login.html')

@app.route('/createAccount')
def registrationPage():
    return render_template('register.html')


## code for login part
@app.route('/login' , methods = ['post'])
def login():
    usernameL = request.form['usernameL']
    userpassL = request.form['userpassL']

    cnn = mysql.connector.connect(user = 'root' , password = 'Mysql$2002' , host = '127.0.0.1')

    mycursor = cnn.cursor()

    mycursor.execute("USE user")

    mycursor.execute("SELECT * FROM user.userTable WHERE userName = %s AND userPass = %s" , (usernameL ,userpassL))

    if len(mycursor.fetchall()) == 0 :
        cnn.close()
        return render_template("login.html" , msg = "No user exists with this username and password.")

    cnn.close()
    return "Welcome to our website."






## code for registration part
@app.route('/register' , methods = ['POST'])
def register():
    username = request.form['username']
    useremail = request.form['useremail']
    userpassword = request.form['userpass']

    if "" in [username , useremail , userpassword] :
        ## this line of code just for registration part only
        # return "Error ! Enter all the information correctly."
        return render_template("register.html" , msg = "Enter all the information correctly")

    try:

        ## creating a connection with mysql
        cnn = mysql.connector.connect(user = 'root' , password = 'Mysql$2002' , host = '127.0.0.1')

        ## create a cursor
        mycursor = cnn.cursor()

        ## create a database if not exists
        mycursor.execute("CREATE DATABASE IF NOT EXISTS user")

        ## select the database
        mycursor.execute("USE user")

        ## create a table if not exists
        mycursor.execute("CREATE TABLE IF NOT EXISTS userTable(userName varchar(30) NOT NULL, userEmail varchar(50) NOT NULL, userPass varchar(30) NOT NULL)")

        ## insert the user values (DML operation)
        mycursor.execute("INSERT INTO user.userTable VALUES(%s , %s , %s)" , (username , useremail , userpassword))

        ## commit changes
        cnn.commit()

        ## close connection
        cnn.close()

    except Exception as e:
        return f"{e}"

    
    ## this line return code just for registration part only
    # return "Congratulations ! You have Successfully Registered."

    ## return code for login/registration both
    return render_template("login.html")





if __name__ == '__main__':
    app.run(host='0.0.0.0')