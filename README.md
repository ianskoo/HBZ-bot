# HBZ-bot
## About
This is a Python bot which automatically reserves a desired study table at one of the HBZ's libraries in Zürich.

## Installation and first start
### MacOS
1. Download and install Python 3 from its official website:  
https://www.python.org/downloads/

2. Download and install Chrome from its official page:  
https://www.google.com/chrome/

3. Download the program using the green Code button above, download it as a zip file and decompress it where you want.

4. Open the terminal, an app included with MacOS. You can search it in the search bar. In the terminal, type:  
`cd `  
with a space after it, then drag and drop with the mouse the unzipped HBZ-bot-main folder into the terminal. Then, press enter. 

5. In the terminal, copy and paste the following, then press enter:  
`pip3 install selenium`

6. Finally, run the program with:  
`python3 hbz_booking.py`

7. If the program gives an error, check if there's a security warning from MacOS for the chromedriver. If so, go to MacOS settings --> Security and Privacy --> General, and check the checkbox to allow the chromedriver to run. Then, repeat step 6.

### Windows
1. Download and install Python 3 from its official website:  
https://www.python.org/downloads/

2. Download and install Chrome from its official page:  
https://www.google.com/chrome/

3. Download the program using the green Code button above, download it as a zip file and decompress it where you want.

4. Open the Windows command prompt and type:
`cd `
with a space afterwards, then drag and drop the unzipped downloaded folder into the cmd prompt, and press enter. You should now see that the path in the command prompt changed to the one of the bot's folder.

5. Type `pip install selenium` in the cmd prompt. It should download some packages for Python.

6. Finally, run the program with:  
`python3 hbz_booking.py`

## Usage
### MacOS and Windows
To run the app after the first time, repeat steps 4 and 7 from the installation part (temporary solution).

After starting the app for the first time (following steps 4 and 7 from the installation), you will be asked to reply to a series of questions about your desired reservation. This info will be then saved for the next time in the userdata.ini file, which will be in the same folder of the app. You can also change your preferences directly in this file with a text editor (Textedit), before opening the app again.

## Suggestions for improvement and bug reports

Suggestions for improvement are welcome. Ask me directly if you know me :) or open an issue here on GitHub by selecting the "issues" tab above, and selecting the right label on the right.

If the app works for you and you like it, let me know as well!

## Disclaimer
Use this bot at your own risk.

The terms of service of the HBZ's booking website don't state anything about the use of bots/automation programs (I would guess they haven't thought about the possibility), but for my safety I cannot accept any responsibility for any ripercussions you may have from using this app.
