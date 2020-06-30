from selenium import webdriver
from time import sleep
import pyautogui
from bs4 import BeautifulSoup
import requests
import shutil

browser = webdriver.Firefox(executable_path='/path/to/geckodriver')
browser.get('https://www.instagram.com/explore/tags/bird/')


# вход в инстаграмм аккаунт
def enter_in_account():
    button_enter = browser.find_element_by_xpath("//*[@class='sqdOP  L3NKy   y3zKF     ']")
    button_enter.click()
    sleep(2)
    login = browser.find_element_by_xpath("//*[@class='_2hvTZ pexuQ zyHYP']")
    login.send_keys('LOGIN')
    sleep(1)
    password = browser.find_element_by_xpath("//*[@class='_2hvTZ pexuQ zyHYP']")
    password.send_keys('PASSWORD')
    enter = browser.find_element_by_xpath(
        "//*[@class='                    Igw0E     IwRSH      eGOV_         _4EzTm                                                                                                              ']")
    enter.click()
    sleep(4)
    not_now_button = browser.find_element_by_xpath("//*[@class='sqdOP yWX7d    y3zKF     ']")
    not_now_button.click()
    sleep(2)



# нажимаем на первый пост
def find_first_post():
    sleep(3)
    pyautogui.moveTo(450, 800, duration=0.5)
    pyautogui.click()


# получаем ссылку на изображение
def get_url():
    sleep(0.5)
    pyautogui.moveTo(1740, 640, duration=0.5)
    pyautogui.click()

    return browser.current_url


# получаем html-код страницы
def get_html(url):
    r = requests.get(url)
    return r.text


# получаем внутренности атрибута src
def get_src(html):
    soup = BeautifulSoup(html, 'lxml')
    src = soup.find('meta', property="og:image")
    return src['content']


# предыдущая функция вернула немного неверный src, поэтому нужно немного поменять
def replace(src):
    src_new = src.replace('amp;', '')
    return src_new


# скачиваем и сохраняем изображение
def download_image(image_name, image_url):
    filename = 'bird/bird{}.jpg'.format(image_name)
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True
        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        print('Image sucessfully Downloaded')

    else:
        print('Image Couldn\'t be retreived')


if __name__ == '__main__':
    enter_in_account()
    find_first_post()
    for i in range(3000):
        try:
            current_url = get_url()
            html = get_html(current_url)
            src = get_src(html)
            src_new = replace(src)
            download_image(i, src_new)
            print(i)
        except Exception:
            pass

