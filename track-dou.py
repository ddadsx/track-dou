import requests
from bs4 import BeautifulSoup
import time
import ctypes  
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    d = ''
    def handle_data(self, data):
        if (data != '\n'):
            self.d += data
        else:
            print(self.d)
            self.d = ''

parser = MyHTMLParser()

name = "Seu nome aqui" 
from_date = "0001-01-01" # aaaa-mm-dd
to_date =  time.strftime("%Y-%m-%d")# current day
time_between_requests = 3600 # In seconds

URL = "http://www.in.gov.br/consulta?q=%22" + name.replace(' ','%20') + "%22&publishFrom=" + from_date + "&publishTo=" + to_date
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
old_content = soup.find_all("div","resultados-wrapper d-none")

while(True):

    when = time.localtime()
    when = str(when.tm_hour) + ":" + str(when.tm_min) + " (" + str(when.tm_mday) + "/" + str(when.tm_mon) + ")"
    msg = "\n[INFO]\tBuscando nova atualização às " + str(when)
    print(msg)
    
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    new_content = soup.find_all("div","resultados-wrapper d-none")
    #print(new_content)
    parser.feed(str(new_content))

    if new_content != old_content:
        ctypes.windll.user32.MessageBoxW(0, "Seu nome apareceu no Diário Oficial da União", "Atualização disponível", 64)
        old_content = new_content
    else:
        msg = "[INFO]\tNada novo...\n"
        print(msg)

    time.sleep(time_between_requests) #Verifica a cada 1h
