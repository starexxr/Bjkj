import requests, os, psutil, sys, jwt, pickle, json, binascii, time, urllib3, base64 , datetime , re , socket , threading , ssl , pytz , aiohttp
from protobuf import DEcwHisPErMsG_pb2 , MajoRLoGinrEs_pb2 , PorTs_pb2 , MajoRLoGinrEq_pb2 , sQ_pb2 , Team_msg_pb2
from utils.conf import GUEST_UID_MAIN, GUEST_PASS_MAIN
from protobuf_decoder.protobuf_decoder import Parser
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from Crypto.Util.Padding import pad, unpad
from flask import Flask, jsonify, request
from Crypto.Cipher import AES
from utils.cipher import *
from utils.headers import *
from utils import proxy
from datetime import datetime
from threading import Thread
from cfonts import render, say
import asyncio
import signal
import sys
import re
import random


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

online_writer = None
whisper_writer = None
spam_room = False
spammer_uid = None
spam_chat_id = None
spam_uid = None
Spy = False
Chat_Leave = False
fast_spam_running = False
fast_spam_task = None
custom_spam_running = False
custom_spam_task = None
spam_request_running = False
spam_request_task = None
evo_fast_spam_running = False
evo_fast_spam_task = None
evo_custom_spam_running = False
evo_custom_spam_task = None
reject_spam_running = False
insquad = None
joining_team = False
reject_spam_task = None
lag_running = False
lag_task = None
reject_spam_running = False
reject_spam_task = None
evo_cycle_running = False
evo_cycle_task = None
auto_start_running = False
auto_start_teamcode = None
stop_auto = False
auto_start_task = None
start_spam_duration = 18
wait_after_match = 20
start_spam_delay = 0.2

evo_emotes={"1":"909000063","2":"909000068","3":"909000075","4":"909040010","5":"909000081","6":"909039011","7":"909000085","8":"909000090","9":"909000098","10":"909035007","11":"909042008","12":"909041005","13":"909033001","14":"909038010","15":"909038012","16":"909045001","17":"909049010","18":"909051003"}
EMOTE_MAP={1:909000063,2:909000081,3:909000075,4:909000085,5:909000134,6:909000098,7:909035007,8:909051012,9:909000141,10:909034008,11:909051015,12:909041002,13:909039004,14:909042008,15:909051014,16:909039012,17:909040010,18:909035010,19:909041005,20:909051003,21:909034001}
BADGE_VALUES={"s1":1048576,"s2":32768,"s3":2048,"s4":64,"s5":262144}

def start_insta_api():
    port = proxy.find_free_port()
    print(f"Starting insta api on port {port}")
    proxy.app.run(host="0.0.0.0", port=port, debug=False)

def dec_to_hex(decimal):
    hex_str = hex(decimal)[2:]
    return hex_str.upper() if len(hex_str) % 2 == 0 else '0' + hex_str.upper()

