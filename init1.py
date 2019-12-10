#!C:/Users/lx615/AppData/Local/Programs/Python/Python38-32/python

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash, Markup
from ast import literal_eval
import pymysql.cursors
import datetime
from datetime import date
from datetime import timedelta
from time import strftime
import time
from dateutil.relativedelta import *

#Initialize the app from Flask
app = Flask(__name__)
#testchange 1

#Configure MySQL
conn = pymysql.connect(host='192.168.64.2',
                       user='root',
                       password='admin',
                       database='blog')

#Variables
searchtype = 'Airport_search'

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
                date_in = depdate
                date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
                date_processing = [int(v) for v in date_processing]
                depdate = datetime.datetime(*date_processing)
            cursor = conn.cursor()
            flightinfoquery = ("SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight WHERE status = 'Upcoming' AND arrival_airport = \"{}\" AND departure_airport = \"{}\" AND departure_time = \"{}\"")
            queryvariables = (arrairport, depairport, depdate)
            cursor.execute(flightinfoquery.format(arrairport, depairport, depdate))
            finalflightdata = []
            # for row in cursor.fetchall():
            #     if row == 'airline_name'
            flightdata = cursor.fetchall()
            cursor.close()
            finalflightdata = flightdata
            error = None
            if arrairport != None and depairport!= None and depdate != None:
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
            flightdata = cursor.fetchall()
            cursor.close()
            finalflightdata = flightdata
            error = None
            if flight_num != None and depdate != None:
                return render_template('testpage1.html', flight_num=flight_num, depdate = depdate, finalflightdata = finalflightdata, searchtype=searchtype)
            else:
                error = 'One or more fields have not been filled in!'
                return render_template('testpage1.html', searchtype=searchtype, error=error)
        return render_template('testpage1.html', searchtype=searchtype)
    if searchtype == 'Airport_search':
        return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, searchtype=searchtype)
    else:
        return render_template('testpage1.html', searchtype=searchtype)

@app.route('/changesearch', methods=['GET', 'POST'])
def toggle():
    global searchtype
    if searchtype == "flight_num_search":
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
        searchtype = "Airport_search"
        return render_template('testpage1.html', arrival_airport=arrival_airportdata, departure_airport=departure_airportdata, searchtype=searchtype)
    elif searchtype == "Airport_search":
        searchtype = "flight_num_search"
        return render_template('testpage1.html', searchtype=searchtype)


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
        session['searchtype'] = searchtype
        session['logged_in'] = True

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
    typeof = session['typeof']
    #cursor = conn.cursor();
    #query = "SELECT ts, blog_post FROM blog WHERE username = \'{}\' ORDER BY ts DESC"
    #cursor.execute(query.format(username))
    #data1 = cursor.fetchall()
    #cursor.close()
    return render_template('home.html', username=username, typeof=typeof)

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
    session.clear()
    # session.pop('email')
    # session.pop('username')
    # session.pop('searchtype')
    # session.pop('logged_in')
    return redirect('/')

@app.route('/viewflights')
def viewflights():
    cursor = conn.cursor()
    query = "SELECT DISTINCT flight_num FROM ticket NATURAL JOIN purchases WHERE customer_email = \"{}\""
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

@app.route('/baviewflights')
def baviewflights():

    cursor = conn.cursor()
    query = "SELECT booking_agent_id from booking_agent WHERE email = \"{}\""
    cursor.execute(query.format(session['email']))
    data = cursor.fetchall()
    cursor.close()
    baid = data[0][0]

    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE booking_agent_id = \"{}\""
    cursor.execute(query.format(baid))
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


    return render_template('baviewflights.html', flightlist = templist)

