import json
import websockets

import WATCHDOG
import utils

uri = "ws://socket.tarkov.lycorecocafe.com"


async def send_proto(api, proto):
    # 发送proto数据到uri

    try:
        async with websockets.connect(api) as websocket:
            await websocket.send(json.dumps(proto))
            # print(f"> {json.dumps(proto)}")

            # greeting = await websocket.recv()
            # print(f"< {greeting}")
            return True
    except websockets.exceptions.InvalidMessage as e:
        utils.print_with_time(f"Failed to connect to WebSocket server: {e}")
        return False
    except Exception as e:
        utils.print_with_time(e)
        return False


async def send_greeting_req(identification_number, player_name):
    api = uri + '/greeting_req'
    # print(api)
    # 发送identification_number到uri/greeting
    proto = {
        "proto_type": "greeting_req",
        "identification_number": identification_number
    }
    if await send_proto(api, proto):
        utils.print_with_time_(f"Hello! {player_name}", "Server")
        return True
    else:
        return False


async def send_player_position_req(identification_number, name, coordinates):
    api = uri + '/'
    date_time, x, y, z, a, b, c, d, time_n, count = coordinates
    proto = {
        "sessionID": identification_number,
        "type": "command",
        "data": {
            "type": "playerPosition",
            "playerPosition": {
                "name": name,
                "date_time": date_time.strftime("%H:%M:%S"),
                "time_n": time_n,
                "position": {
                    "x": x,
                    "y": y,
                    "z": z,
                    "a": a,
                    "b": b,
                    "c": c,
                    "d": d
                }
            }
        }
    }
    if await send_proto(api, proto):
        utils.print_with_time_(f"位置已更新: [{x}, {y}, {z}, {a}, {b}, {c}, {d}]", "Server")
    else:
        utils.print_with_time("位置更新失败[服务器无响应]")
