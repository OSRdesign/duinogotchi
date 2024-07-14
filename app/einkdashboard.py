#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import epd2in13_V4
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import subprocess
import socket
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen 
import random
import cfscrape #pip install cfscrape
import threading
import faces

epd = epd2in13_V4.EPD()
epd.init()
epd.Clear(0xFF)

user = 'user'
miners = []
avrport = []
startbal = 0
tempbal = 0
nowbal = 0
start_shares = 0
temp_shares = 0
quote = []
quote2 = [""]
myface = []
sec = 0
warning = 0
cpu_temp_value = 0.0
# Read the username from the config file

with open("quotes2.txt") as moodfile:
    moodlines = moodfile.readlines()
    
#modify this path to reflect your actual user folder)    
with open("/home/osrde/duino-coin/Duino-Coin AVR Miner 4.0/Settings.cfg") as config_file:
    lines = config_file.readlines()
    for line in lines:
        # check if string present on a current line
        if line.find('username = ') != -1:
            user1 = line.replace('username = ','')
            user = user1.strip()
            print(user)
            for i in range(0,5):
                quote.append(f"Hello {user}")
                myface.append(f"{faces.GRATEFUL}")
        else:
            pass

    for line in lines:
        # check if string present on a current line
        if line.find('identifier = ') != -1:
            miners1 = line.replace('identifier = ','')
            miners = [s.strip() for s in miners1.split(',')]
            print(miners)
            miners2 = ", ".join(miners)
        else:
            pass
    for line in lines:
        # check if string present on a current line
        if line.find('avrport = ') != -1:
            avrport1 = line.replace('avrport =','')
            avrport = [t.strip() for t in avrport1.split(',')]
            print(avrport)
        else:
            pass

#Define the API URL
api_url = f"https://server.duinocoin.com/v3/users/{user}"
print(api_url)

# print(res)
def is_avr_connected():
    comcheck = all(os.path.exists(item) for item in avrport)
    return comcheck

def get_cpu_temperature():
    try:
        # Execute the vcgencmd command to get CPU temperature
        cpu_temp = os.popen("vcgencmd measure_temp").readline()
        return cpu_temp.replace("temp=", "").replace("'","°")
    except:
        return False


cpu_temperature = get_cpu_temperature()

def cpu_temp_warning():
    cpu_temp_value = 0.0
    if cpu_temperature is not False:
        cpu_temp_value = float(cpu_temperature.replace("°C",""))   
        print(cpu_temp_value)
        if 50 <= cpu_temp_value <= 69:
            if len(quote2):
                del quote2[0]
                quote2.append(f"It's hot in here: {cpu_temperature}")
            else:
                quote2.append(f"It's hot in here: {cpu_temperature}")
        elif cpu_temp_value >= 70:
            if len(quote2):
                del quote2[0]
                quote2.append("Im' too hot, heeeeelp!")
            else:
                quote2.append("Im' too hot, heeeeelp!")
        else:
            pass
    else:
        pass

def get_wifi_status():
    try:
        # Check if Wi-Fi is connected by pinging a known IP address
        subprocess.check_output(['ping', '-c', '1', '8.8.8.8'])
        return "WIFI OK"
    except subprocess.CalledProcessError:
        status = False
        quote.append("Not Connected")
        myface.append(faces.BROKEN)
        return "NET ERROR"
    
def get_hostname():
    return socket.gethostname()

def get_ip_address():
    try:
        # Get the IP address of the Wi-Fi interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.255.255.255', 1))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "127.0.0.1"

def is_avr_miner_running():
    global status
    try:
        # Check if the process associated with AVR_miner.py is running
        process_output = subprocess.check_output(['pgrep', '-f', 'AVR_Miner.py'])
        return len(process_output.strip()) > 0
    except subprocess.CalledProcessError:
        return False
    
if is_avr_miner_running():
    print("AVR_Miner.py is currently running.")
    for i in range(0,3):
        quote.append("yeah, active miner found!")
        myface.append(faces.SMART)
else:
    print("AVR_Miner.py is not running.")
    quote.append("I'm not mining...")
    myface.append(faces.BROKEN)

wifi_status = get_wifi_status()
piname = get_hostname()
ip_address = get_ip_address()



