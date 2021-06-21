'''
--------------------------------------------------
'''

# Commands :

SET_TILE = "/tile"

SET_COLOR = "/color"

RESET = "/reset"

'''
--------------------------------------------------
'''

import sys

from g_python.gextension import Extension
from g_python.hmessage import Direction

extension_info = {
    "title": "Beret",
    "description": "Walk to the furni when its your turn",
    "version": "2.0",
    "author": "Lande"
}

ext = Extension(extension_info, sys.argv)
ext.start()


wait = False
id_furni = ""
x_coord = ""
y_coord = ""
color = ""


def speech(msg):
    global wait, color

    text, _, _ = msg.packet.read('sii')

    if text == SET_TILE:
        msg.is_blocked = True
        wait = True
        talk('Double click on the furni')

    if text.startswith(SET_COLOR):
        msg.is_blocked = True
        is_int = text[len(SET_COLOR)+1:]
        try:
            color = int(is_int)
            talk(f'Color set to : {color}')
        except ValueError:
            talk('Only number available')

    if text == RESET:
        msg.is_blocked = True
        reset(0)
        talk('•')


def update_furni(msg):
    idd, _, state = msg.packet.read('sis')

    if idd == str(id_furni):
        if state == str(color):
            ext.send_to_server('{out:MoveAvatar}{i:'+str(x_coord)+'}{i:'+str(y_coord)+'}')


def spawn_bot(msg):
    ext.send_to_client('{in:Users}{i:1}{i:1234567890}{s:"[BOT]&#0;"}{s:"By Lande"}{s:"hd-3092-25.he-3082-93.hr-828-61.fa-3344-110.sh-3275-110.lg-3216-110.ch-255-110"}{i:0}{i:0}{i:0}{s:"1000.0"}{i:0}{i:4}{s:"0"}{i:25297484}{s:"Lande"}{i:0}{b:false}{b:false}{i:0}{i:0}{i:0}{i:0}{i:0}')


def talk(txt):
    ext.send_to_client('{in:Chat}{i:0}{s:" '+txt+'"}{i:0}{i:30}{i:0}{i:0}')


def reset(msg):
    global wait, id_furni, x_coord, y_coord, color

    wait = False
    id_furni, x_coord, y_coord, color = "", "", "", ""


def set_furni(msg):
    global id_furni, wait

    if wait:
        msg.is_blocked = True
        id_furni, _ = msg.packet.read('ii')
        talk(f"Id set to : {id_furni}, coord : {x_coord}x {y_coord}y")
        wait = False


def set_walk(msg):
    global x_coord, y_coord

    if wait:
        msg.is_blocked = True
        x_coord, y_coord = msg.packet.read('ii')


ext.intercept(Direction.TO_SERVER, speech, 'Chat')
ext.intercept(Direction.TO_CLIENT, spawn_bot, 'RoomEntryInfo')
ext.intercept(Direction.TO_SERVER, reset, 'GetGuestRoom')
ext.intercept(Direction.TO_SERVER, set_furni, 'UseFurniture')
ext.intercept(Direction.TO_SERVER, set_walk, 'MoveAvatar')
ext.intercept(Direction.TO_CLIENT, update_furni, 'ObjectDataUpdate')
