from flask import Flask,request
from datetime import datetime
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'upload_destination'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    now = datetime.now()
    now_string = now.strftime("%y-%m-%d")

    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']
        path = os.path.join(app.config['UPLOAD_FOLDER'],'image_' + now_string + '.png')
        file1.save(path)
        return path

        return 'ok'
    return '''
    <h1>Upload new File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file1">
      <input type="submit">
    </form>
    '''

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
