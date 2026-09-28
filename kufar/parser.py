import requests as rq
import re
import json
import os

name_of_product = input("Введите предмет для поиска: ").lower()

pay_load = {
    "query" : name_of_product,
    "ot" : 1,
    "rgn" : "all",
    
}

response = rq.get("https://www.kufar.by/l", params=pay_load)
print(response.status_code)

html_text = response.text

match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html_text, re.DOTALL)

if match:
    json_string = match.group(1)
    data = json.loads(json_string)

    ads = data.get("props", {}).get("initialState", {}).get("listing", {}).get("ads", [])

    with open(f"kufar/report_{name_of_product}.json", "w",encoding="utf-8") as file:
                file.write("[")


    for ad in ads:
        title = ad.get("subject")
        raw_price = ad.get("price_byn")

        if raw_price.isdigit() and float(raw_price) == 0:
            price = "Договорная"
        elif raw_price.isdigit():
            price = str(float(raw_price) / 100) + " BYN"

        link = ad.get("ad_link")
    
        with open(f"kufar/report_{name_of_product}.json", "a",encoding="utf-8") as file:
            file.write("{" + f'"goods":"{title}","price": "{price}","link":"{link}"' + "},\n")


    with open(f"kufar/report_{name_of_product}.json", "rb+") as file:
        file.seek(-3, os.SEEK_END)  # Перемещаемся в конец файла
        file.truncate() 
        

    with open(f"kufar/report_{name_of_product}.json", "a",encoding="utf-8") as file:
        file.write("\n]")    
else:
    print("Тег __NEXT_DATA__ не найден в ответе сервера")