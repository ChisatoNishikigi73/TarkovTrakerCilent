import os
import re
import sys
from datetime import datetime

import utils


def get_user_folder():
    # 获取用户主文件夹路径
    user_folder = os.path.expanduser("~")
    return user_folder


def print_with_time(content):
    print(f'[{get_time()}] {content}')


def print_with_time_(content, msg):
    print(f'[{get_time()} {msg}] {content}')


def get_time():
    now = datetime.now()
    return now.strftime("%H:%M:%S")


def extract_information(input_string):
    pattern = (r'(\d{4}-\d{2}-\d{2})\[(\d{2}-\d{2})\]_(-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)_(-?\d+\.\d+), '
               r'(-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)_([\d.]+) \((\d+)\)')
    pattern_factory = (r'(\d{4}-\d{2}-\d{2})\[(\d{2}-\d{2})\]_(-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)_(-?\d+\.\d+), '
                       r'(-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+) \((\d+)\)')
    is_factory = False
    match = re.match(pattern, input_string)
    if not match:
        match = re.match(pattern_factory, input_string)
        is_factory = True
    if match:
        groups = match.groups()
        if is_factory:
            date_str, time_str, x, y, z, a, b, c, d, count = groups
            time_n = -1
        else:
            date_str, time_str, x, y, z, a, b, c, d, time_n, count = groups
        # 转换日期和时间字符串为 datetime 对象
        date_time_str = f"{date_str} {time_str}"
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H-%M")
        # 将提取的变量放入一个列表
        extracted_variables = [
            date_time,
            float(x), float(y), float(z),
            float(a), float(b), float(c), float(d),
            float(time_n),
            int(count)
        ]
        # 将提取的变量打印出来
        # print(f"日期和时间: {date_time}")
        # print(f"x: {x}, y: {y}, z: {z}")
        # print(f"a: {a}, b: {b}, c: {c}, d: {d}")
        # print(f"time(n): {time_n}")
        # print(f"count: {count}")
        return extracted_variables
    else:
        utils.print_with_time("未匹配到模式")
        return


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)
