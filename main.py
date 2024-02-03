import asyncio
import re
import sys
import time
from datetime import datetime

import WATCHDOG
import config
import utils
import web_client
import _thread
import configparser


async def initialization():
    identification_number = None
    player_name = None
    utc_time = datetime.utcnow()
    print(f'Now time: {utc_time.strftime("%Y-%m-%d %H:%M:%S+8:00")}')

    utils.print_with_time('Initializing...')
    utils.print_with_time('读取Config...')
    config_ = config.check_config()

    if config_:
        utils.print_with_time('Config Found.')
        a = input(f"[{utils.get_time()}] 是否使用上次的配置(y/n):")
        if a == 'y' or a == 'Y':
            # 使用正则表达式提取特定配置项的值
            connection_number_match = re.search(r'connection_number = (.*)', config_)
            name_match = re.search(r'name = (.*)', config_)

            # 获取匹配到的值
            identification_number = connection_number_match.group(1) if connection_number_match else None
            player_name = name_match.group(1) if name_match else None

            if player_name is None or identification_number is None:
                utils.print_with_time_('读取失败，重新创建配置文件', 'ERROR')
                identification_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
                player_name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
        else:
            identification_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
            player_name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
            config.creat_config(identification_number, player_name)
    else:
        utils.print_with_time('未找到Config，将创建:')
        identification_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
        player_name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
        config.creat_config(identification_number, player_name)

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
