import _thread
import asyncio
import os
import sys
import time
from datetime import datetime

import WATCHDOG
import config
import utils
import web_client


async def initialization():
    # 清空控制台
    os.system('cls')

    utc_time = datetime.utcnow()
    print(f'Now time: {utc_time.strftime("%Y-%m-%d %H:%M:%S+8:00")}')
    print("哦咪咪~")
    teammates = []
    utils.print_with_time('Initializing...')
    utils.print_with_time('读取Config...')
    config_ = config.load_config()

    if config_:
        connection_number = config_.get('Default', 'connection_number')
        name = config_.get('Default', 'name')
        teammates_count = config_.get('Default', 'teammates')

        utils.print_with_time('Config Found.')
        a = input(f"[{utils.get_time()}] 是否使用上次的配置(y是/n否/t添加队友):")
        if a == 'y' or a == 'Y':
            utils.print_with_time("加载个人信息...")

            utils.print_with_time(f'Name: {name}')
            utils.print_with_time(f'Connection Code: {connection_number}')

            utils.print_with_time("加载可能的队友信息...")
            if teammates_count > "0":
                for i in range(1, int(teammates_count) + 1):
                    try:
                        teammate_connection_number = config_.get(f"Teammate{i}", "connection_number")
                        teammates.append(teammate_connection_number)
                        utils.print_with_time(f"找到 队友{i}: {teammate_connection_number}")
                    except:
                        utils.print_with_time_(f"未找到队友{i}", "ERROR")
                        continue

            if name is None or connection_number is None:
                utils.print_with_time_('读取失败，重新创建配置文件', 'ERROR')
                connection_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
                name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
                config.creat_config(connection_number, name)
        elif a == 't' or a == 'T':
            goon = False
            while goon is False:
                connection_number = input(f'[{utils.get_time()}] 请输入队友ConnectionNumber: ')
                config.add_teammates(connection_number)
                goon = input(f'[{utils.get_time()}] 是否继续添加队友(y是/n否): ') != 'y'
            utils.print_with_time("添加结束，程序将重启...")
            time.sleep(3)
            # 重启
            utils.restart_program()

        else:
            connection_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
            name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
            config.creat_config(connection_number, name)
    else:
        utils.print_with_time('未找到Config，将创建:')
        connection_number = input(f'[{utils.get_time()}] 请输入ConnectionNumber（点击地图左下角的Connect）: ')
        name = input(f'[{utils.get_time()}] 请输入你的昵称（在地图上显示）: ')
        config.creat_config(connection_number, name)

    utils.print_with_time("Initializing WATCHDOG...")
    # 尝试连接服务器 send_coordinates
    utils.print_with_time_(f"Connecting to server -> {web_client.uri}", "Client")
    if await web_client.send_greeting_req(connection_number, name):
        utils.print_with_time("Connected to server.")
    else:
        utils.print_with_time("Error: Failed to connected to server.")
        input("按下Enter退出程序")
        sys.exit()
    # 运行 WATCHDOG
    try:
        _thread.start_new_thread(WATCHDOG.thread_start, (connection_number, name, teammates))
        utils.print_with_time("WATCHDOG started.")
        utils.print_with_time("Hook启动成功，按下Ctrl+C退出程序")
        while True:
            time.sleep(10)
            if WATCHDOG.state == "stop":
                sys.exit()
    except:
        "Error: unable to start thread"


def start():
    asyncio.run(initialization())


if __name__ == '__main__':
    start()
