from unicodedata import category
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os 
import urllib.request
import json
import datetime
from . import excelFunc
from . import utils
from ..models import *

def save_imgs(data, imgs_url):
    #동영상은 대기하세요~~
    folder = './img'
    data["추가이미지"] = ""

    if not os.path.isdir(folder):
        os.mkdir(folder)
    
    for index, link in enumerate(imgs_url) :
        urllib.request.urlretrieve(link.split('?')[0], f'{folder}/{data["상품번호"]}_{index}.jpg')
        if index == 0:
            data["대표이미지"] = f'{data["상품번호"]}_{index}.jpg'
        else:
            data["추가이미지"] += f'{data["상품번호"]}_{index}.jpg\n'

def parse_script(driver, data, category_dict):
    json_object = json.loads(driver.execute_script("return arguments[0].innerHTML", driver.find_element(By.CSS_SELECTOR, "script")))
    categorys = json_object["category"].split(">")
    temp = category_dict
    for category in categorys:
        temp = temp[category]
    if len(categorys) != 4:
        temp = temp[""]
    data["카테고리코드"] = temp

def add_data(tr, data, delivery, origin_area):
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
        elif key == "재화등의 배송방법에 관한 정보":
            if td[i].text == "택배" or td[i].text == "소포" or td[i].text == "등기":
                data["배송방법"] = "택배, 소포, 등기"
            else:
                data["배송방법"] = "직접배송(화물배달)"
        elif key == "판매자 지정택배사":
            data["택배사코드"] = delivery[td[i].text]
        elif key == "원산지":
            area = td[i].text.split(" ")[-1].split(")")[0]
            if origin_area.get(area):
                data["원산지코드"] = origin_area[area]
            else:
                data["원산지코드"] = "04"
                data["원산지 직접입력"] = td[i].text
        elif key == "반품배송비":
            if td[i].text != "무료":
                data["반품배송비"] = td[i].text.split(" ")[1].replace(",", "").replace("원","")
            else:
                data["반품배송비"] = "0"
        elif key == "교환배송비":
            if td[i].text != "무료":
                data["교환배송비"] = td[i].text.replace(",", "").replace("원","")
            else:
                data["교환배송비"] = "0"
        elif key == "A/S 안내":
            data["A/S 안내"] = ""
            for text in td[i].text.split("\n")[1:]:
                data["A/S 안내"] += text + "\n"
        elif key == "제조일자" or key == "유효일자":
            data[key] = td[i].text.replace(".","-")[:-1]
        else:
            data[key.split("-")[0]] = td[i].text

