from datetime import datetime
import os
import shutil

from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = input("Enter MySQL hostname: ")
app.config['MYSQL_USER'] = input("Enter username: ")
app.config['MYSQL_PASSWORD'] = input("Enter password: ")
app.config['MYSQL_DB'] = "sauron-db-dev1"
app.config['UPLOAD_FOLDER'] = "static/frames"

mysql = MySQL(app)

@app.route('/clear', methods=['GET'])
def clear_data():
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM report_list WHERE 1=1')
    mysql.connection.commit()
    cursor.close()
    shutil.rmtree("static/frames")
    os.mkdir("static/frames")
    shutil.copyfile("default-frame.png", "static/frames/default-frame.png")
    return "Cleared data."

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
			now_string = now.strftime("%y-%m-%d-%h-%M-%s")
			frame_file_name = 'image_' + now_string + '.png'
			frame_file_path = os.path.join(app.config['UPLOAD_FOLDER'],frame_file_name)
			frame_file = request.files["frame-file"]
			frame_file.save(frame_file_path)
		else:
			frame_file_name = 'default-frame.png'

		cursor.execute('''INSERT INTO report_list (type, latitude, longitude, description, frame) VALUES(%s,%s,%s,%s,%s)''',(reportType,latitude,longitude,description, frame_file_name))
		mysql.connection.commit()
		cursor.close()
		return "Submitted!"

shutil.copyfile("default-frame.png", "static/frames/default-frame.png")
app.run(host='0.0.0.0', port=5000, ssl_context=("../cert.pem","../key.pem"))
