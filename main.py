import calendar
import datetime
import platform
import time

from dotenv import dotenv_values
from requests import Session
from selenium import webdriver
from selenium.webdriver.common.by import By

###########################################

HOST = "newage.peopleforce.io"
BASE_URL = f"https://{HOST}"
LOGIN_URL = f"{BASE_URL}/users/sign_in"
LOG_TIMESHEET_URL = "/timesheets/week"
NEW_TIMESHEET_ROW_URL = f"{BASE_URL}/timesheet_rows"
NEW_TIMESHEET_ENTRY_URL = f"{BASE_URL}/timesheet_entries"

###########################################

ENV_VARIABLES = dotenv_values(".env")

USER_ID: str = ENV_VARIABLES['USER_ID']
USER_EMAIL: str = ENV_VARIABLES['USER_EMAIL']
USER_PASSWORD: str = ENV_VARIABLES['USER_PASSWORD']

USER_EMAIL_FIELD_SELECTOR = "user_email"
USER_PASSWORD_FIELD_SELECTOR = "user_password"
USER_LOGIN_BUTTON_SELECTOR = "button"

###########################################

HOURS: str = ENV_VARIABLES['HOURS']

START_DAY = 1
START_MONTH = 2
START_YEAR = 2022


###########################################


def generateDateNumber(number: int) -> str:
    if number < 10:
        return f"0{number}"
    else:
        return f"{number}"


def loginUser():
    driver.get(LOGIN_URL)
    time.sleep(3)

    form = driver.find_element(By.ID, "new_user")
    form.find_element(By.ID, USER_EMAIL_FIELD_SELECTOR).send_keys(USER_EMAIL)
    form.find_element(By.ID, USER_PASSWORD_FIELD_SELECTOR).send_keys(USER_PASSWORD)
    form.find_element(By.NAME, USER_LOGIN_BUTTON_SELECTOR).click()
    time.sleep(5)

    return redirectToTimeSheetPage(START_DAY)


def submitWeekForApproval(entryDate: int):
    try:
        if entryDate >= 4:
            driver.find_element(By.CSS_SELECTOR, "#timesheet_frame > div.mt-4.d-flex > form > button").click()
            time.sleep(2)
    except Exception:
        print("Approval button was not found!")


def redirectToTimeSheetPage(day: int):
    # Get the last day of the month
    lastDayOfTheMonth = calendar.monthrange(START_YEAR, START_MONTH)[1]
    # If current day is more than the last day of the month stop adding of entries
    if day > lastDayOfTheMonth:
        return quitBrowser()

    # TODO check vacation days...
    # If the current day is the vacation day go to the next one

    # Check if the day is a working day
    entryDate = datetime.datetime(START_YEAR, START_MONTH, day).weekday()
    # If it's Saturday or Sunday continue to the next week
    if entryDate >= 5:
        return redirectToTimeSheetPage(day + 1)

    # Add leading zero to the day of the month
    startDay: str = generateDateNumber(day)
    # Add leading zero to the month of the year
    startMonth: str = generateDateNumber(START_MONTH)

    currentDayUrl = f"{BASE_URL}/timesheets/day?date={START_YEAR}-{startMonth}-{startDay}&user_id={USER_ID}"
    driver.get(currentDayUrl)

    time.sleep(3)
    try:
        currentFilledMinutes = driver.find_element(By.CSS_SELECTOR, f"a[href='{currentDayUrl}'] > small") \
            .text.replace(" ", "").replace("\n", "")

        # Check if the entry is already added for the current day
        if currentFilledMinutes == "0:00":
            driver.find_element(By.CSS_SELECTOR, "#timesheet_frame > div.mt-4.d-flex > a").click()
            time.sleep(2)
            driver.find_element(By.ID, "minutes").send_keys(HOURS)
            time.sleep(2)
            driver.find_element(By.CSS_SELECTOR, "#new_timesheet_entry > button").click()
            time.sleep(2)

            submitWeekForApproval(entryDate)

            # After adding an entry go for the next day
            return redirectToTimeSheetPage(day + 1)
        else:
            submitWeekForApproval(entryDate)

            # If there is an entry for the current day go to the next day
            return redirectToTimeSheetPage(day + 1)
    except Exception:
        # If there is no Add Entry button go to the next day
        return redirectToTimeSheetPage(day + 1)


def quitBrowser():
    time.sleep(3)
    driver.close()


with Session() as session:
    if "Windows" in platform.platform() or "Linux" in platform.platform():
        import chromedriver_autoinstaller

        chromedriver_autoinstaller.install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Safari()

    driver.maximize_window()

    loginUser()

