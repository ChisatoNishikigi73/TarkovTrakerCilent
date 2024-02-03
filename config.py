import os
import configparser

import utils


def check_config():
    if not os.path.exists("traker"):
        return []
    else:
        # 读取"cfg"文件内容
        with open("traker", "r") as cfg_file:
            cfg_content = cfg_file.read()
            return cfg_content


def creat_config(connection_number, name):
    utils.print_with_time('写入Config...')
    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'connection_number': connection_number,
        'name': name
    }
    try:
        with open('traker', 'w') as configfile:
            config.write(configfile)
        utils.print_with_time('写入成功')
    except:
        utils.print_with_time_('未知错误', 'ERROR')
