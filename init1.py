#!C:/Users/lx615/AppData/Local/Programs/Python/Python38-32/python

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors
import datetime

#Initialize the app from Flask
app = Flask(__name__)
#testchange 1

#Configure MySQL
conn = pymysql.connect(host='192.168.64.3',
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
    query = "SELECT DISTINCT arrival_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('testpage1.html', test1=data[0])

@app.route('/bootstrap/testpage3.html')
def dropdowntest():
    cursor = conn.cursor()
    query = "SELECT DISTINCT arrival_airport FROM flight"
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()

    return render_template('bootstrap/testpage3.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/aslogin')
def aslogin():
	return render_template('aslogin.html')

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

@app.route('/testpage1', methods=['GET', 'POST'])
def test():
    searchtype = request.form.get('searchtype', None)
    # searchtype = 'flight_num_search'
    if searchtype == 'Airport_search':
        cursor = conn.cursor()
        query = "SELECT DISTINCT arrival_airport FROM flight"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        arrival_airportdata = list(data)
        cursor = conn.cursor()
        query = "SELECT DISTINCT departure_airport FROM flight"
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        departure_airportdata = list(data)
        if request.method == "POST":
            arrairport = request.form.get("arrairport", None)
            depairport = request.form.get("depairport", None)
            depdate = request.form.get("depdate", None)
            if depdate:
                date_in = depdate # replace this string with whatever method or function collects your data
                date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
                date_processing = [int(v) for v in date_processing]
                depdate = datetime.datetime(*date_processing)
            cursor = conn.cursor()
            flightinfoquery = ("SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight WHERE status = 'Upcoming' AND arrival_airport = \"{}\" AND departure_airport = \"{}\" AND departure_time = \"{}\"")
            queryvariables = (arrairport, depairport, depdate)
            cursor.execute(flightinfoquery.format(arrairport, depairport, depdate))
            flightdata = cursor.fetchmany()
            cursor.close()
            finalflightdata = flightdata
            error = None
            if arrairport != None and depairport!= None and depdate != None:
                # return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, arrairport = arrairport, depairport = depairport, depdate = depdate)
                return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, arrairport = arrairport, depairport = depairport, depdate = depdate, finalflightdata = finalflightdata, searchtype=searchtype)
            else:
                error = 'One or more fields have not been filled in!'
                return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, error=error, searchtype = searchtype)
            return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, searchtype=searchtype)
    elif searchtype == 'flight_num_search':
        if request.method == "POST":
            flight_num = request.form.get("flight_num", None)
            depdate = request.form.get("depdate", None)
            if depdate:
                date_in = depdate # replace this string with whatever method or function collects your data
                date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
                date_processing = [int(v) for v in date_processing]
                depdate = datetime.datetime(*date_processing)
            cursor = conn.cursor()
            flightinfoquery = ("SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight WHERE status = 'Upcoming' AND flight_num = \"{}\" AND departure_time = \"{}\"")
            cursor.execute(flightinfoquery.format(flight_num, depdate))
            flightdata = cursor.fetchmany()
            cursor.close()
            finalflightdata = flightdata
            error = None
            if flight_num != None and depdate != None:
                # return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, arrairport = arrairport, depairport = depairport, depdate = depdate)
                return render_template('testpage1.html', flight_num=flight_num, depdate = depdate, finalflightdata = finalflightdata, searchtype=searchtype)
            else:
                error = 'One or more fields have not been filled in!'
                return render_template('testpage1.html', searchtype=searchtype, error=error)

    if searchtype == 'Airport_search':
        return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, searchtype=searchtype)
    else:
        return render_template('testpage1.html', searchtype=searchtype)

@app.route('/toggle', methods=['GET', 'POST'])
def toggle(myboolean):
    myboolean = not myboolean

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
    email = request.form['email']
    password = request.form['password']
    typeof = request.form['typeof']
    #cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = "SELECT * FROM {} WHERE email = \'{}\' and password = \'{}\'"
    cursor.execute(query.format(typeof, email, password))
	#stores the results in a variable
    data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
		#creates a session for the the user
		#session is a built in
        session['email'] = email
        session['typeof'] = typeof

        return redirect(url_for('home'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

@app.route('/asloginAuth', methods=['GET', 'POST'])
def asloginAuth():
	#grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    #cursor used to send queries
    cursor = conn.cursor()
	#executes query
    query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = \'{}\'"
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
        return redirect(url_for('ashome'))
    else:
		#returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('aslogin.html', error=error)

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

    username = session['email']
    #cursor = conn.cursor();
    #query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
    #cursor.execute(query.format(username))
    #data1 = cursor.fetchall()
    #cursor.close()
    return render_template('home.html', username=username)

@app.route('/ashome')
def ashome():
    username = session['username']
    return render_template('ashome.html', username=username)


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
	session.pop('email')
	return redirect('/')

@app.route('/viewflights')
def viewflights():
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE customer_email = \"{}\""
    cursor.execute(query.format(session['email']))
    data = cursor.fetchall()
    cursor.close()
    flightnumlist = flatten(data)


    templist = []
    for i in flightnumlist:
        cursor = conn.cursor()
        query = "SELECT * FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist.append(j)

    return render_template('viewflights.html', flightlist=templist)

def isTuple(x): return type(x) == tuple

def flatten(T):
    if not isTuple(T): return (T,)
    elif len(T) == 0: return ()
    else: return flatten(T[0]) + flatten(T[1:])


app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
