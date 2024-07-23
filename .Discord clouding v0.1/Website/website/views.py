from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_from_directory, send_file, after_this_request, session
from flask_login import login_required, current_user
from .models import Note, File
from . import db
import json
import os
import requests
from threading import *
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
DISCORD_BOT_URL = f"http://{get_ip()}:2121/notify-bot"


QUEUE_FILE_PATH = "queue.json"
DOWNLOAD_QUEUE_FILE_PATH = "download_queue.json"
DONT_DELETE_DICT_PATH = "don't_delete_dict.json"
#ಠ_ಠ
views = Blueprint("views", __name__)



ready_download = {}
with open("ready_download.json", 'w') as f:
    json.dump(ready_download ,f)
download_requests = {}
download_lock = Lock()

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

current_dir = os.path.dirname(__file__)
parent_dir = os.path.join(current_dir, '..', '..')
PATH_TO_FILE_LOG = os.path.join(parent_dir, "Bot", "file_logs")


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        file = request.files['file']
        if not file:
            flash("error, No file selected", category="error")
            return redirect(request.url)

        elif file.filename == '':
            flash("Invalid filename?", category="error")
            return redirect(request.url)
        
        elif file:
            file_name = file.filename
            file_path = os.path.join("uploads", file_name)
            file.save(file_path)
            new_file = File(file_name=file_name, file_path=file_path, user_id=current_user.id)
            db.session.add(new_file)
            db.session.commit()

            with open(QUEUE_FILE_PATH, 'r') as f:
                queue = json.load(f)
            with open(QUEUE_FILE_PATH, 'w') as f:
                queue[f'{file_name}'] = new_file.id
                json.dump(queue, f)
            
            #notify discord bot
            try:
                response = requests.post(DISCORD_BOT_URL, json={'process_queue': True})
                if response.status_code == 222:
                   print("File uploaded and bot notified")
                   flash("File started uploading! Wait for check mark before further operating the file just to be safe.", category="success")
                else:
                   print(f"error code: {response.status_code}")
                   print("file uploaded but bot didn't respond success?")
                   flash("File successfully uploaded!", category="success")
            except requests.exceptions.RequestException as e:
                flash("File uploaded but failed to notify bot... Error: {}".format(e), category="warning")

            return redirect(url_for('views.home'))
        
    return render_template("home.html", user=current_user, files=File.query.filter_by(user_id=current_user.id).all())




@views.route("/delete-file", methods=["POST"])
def delete_file():
    global PATH_TO_FILE_LOG

    file_data = json.loads(request.data)
    file_id = file_data['fileId']
    file = File.query.get(file_id)

    if file:
        if file.user_id == current_user.id:
            path1 = os.path.join(PATH_TO_FILE_LOG, "file_log1.json")
            path2 = os.path.join(PATH_TO_FILE_LOG, "file_log2.json")
            path3 = os.path.join(PATH_TO_FILE_LOG, "file_log3.json")
            with open(path1, 'r') as f:
                file_log1 = json.load(f)
            with open(path2, 'r') as f:
                file_log2 = json.load(f)
            with open(path3, 'r') as f:
                file_log3 = json.load(f)

            id = str(file.id)
            if id in file_log1:
                file_log1.pop(id)
                with open(path1, 'w') as f:
                    json.dump(file_log1, f)
            elif id in file_log2:
                file_log2.pop(id)
                with open(path2, 'w') as f:
                    json.dump(file_log2, f)
            elif id in file_log3:
                file_log3.pop(id)
                with open(path3, 'w') as f:
                    json.dump(file_log3, f)
            else:
                print("couldn't find file XoX")
                return jsonify({})
            
            db.session.delete(file)
            db.session.commit()

    return jsonify({})