@app.route('/purchaseticket', methods=['GET', 'POST'])
def purchaseticket():
    if session['typeof'] == 'customer':
        ticket_info = request.form.get("ticketpurchase", None)
        ticket_info = eval(ticket_info)
        cursor = conn.cursor();
        query = "SELECT MAX(ticket_id) FROM ticket"
        cursor.execute(query)
        ticket_id = cursor.fetchone()
        ticket_id = ticket_id[0]+1
        cursor.close()

        airline_name = ticket_info[0]
        flight_num = ticket_info[1]
        cursor = conn.cursor();
        ticketdatainsertquery = ("INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (\"{}\", \"{}\", \"{}\")")
        cursor.execute(ticketdatainsertquery.format(ticket_id, airline_name,flight_num))
        conn.commit()
        cursor.close()

        d = date.today()
        email = session['email']
        cursor = conn.cursor();
        purchasesdatainsertquery = ("INSERT INTO purchases (ticket_id, customer_email, purchase_date) VALUES (\"{}\", \"{}\", \"{}\")")
        cursor.execute(purchasesdatainsertquery.format(ticket_id, email,d))
        conn.commit()
        cursor.close()

        ##Html information
        departure_aiport=ticket_info[2]
        arrival_aiport=ticket_info[3]
        departure_time=ticket_info[4]
        arrival_time=ticket_info[5]
        flight_status=ticket_info[6]
        return render_template('purchaseticket.html', departure_aiport=departure_aiport,arrival_airport=arrival_aiport,departure_time=departure_time,arrival_time=arrival_time,ticket_info=ticket_info, ticket_id=ticket_id, d=d, airline_name=airline_name, flight_num=flight_num,email=email,flight_status=flight_status)

    elif session['typeof'] == 'booking_agent':

        cursor = conn.cursor()
        query = "SELECT booking_agent_id from booking_agent WHERE email = \"{}\""
        cursor.execute(query.format(session['email']))
        booking_agent_id = cursor.fetchone()
        booking_agent_id = booking_agent_id[0]
        cursor.close()

        ticket_info = request.form.get("ticketpurchase", None)
        ticket_info = eval(ticket_info)
        cursor = conn.cursor();
        query = "SELECT MAX(ticket_id) FROM ticket"
        cursor.execute(query)
        ticket_id = cursor.fetchone()
        ticket_id = ticket_id[0]+1
        cursor.close()

        airline_name = ticket_info[0]
        flight_num = ticket_info[1]
        cursor = conn.cursor();
        ticketdatainsertqueryBA = ("INSERT INTO ticket (ticket_id, airline_name, flight_num) VALUES (\"{}\", \"{}\", \"{}\")")
        cursor.execute(ticketdatainsertqueryBA.format(ticket_id, airline_name,flight_num))
        conn.commit()
        cursor.close()

        d = date.today()
        email = request.form.get("customer_email", None)
        cursor = conn.cursor();
        purchasesdatainsertquery = ("INSERT INTO purchases (ticket_id, customer_email, booking_agent_id, purchase_date) VALUES (\"{}\", \"{}\", \"{}\",\"{}\")")
        cursor.execute(purchasesdatainsertquery.format(ticket_id, email,booking_agent_id,d))
        conn.commit()
        cursor.close()

        ##Html information
        departure_aiport=ticket_info[2]
        arrival_aiport=ticket_info[3]
        departure_time=ticket_info[4]
        arrival_time=ticket_info[5]
        flight_status=ticket_info[6]
        return render_template('bapurchaseticket.html', departure_aiport=departure_aiport,arrival_airport=arrival_aiport,departure_time=departure_time,arrival_time=arrival_time,ticket_info=ticket_info, ticket_id=ticket_id, d=d, airline_name=airline_name, flight_num=flight_num,email=email,flight_status=flight_status, booking_agent_id=booking_agent_id)


@app.route('/createnewflight')
def createnewflight():

    return render_template('createnewflight.html')

@app.route('/changeflightstatus')
def changeflightstatus():

    return render_template('changeflightstatus.html')

@app.route('/trackmyspending')
def trackmyspending():
    d = date.today() - timedelta(days=365)

    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE customer_email=\"{}\" AND purchase_date > \"{}\""
    cursor.execute(query.format(session['email'], d))
    data = cursor.fetchall()
    cursor.close()

    temp1 = flatten(data)

    templist = []
    for i in temp1:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist.append(j[0])

    spending = 0
    for i in templist:
        spending += i



    return render_template('trackmyspending.html', spending=spending, d=d)

