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
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang.builder import Builder
#kivy

worktime, material_costs, count, minimum_wage = 0,0,0,0
#global변수

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
    # for key, value in material_cost.items():
    #     cost += value
    wage = round((minimum_wage * worktime + material_cost) / count)
    print(wage)

    return wage


def on_enter_timetext(instance): #노동시간 입력
    # print('User pressed enter in', instance)
    # print(instance.text)
    global worktime
    worktime = instance.text
    # print("worktime : {}".format(worktime))

def on_enter_count(instance): #총재료 입력
    global count
    count = instance.text
    # print("count : {}".format(count))

class MyApp(App):
    def press(self,instance): #계산 눌렀을 때
        print("Pressed")
        global worktime, material_costs, count, minimum_wage
        self.cost = find_wage(int(worktime), material_costs, int(count), minimum_wage)
        print(self.cost)
        print(worktime, count, material_costs, minimum_wage)

    def on_enter_material_count(self, instance):
        global material_costs
        print(instance.text)
        material_costs += int(instance.text)

    def build(self):
        global minimum_wage
        print(material_costs)
        Builder.load_file('./my.kv')
        a = "안녕하세요"
        font = 'C:\\Users\\mayli\\Desktop\\give_me_the_money\\JejuMyeongjo.ttf'
        minimum_wage = find_minimum_wage(str(datetime.today().year))
        #전체 box insert
        border_box = BoxLayout(orientation='vertical')

        #title box 양식 설정
        minimum_wage_text = "2020년\n최저시급:\n" + str(minimum_wage) +"원"
        title_box = BoxLayout(orientation='horizontal')
        title_image = Image(source='moneysqurriel.png')
        title_label = Label(text="최저시급 계산기", font_name = font, font_size='20sp')
        title_wage = Label(text=minimum_wage_text, font_name = font)
        title_box.add_widget(title_image)
        title_box.add_widget(title_label)
        title_box.add_widget(title_wage)

        #time Schedule box 양식 설정
        time_schedule_box = BoxLayout(orientation='horizontal')
        time_label = Label(text="노동시간\n(전체, 시 기준)", font_name = font, width=100, font_size='17sp')
        time_text_insert = TextInput(text='', multiline=False, font_name = font)
        time_text_insert.bind(on_text_validate=on_enter_timetext)
        time_schedule_box.add_widget(time_label)
        time_schedule_box.add_widget(time_text_insert)
        
        #재료비 입력 box 양식 설정
        material_inform_box = BoxLayout(orientation='vertical')
        material_name = TextInput(text="재료 이름(지우고 입력)", font_name = font, width=100)
        material_detail_count = TextInput(text="총 금액(지우고 입력)",multiline=False,font_name = font)
        material_detail_count.bind(on_text_validate=self.on_enter_material_count)

        material_inform_box.add_widget(material_name)
        material_inform_box.add_widget(material_detail_count)

        #재료비 box 양식 설정
        material_cost_box = BoxLayout(orientation='horizontal')
        material_label = Label(text="총 재료", font_name = font, font_size='17sp')
        material_cost_box.add_widget(material_label)
        material_cost_box.add_widget(material_inform_box)

        #개수 지정 양식 설정
        count_box = BoxLayout(orientation='horizontal')
        count_label = Label(text="생산 개수", font_name = font, font_size='17sp')
        count_text_insert = TextInput(multiline=False,font_name = font)
        count_text_insert.bind(on_text_validate=on_enter_count)
        count_box.add_widget(count_label)
        count_box.add_widget(count_text_insert)

        #확인 양식 지정
        calculate_button = Button(text='계산', font_name = font)
        calculate_button.bind(on_press=self.press)

        #최저시급 출력 box 양식 설정
        cost='0'
        cost_box = BoxLayout(orientation='horizontal')
        cost_insert = Label(text="계산된 최저시급 자리", font_name = font)
        cost_box.add_widget(Label(text="계산된\n최저시급은",font_name = font, font_size='20sp'))
        cost_box.add_widget(Label(text=cost,font_name = font))
        cost_box.add_widget(Label(text="입니다.",font_name = font, font_size='20sp'))

        #copywrite box 양식 설정
        copywrite_box = BoxLayout(orientation='horizontal', height=50)
        copywrite_box.add_widget(Label(text="copywrite maylilyo",font_name = font, height=50))

        #전체 box에 각각의 box insert
        border_box.add_widget(title_box)
        border_box.add_widget(time_schedule_box)
        border_box.add_widget(material_cost_box)
        border_box.add_widget(count_box)
        border_box.add_widget(calculate_button)
        border_box.add_widget(cost_box)     
        border_box.add_widget(copywrite_box)

        #window size 지정
        Window.size = (400, 700)
        return border_box

if __name__ == '__main__':
    current_year = str(datetime.today().year)
    # minimum_wage = find_minimum_wage(current_year)
    # material_cost = {"체인":300, "기타":10000}
    # count = 3 #개수
    # worktime = 10 #전체 노동시간
    # w = find_wage(worktime, material_cost, count, minimum_wage)
    # print("개당 {} 이상 받아야 최저시급 이에요!".format(w))

    MyApp().run()
    #kivy에서 받아와야할 정보 : worktime(int), material_cost(dict), count(int)