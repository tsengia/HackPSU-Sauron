from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'
 
mysql = MySQL(app) 
#Creating a connection cursor
#cursor = mysql.connection.cursor()
 
#Executing SQL Statements
#cursor.execute(''' INSERT INTO report_list VALUES (type,latitude,longitude,description);''')
#Saving the Actions performed on the DB
#mysql.connection.commit()
 
#Closing the cursor
#cursor.close()

@app.route('/form')
def form():
	return render_template('form.html')
 
@app.route('/login', methods = ['POST', 'GET'])
def login():
	if request.method == 'GET':
		return "Login via the login Form"
     
	if request.method == 'POST':
		type = request.form['type']
		latitude = request.form['latitude']
		longitude = request.form['longitude']
		description = request.form['description']        
		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO report_list (type, latitude, longitude, description) VALUES(%s,%s,%s,%s)''',(type,latitude,longitude,description))
		mysql.connection.commit()
		cursor.close()
		return "Done!"

app.run(host='0.0.0.0', port=5000)