@app.route('/testchart', methods=['GET', 'POST'])
def testchart():
    today = date.today()
    thismonth = int(strftime('%m')) - 1
    firstday = today.replace(day=1)
    months = ["January","February","March","April","May","June","July","August", "September", "October", "November", "December"]


    if request.method == "POST":
        startmonth = request.form.get("start_date")
        endmonth = request.form.get("end_date")

        valuelist = []
        monthlist = []
        monthnumlist = []
        monthactuallist = []

        startmonth = datetime.datetime.strptime(startmonth, '%Y-%m-%d')
        endmonth = datetime.datetime.strptime(endmonth, '%Y-%m-%d')

        startmonth = startmonth.replace(day=1)
        endmonth = endmonth.replace(day=1)

        while (startmonth < endmonth):
            monthlist.append(months[int(startmonth.strftime('%m')) - 1])
            monthactuallist.append(startmonth)
            monthnumlist.append(int(startmonth.strftime('%m')) - 1)
            startmonth = startmonth+relativedelta(months=+1)

        monthlist.append(months[int(startmonth.strftime('%m')) - 1])
        monthactuallist.append(startmonth)
        monthnumlist.append(int(startmonth.strftime('%m')) - 1)


        for i in range(len(monthactuallist) - 1):
            j = i + 1
            cursor = conn.cursor()
            query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date>=\"{}\" AND purchase_date<\"{}\""
            cursor.execute(query.format(monthactuallist[i], monthactuallist[j]))
            data = cursor.fetchall()
            cursor.close()
            testvar1 = flatten(data)

            templist1 = []
            for i in testvar1:
                cursor = conn.cursor()
                query = "SELECT price FROM flight WHERE flight_num = \"{}\""
                cursor.execute(query.format(i))
                d = cursor.fetchall()
                cursor.close()
                for j in d:
                    templist1.append(j[0])
            valuelist.append(sum(templist1))

        return render_template('testchart.html', labels = monthlist, values = valuelist)

    lastm1 = get_lastday(today)
    lastm2 = get_lastday(lastm1)
    lastm3 = get_lastday(lastm2)
    lastm4 = get_lastday(lastm3)
    lastm5 = get_lastday(lastm4)

#Last month purchases
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date<\"{}\" AND purchase_date>=\"{}\""
    cursor.execute(query.format(today, lastm1))
    data = cursor.fetchall()
    cursor.close()
    testvar = flatten(data)

    templist = []
    for i in testvar:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist.append(j[0])

    spending = 0
    for i in templist:
        spending += i

#2 months ago purchases
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date<\"{}\" AND purchase_date>=\"{}\""
    cursor.execute(query.format(lastm1, lastm2))
    data = cursor.fetchall()
    cursor.close()
    testvar1 = flatten(data)

    templist1 = []
    for i in testvar1:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist1.append(j[0])

    spending1 = 0
    for i in templist1:
        spending1 += i

#3 months ago purchases
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date<\"{}\" AND purchase_date>=\"{}\""
    cursor.execute(query.format(lastm2, lastm3))
    data = cursor.fetchall()
    cursor.close()
    testvar2 = flatten(data)

    templist2 = []
    for i in testvar2:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist2.append(j[0])

    spending2 = 0
    for i in templist2:
        spending2 += i

#4 months ago
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date<\"{}\" AND purchase_date>=\"{}\""
    cursor.execute(query.format(lastm3, lastm4))
    data = cursor.fetchall()
    cursor.close()
    testvar3 = flatten(data)

    templist3 = []
    for i in testvar3:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist3.append(j[0])

    spending3 = 0
    for i in templist3:
        spending3 += i

#5 months ago
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date<\"{}\" AND purchase_date>=\"{}\""
    cursor.execute(query.format(lastm4, lastm5))
    data = cursor.fetchall()
    cursor.close()
    testvar4 = flatten(data)

    templist4 = []
    for i in testvar4:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            templist4.append(j[0])

    spending4 = 0
    for i in templist4:
        spending4 += i

#This months spending
    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE purchase_date>=\"{}\""
    cursor.execute(query.format(firstday))
    data = cursor.fetchall()
    cursor.close()
    lasttestvar = flatten(data)

    lasttemplist = []
    for i in lasttestvar:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            lasttemplist.append(j[0])

    lastspending = 0
    for i in lasttemplist:
        lastspending += i


    x = thismonth - 5
    startingmonth = x + 1

    v = []

    testlist = []
    for i in range(x, thismonth+1):
        testlist.append(months[i])

    testvar2 = session['email']

    values = [spending4, spending3, spending2, spending1, spending, lastspending]
    return render_template('testchart.html', labels = testlist, values = values, thismonth = testvar)

