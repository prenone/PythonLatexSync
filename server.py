import os
from multiprocessing import Value
from flask import Flask, Response, render_template, send_file, request, abort, make_response
from dataclasses import dataclass
import base64
from ctypes import c_int

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

push_count = Value(c_int, 0)
pull_count = Value(c_int, 0)

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
    with push_count.get_lock(), pull_count.get_lock():
        return render_template('index.html', push_count=push_count.value, pull_count=pull_count.value)

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

    with push_count.get_lock():
        push_count.value += 1

    print(f'Saving "{filename}" in storage for user "{user}". Request ip address: {request.remote_addr}')
    return 'File saved successfully', 200

@app.route('/delete/<user>/<write_password>/<filename>', methods=['DELETE'])
def delete_file(user, write_password, filename):
    if not verify_user_write(user, write_password):
        abort(403, 'Invalid user or write_password')

    filename = sanitize_filename(filename)
    filepath = os.path.join(storage_directory, user, filename)

    if not os.path.exists(filepath):
        abort(404, 'File not found')
    
    os.remove(filepath)

    print(f'Deleted "{filename}" from storage for user "{user}". Request ip address: {request.remote_addr}')
    return 'File deleted successfully', 200

@app.route('/pull/<user>/<read_password>/<filename>', methods=['GET'])
def pull_file(user, read_password, filename):
    if not verify_user_read(user, read_password):
        abort(403, 'Invalid user or read_password')

    requested_filename = filename
    filename = sanitize_filename(filename)
    
    filepath = os.path.join(storage_directory, user, filename)

    if not os.path.exists(filepath):
        abort(404, 'File not found for the user')

    with pull_count.get_lock():
        pull_count.value += 1

    print(f'Serving "{requested_filename}" to user "{user}" Request ip address: {request.remote_addr}')
    response = make_response(send_file(filepath, as_attachment=True, download_name=requested_filename))

    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'

    return response

def sanitize_filename(filename):
    filename = filename.strip()
    return base64.urlsafe_b64encode(filename.encode('UTF-8')).decode('UTF-8')

def unsanitize_filename(sanitized_filename):
    decoded_bytes = base64.urlsafe_b64decode(sanitized_filename.encode('UTF-8'))
    original_filename = decoded_bytes.decode('UTF-8')
    return original_filename


def verify_user_write(user, write_password):
    user = user.strip()
    write_password = write_password.strip()

    if user in users:
        if users[user].write_password == write_password:
            return True

    return False

@app.route('/ui/', methods=['GET'])
def user_interface():
    auth = request.authorization
    if not auth or not verify_user_write(auth.username, auth.password):
        return Response('Authentication required', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return render_template('ui.html', user=auth.username)
    

@app.route('/ui/list/', methods=['GET'])
def list_files():
    auth = request.authorization
    if not auth or not verify_user_write(auth.username, auth.password):
        return Response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    user = auth.username
    write_password = auth.password
    read_password = users[user].read_password

    files = []
    user_folder = os.path.join(storage_directory, user)

    for filename in os.listdir(user_folder):
        filepath = os.path.join(user_folder, filename)
        if os.path.isfile(filepath):
            file_size = os.path.getsize(filepath)
            files.append({
                'name': unsanitize_filename(filename),
                'size': file_size,
            })

    return render_template('list.html', files=files, user=user, read_password=read_password, write_password=write_password)

@app.route('/ui/upload/', methods=['GET'])
def upload_file():
    auth = request.authorization
    if not auth or not verify_user_write(auth.username, auth.password):
        return Response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return render_template('upload.html', user=auth.username, write_password=auth.password)

@app.route('/ui/upload_folder/', methods=['GET'])
def upload_folder():
    auth = request.authorization
    if not auth or not verify_user_write(auth.username, auth.password):
        return Response('Invalid credentials', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return render_template('upload_folder.html', user=auth.username, write_password=auth.password)



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
