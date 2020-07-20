import re
#정규식

import requests
from bs4 import BeautifulSoup
#web crawling

from datetime import datetime
#현재 년도

def find_minimum_wage(current_year): #최저시급 추출
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

    
def find_wage(worktime, base, minimum_wage):
    wage = 0
    #임금을 계산해서 return하는 프로그램이다.
    #input : 노동시간, 재료비, 최저시급 
    #find_wage
    #output : 받아야 하는 임금
    return wage


if __name__ == '__main__':
    current_year = str(datetime.today().year)
    minimum_wage = find_minimum_wage(current_year)
    print(minimum_wage)
    w : int
    w = find_wage(0, 0, minimum_wage)