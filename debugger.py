from flask import Flask, request, jsonify, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import csv
from datetime import datetime
import pytz
import os
import argparse

app = Flask(__name__)
csvdir = '/results'

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_csv(filename):
    return ('.' in filename) and (filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS)

@app.route("/file/<filename>",methods=['GET'])
def get_json(filename):
    global csvdir
    if request.method == 'GET':
        try:
            new_list = []
            jsonfile = {}
            with open(f'{csvdir}/{filename}.csv',newline='') as f:
                jsonfile = csv.DictReader(f)
                for row in jsonfile:
                    new_item = {}
                    for k, v in row.items():
                        if k == 'time':
                            # Timestamp converted to UTC datetime
                            new_item[k] = datetime.fromtimestamp(int(v[:-9]),tz=pytz.UTC).isoformat()
                        else:
                            new_item[k] = v
                    new_list.append(new_item)
            data = new_list
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({'error': 'File not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid Request method'}), 400

@app.route("/upload",methods=['GET','POST'])
def upload_csv():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file and allowed_csv(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('outputs',filename))
            return f"{filename} uploaded successfully"
        except Exception as e:
            return f"Error!, {str(e)}"
        # return redirect(url_for('download'))
    return render_template('csv_upload.html')
    
@app.route("/get",methods=['GET'])
def listallcsvs():
    global csvdir
    if request.method == 'GET':
        try:
            data = []
            for filename in os.listdir(csvdir):
                file = {}
                if filename.endswith('csv'):
                    file['name'] = filename.split('.')[0]
                    data.append(file)
            return jsonify(data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid Request method'}), 400

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default=8080, help='Port to Run the flask server')
    args = parser.parse_args()

    PORT = int(args.port)

    app.run(host='',port=PORT,debug=True)