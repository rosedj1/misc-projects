"""
UF Paystub Web Scraper

Author: Dr. Jake Rosenzweig
Email: Jake.Create@proton.me
Date: 2023-07-14

This code logs into my.ufl.edu, let's you enter your Gatorlink username and
password, and then goes through and downloads the paystub PDFs that you've
selected, according to the User Parameters defined below. Saves the PDFs into
a local directory which you've specified.

Run this code by doing:
`python get_paystubs_uf.py`

NOTE:
* This code requires the module selenium.
* This code has only been tested with Google Chrome; Firefox gave me trouble.
* Lots of sleep time in between actions allow the browser windows to load.
* If the code throws an error at any point, it is likely to be because a page
did not load before an action was attempted.
* If an error is thrown and paystubs were downloaded, then go check the last
paystub downloaded. It is likely to be wrong! Delete it and run the code
starting from that paystub.
* Not sure how secure getpass is; use at your own discretion!
* While the code is running, don't interact with the browser with your cursor.
* This also means don't enter your UN/PW in the browser; use the command line.
* Follow the prompts displayed on the command line.
* In the past, UF used to not have PDF files for their paystubs.
UF implemented PDF paystubs sometime between 2011-08-12 and 2016-09-02.
Therefore, this code probably won't work for paystubs before 2016-09-02.
* I recommend closing the folder into which the paystubs will be downloaded.
If it is open while the code is running, your computer may send that window to
the foreground and then the code can switch its handle from the paystub window
to the local folder  with the paystubs.
"""
import os
import time
from getpass import getpass
from glob import glob
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

#=================#
# User Parameters #
#=================#
dir_paystubs = "/Users/Jake/Desktop/uf_paystubs_test/"
page = 0  # Paychecks 0-99 are on page 0.
paycheck_beg = 0  # Start and end must both be between 0-99.
paycheck_end = 2
sleep = 8  # Download time (seconds).
# UF displays 100 paychecks at a time.
# If user wants to grab paychecks 100-150, then they should use:
# page = 1, paycheck_beg = 0, paycheck_end = 50

def convert_date(date_string):
    """
    Converts a date string from 'MM/DD/YYYY' format to 'YYYYMMDD' format.

    Args:
        date_string (str): The date string to be converted.

    Returns:
        str: The converted date string in 'YYYYMMDD' format.
    """
    parsed_date = datetime.strptime(date_string, '%m/%d/%Y')
    formatted_date = parsed_date.strftime('%Y%m%d')
    return formatted_date

def get_paycheck_daterange(pc):
    """Return a 2-tuple of (Pay Begin Date, Pay End Date).
    
    Args:
        pc (int): Which paycheck on the current page.

    Returns:
        (Pay Begin Date, Pay End Date), (2-tuple): (yyyymmdd, yyyymmdd)
    """
    dt_beg = driver.find_element(By.ID, f"PY_IC_PI_LST_VW_PAY_BEGIN_DT${pc}").text
    dt_end = driver.find_element(By.ID, f"PY_IC_PI_LST_VW_PAY_END_DT_ALT$14$${pc}").text
    dt_beg_cnvrt = convert_date(dt_beg)
    dt_end_cnvrt = convert_date(dt_end)
    return (dt_beg_cnvrt, dt_end_cnvrt)

def rename_paycheck(dt_beg, dt_end, dir_stubs):
    """Rename paycheck number `num` based on Pay Begin Date and Pay End Date.
    
    Args:
        dt_beg (str): The Pay Begin Date of the paycheck.
        dt_end (str): The Pay End Date of the paycheck.
        dir_stubs (str): Path to paycheck PDF.

    Returns:
        int: 0 on success, 1 if error.
    """
    # Rename the most recently downloaded file.
    list_of_files = glob(f"{dir_stubs}/*")
    latest_file = max(list_of_files, key=os.path.getctime)
    assert latest_file != ""
    new_name = f"paystub_uf_{dt_beg}_{dt_end}.pdf"
    os.rename(
        latest_file,
        os.path.join(dir_stubs, new_name)
        )
    print(f"Renamed paycheck to: {new_name}")

def download_paycheck(num, sleep=5):
    """Download a paycheck by clicking the hyperlink of paycheck `num`.
    
    Args:
        num (int): Number of paycheck.
        
    Returns:
        None.
    """
    driver.find_element(By.ID, f"VIEW_PAYCHECK_PB${num}").click()
    time.sleep(sleep)
    print(f"Downloaded paycheck number {num}")

def navigate_to_page(num, sleep=5):
    """Click the right arrow `num` times, sleeping in between clicks.

    Args:
        num (int): Number of right-arrow clicks.
        sleep (int): Number of seconds to sleep.
    
    Returns:
        None

    Clicking the right arrow shows the next set of paychecks. 
    """
    if num > 0:
        for _ in range(num):
            driver.find_element(By.ID, "PY_IC_PI_LST_VW$hdown$0").click()
            time.sleep(sleep)

# Sanity checks.
assert (paycheck_end >= paycheck_beg) and (page >= 0)
assert all(x >= 0 and x <= 99 for x in (paycheck_beg, paycheck_end))

# Prep the workspace.
os.makedirs(dir_paystubs, exist_ok=True)
options = webdriver.ChromeOptions()
options.add_experimental_option(
    'prefs', {
        "download.default_directory": dir_paystubs, # Default downloads.
        "download.prompt_for_download": False, # Auto-download the file.
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True # Don't show PDF in Chrome.
        }
    )
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

num_pc = paycheck_end - paycheck_beg + 1
msg = f"Downloading {num_pc} paychecks (num: {paycheck_beg}-{paycheck_end})."
if num_pc == 1:
    msg = msg.replace("paychecks", "paycheck")
print(msg)

# Log in.
driver.get("https://my.ufl.edu/ps/signon.html")
driver.find_element(By.ID, "button-owa").click()
un = input('Gatorlink: ')
pw = getpass()
driver.find_element(By.ID, "username").send_keys(un)
driver.find_element(By.ID, "password").send_keys(pw)
driver.find_element(By.ID, "submit").click()
_ = input("Push any key after completing the two-factor authentication.")
# User might be very fast. Let the page load.
time.sleep(5)

# Navigate through side menu to webpage of paychecks.
driver.find_element(By.ID, "pthdr2navbar").click()
driver.switch_to.frame(0)
driver.find_element(By.ID, "PTNUI_MENU_ICN$2").click()
# Wait for sidebars to load.
time.sleep(2)
driver.find_element(By.ID, "PTMENUITEM$1").click()
time.sleep(2)
driver.find_element(By.ID, "PTMENUITEM$0").click()
time.sleep(2)
driver.find_element(By.ID, "PTMENUITEM$0").click()

# Expand paycheck dropdown menu.
driver.switch_to.frame(0)
driver.find_element(By.ID, "PY_IC_PI_LST_VW$hviewall$0").click()
time.sleep(3)

# Download paychecks and rename them.
for num in range(paycheck_beg, paycheck_end + 1):
    navigate_to_page(page, sleep=5)
    # While we're here, grab PDF date range info.
    date_beg, date_end = get_paycheck_daterange(num)
    # Click the hyperlink to download the PDF.
    download_paycheck(num, sleep=sleep)
    rename_paycheck(date_beg, date_end, dir_paystubs)
