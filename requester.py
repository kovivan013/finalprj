import requests
import time

from string import digits
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=UserAgent")
    driver = webdriver.Chrome(options=options)
    return driver

def load_page(method: str, wait) -> None:
    locator_element = (By.XPATH, method)
    wait.until(expected_conditions.presence_of_element_located(locator_element))
    time.sleep(0.1)

def get_page():
    driver = init_driver()
    wait = WebDriverWait(driver, 20)
    try:
        driver.get(url="https://www.bbc.com/ukrainian/features-66330880")
        load_page(method="//div[@class=\"bbc-19j92fr ebmt73l0\"]", wait=wait)
        films_div = driver.find_elements(By.XPATH, "//div[@class=\"bbc-19j92fr ebmt73l0\"]")
        films_list: list = []
        divs_list = [i.text for i in films_div]
        for i in divs_list:
            if i[0] in digits:
                films_list.append(i)
        driver.close()
        driver.quit()
        return films_list
    except Exception as err:
        return err

def add_film(name: str):
    url = f"http://127.0.0.1:8000/add_film?film_name={name}"
    requests.post(url)

films = get_page()
for i in films:
    add_film(name=i)