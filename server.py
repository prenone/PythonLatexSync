import os
from flask import Flask, render_template, send_file, request, abort, make_response
from dataclasses import dataclass
import base64

app = Flask(__name__)

@dataclass
class User:
    user: str
    write_password: str
    read_password: str

dirname = os.path.join(os.path.dirname(__file__), 'data')
users_filename = os.path.join(dirname, 'users.txt')
storage_directory = os.path.join(dirname, 'storage/')

os.makedirs(dirname, exist_ok=True)
open(users_filename, 'a').close()
os.makedirs(storage_directory, exist_ok=True)

push_count = 0
pull_count = 0

# Loads users
def load_users():
    global users

    users = {}

    with open(users_filename) as file:
        for line in file:
            words = line.split(';')
            words = [word.strip() for word in words]

            users[words[0]] = User(
                user = words[0],
                write_password = words[1],
                read_password = words[2]
            )

            user_folder = os.path.join(storage_directory, words[0])
            os.makedirs(user_folder, exist_ok=True)

            print(f'Loaded user "{words[0]}" and created folder')

@app.route('/')
def index():
    return render_template('index.html', push_count=push_count, pull_count=pull_count)

@app.route('/docs')
def docs():
    return render_template('docs.html')

@app.route('/push/<user>/<write_password>/<filename>', methods=['POST'])
def push_file(user, write_password, filename):
    if not verify_user_write(user, write_password):
        abort(403, 'Invalid user or write_password')
    
    filename = sanitize_filename(filename)
    filepath = os.path.join(storage_directory, user, filename)

    if 'file' not in request.files:
        abort(400, 'No file part in the request')
    
    file = request.files['file']
    
    if file.filename == '':
        abort(400, 'No file selected')
    
    file.save(filepath)

    global push_count
    push_count += 1

    print(f'Saving "{filename}" in storage for user "{user}". Request ip address: {request.remote_addr}')
    return 'File saved successfully', 200


@app.route('/pull/<user>/<read_password>/<filename>', methods=['GET'])
def pull_file(user, read_password, filename):
    if not verify_user_read(user, read_password):
        abort(403, 'Invalid user or read_password')

    requested_filename = filename
    filename = sanitize_filename(filename)
    
    filepath = os.path.join(storage_directory, user, filename)

    if not os.path.exists(filepath):
        abort(404, 'File not found for the user')

    global pull_count
    pull_count += 1

    print(f'Serving "{requested_filename}" to user "{user}" Request ip address: {request.remote_addr}')
    response = make_response(send_file(filepath, as_attachment=True, download_name=requested_filename))

    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

def sanitize_filename(filename):
    filename = filename.strip()
    return base64.urlsafe_b64encode(filename.encode('UTF-8')).decode('UTF-8')


def verify_user_write(user, write_password):
    user = user.strip()
    write_password = write_password.strip()

    if user in users:
        if users[user].write_password == write_password:
            return True

    return False

def verify_user_read(user, read_password):
    user = user.strip()
    read_password = read_password.strip()

    if user in users:
        if users[user].read_password == read_password:
            return True

    return False

load_users()

if __name__ == '__main__':
    app.run(debug=False)