def set_option(driver, wait, data):
    data["추가상품명"] = ""
    data["추가상품값"] = ""
    data["옵션명"] = ""
    data["옵션값"] = ""
    data["추가상품가"] = ""
    data["옵션가"] = ""
    data["옵션 재고수량"] = ""

    data["직접입력 옵션"] = [input.text for input in driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > label')]
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
        if (type == "추가상품") : 
            data["추가상품명"] += op.text + "\n"
            data["추가상품값"] += utils.array_to_string(utils.remove_price(select_text)) + "\n"
            data["추가상품가"] += utils.array_to_string(utils.only_num_price(price) for price in select_text) + "\n"
        else :
            data["옵션명"] += op.text + "\n"
            data["옵션값"] += utils.array_to_string(utils.remove_price(select_text)) + "\n"
            data["옵션가"] += utils.array_to_string(utils.only_num_price(price) for price in select_text) + "\n"
            data["옵션 재고수량"] += utils.array_to_string(utils.only_num_price("1원)") for price in select_text) + "\n"
        for sel in select:
            if (sel.text.find("(품절)") == -1):
                sel.click()
                break

        if data["옵션가"] == "":
            data["옵션형태"] = ""
        else:
            data["옵션형태"] = "단독형"
        for split_enter in data["옵션가"].split("\n"):
            for price in split_enter.split(","):
                if price != "0":
                    data["옵션형태"] = "조합형"
        data["옵션 재고수량"] = data["옵션 재고수량"].split("\n")[0]

def set_table(driver, data, delivery, origin_area):
    for div in driver.find_elements(By.CSS_SELECTOR, "#INTRODUCE > div > div"):
        if div.get_attribute("class") != "":
            for tr in div.find_elements(By.CSS_SELECTOR, "tr"):
                add_data(tr, data, delivery, origin_area)
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
            # for img in div.find_elements(By.CSS_SELECTOR, "img"):
            #     src = img.get_attribute("data-src")
            #     if src and src.find("video") == -1 and src.find("data:image") == -1:
            #         data["상세설명"] += '<img src="' + img.get_attribute("data-src") + '">\n'

    for tr in driver.find_elements(By.CSS_SELECTOR, "#RETURNPOLICY > div > table > tbody > tr"):
        add_data(tr, data, delivery, origin_area)
    for tr in driver.find_elements(By.CSS_SELECTOR, "#content > div > div.z7cS6-TO7X > div.etc > div._1aH4b0l27f > div._211Avwm-sU > table > tbody > tr"):
        add_data(tr, data, delivery, origin_area)

def save_db(data):
    product = Product()
    # shipping = Shipping()
    # after_service = AS()

    product.category_code = data["카테고리코드"]
    product.product_name = data["상품명"]
    product.product_state = data["상품상태"]
    product.product_price = int(data["판매가"])
    if data.get("부가세"):
        product.vat = data["부가세"]
    product.stock_num = data["재고수량"]
    if data.get("옵션형태"):
        product.option_type = data["옵션형태"]
    product.main_img = data["대표이미지"]
    if data.get("브랜드"):
        product.brand = data["브랜드"]
    if data.get("제조사"):
        product.manufacturer = data["제조사"]
    if data.get("제조일자"):
        date = data["제조일자"].split("-")
        product.manufacturing_date = datetime.date(date[0], date[1], date[2])
    if data.get("유효일자"):
        date = data["유효일자"].split("-")
        product.effective_date = datetime.date(date[0], date[1], date[2])
    product.origin_code = data["원산지코드"]
    if data.get("수입사"):
        product.importer = data["수입사"]
    if data.get("복수원산지여부"):
        product.is_plural_origin = data["복수원산지여부"]
    if data.get("원산지 직접입력"):
        product.origin_direct_input = data["원산지 직접입력"]
    if data.get("상품정보제공고시\n품명"):
        product.info_name = data["상품정보제공고시\n품명"]
    if data.get("상품정보제공시\n모델명"):
        product.info_model_name = data["상품정보제공시\n모델명"]
    if data.get("상품정보제공시\n인증허가사항"):
        product.info_authorization = data["상품정보제공시\n인증허가사항"]
    if data.get("상품정보제공시\n제조자"):
        product.info_manufacturer = data["상품정보제공시\n제조자"]
    print(product.product_name)
    product.save()

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
    
    if data.get("옵션형태"):
        option_names = data["옵션명"].split("\n")[:-1]
        option_values = data["옵션값"].split("\n")[:-1]
        option_prices = data["옵션가"].split("\n")[:-1]
        #재고수량
        
        for idx, name in enumerate(option_names):
            option_name = OptionName()
            option_name.name = name
            option_name.product = product
            option_name.save()
            option_value = option_values[idx].split(",")
            option_price = option_prices[idx].split(",")
            for i in range(len(option_value)):
                option = Option()
                option.value = option_value[i]
                option.price = int(option_price[i])
                option.option_name = option_name
                option.save()
                if idx == 0:
                    nums = data["옵션 재고수량"].split(",")
                    option_stock_num = OptionStockNum()
                    option_stock_num.option = option
                    option_stock_num.num = nums[i]
                    option_stock_num.save()

    # test
    if data.get("직접입력 옵션"):
        for input in data["직접입력 옵션"].split("\n"):
            direct_input_option = DirectInputOption()
            direct_input_option.product = product
            direct_input_option.text = input
    
    if data.get("추가상품값"):
        additional_product_values = data["추가상품값"].split("\n")
        additional_product_prices = data["추가상품가"].split("\n")
        additional_product_nums = data["추가상품 재고수량"].split("\n")
        for name in data["추가상품명"].split("\n"):
            additional_product_name = AdditionalProductName()
            additional_product_name.product = product
            additional_product_name.name = name
            additional_product_name.save()
            for i in range(len(additional_product_values)):
                values = additional_product_values[i].split(",")
                prices = int(additional_product_prices[i].split(","))
                nums = additional_product_nums[i].split(",")
                for j in range(len(values)):
                    addtional_product_detail = AdditionalProductDetail()
                    addtional_product_detail.additional_product_name = additional_product_name
                    addtional_product_detail.value = values[j]
                    addtional_product_detail.price = int(prices[j])
                    addtional_product_detail.num = nums[j]
                    addtional_product_detail.save()

    if data.get("추가이미지"):
        for img in data["추가이미지"].split("\n")[:-1]:
            sub_img = SubImg()
            sub_img.product = product
            sub_img.img = img
            sub_img.save()
    
def goods_details(driver, url, delivery, origin_area, category, sheet, row_count):
    data = {}

    # try:
    driver.get(url)

    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#INTRODUCE'))) #?

    data["상품명"] = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > h3').text
    # price = [find.text for find in driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > fieldset > div > div > div > strong > span')][1]
    price = driver.find_element(By.CSS_SELECTOR, "#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._1ziwSSdAv8 > div.WrkQhIlUY0 > div").find_element(By.CSS_SELECTOR, "span._1LY7DqCnwR").text
    data["판매가"] = utils.only_num_price(price + "원)")
    set_option(driver, wait, data)
    data["상세설명"] = ""
    imgs_url = [img.get_attribute('src') for img in driver.find_elements(By.CSS_SELECTOR, '#content > div > div > div > ul > li > a > img')]
    if (len(imgs_url) == 0):
        imgs_url = [driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > div > div > img').get_attribute('src')]
    set_table(driver, data, delivery, origin_area)
    save_imgs(data, imgs_url)

    data["재고수량"] = 1
    data["배송비유형"] = "무료"

    parse_script(driver, data, category)
    # except:
    #     driver.quit()
    #     exit()
    save_db(data)
    # excelFunc.save_xl(data, sheet, row_count)