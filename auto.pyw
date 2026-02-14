import os
import time
import shutil
from datetime import datetime
import swiftclient
from keystoneauth1.identity import v3
from keystoneauth1 import session

OS_AUTH_URL = os.getenv("OS auth URL")
OS_USERNAME = os.getenv("OS name")
OS_PASSWORD = os.getenv("OS  password")
OS_PROJECT_NAME = os.getenv("OS  project name")
CONTAINER_NAME = "my_first_container"
WATCH_FOLDER = r"C:\Users\Channveerswami H\OneDrive\Desktop\Cloud_Upload"
SENT_FOLDER = os.path.join(WATCH_FOLDER, "Sent")
CHECK_INTERVAL = 240 

def create_swift_connection():
    auth = v3.Password(
        auth_url=OS_AUTH_URL,
        username=OS_USERNAME,
        password=OS_PASSWORD,
        project_name=OS_PROJECT_NAME,
        user_domain_name="default",
        project_domain_name="default",
    )
    sess = session.Session(auth=auth)
    return swiftclient.Connection(session=sess)

def process_pending_files():
    if not os.path.exists(WATCH_FOLDER):
        print(f" error--> watch folder not found: {WATCH_FOLDER}")
        return
    all_items = os.listdir(WATCH_FOLDER)
    files_to_upload = []
    for item in all_items:
        full_path = os.path.join(WATCH_FOLDER, item)
        if os.path.isfile(full_path):
            files_to_upload.append(item)
    if not files_to_upload:
        print(f"[{datetime.now()}] no new files.")
        return
    print(f"[{datetime.now()}] {len(files_to_upload)} file's detected, connecting to OpenStack...")

    try:
        connection = create_swift_connection()
        connection.put_container(CONTAINER_NAME)
        if not os.path.exists(SENT_FOLDER):
            os.makedirs(SENT_FOLDER)
        for filename in files_to_upload:
            file_path = os.path.join(WATCH_FOLDER, filename)
            print(f"Uploading >>> {filename}")
            with open(file_path, "rb") as file_data:
                connection.put_object(
                    CONTAINER_NAME,
                    filename,
                    contents=file_data.read()
                )
            shutil.move(file_path, os.path.join(SENT_FOLDER, filename))
            print(f"Completed -> {filename}")
        print("sync cycle complete.\n")
    except Exception as error:
        print(f"error -> Something went wrong: {error}")
if __name__ == "__main__":
    print(f"watching folder: {WATCH_FOLDER}")
    print("press ctrl + c to stop.\n")
    while True:
        process_pending_files()
        time.sleep(CHECK_INTERVAL)
