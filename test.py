import email
import gc
import imaplib
import json
import logging
import random
import time

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

logger = logging.getLogger("selenium")
logger.setLevel(logging.INFO)

android_ua = "Mozilla/5.0 (Linux; Android 14; LM-X420) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.210 Mobile Safari/537.36"


def load_cookies():
    with open("cookies.json") as f:
        cooks = json.load(f)
    return cooks


def get_options(mobile=False, headless=False):
    options = ChromeOptions()
    if mobile:
        mobile_emulation = {
            "deviceMetrics": {"width": 720, "height": 1280, "pixelRatio": 3.0},
            # "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
            "userAgent": android_ua,
            "clientHints": {"platform": "Android", "mobile": True},
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    # this argument disables the welcome screen
    options.add_argument("--disable-fre")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--show")
    # options.add_argument("--window-size=1080,1920")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension','False')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    # options.add_argument(f"--proxy-server={get_proxies()[0]}")
    # options.add_argument("--proxy-server=http://144.126.141.115:1010")
    # options.add_experimental_option(
    #     "prefs",
    #     {
    #         "profile.default_content_setting_values.media_stream_mic": 1,
    #         "profile.default_content_setting_values.media_stream_camera": 1,
    #         "profile.default_content_setting_values.geolocation": 0,
    #         "profile.default_content_setting_values.notifications": 1,
    #     },
    # )
    # options.add_argument(
    #     "--user-data-dir=C:/Users/Dunes/AppData/Local/Google/Chrome/User Data"
    # )
    return options


def nav_update(driver):
    """This function updates the scroll position of the page
    It basically should be called if you want the browser to scroll to the end of the page.
    """
    try:
        pass
    except Exception:
        pass
    # driver.maximize_window()
    x = driver.execute_script("return window.pageYOffset")
    new = 1
    count = 0
    while x != new:
        gc.collect()
        try:
            driver.execute_script("return window.scrollBy(0,1000)")
            time.sleep(2)
            new = x
            x = driver.execute_script("return window.pageYOffset")
        except:
            pass
        x = driver.execute_script("return window.pageYOffset")
        if x == new or count > 25:
            # count+=1
            # print(x,new)
            # print(count)
            # if count>3:
            break
        count += 1


def get_proxies():
    proxy_url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=us&ssl=yes&anonymity=elite"
    r = requests.get(proxy_url)
    proxies = [i.strip() for i in r.text.splitlines()]
    with open("proxies.txt", "w") as f:
        for proxy in proxies:
            f.write(f"{proxy}\n")
    random.shuffle(proxies)
    print(proxies[0])
    return proxies


def getOTP(userEmail: str, password: str) -> str:
    # Outlook IMAP settings
    outlook_server = "outlook.office365.com"

    # Connect to Outlook's IMAP server
    mail = imaplib.IMAP4_SSL(outlook_server)
    mail.login(userEmail, password)

    # Select the mailbox you want to access
    mail.select("inbox")

    # Search for all emails in the inbox
    status, messages = mail.search(None, "ALL")
    messages = messages[0].split()

    # Get the latest email
    latest_email_id = messages[-1]

    # Fetch the email by ID
    status, msg_data = mail.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]

    # Parse the raw email
    msg = email.message_from_bytes(raw_email)

    # Extract the HTML part of the email
    for part in msg.walk():
        content_type = part.get_content_type()

        # Check for text/html parts
        if "text/html" in content_type:
            # Get the HTML content
            html_content = part.get_payload(decode=True).decode("utf-8")

    # Parse the HTML part with BeautifulSoup
    soup = BeautifulSoup(html_content, "html5lib")

    # Find the confirmation code element by its style attribute
    confirmation_code_element = soup.find(
        "td",
        style="padding:10px;color:#565a5c;font-size:32px;font-weight:500;text-align:center;padding-bottom:25px;",
    )

    # Extract the confirmation code
    if confirmation_code_element:
        confirmation_code = confirmation_code_element.get_text(strip=True)
        code = confirmation_code
    else:
        code = "Confirmation code element not found."

    # Close the connection
    mail.logout()

    # return the code
    return code, soup


driver = uc.Chrome(options=get_options(mobile=False, headless=False))

driver.get("https://httpbin.org/ip")
driver.find_element(By.TAG_NAME, "body").text
driver.get("https://www.tiktok.com")
time.sleep(2)

### This code implements logging in with cookies
### You can comment it out if you wan to test the user/passwd kind of login
##Begin
for cookies in load_cookies():
    cookies["domain"] = ".tiktok.com"
    try:
        print(cookies)
        driver.add_cookie(cookies)
    except Exception as e:
        print(e)
        pass

driver.get("https://www.tiktok.com")
##End


#### The code below implements logging in with email and password
### feel free to make changes but do not uncomment it and run without commenting out the top code.

# driver.get("https://www.tiktok.com/login/phone-or-email/email")
# em = "Enrikkodra461253@outlook.com"
# pwd = "LAj461ciJS."
# time.sleep(10)
# login_elems = driver.find_elements(By.TAG_NAME, "input")
# keys = [em, pwd]
# time.sleep(10)
# for idx, elem in enumerate(login_elems):
#     elem.clear()
#     print(elem.get_attribute("placeholder"))
#     elem.send_keys(keys[idx])
#     time.sleep(5)

# submit = driver.find_element(By.XPATH, '//button[@type="submit"]')
# print(submit.text)
# submit.click()



##This is a fix to prevent the browser from dying until you press enter
input("Press Enter to quit...")