@app.route('/viewcommission', methods=['GET', 'POST'])
def viewcommission():


    today = date.today()
    last30days = date.today() - datetime.timedelta(days=30)

    cursor = conn.cursor()
    query = "SELECT booking_agent_id FROM booking_agent WHERE email=\"{}\""
    cursor.execute(query.format(session['email']))
    data = cursor.fetchall()
    cursor.close()
    baid = flatten(data)[0]

    if request.method == "POST":

        startmonth = request.form.get("start_date")
        endmonth = request.form.get("end_date")
        startmonth1 = startmonth
        endmonth1 = endmonth

        startmonth = datetime.datetime.strptime(startmonth, '%Y-%m-%d')
        endmonth = datetime.datetime.strptime(endmonth, '%Y-%m-%d')

        cursor = conn.cursor()
        query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE booking_agent_id=\"{}\" AND purchase_date >= \"{}\" AND purchase_date <= \"{}\" "
        cursor.execute(query.format(baid, startmonth, endmonth))
        data = cursor.fetchall()
        cursor.close()
        flights = flatten(data)

        numflights = len(flights)

        totalcommission = []
        for i in flights:
            cursor = conn.cursor()
            query = "SELECT price FROM flight WHERE flight_num = \"{}\""
            cursor.execute(query.format(i))
            d = cursor.fetchall()
            cursor.close()
            for j in d:
                totalcommission.append(float(j[0])*.1)

        total = sum(totalcommission)

        av = check0(total, numflights)


        return render_template('viewcommission.html', totcommrecieved=total, totticksold=numflights, avtick=av, startmonth1=startmonth1, endmonth1=endmonth1)


    cursor = conn.cursor()
    query = "SELECT flight_num FROM ticket NATURAL JOIN purchases WHERE booking_agent_id=\"{}\" AND purchase_date > \"{}\" AND purchase_date <= \"{}\" "
    cursor.execute(query.format(baid, last30days, today))
    data = cursor.fetchall()
    cursor.close()
    flights = flatten(data)

    numflights = len(flights)

    totalcommission = []
    for i in flights:
        cursor = conn.cursor()
        query = "SELECT price FROM flight WHERE flight_num = \"{}\""
        cursor.execute(query.format(i))
        d = cursor.fetchall()
        cursor.close()
        for j in d:
            totalcommission.append(float(j[0])*.1)

    total = sum(totalcommission)

    av = check0(total, numflights)



    return render_template('viewcommission.html', total=total, flights=numflights, av = av)


@app.route('/viewtopcustomers')
def viewtopcustomers():

    cursor = conn.cursor()
    query = "SELECT booking_agent_id FROM booking_agent WHERE email=\"{}\""
    cursor.execute(query.format(session['email']))
    data = cursor.fetchall()
    cursor.close()
    baid = flatten(data)[0]

    oldmonth = date.today()+relativedelta(months=-6)
    oldyear = date.today()+relativedelta(years=-1)

    cursor = conn.cursor()
    query = "SELECT customer_email, COUNT(ticket_id) FROM purchases WHERE booking_agent_id = \"{}\" AND purchase_date <= \"{}\" GROUP BY customer_email"
    cursor.execute(query.format(baid, oldmonth))
    data = cursor.fetchall()
    cursor.close()
    test = data

    cust = []
    numtick = []

    for i in data:
        cust.append(i[0])
        numtick.append(i[1])

    if len(cust) > 5:
        cust = cust[:5]
    if len(numtick) > 5:
        numtick = numtick[:5]

    cursor = conn.cursor()
    query = "CREATE VIEW customer_flight AS SELECT flight_num, customer_email FROM ticket NATURAL JOIN purchases WHERE booking_agent_id=\"{}\" AND purchase_date <= \"{}\" "
    cursor.execute(query.format(baid, oldyear))
    query = "SELECT customer_email, sum(price) FROM flight NATURAL JOIN customer_flight GROUP BY customer_email"
    cursor.execute(query)
    data1 = cursor.fetchall()
    query = "DROP VIEW customer_flight"
    cursor.execute(query)
    cursor.close()
    tvar = data1

    cust1=[]
    comm=[]

    for i in data1:
        cust1.append(i[0])
        comm.append(int(i[1])*.1)

    return render_template('viewtopcustomers.html', data=data, labels=cust, values=numtick, tvar=tvar, labels1=cust1, values1=comm)


#Other Functions

def isTuple(x): return type(x) == tuple

def check0(x, y):
    return x/y if y else 0

def flatten(T):
    if not isTuple(T): return (T,)
    elif len(T) == 0: return ()
    else: return flatten(T[0]) + flatten(T[1:])

def get_lastday(current):
    _first_day = current.replace(day=1)
    prev_month_lastday = _first_day - datetime.timedelta(days=1)
    return prev_month_lastday.replace(day=1)

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
