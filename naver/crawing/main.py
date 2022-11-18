from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from . import excelFunc
from . import setData
from . import urlParse
import openpyxl as xl
import os

def crawing(url):
    s = Service('./naver/crawing/chromedriver') # Windows는 chromedriver.exe로 변경
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument( '--headless' )     # 크롬창이 열리지 않음
    chrome_options.add_argument( '--no-sandbox' )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    chrome_options.add_argument( '--disable-gpu' )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
    # chrome_options.add_argument(f"--window-size={ WINDOW_SIZE }")
    chrome_options.add_argument('Content-Type=application/json; charset=utf-8')
    
    driver = webdriver.Chrome( service=s , options=chrome_options )

    delivery = {}
    origin_area = {}
    category = {}

    excelFunc.set_delivery(delivery)
    excelFunc.set_origin(origin_area)
    excelFunc.set_category(category)
    url_list = []

    urlParse.url_parse(driver, url, url_list)

    print(len(url_list))
    for idx, detail_url in enumerate(url_list):
        print(idx)
        if (idx == 40):
            break
        setData.goods_details(driver, detail_url, delivery, origin_area, category)
    # setData.goods_details(driver, "https://brand.naver.com/poled/products/6153167043", delivery, origin_area, category)