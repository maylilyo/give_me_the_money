import re
#정규식

import requests
from bs4 import BeautifulSoup
#web crawling

from datetime import datetime
#현재 년도

import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
#kivy

def find_minimum_wage(current_year): #최저시급 추출
    #current_year = 2020
    webpage = requests.get('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=2020+최저시급')
    soup = BeautifulSoup(webpage.content, "html.parser")
    web_text = soup.select(".wage_table")[0].get_text()
    web_text_list = web_text.split("    ")
    web_text_list = web_text_list[3:]
    for text in web_text_list:
        if current_year + "년" in text:
            w = text
            break
    regex = re.compile(r"\d*,\d+원")
    wage = regex.search(w)
    wage = wage.group()
    wage = wage[:-1].split(",")
    return int("".join(wage))

    
def find_wage(worktime, material_cost, count, minimum_wage):
    #임금을 계산해서 return하는 함수
    #input : 노동시간(hour){전체}, 재료비, 개수, 최저시급
    #output : 개당 받아야 하는 임금
    wage, cost = 0, 0
    for key, value in material_cost.items():
        cost += value
    wage = round((minimum_wage * worktime + cost) / count)
    return wage


class MyApp(App):
    def build(self):
        a = "안녕하세요"
        return Label(text=a)

if __name__ == '__main__':
    current_year = str(datetime.today().year)
    minimum_wage = find_minimum_wage(current_year)
    material_cost = {"체인":300, "기타":10000}
    count = 3 #개수
    worktime = 10 #전체 노동시간
    w = find_wage(worktime, material_cost, count, minimum_wage)
    print("개당 {} 이상 받아야 최저시급 이에요!".format(w))

    MyApp().run()
    #kivy에서 받아와야할 정보 : worktime(int), material_cost(dict), count(int)