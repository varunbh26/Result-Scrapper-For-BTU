from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import easyocr
from PIL import ImageGrab
from PIL import Image
import PIL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pyautogui
import pdfkit
import asyncio
from pyppeteer import launch
from selenium.common.exceptions import NoSuchElementException

pyautogui.FAILSAFE = False
reader = easyocr.Reader(['en'])
def check_exists_by_id(id):
    try:
        driver.find_element(By.ID,id)
    except NoSuchElementException:
        return False
    return True
branchrollchange = {
    #The Middle part of roll no for example 
    # "EEACS" : 89 <--- this will make it so that the ressult will be scraped for roll no 1 to 89 
    }
branchrollchange_list = branchrollchange.keys()
#print(branchrollchange_list)
for i in branchrollchange_list:
    if i == "EEACS":
        j = 72
    else:
        j = 1
    while j <= branchrollchange[i]:
        #print(j)
        if int(j/10) == 0:
            placesetter = "00"
        elif int(j/10) > 0 and int(j/10) < 10:
            placesetter = "0"
        elif int(j/10) >= 10:
            placesetter = "" 
        rollno = "23" + str(i) + str(placesetter) + str(j) #<----- Here 23 is added because that is part of roll no, change it accordingly to your needs
        driver = webdriver.Firefox()
        driver.get("http://btuexam.in/BTU_StuRoll_2324.aspx") #<---- this will go to the website where you need to go to find the result, change the website url accordingly
        ExamTypeElement = Select(driver.find_element(By.ID,"ContentPlaceHolder1_ddlcategory"))
        ExamTypeElement.select_by_index(3)
        RollNoElement = driver.find_element(By.ID,"ContentPlaceHolder1_txtroll")
        RollNoElement.send_keys(rollno)
        SubmitButtonElement = driver.find_element(By.ID,"ContentPlaceHolder1_Button1")
        SubmitButtonElement.click()
        #invalid_message_element = driver.find_element(By.ID,"ContentPlaceHolder1_1b1Message")
        #SubmitButtonElement.click()
        #element = WebDriverWait(driver, 10).until(
        #    EC.element_to_be_clickable((By.ID, "ContentPlaceHolder1_ImgCaptcha"))
        #)
        #element.send_keys("Keys.BACK_SPACE")
        CaptchaElement = driver.find_element(By.ID,"ContentPlaceHolder1_ImgCaptcha")
        CaptchaElement.click()
        time.sleep(2)
        CaptchaSS = ImageGrab.grab(bbox=[990,590,1175,650])
        #CaptchaSS.show()
        CaptchaSS.save("Captcha.png")
        result = reader.readtext("Captcha.png",detail=0)
        pyautogui.press('tab',presses=4)
        time.sleep(1)
        pyautogui.write(result[0])
        #CaptchaElement.send_keys("Keys.BACK_SPACE")
        print(result)
        pyautogui.press('tab')
        pyautogui.press('enter')
        time.sleep(2)
        WebDriverWait(driver, 10).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        #config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
        #pdfkit.from_url(driver.current_url,'23EEACS119.pdf',configuration=config)
        #pyautogui.press("ctrl+p")
        #driver.execute_script("CallPrint('content1')")
        driver.set_window_size(1024, 600)
        driver.maximize_window()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        result_sheet = ImageGrab.grab(bbox=[300,100,1400,1000])
        #result_sheet.show()
        result_sheet.save(rollno + '.png')
        #print(rollno)
        if check_exists_by_id("ContentPlaceHolder1_lblMessage"):
            if driver.find_element(By.ID,"ContentPlaceHolder1_lblMessage").text == 'Result Under Process...':
                j = j+1
            else:
                j = j
        else:
            j = j+1
        driver.quit()
