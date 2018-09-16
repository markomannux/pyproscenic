#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from socket import *
import base64


class Proscenic(object):
    commands = {
    'STOP': 'AA55A55A0DFDE20906000100030000000000',
    'RUN': 'AA55A55A0DFDE20906000100020000000100',
    'DOCK': 'AA55A55A0FFDE20906000100010000000000'
    }

    def __init__(self, serial=None, port=10684):
        self.serial = serial

    def generate_message_body(command):
        transit_info = ET.Element('TRANSIT_INFO')
        ET.SubElement(transit_info, 'COMMAND').text = 'ROBOT_CMD'
        ET.SubElement(transit_info, 'RTU').text = commands[command]
        return ET.tostring(transit_info)

    def exec_command(command):
        if self.serial != "" and command != "":

            cs = socket(AF_INET, SOCK_DGRAM)
            cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

            message = ET.Element("MESSAGE", Version="1.0")
            ET.SubElement(message, "HEADER", MsgType="MSG_TRANSIT_SHAS_REQ", MsgSeq="1", From="020000000000000000", To=self.serial, Keep="0")
            ET.SubElement(message, "BODY").text = base64.b64encode(generate_message_body(command)).decode('ascii')

            cs.sendto(ET.tostring(message, encoding='utf8', method='xml'), ('255.255.255.255', 10684))

    def run_service():
        exec_command('RUN')
    
    def stop_service():
        exec_command('STOP')

    def dock_service():
        exec_command('DOCK')