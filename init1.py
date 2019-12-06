#!C:/Users/lx615/AppData/Local/Programs/Python/Python38-32/python

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors


#Initialize the app from Flask
app = Flask(__name__)
#testchange 1

#Configure MySQL
conn = pymysql.connect(host='192.168.64.2',
                       user='root',
                       password='admin',
                       database='blog')

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Routing to retrieve dropdown options when searching for flight information
@app.route('/getarrivalairport')
def getarrivalairport():
    cursor = conn.cursor()
    query = "SELECT arrival_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('testpage1.html', test1=data[0])

@app.route('/bootstrap/testpage3.html')
def dropdowntest():
    cursor = conn.cursor()
    query = "SELECT arrival_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('bootstrap/testpage3.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/asregister')
def asregister():
    cursor = conn.cursor()
    query = "SELECT airline_name FROM airline"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    airlinenames = list(data)

    return render_template('asregister.html', airlinenames = airlinenames)

@app.route('/baregister')
def baregister():
	return render_template('baregister.html')

@app.route('/testpage1')
def test():
    cursor = conn.cursor()
    query = "SELECT arrival_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    arrival_airportdata = list(data)

    cursor = conn.cursor()
    query = "SELECT departure_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    departure_airportdata = list(data)

    return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata)



@app.route('/submitdropdown', methods=['GET', 'POST'])
def test1():

    if request.method == "POST":
        arrairport = request.form.get("arrairport", None)
        return render_template('login.html')
        if arrairport != None:
            return render_template('testpage1.html', arrairport = arrairport)
        return render_template('testpage1.html')



    # return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata)

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = "SELECT * FROM user WHERE username = \'{}\' and password = \'{}\'"
	cursor.execute(query.format(username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    name = request.form['name']
    pnum = request.form['phone_number']
    ppnum = request.form['passport_number']
    ppcountry = request.form['passport_country']
    ppexp = request.form['passport_expiration']
    dob = request.form['date_of_birth']
    street = request.form['street']
    city = request.form['city']
    state = request.form['state']
    anum = request.form['building_number']



#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = "SELECT * FROM customer WHERE email = \'{}\'"
    cursor.execute(query.format(email))
	#stores the results in a variable

    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
        cursor.execute(ins.format(email, name, password, anum, street, city, state, pnum, ppnum, ppexp, ppcountry, dob))
        conn.commit()
        cursor.close()
        flash("You are logged in")
        return render_template('index.html')


@app.route('/baregisterAuth', methods=['GET', 'POST'])
def baregisterAuth():
	#grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    baid = request.form['booking_agent_id']

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
    cursor.execute(query.format(email))
	#stores the results in a variable

    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('baregister.html', error = error)
    else:
        ins = "INSERT INTO booking_agent VALUES(\'{}\', \'{}\', \'{}\')"
        cursor.execute(ins.format(email, name, baid))
        conn.commit()
        cursor.close()
        flash("You are logged in")
        return render_template('index.html')

@app.route('/asregisterAuth', methods=['GET', 'POST'])
def asregisterAuth():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['first_name']
    lname = request.form['last_name']
    dob = request.form['date_of_birth']
    aname = request.form['airline_name']

#	if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

	#cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = "SELECT * FROM airline_staff WHERE username = \'{}\'"
    cursor.execute(query.format(username))
	#stores the results in a variable

    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
		#If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('asregister.html', error = error)
    else:
        ins = "INSERT INTO customer VALUES(\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\')"
        cursor.execute(ins.format(username, password, fname, lname, dob, aname))
        conn.commit()
        cursor.close()
        flash("You are logged in")
        return render_template('index.html')

@app.route('/home')
def home():

    username = session['username']
    cursor = conn.cursor();
    query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
    cursor.execute(query.format(username))
    data1 = cursor.fetchall()
    cursor.close()
    return render_template('home.html', username=username, posts=data1)


@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = "INSERT INTO blog (blog_post, username) VALUES(\'{}\', \'{}\')"
	cursor.execute(query.format(blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
