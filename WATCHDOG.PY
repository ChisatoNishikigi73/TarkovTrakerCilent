import asyncio
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import utils
import web_client

identification_number = -1
player_name = ""
state = "wait"
teammates = []


def thread_start(identification_number_in, player_name_in, teammates_):
    global identification_number, player_name, teammates, state
    identification_number = identification_number_in
    player_name = player_name_in
    teammates = teammates_
    scr_folder = utils.get_user_folder() + "\\Documents\\Escape from Tarkov\\Screenshots"

    event_handler = WATCHDOG()
    observer = Observer()
    observer.schedule(event_handler, scr_folder, recursive=True)
    observer.start()
    state = "start"

    try:
        while True:
            time.sleep(1)
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
            # 发送自己的信息
            asyncio.run(web_client.send_player_position_req(identification_number, player_name, coordinates))
            # 发送到队友
            teammates_count = len(teammates)
            for i in range(teammates_count):
                asyncio.run(web_client.send_player_position_req(teammates[i], player_name,
                                                                coordinates, False))
