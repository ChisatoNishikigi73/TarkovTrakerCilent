import configparser

import utils


def load_config():
    try:
        config = configparser.ConfigParser()
        config.read('traker.ini')
        if config.sections():
            return config
        else:
            return []
    except:
        return []


def save_config(config):
    with open('traker.ini', 'w') as configfile:
        config.write(configfile)


def creat_config(connection_number, name):
    utils.print_with_time('写入Config...')
    # 创建一个配置解析器对象
    config = configparser.ConfigParser()

    # 添加一个新的部分
    config.add_section("Default")

    # 在特定的部分中设置键值对
    config.set("Default", "connection_number", connection_number)
    config.set("Default", "name", name)
    config.set("Default", "teammates", "0")

    try:
        save_config(config)
        utils.print_with_time('写入成功')
    except:
        utils.print_with_time_('未知错误', 'ERROR')


def add_teammates(connection_number):
    config = load_config()
    if config:
        teammates_count = config.get('Default', 'teammates')
        teammates_count = int(teammates_count) + 1
        config.set("Default", "teammates", str(teammates_count))
        config.add_section(f"Teammate{teammates_count}")
        config.set(f"Teammate{teammates_count}", "connection_number", connection_number)
        save_config(config)
        utils.print_with_time('添加成功')
    else:
        utils.print_with_time_('未找到Config', 'ERROR')
