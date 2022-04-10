from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = input("Enter MySQL hostname: ")
app.config['MYSQL_USER'] = input("Enter username: ")
app.config['MYSQL_PASSWORD'] = input("Enter password: ")
app.config['MYSQL_DB'] = "sauron-db-dev1"

mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('form.html')

	if request.method == 'POST':
		print(request.form)
		reportType = request.form['type']
		latitude = float(request.form['latitude'])
		longitude = float(request.form['longitude'])
		description = request.form['description']
		cursor = mysql.connection.cursor()
		cursor.execute('''INSERT INTO report_list (type, latitude, longitude, description) VALUES(%s,%s,%s,%s)''',(reportType,latitude,longitude,description))
		mysql.connection.commit()
		cursor.close()
		return "Submitted!"

app.run(host='0.0.0.0', port=5000)
