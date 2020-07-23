# coding: utf-8

import re
#정규식

import requests
from bs4 import BeautifulSoup
#web crawling

from datetime import datetime
#현재 년도

import kivy
kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
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
        font = 'C:\\Users\\mayli\\Desktop\\give_me_the_money\\JejuMyeongjo.ttf'
        
        #전체 box insert
        border_box = BoxLayout(orientation='vertical')

        #title box 양식 설정
        minimum_wage_text = "2020년\n최저시급:\n" + str(find_minimum_wage(str(datetime.today().year))) +"원"
        title_box = BoxLayout(orientation='horizontal')
        title_image = Button(text="이미지 삽입", font_name = font)
        title_label = Label(text="최저시급 계산기", font_name = font)
        title_wage = Label(text=minimum_wage_text, font_name = font)
        title_box.add_widget(title_image)
        title_box.add_widget(title_label)
        title_box.add_widget(title_wage)

        #time Schedule box 양식 설정
        time_schedule_box = BoxLayout(orientation='horizontal')
        time_label = Label(text="노동시간(전체, 시 기준)", font_name = font)
        time_text_insert = Label(text="텍스트박스자리", font_name = font)
        time_schedule_box.add_widget(time_label)
        time_schedule_box.add_widget(time_text_insert)
        
        #재료비 입력 box 양식 설정
        material_inform_box = BoxLayout(orientation='vertical')
        material_name = Label(text="재료 이름", font_name = font)
        material_inform_box.add_widget(material_name)

        material_detail_inform_box = BoxLayout(orientation='horizontal')
        material_detail_name = Label(text="양", font_name = font)
        material_detail_count = Label(text="금액자리", font_name = font)
        material_detail_inform_box.add_widget(material_detail_name)
        material_detail_inform_box.add_widget(material_detail_count)
        material_inform_box.add_widget(material_detail_inform_box)

        #재료비 box 양식 설정
        material_cost_box = BoxLayout(orientation='horizontal')
        material_label = Label(text="총 재료", font_name = font)
        material_cost_box.add_widget(material_label)
        material_cost_box.add_widget(material_inform_box)

        #개수 지정 양식 설정
        count_box = BoxLayout(orientation='horizontal')
        count_label = Label(text="생산 개수", font_name = font)
        count_text_insert = Label(text="개수입력자리", font_name = font)
        count_box.add_widget(count_label)
        count_box.add_widget(count_text_insert )

        #최저시급 출력 box 양식 설정
        cost_box = BoxLayout(orientation='horizontal')
        cost_insert = Label(text="계산된 최저시급 자리", font_name = font)
        cost_box.add_widget(Label(text="계산된 최저시급은",font_name = font))
        cost_box.add_widget(cost_insert)
        cost_box.add_widget(Label(text="입니다.",font_name = font))

        #copywrite box 양식 설정
        copywrite_box = BoxLayout(orientation='horizontal')
        copywrite_box.add_widget(Label(text="copywrite maylilyo",font_name = font))

        #전체 box에 각각의 box insert
        border_box.add_widget(title_box)
        border_box.add_widget(time_schedule_box)
        border_box.add_widget(material_cost_box)
        border_box.add_widget(count_box)
        border_box.add_widget(cost_box)     
        border_box.add_widget(copywrite_box)

        return border_box

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