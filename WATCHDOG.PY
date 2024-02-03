import asyncio
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import utils
import web_client

identification_number = -1
player_name = ""
state = "wait"


def thread_start(identification_number_in, player_name_in):
    global identification_number, player_name
    identification_number = identification_number_in
    player_name = player_name_in
    scr_folder = utils.get_user_folder() + "\\Documents\\Escape from Tarkov\\Screenshots"

    event_handler = WATCHDOG()
    observer = Observer()
    observer.schedule(event_handler, scr_folder, recursive=True)
    observer.start()
    state = "start"

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:  # 按Ctrl+C退出
        observer.stop()

    observer.join()


class WATCHDOG(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        # print(f'文件 {event.src_path} 被创建')
        filename = str(event.src_path).split('Escape from Tarkov\\Screenshots\\')[1].split(".png")[0]

        coordinates = utils.extract_information(filename)
        if coordinates:
            asyncio.run(web_client.send_player_position_req(identification_number, player_name, coordinates))