def myGetJson():
    global data
    threading.Timer(60.0, myGetJson).start()
    scraper = cfscrape.create_scraper()
    res = scraper.get(api_url).text
    data = json.loads(res)
    return data
    print(f"Balance: {data['result']['balance']['balance']} DUCO")
myGetJson()

def starting_balance():
    global startbal,start_shares
    startbal = int(data['result']['balance']['balance'])
    return startbal
    tempbal = startbal
    for entry in data['result']['miners']:
                if entry['identifier'] in miners:
                    start_shares += int(entry["accepted"])

class GetValue(object):
    def myValue(self):
        global data,shares,node,nowbal,warning
        node = " "
        accepted_value = 0
        rejected_value = 0
        shares = "A: -- | R: --"
        if is_avr_miner_running():
            node = " "
            shares = "A: -- | R: --"
            for entry in data['result']['miners']:
                if entry['identifier'] in miners:
                    accepted_value += entry["accepted"]
                    rejected_value += entry["rejected"]
                    current_node = entry["pool"]
                    print(f"Shares: {accepted_value}/{rejected_value}")
                    shares = f"A: {accepted_value} | R: {rejected_value}"
                    print(f"connected to :{current_node}")
                    node = f"{current_node}"
                else:
                    print("searching")
            nowbal = int(data['result']['balance']['balance'])
            warning = int(data['result']['balance']['warnings'])
        else:
            pass
# print(res)
# class
class MyClass(object):
    # method
    def myMethod(self):
        global temp_shares,start_shares,cpu_temp_value
        accepted_sum = 0
        identifiers_to_find = miners
        print(cpu_temp_value)
        for miner in data["result"]["miners"]:
            if miner["identifier"] in identifiers_to_find:
                accepted_sum += miner["accepted"]
#         while True:
        print(f"Sum of accepted values for identifiers {identifiers_to_find}: {accepted_sum}")
        if accepted_sum == start_shares:
            temp_shares = accepted_sum
            if len(quote):
                del quote[0]
            if len(myface):
                del myface[0]
            for i in range(0,2):
                quote.append("no shares reported, boring")
                myface.append(faces.DEMOTIVATED)
        elif accepted_sum <= start_shares:
            temp_shares = accepted_sum
            if len(quote):
                del quote[0]
            if len(myface):
                del myface[0]
            for i in range(0,2):
                quote.append("weird, something's wrong here.")
                myface.append(faces.INTENSE)
        elif accepted_sum >= temp_shares:
            if len(quote):
                del quote[0]
            if len(myface):
                del myface[0]
            report_shares = accepted_sum - temp_shares
            temp_shares = accepted_sum
            for i in range(0,2):
                quote.append(f"so cool, {report_shares} new shares")
                myface.append(faces.COOL)
        
            
            

class New_Duco_Mined(object):
    # method
    def NewDuco(self):
        global tempbal,startbal,nowbal,quote,myface,sec
        if is_avr_miner_running():
            sec = sec + 1
            if tempbal == 0:
                for i in range(0,3):
                    quote.append("warming up my chips!")
                    myface.append(faces.GRATEFUL)
                tempbal = startbal
                return tempbal
            elif nowbal == tempbal:
                if sec in range(0,15):
                    quote.append("hash hash baby")
                    N1 = faces.LOOK_R
                    N2 = faces.LOOK_L
                    N3 = faces.LOOK_R_HAPPY
                    N4 = faces.LOOK_L_HAPPY
                    items = [N1,N2,N3,N4]
                    randomface = random.choice(items)
                    myface.append(randomface)
                elif sec in range (16,30):
                    quote.append("mining for glory")
                    N1 = faces.UPLOAD
                    N2 = faces.UPLOAD1
                    N3 = faces.UPLOAD2
                    items = [N1,N2,N3]
                    randomface = random.choice(items)
                    myface.append(randomface)
                elif sec >= 31:
                    sec = 0
            elif nowbal == tempbal +1:
                if len(quote):
                    del quote[0]
                if len(myface):
                    del myface[0]
                for i in range(0,5):
                    quote.append("Yeah new duco mined!")
                    myface.append(faces.FRIEND)
                tempbal = nowbal
        else:
            if is_avr_miner_running() is False:
#                 print("AVR_Miner.py is not running.")
                if len(quote):
                    del quote[0]
                if len(myface):
                    del myface[0]
                quote.append("Oh no miner is not running")
                myface.append(faces.BROKEN)
                nowbal = "--"
            else:
                pass

