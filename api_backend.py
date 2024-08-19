from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

import os

import chrome_handler
import helper_funcs
import sys

# current file path
current_file_path = os.path.dirname(os.path.realpath(__file__))
user_data_folder = current_file_path + "/chromedata"
chrome_profile = "Default"

def load_chrome():
    # service = Service(os.getcwd() + "/chromedriver")

    options = Options()
    options.add_argument(f"--user-data-dir={user_data_folder}")
    options.add_argument(f'--profile-directory={chrome_profile}')

    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    # options.add_argument("--headless")

    global helper_fn, driver

    driver = uc.Chrome(options=options)
    helper_fn = helper_funcs.HelperFn(driver)


#def check_guildlines():
    #guidlines_xpath = "//*[contains(text(), 'Tips for getting started')]"
    #helper_fn.wait_for_element(guidlines_xpath)
    #if helper_fn.is_element_present(guidlines_xpath):
    #    guidlines_close_xpath = "//*[contains(text(), 'Okay, let’s go')]"
    #    guidlines_close = helper_fn.find_element(guidlines_close_xpath)
    #    guidlines_close.click()
    #else:
    #    print("No guidlines found")

def start_chat_gpt():
    load_chrome()
    driver.maximize_window()
    driver.get("https://chatgpt.com/")
    #if login page is present
    time.sleep(3)
    #check for guidlines
    #check_guildlines()

def make_gpt_request(text):
    time.sleep(1)
    text_area_xpath = "//*[@id='prompt-textarea']"
    helper_fn.wait_for_element(text_area_xpath)
    if helper_fn.is_element_present(text_area_xpath):
        text_area = helper_fn.find_element(text_area_xpath)
        text_area.send_keys(text)

        #send button
        send_btn_xpath = "//*[@data-testid='send-button']"
        helper_fn.wait_for_element(send_btn_xpath)
        send_btn = helper_fn.find_element(send_btn_xpath)
        time.sleep(1)
        send_btn.click()

    helper_fn.wait_for_x_seconds(5)
    #waiting for response
    response_xpath_light = "//*[@class='markdown prose w-full break-words dark:prose-invert light']" # for light mode
    response_xpath_dark = "//*[@class='markdown prose w-full break-words dark:prose-invert dark']" # for dark mode
    regenrate_xpath = '//*[@id="__next"]/div[1]/div[2]/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/div/button'
    helper_fn.wait_for_element(regenrate_xpath,120)
    response_xpath = response_xpath_dark if helper_fn.is_element_present(response_xpath_dark) else response_xpath_light # check for dark mode or light mode
    time.sleep(1)
    if helper_fn.is_element_present(response_xpath):
        helper_fn.wait_for_x_seconds(1)
        response = helper_fn.find_elements(response_xpath)[-1]
        # print(response.text)
        return response.text # will return all the texual information under that perticular xpath



def stop_chat_gpt():
    driver.close()
    driver.quit()

    # chrome_handler.kill_chrome()
    
if __name__ == "__main__":
    start_chat_gpt()
    
    try:
        while True:
            req = input("Enter text: ")
            if req == "!quit":
                break
            resp = make_gpt_request(req)
            print(resp)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected, exiting...")
    finally:
        stop_chat_gpt()
