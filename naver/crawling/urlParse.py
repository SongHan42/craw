# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def url_parse(driver, url, url_list):
    page_num = 1
    driver.get(url)
    while (True):
        try:
               #CategoryProducts > ul > li:nth-child(37)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#CategoryProducts > ul > li")))
            time.sleep(1)
            for li in driver.find_elements(By.CSS_SELECTOR, "#CategoryProducts > ul > li._2txbrXXlXM"):
                url_list += [li.find_element(By.CSS_SELECTOR, "a").get_attribute("href")]
        except :
            driver.quit()
            return

        # if page_num % 10 == 0 and page_num != 0:
        if page_num % 10 == 0:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.fAUKm1ewwo._2Ar8-aEUTq")))
                nextBtn = driver.find_element(By.CSS_SELECTOR, "a.fAUKm1ewwo._2Ar8-aEUTq")
                if nextBtn.get_attribute("aria-hidden") == 'false':
                    nextBtn.click()
                    # time.sleep(2)
            except:
                driver.quit()
                return
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.UWN4IvaQza")))
        aList = driver.find_elements(By.CSS_SELECTOR, "a.UWN4IvaQza")
        # if page_num != 0:
        if len(aList) > page_num % 10:
            aList[page_num % 10].click()
        else :
            return
        page_num += 1

# s = Service('./chromedriver') # Windows는 chromedriver.exe로 변경
 
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument( '--headless' )     # 크롬창이 열리지 않음
# chrome_options.add_argument( '--no-sandbox' )   # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
# chrome_options.add_argument( '--disable-gpu' )  # GUI를 사용할 수 없는 환경에서 설정, linux, docker 등
# # chrome_options.add_argument(f"--window-size={ WINDOW_SIZE }")
# chrome_options.add_argument('Content-Type=application/json; charset=utf-8')

# driver = webdriver.Chrome( service=s , options=chrome_options )
# driver.implicitly_wait(10)

# url_list = []

# url_parse(driver, "https://brand.naver.com/eider/category/b3e0f19954724f7e959047c02dd86810?cp=1", url_list)

# for url in url_list:
#     print(url)