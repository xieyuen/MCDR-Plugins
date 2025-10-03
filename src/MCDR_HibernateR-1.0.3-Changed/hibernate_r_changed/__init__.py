#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64
import json
import os.path
import socket
import time
import uuid
from typing import Literal as LiteralType

from mcdreforged.api.all import *

import online_player_api as lib_online_player
from .byte_utils import *


def on_load(server: PluginServerInterface, _old_module):
    server.logger.info("插件已加载")
    server.logger.warning("你使用的并非原版！而是 xieyuen 修改版!")
    server.logger.warning("若需要原版，请在下面的网址下载（或者用MPM）")
    server.logger.warning("https://www.mcdreforged.org/plugins/hibernate_r")
    server.logger.warning("或者用 MPM")


# 服务器启动事件
@new_thread
def on_server_startup(server: PluginServerInterface):
    server.logger.info("事件：服务器启动")
    time.sleep(5)
    check_player_num(server)


# 玩家加入事件
@new_thread
def on_player_left(server: PluginServerInterface, _player):
    server.logger.info("事件：玩家退出")
    time.sleep(5)
    check_player_num(server)


# 倒数并关闭服务器
@spam_proof
def check_player_num(server: PluginServerInterface):
    if len(lib_online_player.get_player_list()) == 0:

        check_config_fire(server)
        time.sleep(2)
        with open("config/HibernateR.json", "r") as file:
            config = json.load(file)
        wait_min = config["wait_min"]

        time.sleep(wait_min * 60)
        if len(lib_online_player.get_player_list()) == 0:
            server.logger.info("倒计时结束，关闭服务器")
            server.stop()
            time.sleep(10)

            whether_kill_server = server.is_server_running()
            if whether_kill_server:
                server.logger.warning("服务器似乎卡死了")
                server.logger.info("3s后将会杀死服务端")
                time.sleep(3)
                server.kill()

            fake_server(server)
        else:
            server.logger.info("服务器内仍有玩家")
    else:
        return


# FakeServer部分
class _MotdVersion(Serializable):
    name: str = "Sleeping"
    protocol: int = 2


class _MotdPlayers(Serializable):
    max: int = 10
    online: int = 10
    sample: list = []


class Motd(Serializable):
    version: _MotdVersion
    players: _MotdPlayers


@spam_proof
def fake_server(server: PluginServerInterface):
    check_config_fire(server)
    time.sleep(2)
    with open("config/HibernateR.json", "r") as file:
        config = json.load(file)
    fs_ip = config["ip"]
    fs_port = config["port"]
    fs_samples = config["samples"]
    fs_motd = config["motd"]["1"] + "\n" + config["motd"]["2"]
    fs_icon = None
    fs_kick_message = ""

    for message in config["kick_message"]:
        fs_kick_message += message + "\n"

    if not os.path.exists(config["server_icon"]):
        server.logger.warning("未找到服务器图标，设置为None")
    else:
        with open(config["server_icon"], 'rb') as image:
            fs_icon = "data:image/png;base64," + base64.b64encode(image.read()).decode()

    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            server_socket.bind((fs_ip, fs_port))
        except:
            server.logger.error("伪装服务端启动失败")
            server_socket.close()
            time.sleep(1)
        else:
            server.logger.info("伪装服务端已启动")
            break

    server_socket.listen(5)
    server.logger.info("开始监听端口")
    try:
        while True:
            # server.logger.info("等待连接")
            client_socket, client_address = server_socket.accept()
            try:
                recv_data = client_socket.recv(1024)
                client_ip = client_address[0]
                (length, i) = read_varint(recv_data, 0)
                (packet_id, i) = read_varint(recv_data, i)

                if packet_id == 0:
                    (version, i) = read_varint(recv_data, i)
                    (ip, i) = read_utf(recv_data, i)

                    (port, i) = read_ushort(recv_data, i)
                    (state, i) = read_varint(recv_data, i)
                    if state == 1:
                        server.logger.info("伪装服务器收到了一次ping: %s" % recv_data)
                        motd = Motd.get_default().serialize()

                        for sample in fs_samples:
                            motd["players"]["sample"].append(
                                {"name": sample, "id": str(uuid.uuid4())})

                        motd["description"] = {"text": fs_motd}
                        if fs_icon and len(fs_icon) > 0:
                            motd["favicon"] = fs_icon
                        write_response(client_socket, json.dumps(motd))

                    elif state == 2:
                        server.logger.info("伪装服务器收到了一次连接请求: %s" % recv_data)

                        # TM判断写一大堆，数据发过来一瞅总是少一截，离大谱。
                        # 找这个原因最起码花了我四五个小时
                        # 直接全部删掉，不是ping直接返回、
                        write_response(client_socket, json.dumps({"text": fs_kick_message}))
                        start_server(server)
                        return
                    elif packet_id == 1:
                        (long, i) = read_long(recv_data, i)
                        response = bytearray()
                        write_varint(response, 9)
                        write_varint(response, 1)
                        response.append(long)
                        client_socket.sendall(bytearray)
                        server.logger.info("Responded with pong packet.")
                    else:
                        server.logger.warning("收到了意外的数据包")

            except (TypeError, IndexError):  # 错误处理（类型错误或索引错误）
                server.logger.warning("[%s:%s]收到了无效数据(%s)" % (client_ip, client_address[1], recv_data))
            except Exception as e:
                server.logger.error(e)
    except Exception as ee:
        server.logger.error("发生错误%s" % ee)
        server.logger.info("关闭套接字")
        server_socket.close()


# 启动服务器
def start_server(server: PluginServerInterface):
    server.logger.info("启动服务器")
    server.start()


@new_thread
def check_config_fire(server: PluginServerInterface):
    if os.path.exists("config/HibernateR.json"):
        pass
    else:
        server.logger.warning("未找到配置文件！正在以默认值创建")
        server.logger.info("配置文件已被 xieyuen 改过了！无需再次改动")
        creative_config_fire()
        return


class Config(Serializable):
    wait_min: int = 10
    ip: str = "0.0.0.0"
    port: int = 119
    protocol: int = 2
    samples: list[str] = [
        "服务器正在休眠",
        "进入服务器以唤醒"
    ]
    version_text: str = "§4Sleeping"
    kick_message: list[str] = [
        "§e§l请求成功！",
        "",
        "§f服务器正在启动！请稍作等待后进入"
    ]
    motd: dict[LiteralType[1, 2], str] = {
        "1": "§e服务器正在休眠！",
        "2": "§c进入服务器可将服务器从休眠中唤醒"
    }


def creative_config_fire():
    config = Config.get_default().serialize()

    with open("config/HibernateR.json", "w") as file:
        json.dump(config, file, sort_keys=True, indent=4, ensure_ascii=False)
    return
