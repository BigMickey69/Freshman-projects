import time
import os
import json
import shutil


DOWNLOAD_FOLDER = 'downloads'

# cleans up downloads folder every 60s! 
def delete_old_files():
    while True:
        time.sleep(60)  
        if not os.path.exists(DOWNLOAD_FOLDER):
            os.makedirs(DOWNLOAD_FOLDER)
        try:
            with open("ready_download.json", "r") as f:
                ready_download = json.load(f)
                
                if ready_download == {}:
                    print(f'[Cleaner] "ready_download" seems empty, cleaning everything >:) ')
                    shutil.rmtree(DOWNLOAD_FOLDER)
                    os.makedirs(DOWNLOAD_FOLDER)

                else:
                    files_in_downloads = os.listdir(DOWNLOAD_FOLDER)
                    print(f"[Cleaner] cleaning items not in {ready_download}")
                    for file_name in files_in_downloads:
                        if file_name not in ready_download.values():
                            file_path = os.path.join(DOWNLOAD_FOLDER, file_name)
                            try:
                                os.remove(file_path)
                                print(f"Removed file {file_path} since it's been downloaded")
                            except Exception as e:
                                print(f"Error removing file QQ: {e}")
        except Exception as e:
            print(f"Error cleaning up download folder >:( == {e}")


