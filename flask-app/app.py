from datetime import datetime
import os

from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = input("Enter MySQL hostname: ")
app.config['MYSQL_USER'] = input("Enter username: ")
app.config['MYSQL_PASSWORD'] = input("Enter password: ")
app.config['MYSQL_DB'] = "sauron-db-dev1"
app.config['UPLOAD_FOLDER'] = "static/frames"

mysql = MySQL(app)

@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('form.html')

	if request.method == 'POST':
		reportType = request.form['type']
		latitude = float(request.form['latitude'])
		longitude = float(request.form['longitude'])
		description = request.form['description']
		cursor = mysql.connection.cursor()

		if 'frame-file' in request.files:
			now = datetime.now()
			now_string = now.strftime("%y-%m-%d-%h-%m-%s")
			frame_file_path = os.path.join(app.config['UPLOAD_FOLDER'],'image_' + now_string + '.png')
			frame_file = request.files["frame-file"]
			frame_file.save(frame_file_path)
		else:
			frame_file_path = os.path.join(app.config['UPLOAD_FOLDER'],'default.png')

		cursor.execute('''INSERT INTO report_list (type, latitude, longitude, description, frame) VALUES(%s,%s,%s,%s,%s)''',(reportType,latitude,longitude,description, frame_file_path))
		mysql.connection.commit()
		cursor.close()
		return "Submitted!"

app.run(host='0.0.0.0', port=5000)