myGetValue = GetValue()
myObject = MyClass()
newDuco = New_Duco_Mined()

def print_every_n_seconds(n=60):
    while True:
        print(time.ctime())
        myObject.myMethod()
        myGetValue.myValue()
        cpu_temp_warning()
        time.sleep(n)
    
thread = threading.Thread(target=print_every_n_seconds, daemon=True)

def print_every_n2_seconds():
    global nowQuote,nowQuote2,nowFace
    threading.Timer(1.1, print_every_n2_seconds).start()
    newDuco.NewDuco()
    if len(quote):
        nowQuote = quote[0]
        del quote[0]
    if len(quote2):
        nowQuote2 = quote2[0]
        del quote2[0]
    else:
        mood = random.choice(moodlines)
        for i in range(0,15):
            quote2.append(mood)
        nowQuote2 = quote2[0]
        del quote2[0]
    if len(myface):
        nowFace = myface[0]
        del myface[0]

    return nowQuote,nowQuote2,nowFace

try:
    thread.start()
    starting_balance()
    print(f"Wi-Fi Status: {wifi_status}")
    print(f"Hostname: {piname}")
    print(f"IP Address: {ip_address}")
    if cpu_temperature is not False:
      print(f"CPU Temperature: {cpu_temperature:}")
    else:
        print("Unable to retrieve CPU temperature.")
    print_every_n2_seconds()

    # Drawing on the image
    font10 = ImageFont.truetype(('DejaVuSansMono.ttf'), 10)
    font15 = ImageFont.truetype(('DejaVuSansMono.ttf'), 15)
    font24 = ImageFont.truetype(('DejaVuSansMono.ttf'), 24)
    face32 = ImageFont.truetype(('DejaVuSansMono.ttf'), 32)
    # partial update
    eink_image = Image.new('1', (epd.height, epd.width), 255)
    eink_draw = ImageDraw.Draw(eink_image)
    epd.displayPartBaseImage(epd.getbuffer(eink_image))
    num = 0
    
    
    while (True):
        eink_draw.rectangle((0, 0, 250, 122), fill = 255)
        eink_draw.text((0, 1), time.strftime('%H:%M:%S'), font = font10, fill = 0)
#         eink_draw.text((40, 0), (f"{piname}"), font = font10, fill = 0)
#         eink_draw.rectangle((80, 0, 250, 12), fill = 255)
        eink_draw.text((60, 1), (f"{wifi_status}"), font = font10, fill = 0)
        if is_avr_miner_running():
            eink_draw.text((125, 1), "MINER ON", font = font10, fill = 0)
        else:
             eink_draw.text((125, 1), "MINER OFF", font = font10, fill = 0)
             node = ""
             shares = "not mining"
        eink_draw.text((190, 1), ("CPU:"+ get_cpu_temperature()), font = font10, fill = 0)
        eink_draw.line([(0,13),(250,13)], fill = 0,width = 1)
        if warning != 0:
               eink_draw.text((125, 50), (f"{warning} WARNING"), font = font15, fill = 0)
        eink_draw.text((125, 35), (miners2), font = font10, fill = 0)
        eink_draw.text((5, 20), (nowFace), font = face32, fill = 0)
        eink_draw.text((5, 65), (nowQuote), font = font15, fill = 0)
        eink_draw.text((5, 85), (nowQuote2), font = font15, fill = 0)
        eink_draw.text((125, 20), (f"{nowbal} DUCO"), font = font10, fill = 0)
        eink_draw.line([(0,108),(250,108)], fill = 0,width = 1)
        eink_draw.text((2, 110), (node), font = font10, fill = 0)
        eink_draw.text((80, 110), (shares), font = font10, fill = 0)
        if is_avr_connected():
            eink_draw.text((190, 110), ("COM OK"), font = font10, fill = 0)
        else:
            eink_draw.text((190, 110), ("COM ERROR"), font = font10, fill = 0)
        if num == 3600:
            epd.display(epd.getbuffer(eink_image))
            num = 0
        else:
            epd.displayPartial(epd.getbuffer(eink_image))
        num = num + 1
        
    epd.init()
    epd.Clear(0xFF)
    epd.sleep()
            
except KeyboardInterrupt:    
    epd2in13_V4.epdconfig.module_exit(cleanup=True)
    exit()
