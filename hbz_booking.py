from time import sleep
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from sys import exit
from os import path
import datetime
import platform
import configparser

def getconfig(want_to_change=False):
    """Get user data from ini file"""
    config = configparser.ConfigParser()

    if path.exists('userdata.ini'):
        config.read('userdata.ini')
        if want_to_change:
            complete = False
        else:
            complete = True
        for el in config['userdata']:
            if config['userdata'][el] == '':
                complete = False
                print(f'Parameter {el} is undefined!')
    else:
        complete = False

    while not complete:
        print('Please complete your data.')
        makeconfig(config)
        complete = True
        for el in config['userdata']:
            if config['userdata'][el] == '':
                complete = False
                print(f'Parameter {el} is undefined!')
    
    return config


def makeconfig(config):
    config['userdata'] = {}
    data = config['userdata']

    time = input('At what hour do you want to start your reservation? Type your reply below and press enter. (format: hh, e.g. 10)\nresponse: ')#.split('.')
    data['start_h'] = time
    #data['start_m'] = time[1]

    time2 = input('At what hour do you want to end your reservation? (format: hh, e.g. 18)\nresponse: ')#.split('.')
    data['end_h'] = time2
    #data['end_m'] = time2[1]

    d = datetime.date.today() + datetime.timedelta(days=8)
    in_a_week = input(f'Do you want to reserve in a week, i.e. the {d}? (yes/no)\nresponse: ').strip('"')
    if in_a_week == 'yes':
        data['date'] = str(d)
    else:
        date = input('Which day then? (format: YYYY-MM-DD, e.g. 2021-05-12)\nresponse: ')
        data['date'] = str(date)

    wait = input('Do you want the program to wait and reserve at midnight? This is necessary if your replied "yes" to the question before! (yes/no)\nresponse: ').strip('"').lower()
    if wait == 'yes':
        data['wait_till_midnight'] = 'True'
    elif wait == 'no':
        data['wait_till_midnight'] = 'False'

    library = input('Please enter the library you want, as shown on the website (e.g. "Hauptbibliothek - Lernzentrum")\nresponse: ')
    data['library'] = library

    seat = input('Please enter the table you want, (e.g. "HBZ-L/424")\nresponse: ')
    data['table_id'] = seat

    facs = {'MeF': '2', 'MNF': '3', 'PhF': '4', 'RWF': '5', 'ThF': '6', 'VSF': '7', 'WWF': '8', 'ZDU': '9'}
    fac = None
    while fac not in facs.keys():
        print('Please enter your faculty. Possibilities: ', end='')
        for k in facs.keys():
            print(k, end='  ')
        fac = input('\nresponse: ')
    data['faculty_nr'] = facs[fac]

    data['email'], data['psw'] = get_credentials()

    # if save_psw == 'yes':
    #     data['psw'] = psw
    # elif save_psw == 'no':
        

    print('\n\n')

    with open('userdata.ini', 'w') as f:
        config.write(f)


def get_credentials():
    print('\nYour credentials will be saved locally in userdata.ini.')
    email = input('Please enter your UZH email address:\nresponse: ')
    psw = input('Please enter your password:\n')
    # save_psw = input('Do you want to save your password? (yes/no)\nresponse: ').lower()
    
    return email, psw #, save_psw
    

def setdriver():
    """Determines system's OS and sets the right chromedriver"""
    system = platform.system()
    system_suffixes = {
        'win32' : '.exe',
        'Darwin' : '_mac',
        'Linux' : '_linux'
    }
    try:
        system_suffix = system_suffixes[system]
        bro = webdriver.Chrome(f'drivers/chromedriver{system_suffix}')
    except:
        print('The browser wasn\t found or couldn\'t be opened, e.g. due to MacOS security settings --> check the installation instructions. Exiting the program...')
        exit()
    
    return bro

def login(bro, config):
    """Login to website"""
    link_login = "https://hbzwwws005.uzh.ch/booked-ubzh/Web/index.php"
    bro.get(link_login)

    WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="email"]')))

    bro.find_element_by_xpath('//*[@id="email"]').send_keys(config['userdata']['email'])
    bro.find_element_by_xpath('//*[@id="password"]').send_keys(config['userdata']['psw'])
    bro.find_element_by_xpath('//*[@id="login-box"]/div[4]/button').click()


