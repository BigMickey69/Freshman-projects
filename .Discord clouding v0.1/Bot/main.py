import os
import discord as dc
from typing import Final
from responses import get_response
from dotenv import load_dotenv
from flask import Flask, request
import threading
import json
import aiofiles
import requests
import shutil
from convert_to_chunks import *
from chunks_to_file import *
import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


QUEUE_PATH = os.path.join("Website", "queue.json")
DL_QUEUE_PATH = os.path.join("Website", "download_queue.json")
DOWNLOAD_QUEUE_PATH = os.path.join("Website", "download_queue.json")

NOTI_SERVER_URL = f"http://{get_ip()}:1212/notify-server"


# 3 channels with 3 respective file_logs
CHANNELS = [1259495507663782040, 1259495540111048724, 1259495563553149038]


file_log1 = {}
file_log2 = {}
file_log3 = {}
def refresh_file_logs():
    global file_log1, file_log2, file_log3
    path1 = os.path.join("Bot","file_logs", "file_log1.json")
    path2 = os.path.join("Bot","file_logs", "file_log2.json")
    path3 = os.path.join("Bot","file_logs", "file_log3.json")
    with open(path1, 'r') as f:
        file_log1 = json.load(f)
    with open(path2, 'r') as f:
        file_log2 = json.load(f)
    with open(path3, 'r') as f:
        file_log3 = json.load(f)

CURRENT_FILE_LOG = "file_log1.json"
PATH_TO_TEMP_UP = os.path.join("temp_upload")
PATH_TO_CHUNK_FOLDER = os.path.join("temp_download")


CURRENT_CHANNEL_ID = 1259495507663782040
NOTIFICATION_CHANNEL_ID = 1259495079127810059
queue = {}
download_queue = {}
remove_queue={}

load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents: dc.Intents = dc.Intents.default()
intents.message_content = True # NQQA
client: dc.Client = dc.Client(intents=intents)



app = Flask(__name__)



@app.route('/notify-bot', methods=['POST'])
def notify_upload():
    global QUEUE_PATH,DOWNLOAD_QUEUE_PATH,queue,download_queue
    data = request.get_json()

    if data.get('process_queue'):
        try:
            with open(QUEUE_PATH, 'r') as f:
                queue = json.load(f)
            client.loop.create_task(process_queue())
            return 'Upload notification received', 222
        except Exception as e:
            print("[Jose] Error processing upload notification:", e)
            return 'Error processing upload notification', 500
    
    elif data.get('process_download_queue'):
        try:
            with open(DOWNLOAD_QUEUE_PATH, 'r') as f:
                download_queue = json.load(f)
            client.loop.create_task(process_download_queue())
            return 'Download notification received', 222
        except Exception as e:
            print("[Jose] Error processing download_queue:", e)
            return 'Error processing download notification', 500
    
    return 'Invalid request', 400

async def notify_server_downloaded(id, file_name):
    try:
        response = requests.post(NOTI_SERVER_URL, json={'downloaded': [id, file_name]})
        if response.status_code == 200:
            print(f"[Jose] Notified server of downloaded file: {file_name}")
        else:
            print(f"[Jose] Failed to notify server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[Jose] Error notifying server: {e}")

async def download_from_message_id(id_list, id):
    global CURRENT_CHANNEL_ID, remove_queue
    channel = client.get_channel(CURRENT_CHANNEL_ID)
    noti_channel = client.get_channel(NOTIFICATION_CHANNEL_ID)
    mother_file_name = id_list[0]
    id_list.pop(0)
    total_chunk_num = len(id_list)
    try:
        num = 1
        for message_ID in id_list:
            message = await channel.fetch_message(message_ID)
            if message.attachments:
                attachment = message.attachments[0]
                file_name = attachment.filename
                path = os.path.join("temp_download",mother_file_name, file_name)
                os.makedirs(os.path.join(PATH_TO_CHUNK_FOLDER, mother_file_name), exist_ok=True)
                print(f"[Jose] Downloading {file_name}...")
                await notify_server_progress(id, f"{num}/{total_chunk_num}")
                num += 1
                await attachment.save(path)
            else:
                print("[Jose] Failed to find attachment with message")
        output_path = os.path.join("Website", "downloads", mother_file_name)
        reassemble_file(output_path, PATH_TO_CHUNK_FOLDER, mother_file_name)
        
        shutil.rmtree(PATH_TO_CHUNK_FOLDER)
        await notify_server_progress(id, "")
        await notify_server_downloaded(id, mother_file_name)
        await noti_channel.send(f"Downloaded file on local: {mother_file_name} of id: {id}")
        remove_queue[id] = None

    except dc.NotFound:
        print("[Jose] Can't find message")
    except dc.HTTPException as e:
        await channel.send(f"[Jose] Failed to fetch message: {e}")


