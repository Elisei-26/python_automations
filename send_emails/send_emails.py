import undetected_chromedriver as uc
import time
import csv
import shutil
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = uc.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
options.add_argument("--user-data-dir=/path/to/new/profile")

driver = uc.Chrome(options=options)
driver.get('https://workspace.google.com/intl/en-US/gmail/')
driver.maximize_window()

# Remove existing user profile to clear all data
shutil.rmtree("https://workspace.google.com/intl/en-US/gmail/", ignore_errors=True)
driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
driver.delete_all_cookies()

with open("credentials.txt", "r") as file:
    lines = file.readlines()  # Read all lines into a list
email = lines[0].strip()  # First line is the email
password = lines[1].strip() if len(lines) > 1 else ""  # Second line is the password (if it exists)

try: # full log in
    sign_in_button = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div[1]/header/div/div[5]/a[2]/span'))
    )
    sign_in_button.click()
    email_input = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="identifierId"]'))
    )
    email_input.send_keys(email)
    time.sleep(1)
    button_next = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="identifierNext"]/div/button/span'))
    )
    button_next.click()

    email_input.send_keys(Keys.RETURN)

    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
except Exception as e:
    print("Must execute partial log in")

try: # partial log in
    sign_in_button = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/form/span/section/div/div/div/div/ul/li[1]/div/div[1]/div/div[2]/div[1]'))
    )
    sign_in_button.click()
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'))
    )
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
except Exception as e:
    print ("Full log in executed")

# Path to your CSV file
input_file = "email_addresses.tsv"
output_file = "sent_emails_status.tsv"
pdf_path = r"C:\Automatizare_Email-uri_Demo.pdf"

# Open and read the CSV file
with open(input_file, mode='r') as infile, open(output_file, mode="w", newline="") as outfile:
    csv_reader = csv.reader(infile, delimiter='\t')
    csv_writer = csv.writer(outfile, delimiter='\t')

    # Iterate over each line in the CSV
    for row in csv_reader:
        try:
            button_write_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Compose')]"))
            )
            button_write_email.click()


            input_to = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='To recipients']"))
            )
            email = row[0]
            input_to.send_keys(email)


            input_subject = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Subject']"))
            )
            email_subject = "Demo automatizare"
            input_subject.send_keys(email_subject)


            input_email_body = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Message Body']"))
            )
            email_body = "Salutare\n\nExplorați eficiența unui proces automatizat de trimitere a email-urilor, economisind timp și resurse prețioase."
            input_email_body.send_keys(email_body)


            button_attach_pdf = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Attach files']"))
            )
            button_attach_pdf.click()


            # Type the file path and press Enter
            time.sleep(1)
            pyautogui.write(pdf_path)
            time.sleep(1)
            pyautogui.press("enter")


            send_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@data-tooltip, 'Send')]"))
            )
            time.sleep(5)
            send_button.click()
        except Exception as e:
            csv_writer.writerow(row)
            print("Error sending email")

print("Finished successfully")