# Reservation
def reserve(bro, config, debug=False):
    WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="reservations"]/table/tbody')))
    sleep(1)
    bro.execute_script("window.scrollTo(0,0)")
    sleep(1)
    #WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="select2-schedules-container"]')))
    bro.find_element_by_xpath('//*[@id="select2-schedules-container"]').click()
    
    WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="reservations"]/table/tbody')))
    sleep(0.5)
    try:
        library = bro.find_element_by_xpath(f'//li[contains(text(), "{config["userdata"]["library"]}")]')
        library_id = int(library.get_attribute('id')[-2:])
        library.click()
    except exceptions.NoSuchElementException:
        print('The given library ID couldn\'t be found, please check if you wrote it correctly.')
        bro.close()
        exit()

    WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="reservations"]/table/tbody')))
    sleep(0.5)

    try:
        path = f'//*[@id="reservations"]/table/tbody/tr/td/a[contains(text(), "{config["userdata"]["table_id"]}")]'
        table = bro.find_element_by_xpath(path)
        table_id = int(table.get_attribute('resourceid'))
    except exceptions.NoSuchElementException:
        print('The given table ID couldn\'t be found, please check if you wrote it correctly.')
        bro.close()
        exit()

    link_res = f"https://hbzwwws005.uzh.ch/booked-ubzh/Web/reservation.php?rid={table_id}&sid={library_id}&rd={config['userdata']['date']}&sd={config['userdata']['date']}%20{config['userdata']['start_h']}%3A00%3A00&ed={config['userdata']['date']}%20{config['userdata']['end_h']}%3A00%3A00"  
    bro.get(link_res)

    WebDriverWait(bro, 10).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="psiattribute5"]')))
    sleep(1)
    bro.find_element_by_xpath('//*[@id="psiattribute5"]').click()
    bro.find_element_by_xpath(f'//*[@id="psiattribute5"]/option[{config["userdata"]["faculty_nr"]}]').click()
    bro.find_element_by_xpath('//*[@id="termsAndConditions"]/div/div/label').click()

    if not debug:
        bro.find_element_by_xpath('//*[@id="form-reservation"]/div[5]/div/div/button[2]').click()
    sleep(5)


def wait_till(hour, minutes=0, seconds=0, year=datetime.datetime.today().year, month=datetime.datetime.today().month, day=datetime.datetime.today().day):
    """ Wait until a certain time, or a specific date and time."""

    d = datetime.datetime.today()
    d2 = datetime.datetime(year, month, day, hour, minutes, seconds)

    if d2 < d:
        print('Adding one day')
        d2 += datetime.timedelta(days=1)

    print(f'Waiting until {d2}... Please keep the terminal open and your computer on, and don\'t let it go to sleep before then.')
    sleep((d2-d).total_seconds())


# main function
def main():

    want_to_change = False
    configured = False
    while not configured:
        print('\n-----------------------------------------------')
        print('Welcome to the HBZ reservations bot!')
        print('-----------------------------------------------')
        print('The reservation will be made with the following\nparameters from the "userdata.ini" file:\n')
        
        config = getconfig(want_to_change)
        for el in config['userdata']:
            if el == 'psw':
                print(f'{el}:  {"*" * len(config["userdata"][el])}')
            else:
                print(f'{el}:  {config["userdata"][el]}')

        print('\n-----------------------------------------------')
        res = input('Do you want to proceed with these parameters?\nType yes or no and press enter.\n\nresponse: ')
        
        if res == 'yes' or res == 'y' or res == '':
            configured = True
        else:
            want_to_change = True
        

    # Wait till midnight
    if(config['userdata']['wait_till_midnight'] == 'True'):
        print('Testing if the automated browser works... ', end='')
        bro = setdriver()
        bro.close()
        print('success.')
        wait_till(23, 59, 55)
        print(f'Starting reservation.')

    bro = setdriver()
    login(bro, config)
    reserve(bro, config)
    bro.close()

# Run everything
if __name__ == "__main__":
    main()