#author malik
import csv
import os
import time
import re
import requests
import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(ChromeDriverManager().install())

def login_and_access_user_accounts(email, password, user_urls, folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
    except:
        pass
    os.chdir(os.path.join(os.getcwd(), folder))

    driver.get("https://www.strava.com/login")

    email_field = driver.find_element_by_id("email")
    email_field.send_keys(email)
    password_field = driver.find_element_by_id("password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)  

    time.sleep(3)  
    data = []
    i = 1
    for user_url in user_urls:
        driver.get(user_url)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        Contents = soup.find_all('div' , class_="react-feed-container simple")
        fields = ['id','name', 'likes', 'distance']
        
        for content in Contents:
            con = content.find_all('div',class_='------packages-feed-ui-src-components-media-Card-Card__feed-entry--WKvAQ ------packages-feed-ui-src-components-media-Card-Card__card--dkL_L')
            for con1 in con:
                images1 = con1.find_all('img',class_=re.compile(r'packages-feed-ui-src-components-PhotosAndMapImage-PhotosAndMapImage.*'))
                rdata1 = con1.find_all('button', class_='------packages-ui-Button-Button-module__btn--mQaJJ ------packages-ui-Button-Button-module__text--c1xAA ------packages-feed-ui-src-components-KudosAndComments-KudosAndComments__count-button--xEA22')
                names = con1.find_all('div' , class_='------packages-feed-ui-src-components-HeaderWithOwnerMetadata-HeaderWithOwnerMetadata-module__nameBoosted--ejkqR')
                distances = con1.find_all('div' , class_='------packages-ui-Stat-Stat-module__statValue--phtGK') 
                for image, r1, uname, distance in zip(images1, rdata1, names, distances):
                   if 'src' in image.attrs:
                       name = image.get('alt', 'Unnamed')
                       temp_name = name.strip().replace(' ', '_') 
                       if name.strip() and name != 'Malik shameer' and name != 'Unnamed':
                           link = image['src']
                           r = r1.text.split('\xa0')[0]
                           filename = f"{str(i)}_Image_{uname.text}_Image_{temp_name}_{r}_{distance.text}.jpg"
                           data.append([i,uname.text,r,distance.text])
                           #if not os.path.exists(folder):
                            #os.makedirs(folder)
                           try:
                                with open(filename, 'wb') as f:
                                    im = requests.get(link)
                                    f.write(im.content)
                                    print('Writing:', name)
                           except Exception as e:
                                print(f"Error occurred while writing {filename}: {e}. Skipping...")
                                continue              
            time.sleep(1)   
        i+=1    
        time.sleep(1) 
    print(data)
    with open('file.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            for row in data:
                writer.writerow(row) 
    driver.quit()
gmail_email = ""
gmail_password = ""
strava_user_urls = ['https://www.strava.com/athletes/269248', 
                    'https://www.strava.com/athletes/123456',
                    'https://www.strava.com/athletes/38546535',
                    'https://www.strava.com/athletes/28695480',
                    'https://www.strava.com/athletes/3780658',
                    'https://www.strava.com/athletes/2835001',
                    'https://www.strava.com/pros/733569',
                    'https://www.strava.com/athletes/3352833',
                    'https://www.strava.com/athletes/26406496',
                    'https://www.strava.com/athletes/8675445',
                    'https://www.strava.com/pros/2620163',
                    'https://www.strava.com/athletes/25632508',
                    'https://www.strava.com/athletes/34778940',
                    'https://www.strava.com/athletes/17320052',
                    'https://www.strava.com/athletes/18758177',
                    'https://www.strava.com/athletes/17341838']
folderNametime = f'strava_data{datetime.datetime.now().strftime("%Y%H%M%S")}'
login_and_access_user_accounts(gmail_email, gmail_password, strava_user_urls, folderNametime)
