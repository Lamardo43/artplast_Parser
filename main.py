import requests
from bs4 import BeautifulSoup
import warnings
import time

warnings.filterwarnings('ignore')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}

characteristic_names = ['Вид', 'Модель', 'Страна', 'Материал', 'Вместимость', 'Диаметр', 'Длина', 'Ширина',
                        'Производитель', 'Форма', 'Цвет', 'Вложение', 'Упаковка', 'Объем', 'Вес', 'Толщина',
                        'Высота', 'Назначение']

characteristic_list = {}

def try_return(text):
    for key, val in characteristic_list.items():
        if key.find(text) >= 0:
            return str(val)

    return "Не указано"

def get_data(url):
    try:
        req = requests.get(url, verify=False)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        containers = soup.find_all("div", class_="col-span-3 space-y-3")
        for contain_url in containers:
            contain_url = "https://www.artplast.ru" + contain_url.find("a").get("href")
            with open("links.txt", "a", encoding="utf-8") as file:
                file.write(f"{contain_url}\n")

    except:
        pass

    # with open("site_code.html", "w", encoding="utf-8") as file:
    #     file.write(src)

count = 1

def get_info_container(url):
    global characteristic_names
    global characteristic_list
    global count

    try:
        req = requests.get(url, verify=False)
        src = req.text
        soup = BeautifulSoup(src, "lxml")

        try:
            name = soup.find("h1", class_="title title--h1").text.replace("\n", "").replace("\t", "").replace("\n", "")
        except:
            name = 'Имя не найдено'

        try:
            discr = str(soup.find("div", class_="prose"))[28:].replace('\t', "").replace("\n", " ").split("<br/>")
            discr[len(discr)-1] = discr[len(discr)-1].replace("</div>", "")
        except:
            discr = ["Описание не найдено"]

        try:
            art = soup.find("div", class_="space-x-2 text-sm")\
                .find("span", class_="text-black font-bold")\
                .text.replace("\t", "").replace("\n", "")
        except:
            art = "Артикул не найден"

        try:
            price = soup.find("div", class_="flex items-end space-x-1")\
                .find("span", class_="text-2xl font-extrabold").text.replace("\t", "").replace("\n", "")
        except:
            price = "Цена не найдена"

        img_list = []
        try:
            img_links = soup.find("div", class_="grid grid-cols-1 gap-8 lg:gap-16 lg:grid-cols-4")\
            .find("div", class_="relative")\
            .find("div", class_="swiper swiper--product")\
            .find("div", class_="swiper-wrapper")\
            .find_all("div", class_="swiper-slide")
            for img_link in img_links:
                img_list.append("https://www.artplast.ru/" + img_link.find("a").get("href"))
        except:
            img_list.append("Изображения не найдены")

        try:
            package_count = soup.find("div", class_="grid grid-cols-1 gap-8 lg:gap-16 lg:grid-cols-4")\
                .find("div", class_="space-y-6 lg:mx-10 lg:col-span-2 2xl:col-span-1")\
                .find("div", class_="space-y-6")\
                .find("span", class_="text-xs whitespace-nowrap text-black-gray").text.replace("\t", "").replace("\n", "")
            count_up = package_count[:package_count.find("х")-1]
            count_sht = package_count[package_count.find("х") + 2:package_count.find("=") - 1]
            equals = package_count[package_count.find("=") + 2:]
        except:
            count_up = "-"
            count_sht = "-"
            equals = "-"

        category_list = []
        try:
            categories = soup.find_all("div", class_="px-[6px] py-2 md:py-3")
            for category in categories:
                category_list.append(category.find("a", class_="tag tag--xs").text.replace("\t", "").replace("\n", ""))
        except:
            category_list.append("Категори не найдены")

        try:
            characteristics = soup.find("div", class_="w-full lg:w-5/12")\
                .find("div", class_="space-y-5 lg:space-y-10")\
                .find("ul", class_="space-y-4").find_all("li", class_="relative flex items-end justify-between before:border-b before:absolute before:bottom-1 before:w-full before:border-gray before:border-dashed before:-z-10")
            for characteristic in characteristics:
                characteristic_name = characteristic.find("span", class_="pr-3 bg-white text-sm md:text-base "
                                                                      "whitespace-nowrap").text.replace("\t", "").replace("\n", "")
                characteristic_val = characteristic.find("span", class_="w-1/3 pl-3 text-sm bg-white md:text-base "
                                                                        "md:font-semibold").text.replace("\t", "").replace("\n", "")
                characteristic_list[characteristic_name] = characteristic_val
        except:
            pass

        with open("itog.txt", "a", encoding="utf-8") as file:
            file.write(f"{name}\t")
            for disc in discr:
                file.write(f"{disc}, ")
            file.write(f"\t{art}\t{price}\t")
            for img in img_list:
                file.write(f"{img} ")
            file.write(f"\t{count_up}\t{count_sht}\t{equals}\t")
            for category in category_list:
                file.write(f"{category}, ")
            file.write("\t")

            for characteristic in characteristic_names:
                file.write(f"{try_return(characteristic)}\t")

            file.write(url)

            file.write("\n")
        count+=1
    except:
        print(f"WARNING ---------------------- {count}")
        count+=1


# for i in range(4):
#     get_data(f"https://www.artplast.ru/catalog/kanctovary/?page={i}")

with open("links.txt", "r", encoding="utf-8") as linkss:
    links = linkss.readlines()
linkss.close()

for link in links:
    characteristic_list.clear()
    print(f"{count}")
    get_info_container(link[:-1])

# get_info_container("https://www.artplast.ru/tovar/sousnik-s-kryshkoy-nakhlobuchkoy-prozrachnyy-50-ml-d-60-mm-kh1200-1244-box4food-rossiya-43657/")