@views.route("/download-file/<int:file_id>")
@login_required
def download_file(file_id):
    global DOWNLOAD_QUEUE_FILE_PATH, download_requests
    file = File.query.get(file_id)
    if file and file.user_id == current_user.id:
        file.progress = "downloading..."
        db.session.commit()
        file_name = file.file_name
        with open(DOWNLOAD_QUEUE_FILE_PATH, 'r') as f:
            queue = json.load(f)
        with open(DOWNLOAD_QUEUE_FILE_PATH, 'w') as f:
            queue[file.id] = file_name
            json.dump(queue, f)
        flash("Download process has started, please be patient!", category="info")

        with download_lock:
            download_requests[file_name] = current_user.id
            session['download_file'] = [file_name, file.id]

        try:
            response = requests.post(DISCORD_BOT_URL, json={'process_download_queue': True})
            if response.status_code == 222:
                print("Request for bot to download file locally sent!")
            else:
                print("Failed to notify bot for download")
        except requests.exceptions.RequestException as e:
            flash(f"Failed to notify bot for download. Error: {e}", category="error")

        return redirect(url_for('views.home'))
    else:
        flash("You don't have permission to download this file", category="error")
        return redirect(url_for('views.home'))


@views.route('/check-download')
@login_required
def check_download():
    global ready_download
    file_list = session.get('download_file')
    print("checking file_list: ",file_list)
    print("checking ready_download", ready_download)
    
    if file_list[1] and ready_download.get(str(file_list[1])):
        file_name = file_list[0]
        file_id = str(file_list[1])
        full_path = os.path.abspath(os.path.join("downloads", file_name))
        if os.path.exists(full_path):
            ready_download.pop(file_id)
            file = File.query.get(file_id)
            file.download_ready = 0
            db.session.commit()
            with open("ready_download.json", 'w') as f:
                json.dump(ready_download, f)
            return render_template('download.html', user=current_user, file_path=url_for('views.send_file_route', filename=file_name))
        else:
            flash("Error, file not found", category="error")
            return redirect(url_for('views.home'))
    else:
        flash("File is not ready for download yet", category="info")
        return redirect(url_for('views.home'))


@views.route('/notify-server', methods=['POST'])
def notify_server():
    global ready_download, download_requests
    data = request.get_json()

    if data.get('progress'):#[id, progress]
        lister = data.get('progress') 
        ID = lister[0]
        text = lister[1]
        file = File.query.get(ID)
        if file:
            file.progress = text
            db.session.commit()
            return 'Notification received', 200
        return 'Invalid request', 400

    if data.get('upload_complete'):
        ID = data.get('upload_complete')
        file = File.query.get(ID)
        if file:
            file.upload_ready = 1
            db.session.commit()
            return 'Notification received', 200
        return 'Invalid request', 400

    if data.get('downloaded'):
        file_list = data.get('downloaded')
        print(file_list)
        if file_list[0]:
            print(f"File {file_list[1]} of id: {file_list[0]} is downloaded locally.")
            ready_download[file_list[0]] = file_list[1]
            with open("ready_download.json", 'w') as f:
                json.dump(ready_download, f)
            print(f"download_requests: {download_requests}")
            print(f"ready_download: {ready_download}")
            user_id = download_requests[file_list[1]]
            download_requests.pop(file_list[1])
            if user_id:
                session['download_file'] = file_list

            file = File.query.get(file_list[0])
            if file:
                file.download_ready = 1
                db.session.commit()

            return 'Notification received', 200
        return 'Invalid request', 400

@views.route('/send_file/<filename>')
@login_required
def send_file_route(filename):
    full_path = os.path.abspath(os.path.join("downloads", filename))
    return send_file(full_path, as_attachment=True)


@views.route('/about-me')
def about_me():
    return render_template("about_me.html", user=current_user)

@views.route('/how-to-use')
def how_to_use():
    return render_template("how_to_use.html", user=current_user)

@views.route('/how-to-use-en')
def how_to_use_en():
    return render_template("how_to_use_en.html", user=current_user)

@views.route('/how-to-use-ch')
def how_to_use_ch():
    return render_template("how_to_use_ch.html", user=current_user)

@views.route('/logic')
def logic():
    return render_template("logic.html", user=current_user)
