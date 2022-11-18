from unicodedata import category
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
from . import utils
from ..models import *
import time

def save_imgs(data, imgs_url, product):
    #동영상은 대기하세요~~
    # folder = './img'
    # data["추가이미지"] = ""
    # print(imgs_url)

    # if not os.path.isdir(folder):
    #     os.mkdir(folder)
    
    for index, link in enumerate(imgs_url):
        # urllib.request.urlretrieve(link.split('?')[0], f'{folder}/{data["상품번호"]}_{index}.jpg')
        # img = "<img src=" + link.split('?')[0] + "/>"
        img = link.split('?')[0]
        if index == 0:
            product.main_img = img
            # data["대표이미지"] = f'{data["상품번호"]}_{index}.jpg'
        else:
            sub_img = SubImg()
            sub_img.product = product
            sub_img.img = img
            sub_img.save()
            # data["추가이미지"] += f'{data["상품번호"]}_{index}.jpg\n'

def parse_script(driver, category_dict, product):
    wait = WebDriverWait(driver,20)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'script')))
    time.sleep(1)

    json_object = ""
    for script in driver.find_elements(By.CSS_SELECTOR, "script"):
        if script.get_attribute("type") == "application/ld+json":
            json_object = json.loads(driver.execute_script("return arguments[0].innerHTML", script))
    categorys = json_object["category"].split(">")
    temp = category_dict
    for category in categorys:
        temp = temp[category]
    if len(categorys) != 4:
        temp = temp[""]
    product.category_code = temp

def add_data(tr, data, delivery, origin_area, product):
    key = ""
    th = tr.find_elements(By.CSS_SELECTOR, "th")
    td = tr.find_elements(By.CSS_SELECTOR, "td")
    if len(th):
        key = th[0].text
    for i in range(len(td)):
        if i < len(th):
            key = th[i].text
        if key == "재화등의 A/S 관련 전화번호":
            data["A/S 전화번호"] = td[i].text
        # elif key == "재화등의 배송방법에 관한 정보":
        #     if td[i].text == "택배" or td[i].text == "소포" or td[i].text == "등기":
        #         data["배송방법"] = "택배, 소포, 등기"
        #     else:
        #         data["배송방법"] = "직접배송(화물배달)"
        # elif key == "판매자 지정택배사":
        #     data["택배사코드"] = delivery[td[i].text]
        elif key == "원산지":
            area = td[i].text.split(" ")[-1].split(")")[0]
            if origin_area.get(area):
                product.origin_code = origin_area[area]
            else:
                product.origin_code = "04"
                product.origin_direct_input = td[i].text
        # elif key == "반품배송비":
        #     if td[i].text != "무료":
        #         data["반품배송비"] = td[i].text.split(" ")[1].replace(",", "").replace("원","")
        #     else:
        #         data["반품배송비"] = "0"
        # elif key == "교환배송비":
        #     if td[i].text != "무료":
        #         data["교환배송비"] = td[i].text.replace(",", "").replace("원","")
        #     else:
        #         data["교환배송비"] = "0"
        elif key == "A/S 안내":
            data["A/S 안내"] = ""
            for text in td[i].text.split("\n")[1:]:
                data["A/S 안내"] += text + "\n"
        elif key == "제조일자":
            date = td[i].text.split(".")
            product.manufacturing_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        elif key == "유효일자":
            date = td[i].text.split(".")
            product.effective_date = datetime.date(int(date[0]), int(date[1]), int(date[2]))
        elif key == "품명 / 모델명":
            data["상품정보제공고시\n품명"] = td[i].text.split(" / ")[0]
            data["상품정보제공고시\n모델명"] = td[i].text.split(" / ")[1]
        elif key == "제조자(사)":
            data["상품정보제공고시\n제조자"] = td[i].text
        else:
            data[key.split("-")[0]] = td[i].text

def set_option(driver, wait, data, product):

    for input in driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > label'):
        direct_input_option = DirectInputOption()
        direct_input_option.product = product
        direct_input_option.text = input.text
        direct_input_option.save()

    product.option_type = "단독형"
    option_button = driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > a')
    if len(option_button) == 0:
        return
    if (option_button[0].text == "배송비 절약상품 보기"):
        del option_button[0]
    for op in option_button:
        type = op.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.CSS_SELECTOR, 'span').text
        op.click()
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > ul > li > a')))
        select = driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > ul > li > a')
        select_text = [sel.text for sel in select]
        if (type == "추가상품"):
            additional_product_name = AdditionalProductName()
            additional_product_name.name = op.text
            additional_product_name.product = product
            additional_product_name.save()

            values = (utils.remove_price(select_text))
            prices = [utils.only_num_price(price) for price in select_text]
            for i in range(len(values)):
                additional_product_detail = AdditionalProductDetail()
                additional_product_detail.additional_product_name = additional_product_name
                additional_product_detail.value = values[i]
                additional_product_detail.price = prices[i]
                additional_product_detail.num = 1
                additional_product_detail.save()
        else:
            option_name = OptionName()
            option_name.product = product
            option_name.name = op.text
            option_name.save()

            values = (utils.remove_price(select_text))
            prices = [utils.only_num_price(price) for price in select_text]
            for i in range(len(values)):
                option = Option()
                option.option_name = option_name
                option.value = values[i]
                if prices[i] != '0':
                    product.option_type = "조합형"
                option.price = prices[i]
                option.save()
        check = 0
        for sel in select:
            if (sel.text.find("(품절)") == -1):
                check = 1
                sel.click()
                break
        if check != 1:
            op.click()

    option_names = product.optionname_set.all()
    if product.option_type == "조합형":
        for option_name in option_names:
            options = option_name.option_set.all()
            for option in options:
                option_stock_num = OptionStockNum()
                option_stock_num.option = option
                option_stock_num.num = 1
                option_stock_num.save()
    else:
        if option_names:
            options = option_names[0].option_set.all()
            for option in options:
                option_stock_num = OptionStockNum()
                option_stock_num.option = option
                option_stock_num.num = 1
                option_stock_num.save()


