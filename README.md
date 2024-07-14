# Duinogotchi
Duino coin virtual pet project.
## About / Intro
I'm not a dev at all and did this project as an hobby, it helped me to get into python and is provided as is.
the structure of the code, logic applied or even functions ordering are for sure not optimized yet. feel free to take it and change it.
my goal was to make a small miner based on a former pwnagotchi HW. 
commercial use of any material based on the following project is not allowed. If this project use material not credited or copyrighted accordingly let me know to fix it.

## Before you start:
Duinogotchi is a companion app to work with an already working Duino-Coin mining setup based on raspberry pi with either Arduino or RP2040 connected by USB.
so far tested and wroking on Rpi4B, Rpi5 and Rpi zero 2W but **not working on Rpi Zero W**
it's completely inspired from the screen rendering of Pwnagotchi and the "faces.py" is a actually a simple copy from the amazing team behind this porject.
visit them here if you want to know more: https://pwnagotchi.org/

**to get there you'll need:**

-an account and verified to mine the fantastic Duino-Coin :https://duinocoin.com/
-a mining rig setup based on raspberry pi + arduino or rp2040
-a waveshare eink 2.13inch display HAT V3 or V4 : https://www.waveshare.com/product/2.13inch-e-paper-hat.htm
-screen (sudo apt install screen, comprehensive tutorial here: https://linuxize.com/post/how-to-use-linux-screen/)
-SSH access to your Rpi

you will need to follow the setup of the eink screen as described in the wiki:
https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT_Manual#Working_With_Raspberry_Pi
go though all steps for pyhton and test your screen.
This ensure that all necessary files and python environement is working.

## What's Duinogotchi
Duinogotchi is virtual pet lookalike interface dedicated to display important information of your mining set.
For this the script will read from your duino-coin folder the setting file to retrieve your username, miner(s) name(s), list of USB/COM ports used.
With this duinogotchi wil use the duco rest API (v3) (details available here: https://github.com/revoxhere/duco-rest-api)

**Duinogotchi will only monitor the miners connected to the raspberry pi.**

![duinogotchiUI](https://github.com/user-attachments/assets/b75ee297-3f00-49ce-ba53-ee0f24f906e7)

## How to use Duinogotchi

### Requirements
  the following are need to use duinogotchi:
      epd2in13_V4.py (included in /app/)
      epdconfig.py (included in /app/)
      time
      PIL (should be added when setting up the screen)
      urllib (pip install urllib)
      cfscrape (pip install cfscrape) I had to use this to connect to the API otherwise I was blocked by cloudfare.
      faces.py (included in /app/)
      quotes2.txt (incluced in /app/)
      
### things that you need to change in the einkdashboard.py file
  in einkdashboard.py, I could not manage yet to get the script to look automatically for the duino-coin folder so you need to chnage the path for your actual where the AVR_Miner.py is located.
it's on line 44 "/home/your username/duino-coin/Duino-Coin AVR Miner 4.0/Settings.cfg"

### use SSH & SCREEN 
  log to your Rpi over SSH
  send the screen commande
  accept and now you can open the folder of the app i.e cd /app/
  and launch the script with : pyhton3 einkdashboard.py
  and voilà screen should start to flicker first and your duinogotchi should come to life.
  if all good simply ctrl+A then ctrl+D to go back to your previous shell.

## Known bugs/issue (help needed)

  - manual entry of the duino-coin folder needed.
  - tend to crash after 3-4 days, I suspect the threading causing this.
  - lantency, because of it's API based nature, duinogotchi is not real time and fully dependant on the API availability.

  
