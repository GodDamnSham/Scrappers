import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

def scrape_reviews(url, driver, csv_writer, unique_reviews):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.uqMDf.z.BGJxv.xOykd.jFVeD.yikFK")))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        contents = soup.find_all('div', class_="uqMDf z BGJxv xOykd jFVeD yikFK")
        
        for content in contents:
            con = content.find_all('div', class_='azLzJ MI R2 Gi z Z BB kYVoW tpnRZ')
            for con1 in con:
                names = con1.find_all('a', class_='MjDLG VKCbE')
                dates = con1.find_all('span', class_='sIZXw S2 H2 Ch d')
                stay_dates = con1.find_all('span', class_='iSNGb _R Me S4 H3 Cj')
                reviews = con1.find_all('span', class_='orRIx Ci _a C')
                for name, date, stay_date, review in zip(names, dates, stay_dates, reviews):
                    reviewer_name = name.text.strip()
                    stay_year = None
                    date_of_stay_text = stay_date.find(text='Date of stay:')
                    if date_of_stay_text:
                        stay_year = int(stay_date.text.strip().split()[-1])
                    review_comment = review.text.strip()
                    if stay_year is not None and stay_year >= 2017:
                        if review_comment not in unique_reviews:
                            csv_writer.writerow([url, reviewer_name, stay_year, review_comment])
                            unique_reviews.add(review_comment)
    except Exception as e:
        print("Error while scraping:", e)

path_to_file = "/Users/malik/Desktop/reviews.csv"

urls = [
    "https://www.tripadvisor.com/Hotel_Review-g150807-d154429-Reviews-Smart_Cancun_The_Urban_Oasis-Cancun_Yucatan_Peninsula.html",
    "https://www.tripadvisor.com/Hotel_Review-g150807-d23738165-Reviews-Hilton_Garden_Inn_Cancun_Airport-Cancun_Yucatan_Peninsula.html",
    "https://www.tripadvisor.com/Hotel_Review-g150807-d17793092-Reviews-Mex_Hoteles-Cancun_Yucatan_Peninsula.html"
]

# Open CSV file for writing
with open(path_to_file, 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Hotel', 'Reviewer Name', 'Stay Year', 'Review Comment'])
    unique_reviews = set() 
    
    # Initialize WebDriver 
    #driver = webdriver.Chrome(ChromeDriverManager().install())
    driver =  webdriver.Safari()
    for url in urls:
        driver.get(url)
        while True:
            time.sleep(5)  
            scrape_reviews(url, driver, csv_writer, unique_reviews)
            try:
                next_button = driver.find_element(by=By.CSS_SELECTOR, value='#lithium-root main div.mXiGB > div > div:nth-child(3) > div:nth-child(1) > div > div > div:nth-child(1) > div:nth-child(3) > div.ruCQl > div.uqMDf > div:nth-child(n) div.OvVFl > div.xkSty > div > a')
                next_button.click()
            except Exception as e:
                print("Error while clicking next button:", e)
                break  
            time.sleep(3)  

print("Data has been saved to:", path_to_file)

# Close the webdriver
driver.quit()