def set_table(driver, data, delivery, origin_area, product):
    for div in driver.find_elements(By.CSS_SELECTOR, "#INTRODUCE > div > div"):
        if div.get_attribute("class") != "":
            for tr in div.find_elements(By.CSS_SELECTOR, "tr"):
                add_data(tr, data, delivery, origin_area, product)
        else:
            main_div = div.find_elements(By.CSS_SELECTOR, "div.se-main-container > div")
            for detail in main_div:
                if detail.text:
                    data["상세설명"] += detail.text + "\n"
                else:
                    img = div.find_element(By.CSS_SELECTOR, "img")
                    src = img.get_attribute("data-src")
                    if src and src.find("video") == -1 and src.find("data:image") == -1:
                        data["상세설명"] += '<img src="' + img.get_attribute("data-src") + '">\n'

    for tr in driver.find_elements(By.CSS_SELECTOR, "#RETURNPOLICY > div > table > tbody > tr"):
        add_data(tr, data, delivery, origin_area, product)
    for tr in driver.find_elements(By.CSS_SELECTOR, "#content > div > div.z7cS6-TO7X > div.etc > div._1aH4b0l27f > div._211Avwm-sU > table > tbody > tr"):
        add_data(tr, data, delivery, origin_area, product)

def save_db(data, product):
    product.product_state = data["상품상태"]
    if data.get("부가세"):
        product.vat = data["부가세"]
    if data.get("브랜드"):
        product.brand = data["브랜드"]
    if data.get("제조사"):
        product.manufacturer = data["제조사"]
    if data.get("수입사"):
        product.importer = data["수입사"]
    if data.get("복수원산지여부"):
        product.is_plural_origin = data["복수원산지여부"]
    if data.get("상품정보제공고시\n품명"):
        product.info_name = data["상품정보제공고시\n품명"]
    if data.get("상품정보제공시\n모델명"):
        product.info_model_name = data["상품정보제공시\n모델명"]
    if data.get("상품정보제공시\n인증허가사항"):
        product.info_authorization = data["상품정보제공시\n인증허가사항"]
    if data.get("상품정보제공시\n제조자"):
        product.info_manufacturer = data["상품정보제공시\n제조자"]
    product.save()

    after_service = AfterService()
    after_service.product = product
    after_service.phone_number = data["A/S 전화번호"]
    after_service.announcement = data["A/S 안내"]
    if data.get("판매자 특이사항"):
        after_service.seller_specifics = data["판매자 특이사항"]
    after_service.save()

    if data.get("ISBN") or data.get("ISSN") or data.get("독립출판") or data.get("출간일") or data.get("출판사") or data.get("글작가") or data.get("그림작가") or data.get("번역자명") or data.get("문화비 소득공제"):
        book = Book()
        book.ISBN = data["ISBN"]
        book.ISSN = data["ISSN"]
        # book.is_independent_publication = data["독립출판"]
        book.is_independent_publication = False
        date = data["출간일"].split("-")
        book.publication_date = datetime.date(date[0], date[1], date[2])
        book.publisher = data["출판사"]
        book.writer = data["글작가"]
        book.painter = data["그림작가"]
        book.translator = data["번역가명"]
        book.is_cultural_expenses_income_tax_deduction = data["문화비 소득공제"]
        book.save()
   
def goods_details(driver, url, delivery, origin_area, category):
    data = {}
    product = Product()

    # try:
    driver.get(url)

    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#INTRODUCE')))

    product.product_name = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > h3').text
    parse_script(driver, category, product)
    product.product_price = int(utils.only_num_price(driver.find_element(By.CSS_SELECTOR, "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1ziwSSdAv8 > div.WrkQhIlUY0 > div").find_element(By.CSS_SELECTOR, "span._1LY7DqCnwR").text + "원)"))
    product.stock_num = 1
    product.product_state = "신상품"
    product.save()
    set_option(driver, wait, data, product)
    data["상세설명"] = ""
    imgs_url = [img.get_attribute('src') for img in driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > ul > li > a > img')]
    if (len(imgs_url) == 0):
        imgs_url = [driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > div > div > img').get_attribute('src')]
    set_table(driver, data, delivery, origin_area, product)
    save_imgs(data, imgs_url, product)

    # except:
    #     driver.quit()
    #     exit()
    save_db(data, product)