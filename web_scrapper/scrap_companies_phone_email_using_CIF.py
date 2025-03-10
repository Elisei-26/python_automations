import undetected_chromedriver as uc
import time
import csv
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--user-data-dir=/path/to/new/profile")

driver = uc.Chrome(options=options)
driver.get('https://targetare.ro/cauta-firme?state=eyJxdWVyeSI6IiIsImZpbHRlcnMiOlt7ImlkZW50aWZpZXIiOiJzdGF0dXMiLCJ2YWx1ZSI6ImZ1bmN0aXVuZSJ9LHsiaWRlbnRpZmllciI6Imhhc1Bob25lIiwidmFsdWUiOiJkYSJ9XSwicGFnZSI6eyJzaXplIjoxMCwiZnJvbSI6MH0sInNvcnRCeSI6IiJ9')
driver.maximize_window()

# Remove existing user profile to clear all data
shutil.rmtree("https://targetare.ro/cauta-firme?state=eyJxdWVyeSI6IiIsImZpbHRlcnMiOlt7ImlkZW50aWZpZXIiOiJzdGF0dXMiLCJ2YWx1ZSI6ImZ1bmN0aXVuZSJ9LHsiaWRlbnRpZmllciI6Imhhc1Bob25lIiwidmFsdWUiOiJkYSJ9XSwicGFnZSI6eyJzaXplIjoxMCwiZnJvbSI6MH0sInNvcnRCeSI6IiJ9", ignore_errors=True)

# Path to your CSV file
input_file = "cifs_for_search.tsv"
output_file = "resulted_file.tsv"

# Open and read the CSV file
with open(input_file, mode='r') as infile, open(output_file, mode="w", newline="") as outfile:
    csv_reader = csv.reader(infile, delimiter='\t')
    csv_writer = csv.writer(outfile, delimiter='\t')

    # Iterate over each line in the CSV
    for row in csv_reader:
        # Save the first element of each line in a variable
        first_element = row[0]
        phoneNumber = '*'
        emailAddress = '*'
        # Clear cache and cookies
        driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
        driver.delete_all_cookies()
        try:
            input_field = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, "(//input)[2]"))
            )
            input_field.send_keys(first_element)
            input_field.send_keys(Keys.CONTROL + "a")  # Select all text
            input_field.send_keys(Keys.BACKSPACE)  # Delete selected text
            input_field.send_keys(first_element)
            time.sleep(1)
            input_field.send_keys(Keys.RETURN)
            time.sleep(1)

            try:
                h2Element = WebDriverWait(driver, 3).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[3]/div[1]/h2'))
                )
                driver.execute_script("arguments[0].scrollIntoView();", h2Element)

                button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Arată date de contact"]')
                time.sleep(1)
                button.click()
                try:
                    try:
                        phoneElement = WebDriverWait(driver, 2).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[1]/a'))
                        )
                        phoneNumber = phoneElement.text
                    except Exception as e:
                        driver.refresh()
                        time.sleep(1)
                        button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Arată date de contact"]')
                        button.click()
                        phoneElement = WebDriverWait(driver, 2).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[1]/a'))
                        )
                        phoneNumber = phoneElement.text
                    print(phoneNumber)
                except Exception as e:
                    phoneElement = WebDriverWait(driver, 1).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[1]'))
                    )
                    phoneNumber = phoneElement.text
                    print(phoneNumber)
                try:
                    try:
                        emailElement = WebDriverWait(driver, 2).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[2]/a'))
                        )
                        emailAddress = emailElement.text
                    except Exception as e:
                        driver.refresh()
                        time.sleep(1)
                        button = driver.find_element(By.CSS_SELECTOR, '[aria-label="Arată date de contact"]')
                        button.click()
                        emailElement = WebDriverWait(driver, 2).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[2]/a'))
                        )
                        emailAddress = emailElement.text
                except Exception as e:
                    emailElement = WebDriverWait(driver, 1).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[2]'))
                    )
                    emailAddress = emailElement.text
                    print(emailAddress)
            except Exception as e:
                phoneElement = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[1]'))
                )
                phoneNumber = phoneElement.text
                emailElement = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__next"]/div[3]/div[3]/div[11]/div[1]/dl/dd[2]'))
                )
                emailAddress = emailElement.text
                print(f"Scrolling and see button error")
            row.append(phoneNumber)
            row.append(emailAddress)
            csv_writer.writerow(row)

            try: # verifica daca se afla in pagina in care trebuie inainte sa dea back
                input_field = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, "(//input)[2]"))
                )
            except Exception as e:
                driver.back()
                print(f"Driver is in expected page")
        except Exception as e:
            row.append(phoneNumber)
            row.append(emailAddress)
            csv_writer.writerow(row)
            print(f"Error finding input for CIF")
print("Finished successfully")
