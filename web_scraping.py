import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

def get_currencies(currencies, start, end, export_csv):
    frames = []
    option = Options()
    option.headless = False
    driver = webdriver.Chrome(executable_path = "C:/Users/User/Desktop/chromedriver.exe", options=option)

    for currency in currencies:
        data_scraped = False
        while data_scraped == False:
            try:
                #Opening the connection and obtaining the page
                url = f'https://www.investing.com/currencies/usd-{currency.lower()}-historical-data'
                driver.get(url)
                driver.maximize_window()
            
                #Clicking the date button
                date_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, \
                "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))

                date_button.click()

                #Sending the start date
                start_bar = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, \
                "/html/body/div[7]/div[1]/input[1]")))

                start_bar.clear()
                start_bar.send_keys(start)

                #Sending the end date
                end_bar = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, \
                "/html/body/div[7]/div[1]/input[2]")))

                end_bar.clear()
                end_bar.send_keys(end)

                #Clicking the apply button
                apply_button = WebDriverWait(driver, 200).until(EC.element_to_be_clickable((By.XPATH, \
                "/html/body/div[7]/div[5]/a")))

                apply_button.click()
                sleep(5)

                #Getting tables on the page and exiting
                dataframes = pd.read_html(driver.page_source)
                driver.quit()
                print(f'{currency} scraped.')

                data_scraped = True
            except:
                driver.quit()
                print(f"Failed to scrape {currency}. Trying again in 30 seconds")
                sleep(30)
                continue

        # Selecting the correct table
        print("Dataframe extraction...")
        sleep(1)           
        for dataframe in dataframes:
            if dataframe.columns.tolist() == ['Date', 'Price', 'Open', 'High', 'Low', 'Change %']:
                df = dataframe
                frames.append(df)

                # Exporting the .csv file
                if export_csv:
                    print("Exporting to csv...")
                    df.to_csv(f'{currency.upper()}.csv', index=False)
                    sleep(3)
                    print(f'{currency}.csv exported.')

                break
                  
    return frames

get_currencies(['inr'], "12/31/2020", "01/15/2021", True)