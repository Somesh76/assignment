import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome WebDriver (make sure to have the chromedriver executable in your PATH)
ser_obj = Service('./driver/chromedriver.exe')
driver = webdriver.Chrome(service=ser_obj)

try:
    # Navigate to the webpage

    driver.get('https://www.fitpeo.com/')
    driver.maximize_window()
    # Navigation to the revenue calculator
    ele = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="/revenue-calculator"]'))
    )
    ele.click()
    # Getting slider locator
    slider = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='range']")))
    # Locating slider text box
    text_bax_value = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='number']")))

    # As checked moving slider by action method is not possible because of the offset value increases the slider
    # value by 6-7 because of which using keyword actions

    # move the cursor till value reaches to 820 and once found break the loop
    while True:
        slider.send_keys(Keys.ARROW_RIGHT)
        value = text_bax_value.get_attribute('value')

        if value == '820':
            break

    # asserting the value to check it value on cursor is being reflected correctly on text box below
    assert value == slider.get_attribute('value')
    time.sleep(2)

    # Also clear() function is not working on the slider text box so using keyword button action
    for i in range(len(value)):
        text_bax_value.send_keys(Keys.BACK_SPACE)

    # Sending the value into text box
    text_bax_value.send_keys('560')

    # checking if the value in slider is updated or not
    assert text_bax_value.get_attribute('value') == slider.get_attribute('value')

    # Scrolling to reimbursement
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="MuiBox-root css-m1khva"]/p[2]'))
    )

    # Scroll to the element
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Getting all the CPTS values
    cpts = driver.find_elements(By.XPATH, '//div[@class="MuiBox-root css-1p19z09"]/div/p[1]')

    # Creating list of CTPS we can to click
    cpts_lst = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']

    # Looping over the total CPTS and clicking on CPTS we have stored in list with dynamic xpath
    i = 1
    for cpt in cpts:
        if cpt.text in cpts_lst:
            driver.find_element(By.XPATH, "(//div[@class='MuiBox-root css-1p19z09']//label//input)[" + str(i) + "]").click()
        i += 1

    # checking reimbursement value
    reimbursement = driver.find_element(By.XPATH, '//div[@class="MuiBox-root css-m1khva"]/p[2]').text
    assert reimbursement == '$75600'


finally:
    # Close the WebDriver

    driver.quit()
