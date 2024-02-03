import asyncio
import sys
import time
from datetime import datetime

import WATCHDOG
import utils
import web_client
import _thread


async def initialization():
    utc_time = datetime.utcnow()
    print(f'Now time: {utc_time.strftime("%Y-%m-%d %H:%M:%S+8:00")}')

    utils.print_with_time('Initializing...')

    identification_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
    player_name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
    utils.print_with_time("Initializing WATCHDOG...")
    # 尝试连接服务器 send_coordinates
    utils.print_with_time_(f"Connecting to server -> {web_client.uri}", "Client")
    if await web_client.send_greeting_req(identification_number, player_name):
        utils.print_with_time("Connected to server.")
    else:
        utils.print_with_time("Error: Failed to connected to server.")
        input("按下Enter退出程序")
        sys.exit()

    # 运行 WATCHDOG
    try:
        _thread.start_new_thread(WATCHDOG.thread_start, (identification_number, player_name,))
        utils.print_with_time("WATCHDOG started.")
        while True:
            time.sleep(10000)
            if WATCHDOG.state == "stop":
                sys.exit()
    except:
        "Error: unable to start thread"


def start():
    asyncio.run(initialization())


if __name__ == '__main__':
    start()