async def encrypt_packet(packet_hex, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    packet_bytes = bytes.fromhex(packet_hex)
    padded_packet = pad(packet_bytes, AES.block_size)
    encrypted = cipher.encrypt(padded_packet)
    return encrypted.hex()

async def nmnmmmmn(packet_hex, key, iv):
    return await encrypt_packet(packet_hex, key, iv)

def get_idroom_by_idplayer(packet_hex):
    try:
        json_result = get_available_room(packet_hex)
        parsed_data = json.loads(json_result)
        json_data = parsed_data["5"]["data"]
        data = json_data["1"]["data"]
        idroom = data['15']["data"]
        return idroom
    except Exception as e:
        print(f"Error extracting room ID: {e}")
        return None

async def check_player_in_room(target_uid, key, iv):
    try:
        status_packet = await GeT_Status(int(target_uid), key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', status_packet)
        return True
    except Exception as e:
        print(f"Error checking player room status: {e}")
        return False

class MultiAccountManager:
    def __init__(self):
        self.accounts_file = "utils/main.json"
        self.accounts_data = self.load_accounts()

    def load_accounts(self):
        try:
            with open(self.accounts_file, "r", encoding="utf-8") as f:
                accounts = json.load(f)
                return accounts
        except FileNotFoundError:
            print(f"Accounts file {self.accounts_file} not found!")
            return {}
        except Exception as e:
            print(f"Error loading accounts: {e}")
            return {}

    async def get_account_token(self, uid, password):
        try:
            url = "https://100067.connect.garena.com/oauth/guest/token/grant"
            headers = {
                "Host": "100067.connect.garena.com",
                "User-Agent": await Ua(),
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "close"
            }
            data = {
                "uid": uid,
                "password": password,
                "response_type": "token",
                "client_type": "2",
                "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
                "client_id": "100067"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, data=data) as response:
                    if response.status == 200:
                        data = await response.json()
                        open_id = data.get("open_id")
                        access_token = data.get("access_token")
                        return open_id, access_token
            return None, None
        except Exception as e:
            print(f"Error getting token for {uid}: {e}")
            return None, None

    async def send_join_from_account(self, target_uid, account_uid, password, key, iv, region):
        try:
            open_id, access_token = await self.get_account_token(account_uid, password)
            if not open_id or not access_token:
                return False
            join_packet = await self.create_account_join_packet(target_uid, account_uid, open_id, access_token, key, iv, region)
            if join_packet:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                return True
            return False
        except Exception as e:
            print(f"Error sending join from {account_uid}: {e}")
            return False

async def SEnd_InV_with_Cosmetics(Nu, Uid, K, V, region):
    region = "ind"
    fields = {
        1: 2,
        2: {
            1: int(Uid),
            2: region,
            4: int(Nu),
            5: {
                1: "BOT",
                2: int(await get_random_avatar()),
                5: random.choice([1048576, 32768, 2048]),
            }
        }
    }

    if region.lower() == "ind":
        packet = '0514'
    elif region.lower() == "bd":
        packet = "0519"
    else:
        packet = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet, K, V)

async def join_custom_room(room_id, room_password, key, iv, region):
    fields = {
        1: 61,
        2: {
            1: int(room_id),
            2: {
                1: int(room_id),
                2: int(time.time()),
                3: "BOT",
                5: 12,
                6: 9999999,
                7: 1,
                8: {
                    2: 1,
                    3: 1,
                },
                9: 3,
            },
            3: str(room_password),
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)

async def RedZed_SendInv(bot_uid, uid, key, iv):
    try:
        fields = {
            1: 33,
            2: {
                1: int(uid),
                2: "IND",
                3: 1,
                4: 1,
                6: "RedZedKing!!",
                7: 330,
                8: 1000,
                9: 100,
                10: "DZ",
                12: 1,
                13: int(uid),
                16: 1,
                17: {
                    2: 159,
                    4: "y[WW",
                    6: 11,
                    8: "1.118.1",
                    9: 3,
                    10: 1
                },
                18: 306,
                19: 18,
                24: 902000306,
                26: {},
                27: {
                    1: 11,
                    2: int(bot_uid),
                    3: 99999999999
                },
                28: {},
                31: {
                    1: 1,
                    2: 32768
                },
                32: 32768,
                34: {
                    1: bot_uid,
                    2: 8,
                    3: b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
                }
            }
        }
        if isinstance(fields[2][34][3], str):
            fields[2][34][3] = b"\x10\x15\x08\x0A\x0B\x13\x0C\x0F\x11\x04\x07\x02\x03\x0D\x0E\x12\x01\x05\x06"
        packet = await CrEaTe_ProTo(fields)
        packet_hex = packet.hex()
        final_packet = await GeneRaTePk(packet_hex, '0515', key, iv)
        return final_packet
    except Exception as e:
        print(f"Error in RedZed_SendInv: {e}")
        import traceback
        traceback.print_exc()
        return None

async def request_join_with_badge(target_uid, badge_value, key, iv, region):
    fields = {
        1: 33,
        2: {
            1: int(target_uid),
            2: region.upper(),
            3: 1,
            4: 1,
            5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
            6: "iG:[C][B][FF0000] KRISHNA",
            7: 330,
            8: 1000,
            10: region.upper(),
            11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                       97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
            12: 1,
            13: int(target_uid),
            14: {
                1: 2203434355,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            16: 1,
            17: 1,
            18: 312,
            19: 46,
            23: bytes([16, 1, 24, 1]),
            24: int(await get_random_avatar()),
            26: "",
            28: "",
            31: {
                1: 1,
                2: badge_value
            },
            32: badge_value,
            34: {
                1: int(target_uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        },
        10: "en",
        13: {
            2: 1,
            3: 1
        }
    }
    packet = (await CrEaTe_ProTo(fields)).hex()
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk(packet, packet_type, key, iv)

async def start_auto_packet(key, iv, region):
    fields = {
        1: 9,
        2: {
            1: 12480598706,
        },
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def leave_squad_packet(key, iv, region):
    fields = {
        1: 7,
        2: {
            1: 12480598706,
        },
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def join_teamcode_packet(team_code, key, iv, region):
    fields = {
        1: 4,
        2: {
            4: bytes.fromhex("01090a0b121920"),
            5: str(team_code),
            6: 6,
            8: 1,
            9: {
                2: 800,
                6: 11,
                8: "1.111.1",
                9: 5,
                10: 1
            }
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def auto_start_loop(team_code, uid, chat_id, chat_type, key, iv, region):
    global auto_start_running, stop_auto
    print(f"Auto start loop started for team {team_code}")
    while not stop_auto:
        try:
            status_msg = f"[B][C][FFA500]Auto Start Bot\nTeam: {team_code}\nJoining team"
            await safe_send_message(chat_type, status_msg, uid, chat_id, key, iv)
            join_packet = await join_teamcode_packet(team_code, key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(2)
            start_msg = f"[B][C]{get_random_color()}Joined team {team_code}\nStarting match for {start_spam_duration} seconds"
            await safe_send_message(chat_type, start_msg, uid, chat_id, key, iv)
            start_packet = await start_auto_packet(key, iv, region)
            end_time = time.time() + start_spam_duration
            spam_count = 0
            while time.time() < end_time and not stop_auto:
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', start_packet)
                spam_count += 1
                await asyncio.sleep(start_spam_delay)
            if stop_auto:
                break
            wait_msg = f"[B][C][FFFF00]Match started! Bot in lobby waiting {wait_after_match} seconds"
            await safe_send_message(chat_type, wait_msg, uid, chat_id, key, iv)
            waited = 0
            while waited < wait_after_match and not stop_auto:
                await asyncio.sleep(1)
                waited += 1
            if stop_auto:
                break
            leave_msg = f"[B][C][FF0000]Leaving team {team_code} to rejoin and start again"
            await safe_send_message(chat_type, leave_msg, uid, chat_id, key, iv)
            leave_packet = await leave_squad_packet(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Error in auto_start_loop: {e}")
            error_msg = f"[B][C][FF0000]Auto start error: {str(e)}"
            await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
            break
    auto_start_running = False
    stop_auto = False
    print(f"Auto start loop stopped for team {team_code}")

async def reset_bot_state(key, iv, region):
    try:
        leave_packet = await leave_squad(key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        await asyncio.sleep(0.5)
        print("Bot state reset - left squad")
        return True
    except Exception as e:
        print(f"Error resetting bot: {e}")
        return False

async def create_custom_room(room_name, room_password, max_players, key, iv, region):
    fields = {
        1: 3,
        2: {
            1: room_name,
            2: room_password,
            3: max_players,
            4: 1,
            5: 1,
            6: "en",
            7: {
                1: "BotHost",
                2: int(await get_random_avatar()),
                3: 330,
                4: 1048576,
                5: "BOTCLAN"
            }
        }
    }
    if region.lower() == "ind":
        packet_type = '0514'
    elif region.lower() == "bd":
        packet_type = "0519"
    else:
        packet_type = "0515"
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), packet_type, key, iv)

async def real_multi_account_join(target_uid, key, iv, region):
    try:
        accounts_data = load_accounts()
        if not accounts_data:
            return 0, 0
        success_count = 0
        total_accounts = len(accounts_data)
        for account_uid, password in accounts_data.items():
            try:
                print(f"Authenticating account: {account_uid}")
                open_id, access_token = await GeNeRaTeAccEss(account_uid, password)
                if not open_id or not access_token:
                    print(f"Failed to authenticate {account_uid}")
                    continue
                join_packet = await create_authenticated_join(target_uid, account_uid, key, iv, region)
                if join_packet:
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                    success_count += 1
                    print(f"Join sent from authenticated account: {account_uid}")
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Error with account {account_uid}: {e}")
                continue
        return success_count, total_accounts
    except Exception as e:
        print(f"Multi-account join error: {e}")
        return 0, 0

async def handle_badge_command(cmd, inPuTMsG, uid, chat_id, key, iv, region, chat_type):
    parts = inPuTMsG.strip().split()
    if len(parts) < 2:
        error_msg = f"[B][C][FF0000]Usage: /{cmd} (uid)\nExample: /{cmd} 123456789"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    target_uid = parts[1]
    badge_value = BADGE_VALUES.get(cmd, 1048576)
    if not target_uid.isdigit():
        error_msg = f"[B][C][FF0000]Please write a valid player ID!"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)
        return
    initial_msg = f"[B][C][1E90FF]Request received! Preparing to spam {target_uid}"
    await safe_send_message(chat_type, initial_msg, uid, chat_id, key, iv)
    try:
        await reset_bot_state(key, iv, region)
        join_packet = await request_join_with_badge(target_uid, badge_value, key, iv, region)
        spam_count = 3
        for i in range(spam_count):
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            print(f"Sent /{cmd} request #{i+1} with badge {badge_value}")
            await asyncio.sleep(0.1)
        success_msg = f"[B][C]{get_random_color()}Successfully Sent {spam_count} Join Requests!\nTarget: {target_uid}\nBadge: {badge_value}"
        await safe_send_message(chat_type, success_msg, uid, chat_id, key, iv)
        await asyncio.sleep(1)
        await reset_bot_state(key, iv, region)
    except Exception as e:
        error_msg = f"[B][C][FF0000]Error in /{cmd}: {str(e)}"
        await safe_send_message(chat_type, error_msg, uid, chat_id, key, iv)

async def create_authenticated_join(target_uid, account_uid, key, iv, region):
    try:
        join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
        return join_packet
    except Exception as e:
        print(f"Error creating join packet: {e}")
        return None

    async def create_account_join_packet(self, target_uid, account_uid, open_id, access_token, key, iv, region):
        try:
            fields = {
                1: 33,
                2: {
                    1: int(target_uid),
                    2: region.upper(),
                    3: 1,
                    4: 1,
                    5: bytes([1, 7, 9, 10, 11, 18, 25, 26, 32]),
                    6: f"BOT:[C][B][FF0000] ACCOUNT_{account_uid[-4:]}",
                    7: 330,
                    8: 1000,
                    10: region.upper(),
                    11: bytes([49, 97, 99, 52, 98, 56, 48, 101, 99, 102, 48, 52, 55, 56,
                               97, 52, 52, 50, 48, 51, 98, 102, 56, 102, 97, 99, 54, 49, 50, 48, 102, 53]),
                    12: 1,
                    13: int(account_uid),
                    14: {
                        1: 2203434355,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    },
                    16: 1,
                    17: 1,
                    18: 312,
                    19: 46,
                    23: bytes([16, 1, 24, 1]),
                    24: int(await get_random_avatar()),
                    26: "",
                    28: "",
                    31: {
                        1: 1,
                        2: 32768
                    },
                    32: 32768,
                    34: {
                        1: int(account_uid),
                        2: 8,
                        3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
                    }
                },
                10: "en",
                13: {
                    2: 1,
                    3: 1
                }
            }
            packet = (await CrEaTe_ProTo(fields)).hex()
            if region.lower() == "ind":
                packet_type = '0514'
            elif region.lower() == "bd":
                packet_type = "0519"
            else:
                packet_type = "0515"
            return await GeneRaTePk(packet, packet_type, key, iv)
        except Exception as e:
            print(f"Error creating join packet for {account_uid}: {e}")
            return None

multi_account_manager = MultiAccountManager()

async def auto_rings_emote_dual(sender_uid, key, iv, region):
    try:
        rings_emote_id = 909050009
        bot_uid = 13877859382
        emote_to_sender = await Emote_k(int(sender_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
        await asyncio.sleep(0.5)
        emote_to_bot = await Emote_k(int(bot_uid), rings_emote_id, key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_bot)
        print(f"Bot performed dual Rings emote with sender {sender_uid} and bot {bot_uid}!")
    except Exception as e:
        print(f"Error sending dual rings emote: {e}")

async def Room_Spam(Uid, Rm, Nm, K, V):
    same_value = random.choice([32768])
    fields = {
        1: 78,
        2: {
            1: int(Rm),
            2: "iG:[C][B][FF0000] realstarexx",
            3: {
                2: 1,
                3: 1
            },
            4: 330,
            5: 6000,
            6: 201,
            10: int(await get_random_avatar()),
            11: int(Uid),
            12: 1,
            15: {
                1: 1,
                2: same_value
            },
            16: same_value,
            18: {
                1: 11481904755,
                2: 8,
                3: "\u0010\u0015\b\n\u000b\u0013\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
            },
            31: {
                1: 1,
                2: same_value
            },
            32: same_value,
            34: {
                1: int(Uid),
                2: 8,
                3: bytes([15,6,21,8,10,11,19,12,17,4,14,20,7,2,1,5,16,3,13,18])
            }
        }
    }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex(), '0e15', K, V)

async def evo_cycle_spam(uids, key, iv, region):
    global evo_cycle_running
    cycle_count = 0
    while evo_cycle_running:
        cycle_count += 1
        print(f"Starting evolution emote cycle #{cycle_count}")
        for emote_number, emote_id in evo_emotes.items():
            if not evo_cycle_running:
                break
            print(f"Sending evolution emote {emote_number} (ID: {emote_id})")
            for uid in uids:
                try:
                    uid_int = int(uid)
                    H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                    print(f"Sent emote {emote_number} to UID: {uid}")
                except Exception as e:
                    print(f"Error sending evo emote {emote_number} to {uid}: {e}")
            if evo_cycle_running:
                print(f"Waiting 5 seconds before next emote")
                for i in range(5):
                    if not evo_cycle_running:
                        break
                    await asyncio.sleep(1)
        if evo_cycle_running:
            print("Completed one full cycle of all evolution emotes. Restarting")
            await asyncio.sleep(2)
    print("Evolution emote cycle stopped")

async def reject_spam_loop(target_uid, key, iv):
    global reject_spam_running
    count = 0
    max_spam = 150
    while reject_spam_running and count < max_spam:
        try:
            packet1 = await banecipher1(target_uid, key, iv)
            packet2 = await banecipher(target_uid, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet1)
            await asyncio.sleep(0.1)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', packet2)
            count += 1
            print(f"Sent reject spam #{count} to {target_uid}")
            await asyncio.sleep(0.2)
        except Exception as e:
            print(f"Error in reject spam: {e}")
            break
    return count

async def handle_reject_completion(spam_task, target_uid, sender_uid, chat_id, chat_type, key, iv):
    try:
        spam_count = await spam_task
        if spam_count >= 150:
            completion_msg = f"[B][C]{get_random_color()}Reject Spam Completed Successfully for ID {target_uid}\nTotal packets sent: {spam_count * 2}"
        else:
            completion_msg = f"[B][C][FFFF00]Reject Spam Partially Completed for ID {target_uid}\nTotal packets sent: {spam_count * 2}"
        await safe_send_message(chat_type, completion_msg, sender_uid, chat_id, key, iv)
    except asyncio.CancelledError:
        print("Reject spam was cancelled")
    except Exception as e:
        error_msg = f"[B][C][FF0000]ERROR in reject spam: {str(e)}"
        await safe_send_message(chat_type, error_msg, sender_uid, chat_id, key, iv)

async def banecipher(client_id, key, iv):
    banner_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
"""
    fields = {
        1: 5,
        2: {
            1: int(client_id),
            2: 1,
            3: int(client_id),
            4: banner_text
        }
    }
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)

async def banecipher1(client_id, key, iv):
    gay_text = f"""
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
[b][000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███[000000]███
"""
    fields = {
        1: int(client_id),
        2: 5,
        4: 50,
        5: {
            1: int(client_id),
            2: gay_text,
        }
    }
    packet = await CrEaTe_ProTo(fields)
    packet_hex = packet.hex()
    encrypted_packet = await EnC_PacKeT(packet_hex, key, iv)
    header_length = len(encrypted_packet) // 2
    header_length_final = await DecodE_HeX(header_length)
    if len(header_length_final) == 2:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 3:
        final_packet = "051500000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 4:
        final_packet = "05150000" + header_length_final + encrypted_packet
    elif len(header_length_final) == 5:
        final_packet = "0515000" + header_length_final + encrypted_packet
    else:
        final_packet = "0515000000" + header_length_final + encrypted_packet
    return bytes.fromhex(final_packet)

async def lag_team_loop(team_code, key, iv, region):
    global lag_running
    count = 0
    while lag_running:
        try:
            join_packet = await GenJoinSquadsPacket(team_code, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
            await asyncio.sleep(0.01)
            leave_packet = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
            count += 1
            print(f"Lag cycle #{count} completed for team: {team_code}")
            await asyncio.sleep(0.01)
        except Exception as e:
            print(f"Error in lag loop: {e}")
            await asyncio.sleep(0.1)

def Get_clan_info(clan_id):
    try:
        url = f"https://get-clan-info.vercel.app/get_clan_info?clan_id={clan_id}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            msg = f"""[B][C]
Achievements: {data['achievements']}
Balance : {fix_num(data['balance'])}
Clan Name : {data['clan_name']}
Expire Time : {fix_num(data['guild_details']['expire_time'])}
Members Online : {fix_num(data['guild_details']['members_online'])}
Regional : {data['guild_details']['regional']}
Reward Time : {fix_num(data['guild_details']['reward_time'])}
Total Members : {fix_num(data['guild_details']['total_members'])}
ID : {fix_num(data['id'])}
Last Active : {fix_num(data['last_active'])}
Level : {fix_num(data['level'])}
Rank : {fix_num(data['rank'])}
Region : {data['region']}
Score : {fix_num(data['score'])}
Timestamp1 : {fix_num(data['timestamp1'])}
Timestamp2 : {fix_num(data['timestamp2'])}
Welcome Message: {data['welcome_message']}
XP: {fix_num(data['xp'])}
"""
            return msg
        else:
            msg = """
[C][B]Failed to get info, please try again later!!
"""
            return msg
    except:
        pass

def get_player_info(player_id):
    url = f"https://like2.vercel.app/player-info?uid={player_id}&server={server2}&key={key2}"
    response = requests.get(url)
    print(response)
    if response.status_code == 200:
        try:
            r = response.json()
            return {
                "Account Booyah Pass": f"{r.get('booyah_pass_level', 'N/A')}",
                "Account Create": f"{r.get('createAt', 'N/A')}",
                "Account Level": f"{r.get('level', 'N/A')}",
                "Account Likes": f" {r.get('likes', 'N/A')}",
                "Name": f"{r.get('nickname', 'N/A')}",
                "UID": f" {r.get('accountId', 'N/A')}",
                "Account Region": f"{r.get('region', 'N/A')}",
                }
        except ValueError as e:
            pass
            return {
                "error": "Invalid JSON response"
            }
    else:
        pass
        return {
            "error": f"Failed to fetch data: {response.status_code}"
        }

def get_player_bio(uid):
    try:
        url = f"https://info-wotaxxdev-api.vercel.app/info?uid={uid}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            bio = data.get('socialInfo', {}).get('signature', None)
            if bio:
                return bio
            else:
                return "No bio available"
        else:
            return f"Failed to fetch bio. Status code: {res.status_code}"
    except Exception as e:
        return f"Error occurred: {e}"

def talk_with_ai(question):
    url = f"https://aashish-ai-api.vercel.app/ask?key=AASHISH65&message={question}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        msg = data["message"]["content"]
        return msg
    else:
        return "An error occurred while connecting to the server."

def spam_requests(player_id):
    url = f"https://like2.vercel.app/send_requests?uid={player_id}&server={server2}&key={key2}"
    try:
        res = requests.get(url, timeout=20)
        if res.status_code == 200:
            data = res.json()
            return f"API Status: Success [{data.get('success_count', 0)}] Failed [{data.get('failed_count', 0)}]"
        else:
            return f"API Error: Status {res.status_code}"
    except requests.exceptions.RequestException as e:
        print(f"Could not connect to spam API: {e}")
        return "Failed to connect to spam API."

def newinfo(uid):
    url = "https://like2.vercel.app/player-info"
    params = {
        'uid': uid,
        'server': server2,
        'key': key2
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "basicInfo" in data:
                return {"status": "ok", "data": data}
            else:
                return {"status": "error", "message": data.get("error", "Invalid ID or data not found.")}
        else:
            try:
                error_msg = response.json().get('error', f"API returned status {response.status_code}")
                return {"status": "error", "message": error_msg}
            except ValueError:
                return {"status": "error", "message": f"API returned status {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Network error: {str(e)}"}
    except ValueError:
        return {"status": "error", "message": "Invalid JSON response from API."}

    async def run_spam(chat_type, message, count, uid, chat_id, key, iv):
        try:
            for i in range(count):
                await safe_send_message(chat_type, message, uid, chat_id, key, iv)
                await asyncio.sleep(0.12)
        except Exception as e:
            print("Spam Error:", e)

    async def send_title_msg(self, chat_id, key, iv):
        fields = {
            1: 1,
            2: {
                1: "13777777720",
                2: str(chat_id),
                3: f"{{\"TitleID\":{get_random_title()},\"type\":\"Title\"}}",
                4: int(datetime.now().timestamp()),
                5: 0,
                6: "en",
                9: {
                    1: "[C][B][FF0000] KRN ON TOP",
                    2: await get_random_avatar(),
                    3: 330,
                    4: 102000015,
                    5: "TEMP GUILD",
                    6: 1,
                    7: 1,
                    8: {
                        1: 2
                    },
                    9: {
                        1: 1158053040,
                        2: 8,
                        3: "\u0010\u0015\b\n\u000b\u0015\f\u000f\u0011\u0004\u0007\u0002\u0003\r\u000e\u0012\u0001\u0005\u0006"
                    }
                },
                13: {
                    1: 2,
                    2: 1
                },
                99: b""
            }
        }
        packet = create_protobuf_packet(fields)
        packet = packet.hex()
        header_length = len(encrypt_packet(packet, key, iv)) // 2
        header_length_final = dec_to_hex(header_length)
        if len(header_length_final) == 2:
            final_packet = "0515000000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 3:
            final_packet = "051500000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 4:
            final_packet = "05150000" + header_length_final + self.nmnmmmmn(packet)
        elif len(header_length_final) == 5:
            final_packet = "0515000" + header_length_final + self.nmnmmmmn(packet)
        return bytes.fromhex(final_packet)

def send_likes(uid):
    try:
        likes_api_response = requests.get(
             f"https://yourlikeapi/like?uid={uid}&server_name={server2}&x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass={BYPASS_TOKEN}",
             timeout=15
             )
        if likes_api_response.status_code != 200:
            return f"""
Like API Error!
Status Code: {likes_api_response.status_code}
Please check if the uid is correct.
"""
        api_json_response = likes_api_response.json()
        player_name = api_json_response.get('PlayerNickname', 'Unknown')
        likes_before = api_json_response.get('LikesbeforeCommand', 0)
        likes_after = api_json_response.get('LikesafterCommand', 0)
        likes_added = api_json_response.get('LikesGivenByAPI', 0)
        status = api_json_response.get('status', 0)
        if status == 1 and likes_added > 0:
            return f"""
[C][B]Likes Sent Successfully!

Player Name : {player_name}
Likes Added : {likes_added}
Likes Before : {likes_before}
Likes After : {likes_after}
"""
        elif status == 2 or likes_before == likes_after:
            return f"""
You have already taken likes with this UID.
"""
        else:
            return f"""
Something went wrong.
"""
    except requests.exceptions.RequestException:
        return """
Like API Connection Failed!
"""
    except Exception as e:
        return f"""
An unexpected error occurred: {str(e)}
"""

def send_insta_info(username):
    try:
        response = requests.get(f"http://127.0.0.1:8080/api/insta/{username}", timeout=15)
        if response.status_code != 200:
            return f"Instagram API Status Code: {response.status_code}"
        user = response.json()
        full_name = user.get("full_name", "Unknown")
        followers = user.get("edge_followed_by", {}).get("count") or user.get("followers_count", 0)
        following = user.get("edge_follow", {}).get("count") or user.get("following_count", 0)
        posts = user.get("media_count") or user.get("edge_owner_to_timeline_media", {}).get("count", 0)
        profile_pic = user.get("profile_pic_url_hd") or user.get("profile_pic_url")
        private_status = user.get("is_private")
        verified_status = user.get("is_verified")
        return f"""
[C][B][FF0000]INSTAGRAM INFO[FFFFFF]

Name: {full_name}
Username: {username}
Followers: {followers}
Following: {following}
Posts: {posts}
Private: {private_status}
Verified: {verified_status}
"""
    except requests.exceptions.RequestException:
        return "Instagram API Connection Failed!"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"

Hr = {
    'User-Agent': "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
    'Connection': "Keep-Alive",
    'Accept-Encoding': "gzip",
    'Content-Type': "application/x-www-form-urlencoded",
    'Expect': "100-continue",
    'X-Unity-Version': "2018.4.11f1",
    'X-GA': "v1 1",
    'ReleaseVersion': "OB51"}

def get_random_color():
    colors = [
        "[FF0000]", "[00FF00]", "[0000FF]", "[FFFF00]", "[FF00FF]", "[00FFFF]", "[FFFFFF]", "[FFA500]",
        "[A52A2A]", "[800080]", "[000000]", "[808080]", "[C0C0C0]", "[FFC0CB]", "[FFD700]", "[ADD8E6]",
        "[90EE90]", "[D2691E]", "[DC143C]", "[00CED1]", "[9400D3]", "[F08080]", "[20B2AA]", "[FF1493]",
        "[7CFC00]", "[B22222]", "[FF4500]", "[DAA520]", "[00BFFF]", "[00FF7F]", "[4682B4]", "[6495ED]",
        "[5F9EA0]", "[DDA0DD]", "[E6E6FA]", "[B0C4DE]", "[556B2F]", "[8FBC8F]", "[2E8B57]", "[3CB371]",
        "[6B8E23]", "[808000]", "[B8860B]", "[CD5C5C]", "[8B0000]", "[FF6347]", "[FF8C00]", "[BDB76B]",
        "[9932CC]", "[8A2BE2]", "[4B0082]", "[6A5ACD]", "[7B68EE]", "[4169E1]", "[1E90FF]", "[191970]",
        "[00008B]", "[000080]", "[008080]", "[008B8B]", "[B0E0E6]", "[AFEEEE]", "[E0FFFF]", "[F5F5DC]",
        "[FAEBD7]"
    ]
    return random.choice(colors)

print(get_random_color())

async def get_random_avatar():
    await asyncio.sleep(0)
    avatar_list = [
        '902050001', '902050002', '902050003', '902039016', '902050004',
        '902047011', '902047010', '902049015', '902050006', '902049020'
    ]
    return random.choice(avatar_list)

async def ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region):
    try:
        join_packet = await GenJoinSquadsPacket(team_code, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
        print(f"Joined team: {team_code}")
        await asyncio.sleep(1.5)
        emote_packet = await Emote_k(int(target_uid), int(emote_id), key, iv, region)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_packet)
        print(f"Performed emote {emote_id} to UID {target_uid}")
        await asyncio.sleep(0.5)
        leave_packet = await ExiT(None, key, iv)
        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', leave_packet)
        print(f"Left team: {team_code}")
        return True, f"Quick emote attack completed! Sent emote to UID {target_uid}"
    except Exception as e:
        return False, f"Quick emote attack failed: {str(e)}"

async def encrypted_proto(encoded_hex):
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(encoded_hex, AES.block_size)
    encrypted_payload = cipher.encrypt(padded_message)
    return encrypted_payload

async def GeNeRaTeAccEss(uid , password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": (await Ua()),
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=Hr, data=data) as response:
            if response.status != 200: return "Failed to get access token"
            data = await response.json()
            open_id = data.get("open_id")
            access_token = data.get("access_token")
            return (open_id, access_token) if open_id and access_token else (None, None)

async def EncRypTMajoRLoGin(open_id, access_token):
    major_login = MajoRLoGinrEq_pb2.MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 1
    major_login.client_version = "1.118.1"
    major_login.system_software = "Android OS 9 / API-28 (PQ3B.190801.10101846/G9650ZHU2ARC6)"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = "Verizon"
    major_login.network_type = "WIFI"
    major_login.screen_width = 1920
    major_login.screen_height = 1080
    major_login.screen_dpi = "280"
    major_login.processor_details = "ARM64 FP ASIMD AES VMH | 2865 | 4"
    major_login.memory = 3003
    major_login.gpu_renderer = "Adreno (TM) 640"
    major_login.gpu_version = "OpenGL ES 3.1 v1.46"
    major_login.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    memory_available = major_login.memory_available
    memory_available.version = 55
    memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 1
    major_login.network_operator_a = "Verizon"
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019118695"
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 1
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    string = major_login.SerializeToString()
    return  await encrypted_proto(string)

async def MajorLogin(payload):
    url = "https://loginbp.ggblueshark.com/MajorLogin"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def GetLoginData(base_url, payload, token):
    url = f"{base_url}/GetLoginData"
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    Hr['Authorization']= f"Bearer {token}"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=Hr, ssl=ssl_context) as response:
            if response.status == 200: return await response.read()
            return None

async def DecRypTMajoRLoGin(MajoRLoGinResPonsE):
    proto = MajoRLoGinrEs_pb2.MajorLoginRes()
    proto.ParseFromString(MajoRLoGinResPonsE)
    return proto

async def DecRypTLoGinDaTa(LoGinDaTa):
    proto = PorTs_pb2.GetLoginData()
    proto.ParseFromString(LoGinDaTa)
    return proto

async def DecodeWhisperMessage(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = DEcwHisPErMsG_pb2.DecodeWhisper()
    proto.ParseFromString(packet)
    return proto

async def decode_team_packet(hex_packet):
    packet = bytes.fromhex(hex_packet)
    proto = sQ_pb2.recieved_chat()
    proto.ParseFromString(packet)
    return proto

async def xAuThSTarTuP(TarGeT, token, timestamp, key, iv):
    uid_hex = hex(TarGeT)[2:]
    uid_length = len(uid_hex)
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_account_token = token.encode().hex()
    encrypted_packet = await EnC_PacKeT(encrypted_account_token, key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    if uid_length == 9: headers = '0000000'
    elif uid_length == 8: headers = '00000000'
    elif uid_length == 10: headers = '000000'
    elif uid_length == 7: headers = '000000000'
    else: print('Unexpected length') ; headers = '0000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

async def cHTypE(H):
    if not H: return 'Squid'
    elif H == 1: return 'CLan'
    elif H == 2: return 'PrivaTe'

async def SEndMsG(H , message , Uid , chat_id , key , iv):
    TypE = await cHTypE(H)
    if TypE == 'Squid': msg_packet = await xSEndMsgsQ(message , chat_id , key , iv)
    elif TypE == 'CLan': msg_packet = await xSEndMsg(message , 1 , chat_id , chat_id , key , iv)
    elif TypE == 'PrivaTe': msg_packet = await xSEndMsg(message , 2 , Uid , Uid , key , iv)
    return msg_packet

async def SEndPacKeT(OnLinE , ChaT , TypE , PacKeT):
    if TypE == 'ChaT' and ChaT: whisper_writer.write(PacKeT) ; await whisper_writer.drain()
    elif TypE == 'OnLine': online_writer.write(PacKeT) ; await online_writer.drain()
    else: return 'UnsoPorTed TypE ! >> ErrrroR (:():)'

async def safe_send_message(chat_type, message, target_uid, chat_id, key, iv, max_retries=3):
    for attempt in range(max_retries):
        try:
            P = await SEndMsG(chat_type, message, target_uid, chat_id, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'ChaT', P)
            print(f"Message sent successfully on attempt {attempt + 1}")
            return True
        except Exception as e:
            print(f"Failed to send message (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(0.5)
    return False

async def fast_emote_spam(uids, emote_id, key, iv, region):
    global fast_spam_running
    count = 0
    max_count = 25
    while fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, int(emote_id), key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in fast_emote_spam for uid {uid}: {e}")
        count += 1
        await asyncio.sleep(0.1)

async def custom_emote_spam(uid, emote_id, times, key, iv, region):
    global custom_spam_running
    count = 0
    while custom_spam_running and count < times:
        try:
            uid_int = int(uid)
            H = await Emote_k(uid_int, int(emote_id), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            count += 1
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Error in custom_emote_spam for uid {uid}: {e}")
            break

async def spam_request_loop_with_cosmetics(target_uid, key, iv, region):
    global spam_request_running
    count = 0
    max_requests = 30
    badge_rotation = [1048576, 32768, 2048, 64, 4094, 11233, 262144]
    while spam_request_running and count < max_requests:
        try:
            current_badge = badge_rotation[count % len(badge_rotation)]
            PAc = await OpEnSq(key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
            await asyncio.sleep(0.2)
            C = await cHSq(5, int(target_uid), key, iv, region)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
            await asyncio.sleep(0.2)
            V = await SEnd_InV_With_Cosmetics(5, int(target_uid), key, iv, region, current_badge)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
            E = await ExiT(None, key, iv)
            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
            count += 1
            print(f"Sent cosmetic invite #{count} to {target_uid} with badge {current_badge}")
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Error in cosmetic spam: {e}")
            await asyncio.sleep(0.5)
    return count

async def evo_emote_spam(uids, number, key, iv, region):
    try:
        emote_id = EMOTE_MAP.get(int(number))
        if not emote_id:
            return False, f"Invalid number! Use 1-21 only."
        success_count = 0
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                success_count += 1
                await asyncio.sleep(0.1)
            except Exception as e:
                print(f"Error sending evo emote to {uid}: {e}")
        return True, f"Sent evolution emote {number} (ID: {emote_id}) to {success_count} player(s)"
    except Exception as e:
        return False, f"Error in evo_emote_spam: {str(e)}"

async def evo_fast_emote_spam(uids, number, key, iv, region):
    global evo_fast_spam_running
    count = 0
    max_count = 25
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    while evo_fast_spam_running and count < max_count:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_fast_emote_spam for uid {uid}: {e}")
        count += 1
        await asyncio.sleep(0.1)
    return True, f"Completed fast evolution emote spam {count} times"

async def evo_custom_emote_spam(uids, number, times, key, iv, region):
    global evo_custom_spam_running
    count = 0
    emote_id = EMOTE_MAP.get(int(number))
    if not emote_id:
        return False, f"Invalid number! Use 1-21 only."
    while evo_custom_spam_running and count < times:
        for uid in uids:
            try:
                uid_int = int(uid)
                H = await Emote_k(uid_int, emote_id, key, iv, region)
                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
            except Exception as e:
                print(f"Error in evo_custom_emote_spam for uid {uid}: {e}")
        count += 1
        await asyncio.sleep(0.1)
    return True, f"Completed custom evolution emote spam {count} times"

async def ArohiAccepted(uid,code,K,V):
    fields = {
        1: 4,
        2: {
            1: uid,
            3: uid,
            8: 1,
            9: {
            2: 161,
            4: "y[WW",
            6: 11,
            8: "1.114.18",
            9: 3,
            10: 1
            },
            10: str(code),
        }
        }
    return await GeneRaTePk((await CrEaTe_ProTo(fields)).hex() , '0515' , K , V)

async def TcPOnLine(ip, port, key, iv, AutHToKen, reconnect_delay=0.5):
    global online_writer, last_status_packet, status_response_cache, insquad, joining_team, whisper_writer, region
    if insquad is not None:
        insquad = None
    if joining_team is True:
        joining_team = False
    online_writer = None
    whisper_writer = None
    while True:
        try:
            print(f"Attempting to connect to {ip}:{port}")
            reader, writer = await asyncio.open_connection(ip, int(port))
            online_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            online_writer.write(bytes_payload)
            await online_writer.drain()
            print("Authentication token sent. Entering read loop")
            while True:
                data2 = await reader.read(9999)
                if not data2:
                    print("Connection closed by the server.")
                    break
                data_hex = data2.hex()
                if data_hex.startswith('0514'):
                    try:
                        decrypted = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(decrypted)
                        if packet_json.get('1') == 21:
                            if '2' in packet_json and 'data' in packet_json['2']:
                                emote_data = packet_json['2']['data']
                                if ('1' in emote_data and '2' in emote_data and
                                    '5' in emote_data and 'data' in emote_data['5']):
                                    nested = emote_data['5']['data']
                                    if '1' in nested and '3' in nested:
                                        sender_uid = nested.get('1', {}).get('data')
                                        emote_id = nested.get('3', {}).get('data')
                                        print(f"EMOTE HIJACK DETECTED!")
                                        print(f"Sender: {sender_uid}")
                                        print(f"Original emote: {emote_id}")
                                        special_emote = await Emote_k(int(sender_uid), 909038002, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', special_emote)
                                        print(f"Sent special emote 909038002 to {sender_uid}")
                                        await asyncio.sleep(0.3)
                                        try:
                                            mirror_emote_id = int(emote_id)
                                            mirror_packet = await Emote_k(int(sender_uid), mirror_emote_id, key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', mirror_packet)
                                            print(f"Mirroring user's emote {emote_id} back")
                                        except ValueError:
                                            print(f"Could not convert emote ID: {emote_id}")
                                        await asyncio.sleep(0.2)
                                        try:
                                            bot_uid = 14009897329
                                            bot_self_emote = await Emote_k(bot_uid, int(emote_id), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_self_emote)
                                            print(f"Bot also doing emote {emote_id}")
                                        except Exception as e:
                                            print(f"Bot self-emote failed: {e}")
                                        continue
                    except Exception as e:
                        print(f"Emote hijack error: {e}")
                        pass
                if data_hex.startswith('0500') and insquad is not None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        if packet_json.get('1') in [6, 7]:
                             insquad = None
                             joining_team = False
                             print("Squad cancelled or exited (code 6/7).")
                             continue
                    except Exception as e:
                        print(f"Error in auto-accept case 1: {e}")
                        pass
                if data_hex.startswith("0500") and insquad is None and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        uid = packet_json['5']['data']['1']['data']
                        invite_uid = packet_json['5']['data']['2']['data']['1']['data']
                        squad_owner = packet_json['5']['data']['1']['data']
                        code = packet_json['5']['data']['8']['data']
                        emote_id = 909050009
                        bot_uid = 14009897329
                        SendInv = await RedZed_SendInv(bot_uid, invite_uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', SendInv)
                        inv_packet = await RejectMSGtaxt(squad_owner, uid, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', inv_packet)
                        print(f"Received squad invite from {squad_owner}, accepting")
                        Join = await ArohiAccepted(squad_owner, code, key, iv)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', Join)
                        await asyncio.sleep(2)
                        emote_to_sender = await Emote_k(int(uid), emote_id, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', emote_to_sender)
                        bot_emote = await Emote_k(int(bot_uid), emote_id, key, iv, region)
                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', bot_emote)
                        insquad = True
                    except Exception as e:
                        print(f"Auto-accept error: {e}")
                        insquad = None
                        joining_team = False
                        continue
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        print(f"Received squad data for joining team, attempting chat auth for {OwNer_UiD}")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                        joining_team = False
                    except Exception as e:
                        print(f"Error in joining_team chat auth: {e}")
                        pass
                if data_hex.startswith('0500') and len(data_hex) > 1000 and joining_team == False:
                    try:
                        packet = await DeCode_PackEt(data_hex[10:])
                        packet_json = json.loads(packet)
                        OwNer_UiD , CHaT_CoDe , SQuAD_CoDe = await GeTSQDaTa(packet_json)
                        print(f"Received long packet, attempting general chat auth for {OwNer_UiD}")
                        JoinCHaT = await AutH_Chat(3 , OwNer_UiD , CHaT_CoDe, key,iv)
                        await SEndPacKeT(whisper_writer , online_writer , 'ChaT' , JoinCHaT)
                    except Exception as e:
                        print(f"Error in general chat auth: {e}")
                        pass
                if data_hex.startswith('0f00') and len(data_hex) > 100:
                    print(f"Received status response packet")
                    try:
                        if '08' in data_hex:
                            proto_part = f'08{data_hex.split("08", 1)[1]}'
                        else:
                            print("Status packet structure missing '08' marker.")
                            continue
                        parsed_data = get_available_room(proto_part)
                        if parsed_data:
                            parsed_json = json.loads(parsed_data)
                            if "2" in parsed_json and parsed_json["2"]["data"] == 15:
                                player_id = parsed_json["5"]["data"]["1"]["data"]["1"]["data"]
                                player_status = get_player_status(proto_part)
                                print(f"Parsed status for {player_id}: {player_status}")
                                cache_entry = {
                                    'status': player_status,
                                    'packet': proto_part,
                                    'timestamp': time.time(),
                                    'full_packet': data_hex,
                                    'parsed_json': parsed_json
                                }
                                try:
                                    StatusData = parsed_json
                                    if ("5" in StatusData and "data" in StatusData["5"] and
                                        "1" in StatusData["5"]["data"] and "data" in StatusData["5"]["data"]["1"] and
                                        "3" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["3"] and
                                        StatusData["5"]["data"]["1"]["data"]["3"]["data"] == 1 and
                                        "11" in StatusData["5"]["data"]["1"]["data"] and "data" in StatusData["5"]["data"]["1"]["data"]["11"] and
                                        StatusData["5"]["data"]["1"]["data"]["11"]["data"] == 1):
                                        print(f"SPECIAL CONDITION MET: Player {player_id} is in SOLO mode with special flag 11=1")
                                        cache_entry['special_state'] = 'SOLO_WITH_FLAG_1'
                                except Exception as cond_error:
                                    print(f"Error checking special condition: {cond_error}")
                                if "IN ROOM" in player_status:
                                    try:
                                        room_id = get_idroom_by_idplayer(proto_part)
                                        if room_id:
                                            cache_entry['room_id'] = room_id
                                            print(f"Room ID extracted: {room_id}")
                                    except Exception as room_error:
                                        print(f"Failed to extract room ID: {room_error}")
                                elif "INSQUAD" in player_status:
                                    try:
                                        leader_id = get_leader(proto_part)
                                        if leader_id:
                                            cache_entry['leader_id'] = leader_id
                                            print(f"Leader ID: {leader_id}")
                                    except Exception as leader_error:
                                        print(f"Failed to extract leader: {leader_error}")
                                print(f"Status cache updated: {player_id} = {player_status}")
                    except Exception as e:
                        print(f"Error parsing status: {e}")
                        import traceback
                        traceback.print_exc()
            if online_writer is not None:
                online_writer.close()
                await online_writer.wait_closed()
                online_writer = None
            if whisper_writer is not None:
                try:
                    whisper_writer.close()
                    await whisper_writer.wait_closed()
                except:
                    pass
                whisper_writer = None
            insquad = None
            joining_team = False
            print(f"Connection closed. Reconnecting in {reconnect_delay} seconds")
        except ConnectionRefusedError:
            print(f"Connection refused to {ip}:{port}. Retrying")
            await asyncio.sleep(reconnect_delay)
        except asyncio.TimeoutError:
            print(f"Connection timeout to {ip}:{port}. Retrying")
            await asyncio.sleep(reconnect_delay)
        except Exception as e:
            print(f"Unexpected error in TcPOnLine: {e}")
            await asyncio.sleep(reconnect_delay)

async def TcPChaT(ip, port, AutHToKen, key, iv, LoGinDaTaUncRypTinG, ready_event, region , reconnect_delay=0.5):
    print(region, 'TCP CHAT')
    global spam_room , whisper_writer , spammer_uid , spam_chat_id , spam_uid , online_writer , chat_id , XX , uid , Spy,data2, Chat_Leave, fast_spam_running, fast_spam_task, custom_spam_running, custom_spam_task, spam_request_running, spam_request_task, evo_fast_spam_running, evo_fast_spam_task, evo_custom_spam_running, evo_custom_spam_task, lag_running, lag_task, evo_cycle_running, evo_cycle_task, reject_spam_running, reject_spam_task
    while True:
        try:
            reader , writer = await asyncio.open_connection(ip, int(port))
            whisper_writer = writer
            bytes_payload = bytes.fromhex(AutHToKen)
            whisper_writer.write(bytes_payload)
            await whisper_writer.drain()
            ready_event.set()
            if LoGinDaTaUncRypTinG.Clan_ID:
                clan_id = LoGinDaTaUncRypTinG.Clan_ID
                clan_compiled_data = LoGinDaTaUncRypTinG.Clan_Compiled_Data
                print('\n - TarGeT BoT in CLan ! ')
                print(f' - Clan Uid > {clan_id}')
                print(f' - BoT ConnEcTed WiTh CLan ChaT SuccEssFuLy ! ')
                pK = await AuthClan(clan_id , clan_compiled_data , key , iv)
                if whisper_writer: whisper_writer.write(pK) ; await whisper_writer.drain()
            while True:
                data = await reader.read(9999)
                if not data: break
                if data.hex().startswith("120000"):
                    msg = await DeCode_PackEt(data.hex()[10:])
                    chatdata = json.loads(msg)
                    try:
                        response = await DecodeWhisperMessage(data.hex()[10:])
                        uid = response.Data.uid
                        chat_id = response.Data.Chat_ID
                        XX = response.Data.chat_type
                        inPuTMsG = response.Data.msg.lower()
                        print(f"Received message: {inPuTMsG} from UID: {uid} in chat type: {XX}")
                    except:
                        response = None
                    if response:
                        if inPuTMsG.strip().startswith('/ai '):
                            print('Processing AI command in any chat type')
                            question = inPuTMsG[4:].strip()
                            if question:
                                initial_message = f"[B][C]{get_random_color()}AI is thinking"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    ai_response = await loop.run_in_executor(executor, talk_with_ai, question)
                                ai_message = f"""
[B][C]{get_random_color()}AI Response:
[FFFFFF]{ai_response}
[C][B][FFB300]Question: [FFFFFF]{question}
"""
                                await safe_send_message(response.Data.chat_type, ai_message, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]Please provide a question after /ai\nExample: /ai What is Free Fire?"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/likes '):
                            print('Processing likes command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /likes (uid)\nExample: /likes 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Sending 100 likes to {target_uid}"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    likes_result = await loop.run_in_executor(executor, send_likes, target_uid)
                                await safe_send_message(response.Data.chat_type, likes_result, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/text '):
                            print('Processing /text command')
                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)
                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]Usage:\n"
                                        "/text <message>\n"
                                        "Example: /text STAREXX"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    user_message = parts[1].strip()
                                    for _ in range(30):
                                        color = get_random_color()
                                        colored_message = f"[B][C]{color} {user_message}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/gali '):
                            print('Processing /gali command')
                            try:
                                parts = inPuTMsG.strip().split(maxsplit=1)
                                if len(parts) < 2:
                                    error_msg = (
                                        "[B][C][FF0000]Usage:\n"
                                        "/gali <name>\n"
                                        "Example: /gali hater"
                                    )
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    name = parts[1].strip()
                                    messages = [
                                        "{Name} Teri séxy bhen ki chxt me l0da DAAL KAR RAAT BHAR JOR JOR SE CH0DUNGA",
                                        "{Name} MADHERXHOD TƐRI MÁÁ KI KALI G4ND MƐ LÀND MARU",
                                        "{Name} TƐRI BHƐN KI TIGHT CHXT KO 5G KI SPEED SE CHÒD DU",
                                        "{Name} TƐRI BEHEN KI CHXT ME L4ND MARU",
                                        "{Name} TƐRI MÁÁ KI CHXT 360 BAR",
                                        "{Name} TƐRI BƐHƐN KI CHXT 720 BAR",
                                        "{Name} BEHEN KE L0DE",
                                        "{Name} MADARCHXD",
                                        "{Name} BETE TƐRA BAAP HUN ME",
                                        "{Name} G4NDU APNE BAAP KO H8 DEGA",
                                        "{Name} KI MÀÀ KI CHXT PER NIGHT 4000",
                                        "{Name} KI BƐHƐN KI CHXT PER NIGHT 8000",
                                        "{Name} R4NDI KE BACHHƐ APNE BAP KO H8 DEGA",
                                        "INDIA KA NO-1 G4NDU {Name}",
                                        "{Name} CHAPAL CH0R",
                                        "{Name} TƐRI MÀÀ KO GB ROAD PE BETHA KE CHXDUNGA",
                                        "{Name} BETA JHULA JHUL APNE BAAP KO MAT BHUL"
            ]
                                    for msg in messages:
                                        colored_message = f"[B][C]{get_random_color()} {msg.replace('{Name}', name.upper())}"
                                        await safe_send_message(response.Data.chat_type, colored_message, uid, chat_id, key, iv)
                                        await asyncio.sleep(0.5)
                            except Exception as e:
                                error_msg = f"[B][C][FF0000]Something went wrong:\n{str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/ig '):
                            print('Processing insta command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /ig <username>\nExample: /ig realstarexx"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_username = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Fetching instagram info of {target_username}"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    insta_result = await loop.run_in_executor(executor, send_insta_info, target_username)
                                await safe_send_message(response.Data.chat_type, insta_result, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/bio '):
                            print('Processing bio command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /bio [uid]\nExample: /bio 4368569733"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Fetching the player bio"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                loop = asyncio.get_event_loop()
                                with ThreadPoolExecutor() as executor:
                                    bio_result = await loop.run_in_executor(executor, get_player_bio, target_uid)
                                await safe_send_message(response.Data.chat_type, f"[B][C]{get_random_color()}{bio_result}", uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/quick'):
                            print('Processing quick emote attack command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /quick (team_code) [emote_id] [target_uid]\n\n[FFFFFF]Examples:\n{get_random_color()}/quick ABC123[FFFFFF] - Join, send Rings emote, leave\n{get_random_color()}/ghostquick ABC123[FFFFFF] - Ghost join, send emote, leave"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                emote_id = parts[0]
                                target_uid = str(response.Data.uid)
                                if len(parts) >= 3:
                                    emote_id = parts[2]
                                if len(parts) >= 4:
                                    target_uid = parts[3]
                                if target_uid == str(response.Data.uid):
                                    target_name = "Yourself"
                                else:
                                    target_name = f"UID {target_uid}"
                                initial_message = f"[B][C][FFFF00]QUICK EMOTE ATTACK!\n\n[FFFFFF]Team: {get_random_color()}{team_code}\n[FFFFFF]Emote: {get_random_color()}{emote_id}\n[FFFFFF]Target: {get_random_color()}{target_name}\n[FFFFFF]Estimated: {get_random_color()}2 seconds\n\n[FFFF00]Executing sequence"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    success, result = await ultra_quick_emote_attack(team_code, emote_id, target_uid, key, iv, region)
                                    if success:
                                        success_message = f"[B][C]{get_random_color()}QUICK ATTACK SUCCESS!\n\n[FFFFFF]Team: {get_random_color()}{team_code}\n[FFFFFF]Emote: {get_random_color()}{emote_id}\n[FFFFFF]Target: {get_random_color()}{target_name}\n\n{get_random_color()}Bot joined → emoted → left!"
                                    else:
                                        success_message = f"[B][C][FF0000]Regular attack failed: {result}"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    print("failed")
                        if inPuTMsG.strip().startswith('/inv '):
                            print('Processing invite command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /inv (uid)\nExample: /inv 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Creating 5-Player Group and sending request to {target_uid}"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    PAc = await OpEnSq(key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                                    await asyncio.sleep(0.3)
                                    C = await cHSq(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                                    await asyncio.sleep(0.3)
                                    V = await SEnd_InV(5, int(target_uid), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                                    await asyncio.sleep(0.3)
                                    E = await ExiT(None, key, iv)
                                    await asyncio.sleep(2)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                                    success_message = f"[B][C]{get_random_color()}5-Player Group invitation sent successfully to {target_uid}!"
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR sending invite: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.startswith(("/6")):
                            initial_message = f"[B][C]{get_random_color()}Creating 6-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(6, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C]{get_random_color()}6-Player Group invitation sent successfully to {uid}!"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                        if inPuTMsG.startswith(("/3")):
                            initial_message = f"[B][C]{get_random_color()}Creating 3-Player Group"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(3, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C]{get_random_color()}6-Player Group invitation sent successfully to {uid}!"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/roommsg'):
                            print('Processing room message command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /roommsg (room_id) (message)\nExample: /roommsg 489775386 Hello room!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                message = " ".join(parts[2:])
                                initial_msg = f"[B][C]{get_random_color()}Sending to room {room_id}: {message}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else 13699776666
                                    room_chat_packet = await send_room_chat_enhanced(message, room_id, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', room_chat_packet)
                                    success_msg = f"[B][C]{get_random_color()}Message sent to room {room_id}!"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"Room message sent to {room_id}: {message}")
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Failed: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.startswith(("/5")):
                            initial_message = f"[B][C]{get_random_color()}Sending Group Invitation"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            PAc = await OpEnSq(key, iv, region)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', PAc)
                            C = await cHSq(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', C)
                            V = await SEnd_InV(5, uid, key, iv, region)
                            await asyncio.sleep(0.3)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', V)
                            E = await ExiT(None, key, iv)
                            await asyncio.sleep(3.5)
                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', E)
                            success_message = f"[B][C]{get_random_color()}Group invitation sent successfully to {uid}!"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == "/admin":
                            admin_message = """[B][C]
Name: Ankit Mehta
Username: @realstarexx
"""
                            await safe_send_message(response.Data.chat_type, admin_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/multijoin'):
                            print('Processing multi-account join request')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /multijoin (target_uid)\nExample: /multijoin 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]Please write a valid player ID!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                initial_msg = f"[B][C]{get_random_color()}Starting multi-join attack on {target_uid}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    success_count, total_attempts = await real_multi_account_join(target_uid, key, iv, region)
                                    if success_count > 0:
                                        result_msg = f"""
[B][C]{get_random_color()}MULTI-JOIN ATTACK COMPLETED![FFFFFF]

Target: {target_uid}
Total Attempts: {total_attempts}
Successful Requests: {success_count}
"""
                                    else:
                                        result_msg = f"[B][C][FF0000]All join requests failed! Check bot connection."
                                    await safe_send_message(response.Data.chat_type, result_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Multi-join error: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/fastmultijoin'):
                            print('Processing fast multi-account join spam')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /fastmultijoin (uid)\nExample: /fastmultijoin 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                accounts_data = load_accounts()
                                if not accounts_data:
                                    error_msg = f"[B][C][FF0000]No accounts found!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                initial_msg = f"[B][C]{get_random_color()}FAST MULTI-ACCOUNT JOIN SPAM!\nTarget: {target_uid}\nAccounts: {len(accounts_data)}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    join_count = 0
                                    for uid, password in accounts_data.items():
                                        try:
                                            join_packet = await SEnd_InV(5, int(target_uid), key, iv, region)
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                            join_count += 1
                                            print(f"Fast join from account {uid}")
                                            await asyncio.sleep(0.1)
                                        except Exception as e:
                                            print(f"Fast join failed for {uid}: {e}")
                                            continue
                                    success_msg = f"[B][C]{get_random_color()}FAST MULTI-JOIN COMPLETED![FFFFFF]\nTarget: {target_uid}\nSuccessful: {join_count}/{len(accounts_data)}\nSpeed: Ultra fast"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR in fast multi-join: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/reject'):
                            print('Processing reject spam command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /reject (target_uid)\nExample: /reject 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if reject_spam_task and not reject_spam_task.done():
                                    reject_spam_running = False
                                    reject_spam_task.cancel()
                                    await asyncio.sleep(0.5)
                                start_msg = f"[B][C][1E90FF]Started Reject Spam on: {target_uid}\nPackets: 150 each type\nInterval: 0.2 seconds"
                                await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                reject_spam_running = True
                                reject_spam_task = asyncio.create_task(reject_spam_loop(target_uid, key, iv))
                                asyncio.create_task(handle_reject_completion(reject_spam_task, target_uid, uid, chat_id, response.Data.chat_type, key, iv))
                        if inPuTMsG.strip() == '/reject_stop':
                            if reject_spam_task and not reject_spam_task.done():
                                reject_spam_running = False
                                reject_spam_task.cancel()
                                stop_msg = f"[B][C]{get_random_color()}Reject spam stopped successfully!"
                                await safe_send_message(response.Data.chat_type, stop_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No active reject spam to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/room'):
                            print('Processing advanced room spam command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /room (uid)\nExample: /room 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                room_id = parts[2]
                                if not target_uid.isdigit():
                                    error_msg = f"[B][C][FF0000]Please write a valid player ID!"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    return
                                initial_msg = f"[B][C]{get_random_color()}Working on room spam for {target_uid}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    room_msg = f"[B][C]{get_random_color()}Detected player in room {room_id}"
                                    await safe_send_message(response.Data.chat_type, room_msg, uid, chat_id, key, iv)
                                    spam_packet = await Room_Spam(target_uid, room_id, "STAREXX", key, iv)
                                    spam_count = 99
                                    start_msg = f"[B][C]{get_random_color()}Starting spam: {spam_count} packets to room {room_id}"
                                    await safe_send_message(response.Data.chat_type, start_msg, uid, chat_id, key, iv)
                                    for i in range(spam_count):
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', spam_packet)
                                        if (i + 1) % 25 == 0:
                                            progress_msg = f"[B][C]{get_random_color()}Progress: {i+1}/{spam_count} packets sent"
                                            await safe_send_message(response.Data.chat_type, progress_msg, uid, chat_id, key, iv)
                                            print(f"Room spam progress: {i+1}/{spam_count} to UID: {target_uid}")
                                        await asyncio.sleep(0.05)
                                    success_msg = f"[B][C]{get_random_color()}Room spam completed![FFFFFF]\nTarget: {target_uid}\nPackets: {spam_count}\nRoom: {room_id}\nSpeed: Ultra fast"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    print(f"Room spam completed for UID: {target_uid}")
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Error in room spam: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    print(f"Room spam error: {e}")
                        if inPuTMsG.strip().startswith('/s1'):
                            await handle_badge_command('s1', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/s2'):
                            await handle_badge_command('s2', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/s3'):
                            await handle_badge_command('s3', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/s4'):
                            await handle_badge_command('s4', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/s5'):
                            await handle_badge_command('s5', inPuTMsG, uid, chat_id, key, iv, region, response.Data.chat_type)
                        if inPuTMsG.strip().startswith('/s6'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = "[B][C][FF0000]Usage: /s6 [uid]\nExample: /s6 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                total_requests = 10
                                sequence = ['s1', 's2', 's3', 's4', 's5']
                                initial_msg = f"[B][C][1E90FF]Request received! Preparing to spam {target_uid} with all badges"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                count = 0
                                while count < total_requests:
                                    for cmd in sequence:
                                        if count >= total_requests:
                                            break
                                        fake_command = f"/{cmd} {target_uid}"
                                        await handle_badge_command(cmd, fake_command, uid, chat_id, key, iv, region, response.Data.chat_type)
                                        count += 1
                                success_msg = f"[B][C]{get_random_color()}Successfully sent {total_requests} Join Requests!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/joinroom'):
                            print('Processing custom room join command')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /joinroom (room_id) (password)\nExample: /joinroom 123456 0000"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_id = parts[1]
                                room_password = parts[2]
                                initial_msg = f"[B][C]{get_random_color()}Joining custom room\n[FFFFFF]Room: [f5f5f5]{room_id}[FFFFFF]\nPassword: [f5f5f5]{room_password}[FFFFFF]"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    join_packet = await join_custom_room(room_id, room_password, key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', join_packet)
                                    success_msg = f"[B][C]{get_random_color()}Joined custom room {room_id}!\nBot is now in room chat!"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Failed to join room: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/createroom'):
                            print('Processing custom room creation')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /createroom (room_name) (password) [players=4]\nExample: /createroom BOTROOM 0000 4"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                room_name = parts[1]
                                room_password = parts[2]
                                max_players = parts[3] if len(parts) > 3 else "4"
                                initial_msg = f"[B][C]{get_random_color()}Creating custom room\nName: {room_name}\nPassword: {room_password}\nMax Players: {max_players}"
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                try:
                                    create_packet = await create_custom_room(room_name, room_password, int(max_players), key, iv, region)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', create_packet)
                                    success_msg = f"[B][C]{get_random_color()}Custom room created![FFFFFF]\nRoom: {room_name}\nPassword: {room_password}\nMax: {max_players}\nBot is now hosting!"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Failed to create room: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.startswith('/join'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /join (team_code)\nExample: /join ABC123"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                sender_uid = response.Data.uid
                                initial_message = f"[B][C]{get_random_color()}Joining squad with code: {CodE}"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    EM = await GenJoinSquadsPacket(CodE, key, iv)
                                    await SEndPacKeT(whisper_writer, online_writer, 'OnLine', EM)
                                    await asyncio.sleep(2)
                                    try:
                                        await auto_rings_emote_dual(sender_uid, key, iv, region)
                                    except Exception as emote_error:
                                        print(f"Dual emote failed but join succeeded: {emote_error}")
                                    success_message = f"[B][C]{get_random_color()}Joined squad: {CodE}!\nDual Rings emote activated!\nBot + You ="
                                    await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                except Exception as e:
                                    print(f"Regular join failed, trying ghost join: {e}")
                                    try:
                                        bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                        ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                        if ghost_packet:
                                            await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                            await asyncio.sleep(2)
                                            try:
                                                await auto_rings_emote_dual(sender_uid, key, iv, region)
                                            except Exception as emote_error:
                                                print(f"Dual emote failed but ghost join succeeded: {emote_error}")
                                            success_message = f"[B][C]{get_random_color()}Ghost joined squad: {CodE}!\nDual Rings emote activated!\nBot + You ="
                                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                        else:
                                            error_msg = f"[B][C][FF0000]Failed to create ghost join packet."
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except Exception as ghost_error:
                                        print(f"Ghost join also failed: {ghost_error}")
                                        error_msg = f"[B][C][FF0000]Failed to join squad: {str(ghost_error)}"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/ghost'):
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /ghost (team_code)\nExample: /ghost ABC123"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                CodE = parts[1]
                                initial_message = f"[B][C]{get_random_color()}Ghost joining squad with code: {CodE}"
                                await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                try:
                                    bot_uid = LoGinDaTaUncRypTinG.AccountUID if hasattr(LoGinDaTaUncRypTinG, 'AccountUID') else TarGeT
                                    ghost_packet = await ghost_join_packet(bot_uid, CodE, key, iv)
                                    if ghost_packet:
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', ghost_packet)
                                        success_message = f"[B][C]{get_random_color()}Ghost joined squad with code: {CodE}!"
                                        await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                                    else:
                                        error_msg = f"[B][C][FF0000]Failed to create ghost join packet."
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]Ghost join failed: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/lag '):
                            print('Processing lag command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /lag (team_code)\nExample: /lag ABC123"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                if lag_task and not lag_task.done():
                                    lag_running = False
                                    lag_task.cancel()
                                    await asyncio.sleep(0.1)
                                lag_running = True
                                lag_task = asyncio.create_task(lag_team_loop(team_code, key, iv, region))
                                success_msg = f"[B][C]{get_random_color()}Lag attack started!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == '/stop lag':
                            if lag_task and not lag_task.done():
                                lag_running = False
                                lag_task.cancel()
                                success_msg = f"[B][C]{get_random_color()}Lag attack stopped successfully!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No active lag attack to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.startswith('/exit'):
                            initial_message = f"[B][C]{get_random_color()}Leaving current squad"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            leave = await ExiT(uid,key,iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , leave)
                            success_message = f"[B][C]{get_random_color()}Left the squad successfully!"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/start'):
                            initial_message = f"[B][C]{get_random_color()}Starting match"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            EM = await FS(key , iv)
                            await SEndPacKeT(whisper_writer , online_writer , 'OnLine' , EM)
                            success_message = f"[B][C]{get_random_color()}Match starting command sent!"
                            await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/title'):
                            parts = inPuTMsG.strip().split()
                            initial_message = f"[B][C]{get_random_color()}Sending title to current team"
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            try:
                                title_packet = await send_title_msg(chat_id, key, iv)
                                await SEndPacKeT(whisper_writer, online_writer, 'OnLine', title_packet)
                                success_message = f"[B][C]{get_random_color()}Title sent to current team!"
                                await safe_send_message(response.Data.chat_type, success_message, uid, chat_id, key, iv)
                            except Exception as e:
                                print(f"Title send failed: {e}")
                                error_msg = f"[B][C][FF0000]Failed to send title: {str(e)}"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/e1'):
                            print(f'Processing emote command in chat type: {response.Data.chat_type}')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /e1 (uid) (emote_id)\nExample: /e1 123456789 909000001"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                continue
                            initial_message = f'[B][C]{get_random_color()}Emote started to target'
                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                            uid2 = uid3 = uid4 = uid5 = None
                            s = False
                            target_uids = []
                            try:
                                target_uid = int(parts[1])
                                target_uids.append(target_uid)
                                uid2 = int(parts[2]) if len(parts) > 2 else None
                                if uid2: target_uids.append(uid2)
                                uid3 = int(parts[3]) if len(parts) > 3 else None
                                if uid3: target_uids.append(uid3)
                                uid4 = int(parts[4]) if len(parts) > 4 else None
                                if uid4: target_uids.append(uid4)
                                uid5 = int(parts[5]) if len(parts) > 5 else None
                                if uid5: target_uids.append(uid5)
                                idT = int(parts[-1])
                            except ValueError as ve:
                                print("ValueError:", ve)
                                s = True
                            except Exception as e:
                                print(f"Error parsing emote command: {e}")
                                s = True
                            if not s:
                                try:
                                    for target in target_uids:
                                        H = await Emote_k(target, idT, key, iv, region)
                                        await SEndPacKeT(whisper_writer, online_writer, 'OnLine', H)
                                        await asyncio.sleep(0.1)
                                    success_msg = f"[B][C]{get_random_color()}Emote {idT} sent to {len(target_uids)} player(s)!\nTargets: {', '.join(map(str, target_uids))}"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]ERROR sending emote: {str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]Invalid UID format. Usage: /e1 (uid) (emote_id)"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/lw'):
                            print('Processing /lw auto-start command')
                            global auto_start_running, auto_start_teamcode, stop_auto, auto_start_task
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /lw (team_code)\nExample: /lw 123456"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                team_code = parts[1]
                                if not team_code.isdigit():
                                    error_msg = f"[B][C][FF0000]Team code must be numbers only!\nExample: /lw 123456"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                if auto_start_running:
                                    error_msg = f"[B][C][FF0000]Auto start already running for team {auto_start_teamcode}!\nUse /stop_auto to stop first."
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    continue
                                global auto_start_task, stop_auto
                                stop_auto = False
                                auto_start_running = True
                                auto_start_teamcode = team_code
                                initial_msg = f"""
[B][C][00FFFF]AUTO START BOT ACTIVATED![FFFFFF]

Team Code: [f5f5f5]{team_code}[FFFFFF]
Start Spam: [f5f5f5]{start_spam_duration} seconds[FFFFFF]
Wait Time: [f5f5f5]{wait_after_match} seconds[FFFFFF]
"""
                                await safe_send_message(response.Data.chat_type, initial_msg, uid, chat_id, key, iv)
                                auto_start_task = asyncio.create_task(
                                    auto_start_loop(team_code, uid, chat_id, response.Data.chat_type, key, iv, region)
                                )
                        if inPuTMsG.strip().startswith('/ev4'):
                            print('Processing evo cycle start command in any chat type')
                            parts = inPuTMsG.strip().split()
                            uids = []
                            sender_uid = str(response.Data.uid)
                            uids.append(sender_uid)
                            print(f"Using sender's UID: {sender_uid}")
                            if len(parts) > 1:
                                for part in parts[1:]:
                                    if part.isdigit() and len(part) >= 7 and part != sender_uid:
                                        uids.append(part)
                                        print(f"Added additional UID: {part}")
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                await asyncio.sleep(0.5)
                            evo_cycle_running = True
                            evo_cycle_task = asyncio.create_task(evo_cycle_spam(uids, key, iv, region))
                            if len(uids) == 1:
                                success_msg = f"[B][C]{get_random_color()}Evolution emote cycle started!"
                            else:
                                success_msg = f"[B][C]{get_random_color()}Evolution emote cycle started!"
                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            print(f"Started evolution emote cycle for UIDs: {uids}")
                        if inPuTMsG.strip() == '/ev5':
                            if evo_cycle_task and not evo_cycle_task.done():
                                evo_cycle_running = False
                                evo_cycle_task.cancel()
                                success_msg = f"[B][C]{get_random_color()}Evolution emote cycle stopped successfully!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                print("Evolution emote cycle stopped by command")
                            else:
                                error_msg = f"[B][C][FF0000]No active evolution emote cycle to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/e2'):
                            print('Processing fast emote spam in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /e2 uid1 [uid2] [uid3] [uid4] emoteid"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                emote_id = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) > 3:
                                            uids.append(part)
                                        else:
                                            emote_id = part
                                    else:
                                        break
                                if not emote_id and parts[-1].isdigit():
                                    emote_id = parts[-1]
                                if not uids or not emote_id:
                                    error_msg = f"[B][C][FF0000]Usage: /e2 uid1 [uid2] [uid3] [uid4] emoteid"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    if fast_spam_task and not fast_spam_task.done():
                                        fast_spam_running = False
                                        fast_spam_task.cancel()
                                    fast_spam_running = True
                                    fast_spam_task = asyncio.create_task(fast_emote_spam(uids, emote_id, key, iv, region))
                                    success_msg = f"[B][C]{get_random_color()}Fast emote spam started!\nTargets: {len(uids)} players\nEmote: {emote_id}\nSpam count: 25 times"
                                    await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/e3'):
                            print('Processing custom emote spam in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 4:
                                error_msg = f"[B][C][FF0000]Usage: /e3 (uid) (emote_id) (times)\nExample: /e3 123456789 909000001 10"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                try:
                                    target_uid = parts[1]
                                    emote_id = parts[2]
                                    times = int(parts[3])
                                    if times <= 0:
                                        error_msg = f"[B][C][FF0000]Times must be greater than 0!"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    elif times > 100:
                                        error_msg = f"[B][C][FF0000]Maximum 100 times allowed for safety!"
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    else:
                                        if custom_spam_task and not custom_spam_task.done():
                                            custom_spam_running = False
                                            custom_spam_task.cancel()
                                            await asyncio.sleep(0.5)
                                        custom_spam_running = True
                                        custom_spam_task = asyncio.create_task(custom_emote_spam(target_uid, emote_id, times, key, iv, region))
                                        success_msg = f"[B][C]{get_random_color()}Custom emote spam started!\nTarget: {target_uid}\nEmote: {emote_id}\nTimes: {times}"
                                        await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                except ValueError:
                                    error_msg = f"[B][C][FF0000]Invalid number format! Usage: /e3 (uid) (emote_id) (times)"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                except Exception as e:
                                    error_msg = f"[B][C][FF0000]{str(e)}"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/invs'):
                            print('Processing spam invite with cosmetics')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /invs (uid)\nExample: /invs 123456789"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                target_uid = parts[1]
                                if spam_request_task and not spam_request_task.done():
                                    spam_request_running = False
                                    spam_request_task.cancel()
                                    await asyncio.sleep(0.5)
                                spam_request_running = True
                                spam_request_task = asyncio.create_task(spam_request_loop_with_cosmetics(target_uid, key, iv, region))
                                success_msg = f"[B][C]{get_random_color()}Cosmetic spam started!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == '/stop spm_inv':
                            if spam_request_task and not spam_request_task.done():
                                spam_request_running = False
                                spam_request_task.cancel()
                                success_msg = f"[B][C]{get_random_color()}Spam request stopped successfully!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No active spam request to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/ev1 '):
                            print('Processing evo command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /ev1 uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /ev1 123456789 1"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]Usage: /ev1 uid1 [uid2] [uid3] [uid4] number(1-21)"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]Number must be between 1-21 only!"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            initial_message = f"[B][C]{get_random_color()}Sending evolution emote {number_int}"
                                            await safe_send_message(response.Data.chat_type, initial_message, uid, chat_id, key, iv)
                                            success, result_msg = await evo_emote_spam(uids, number_int, key, iv, region)
                                            if success:
                                                success_msg = f"[B][C]{get_random_color()}{result_msg}"
                                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                            else:
                                                error_msg = f"[B][C][FF0000]{result_msg}"
                                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]Invalid number format! Use 1-21 only."
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/ev2 '):
                            print('Processing evo_fast command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 2:
                                error_msg = f"[B][C][FF0000]Usage: /ev2 uid1 [uid2] [uid3] [uid4] number(1-21)\nExample: /ev2 123456789 1"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:
                                            number = part
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not number and parts[-1].isdigit() and len(parts[-1]) <= 2:
                                    number = parts[-1]
                                if not uids or not number:
                                    error_msg = f"[B][C][FF0000]Usage: /ev2 uid1 [uid2] [uid3] [uid4] number(1-21)"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]Number must be between 1-21 only!"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                                evo_fast_spam_running = False
                                                evo_fast_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            evo_fast_spam_running = True
                                            evo_fast_spam_task = asyncio.create_task(evo_fast_emote_spam(uids, number_int, key, iv, region))
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C]{get_random_color()}Fast evolution emote spam started!\nTargets: {len(uids)} players\nEmote: {number_int} (ID: {emote_id})\nSpam count: 25 times\nInterval: 0.1 seconds"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]Invalid number format! Use 1-21 only."
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().startswith('/ev3 '):
                            print('Processing evo_c command in any chat type')
                            parts = inPuTMsG.strip().split()
                            if len(parts) < 3:
                                error_msg = f"[B][C][FF0000]Usage: /ev3 uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)\nExample: /ev3 123456789 1 10"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                            else:
                                uids = []
                                number = None
                                time_val = None
                                for part in parts[1:]:
                                    if part.isdigit():
                                        if len(part) <= 2:
                                            if number is None:
                                                number = part
                                            elif time_val is None:
                                                time_val = part
                                            else:
                                                uids.append(part)
                                        else:
                                            uids.append(part)
                                    else:
                                        break
                                if not time_val and len(parts) >= 3:
                                    last_part = parts[-1]
                                    if last_part.isdigit() and len(last_part) <= 3:
                                        time_val = last_part
                                        if time_val in uids:
                                            uids.remove(time_val)
                                if not uids or not number or not time_val:
                                    error_msg = f"[B][C][FF0000]Usage: /ev3 uid1 [uid2] [uid3] [uid4] number(1-21) time(1-100)"
                                    await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                else:
                                    try:
                                        number_int = int(number)
                                        time_int = int(time_val)
                                        if number_int not in EMOTE_MAP:
                                            error_msg = f"[B][C][FF0000]Number must be between 1-21 only!"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        elif time_int < 1 or time_int > 100:
                                            error_msg = f"[B][C][FF0000]Time must be between 1-100 only!"
                                            await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                                        else:
                                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                                evo_custom_spam_running = False
                                                evo_custom_spam_task.cancel()
                                                await asyncio.sleep(0.5)
                                            evo_custom_spam_running = True
                                            evo_custom_spam_task = asyncio.create_task(evo_custom_emote_spam(uids, number_int, time_int, key, iv, region))
                                            emote_id = EMOTE_MAP[number_int]
                                            success_msg = f"[B][C]{get_random_color()}Custom evolution emote spam started!"
                                            await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                                    except ValueError:
                                        error_msg = f"[B][C][FF0000]Invalid format! Use numbers only."
                                        await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == '/stop evo_fast':
                            if evo_fast_spam_task and not evo_fast_spam_task.done():
                                evo_fast_spam_running = False
                                evo_fast_spam_task.cancel()
                                success_msg = f"[B][C]{get_random_color()}Evolution fast spam stopped successfully!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No active evolution fast spam to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip() == '/stop evo_c':
                            if evo_custom_spam_task and not evo_custom_spam_task.done():
                                evo_custom_spam_running = False
                                evo_custom_spam_task.cancel()
                                success_msg = f"[B][C]{get_random_color()}Evolution custom spam stopped successfully!"
                                await safe_send_message(response.Data.chat_type, success_msg, uid, chat_id, key, iv)
                            else:
                                error_msg = f"[B][C][FF0000]No active evolution custom spam to stop!"
                                await safe_send_message(response.Data.chat_type, error_msg, uid, chat_id, key, iv)
                        if inPuTMsG.strip().lower() in (".","help", "/help", "menu", "/menu", "commands"):
                            print(f"Help command detected from UID: {uid} in chat type: {response.Data.chat_type}")
                            header = f"[b][c]{get_random_color()}Welcome to Starexx"
                            await safe_send_message(response.Data.chat_type, header, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            group_commands = """
[C][B][FFD700]GROUP COMMANDS[FFFFFF]\n                            
/3, /5, /6 - [f5f5f5]Create group[FFFFFF]
/inv [uid] - [f5f5f5]Invite player[FFFFFF]
/join [code] - [f5f5f5]Join team[FFFFFF]
/exit - [f5f5f5]Leave team[FFFFFF]
"""
                            await safe_send_message(response.Data.chat_type, group_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            advanced_commands = """
[C][B][007AFF]TOOLS COMMANDS[FFFFFF]\n                           
/invs [uid] - [f5f5f5]Spam invites[FFFFFF]
/lag [code] - [f5f5f5]Lag attack[FFFFFF]
/reject [uid] - [f5f5f5]Reject spam[FFFFFF]
/ig [user] - [f5f5f5]Insta info[FFFFFF]
/text [text] - [f5f5f5]Spam msg[FFFFFF]
/admin - [f5f5f5]About Owner[FFFFFF]
"""
                            await safe_send_message(response.Data.chat_type, advanced_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            emote_commands = """
[C][B][32CD32]EMOTE COMMANDS[FFFFFF][B]\n       
/e1  [uid] [id] - [f5f5f5]Normal Emote[FFFFFF]
/e2 [uid] [id] - [f5f5f5]Fast Emote[FFFFFF]
/e3 [uid] [id] [x] - [f5f5f5]Custom Emote[FFFFFF]
"""
                            await safe_send_message(response.Data.chat_type, emote_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            evo_commands = """
[C][B][FFA500]EVOLUTION EMOTES[FFFFFF]\n    
/ev1  [uid] [1-21] - [B][FFFFFF]Evo Emote
/ev2 [uid] [1-21] - Fast Evo Emote
/ev3 [uid] [1-21] [x] - Custom Evo
/ev4 [uid] - Auto Emotes
/ev5 - Stop Emotes
"""
                            await safe_send_message(response.Data.chat_type, evo_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                            badge_commands = """
[C][B][FF4500]BADGE JOIN REQUESTS[FFFFFF][B]\n
/s1  [uid] - [f5f5f5]Craftland Badge[FFFFFF]
/s2 [uid] - [f5f5f5]New V-Badge[FFFFFF]
/s3 [uid] - [f5f5f5]Mod Badge[FFFFFF]
/s4 [uid] - [f5f5f5]Small V-Badge[FFFFFF]
/s5 [uid] - [f5f5f5]Pro Badge[FFFFFF]
/s6 [uid] - [f5f5f5]Spam All Badges[FFFFFF]
"""
                            await safe_send_message(response.Data.chat_type, badge_commands, uid, chat_id, key, iv)
                            await asyncio.sleep(0.2)
                        response = None
                        try:
                            if whisper_writer:
                                whisper_writer.close()
                                await whisper_writer.wait_closed()
                        except:
                            pass
                        finally:
                            whisper_writer = None
        except Exception as e: print(f"Error {ip}:{port} - {e}") ; whisper_writer = None
        await asyncio.sleep(reconnect_delay)

async def MaiiiinE():
    Uid , Pw = GUEST_UID_MAIN, GUEST_PASS_MAIN
    open_id , access_token = await GeNeRaTeAccEss(Uid , Pw)
    if not open_id or not access_token: print("Error - Invalid Account") ; return None
    PyL = await EncRypTMajoRLoGin(open_id , access_token)
    MajoRLoGinResPonsE = await MajorLogin(PyL)
    if not MajoRLoGinResPonsE: print("Target Account is Banned/Not Registered ! ") ; return None
    MajoRLoGinauTh = await DecRypTMajoRLoGin(MajoRLoGinResPonsE)
    UrL = MajoRLoGinauTh.url
    os.system('clear')
    print("Wait a minute.")
    region = MajoRLoGinauTh.region
    ToKen = MajoRLoGinauTh.token
    print("Authentication successful")
    TarGeT = MajoRLoGinauTh.account_uid
    key = MajoRLoGinauTh.key
    iv = MajoRLoGinauTh.iv
    timestamp = MajoRLoGinauTh.timestamp
    LoGinDaTa = await GetLoginData(UrL , PyL , ToKen)
    if not LoGinDaTa: print("Error - Getting Ports From Login Data !") ; return None
    LoGinDaTaUncRypTinG = await DecRypTLoGinDaTa(LoGinDaTa)
    OnLinePorTs = LoGinDaTaUncRypTinG.Online_IP_Port
    ChaTPorTs = LoGinDaTaUncRypTinG.AccountIP_Port
    OnLineiP , OnLineporT = OnLinePorTs.split(":")
    ChaTiP , ChaTporT = ChaTPorTs.split(":")
    acc_name = LoGinDaTaUncRypTinG.AccountName
    equie_emote(ToKen,UrL)
    AutHToKen = await xAuThSTarTuP(int(TarGeT) , ToKen , int(timestamp) , key , iv)
    ready_event = asyncio.Event()
    task1 = asyncio.create_task(TcPChaT(ChaTiP, ChaTporT , AutHToKen , key , iv , LoGinDaTaUncRypTinG , ready_event ,region))
    task2 = asyncio.create_task(TcPOnLine(OnLineiP , OnLineporT , key , iv , AutHToKen))
    os.system('clear')
    print("Initializing Starexx!")
    print("----------------------------------------")
    time.sleep(0.5)
    os.system('clear')
    print("Connecting to Free Fire Server!")
    print("----------------------------------------")
    time.sleep(0.5)
    os.system('clear')
    print(f"{acc_name} is now online")
    print("----------------------------------------")
    print(f"Activity logs for {TarGeT}\n")
    await asyncio.gather(task1, task2)
    time.sleep(0.5)
    os.system('clear')
    await ready_event.wait()
    await asyncio.sleep(1)
    os.system('clear')
    print(render('STAREXXs', colors=['white', 'green'], align='center'))
    print('')

def handle_keyboard_interrupt(signum, frame):
    print("Thanks for using Starexx bot!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_keyboard_interrupt)

async def StarTinG():
    while True:
        try:
            await asyncio.wait_for(MaiiiinE() , timeout = 7 * 60 * 60)
        except KeyboardInterrupt:
            print("Thanks for using Starexx bot!")
            break
        except asyncio.TimeoutError: print("Token Expired, Restarting")
        except Exception as e: print(f"Error {e} | Restarting")

if __name__ == '__main__':
    threading.Thread(target=start_insta_api, daemon=True).start()
    asyncio.run(StarTinG())