async def process_download_queue():
    global download_queue, remove_queue, QUEUE_PATH, DOWNLOAD_QUEUE_PATH, CURRENT_CHANNEL_ID, file_log1,file_log2,file_log3
    with open(DOWNLOAD_QUEUE_PATH, 'r') as f:
        download_queue = json.load(f)
    refresh_file_logs()
    if download_queue:
        for id in list(download_queue):
            if id in file_log1:
                file_log = file_log1
            elif id in file_log2:
                file_log = file_log2
            elif id in file_log1:
                file_log = file_log3
            else: 
                print("[Jose] Can't find file in file_logs...")
                break


            await download_from_message_id(file_log[id], id)
            
            for i in remove_queue:
                download_queue.pop(i)
            remove_queue = {}
        with open(DOWNLOAD_QUEUE_PATH, 'w') as f:
            json.dump(download_queue, f)

async def process_queue():
    global queue, QUEUE_PATH, CURRENT_CHANNEL_ID, CURRENT_FILE_LOG

    if queue:
        LOG_PATH = os.path.join("Bot","file_logs", CURRENT_FILE_LOG)
        try:
            with open(LOG_PATH, 'r') as f:
                file_log = json.load(f)
        except FileNotFoundError:
            file_log = {}

        for file_name in queue:
            file_path = os.path.join("Website", "uploads", file_name)
            ID = queue[file_name]
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        total_chunk_num = write_file_in_chunks(f, PATH_TO_TEMP_UP, file_name, file_path)

                    channel = client.get_channel(CURRENT_CHANNEL_ID)
                    message_ids = []

                    pather = os.path.join(PATH_TO_TEMP_UP, file_name)
                    for chunk_name in sorted(os.listdir(pather)):
                        num = int(chunk_name[:-5])
                        chunk_path = os.path.join(pather, chunk_name)
                        print(f"[Jose] Looking at {chunk_path}")
                        await notify_server_progress(ID, f"{num}/{total_chunk_num}")
                        with open(chunk_path, 'rb') as f:
                            message_sent = await channel.send("", file = dc.File(f, f"{file_name}#{num}"))
                            message_ids.append(message_sent.id)

                    
                    message_ids.insert(0, file_name)
                    file_log[queue[file_name]] = message_ids

                    with open(LOG_PATH, 'w') as f:
                        json.dump(file_log, f)

                    await notify_server_progress(ID, "")
                    print(f"[Jose] current file_log is {file_log}")
                    
                    await notify_server_uploaded(queue[file_name], file_name)

                except Exception as e:
                    print(f"[Jose] Error uploading file: {e}")
                finally:
                    pass
                try:
                    os.remove(file_path)  
                    shutil.rmtree(pather)
                    print(f"[Jose] Removed file: {file_name}, id = {queue[file_name]}")
                except Exception as e:
                    print(f"[Jose] Error removing file: {e}")  
                        
            else:
                print(f"[Jose] file={file_name} of id={queue[file_name]} not found?")
        print("[Jose] files in queue uploaded, clearing queue.json...")            
        queue = {}
        async with aiofiles.open(QUEUE_PATH, 'w') as f:
            await f.write(json.dumps(queue))
        print("[Jose] Complete!")    


async def notify_server_uploaded(id, file_name):
    try:
        response = requests.post(NOTI_SERVER_URL, json={'upload_complete': id})
        if response.status_code == 200:
            print(f"[Jose] Notified server of downloaded file: {file_name}")
        else:
            print(f"[Jose] Failed to notify server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[Jose] Error notifying server: {e}")

async def notify_server_progress(ID, text:str):
    try:
        response = requests.post(NOTI_SERVER_URL, json={'progress': [ID, text]})
        if response.status_code == 200:
            pass
        else:
            print(f"[Jose] Failed to notify progress to server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[Jose] Error notifying server: {e}")

async def send_message(message: dc.Message, user_message: str) -> None:
    if not user_message:
        print("[Jose] Unable to read message or empty")
        return
    
    if user_message[0] == '?': 
        is_private = True
    else: is_private = False

    if is_private:
        user_message = user_message[1:]

    try:
        respose: str = get_response(user_message)
        if is_private:
            sent_message = await message.author.send(respose)
            await message.channel.send("Sent private message!")
        else:
            sent_message = await message.channel.send(respose)

    except Exception as e:
        print(e)

#start up!
@client.event
async def on_ready() -> None:
    print(f"{client.user}  is now running!")
    print("[Jose] Hello! I am now online.")
    noti_channel = client.get_channel(NOTIFICATION_CHANNEL_ID)
    await noti_channel.send(f"Hello! I am now online.")




#handling incoming messages
@client.event
async def on_message(message: dc.Message) -> None:
    if message.author == client.user:
        return
    

    if message.content.startswith('!dog') :
        dog_path = os.path.join("Bot", "doggo coding.gif")
        if os.path.exists(dog_path):
            with open(dog_path, 'rb') as f:
                await message.channel.send("", file = dc.File(f, "doggo coding.gif"))
        else:
            await message.channel.send("Doggo not found!!! QQ")
    else:
        username: str = str(message.author)
        user_message: str = str(message.content)
        channel: str = str(message.channel)
        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message)


def run_flask():
    app.run(host='0.0.0.0', debug=False, port=2121)



def main() -> None:
    threading.Thread(target=run_flask).start()
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()




