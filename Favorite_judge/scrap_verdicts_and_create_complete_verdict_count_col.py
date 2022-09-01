import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime


import pandas as pd

df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCount.csv', low_memory=False)



url_list = df['url'].to_list()

url_to_word_count_dict = dict()
for i,url in enumerate(url_list):
    # if i <= 3000:
    #     continue
    if i%1000==0:
        df.to_csv('..\LawDbWithSeniorityAndVerdictCount.csv', encoding="utf-8-sig", index=False)
        df = pd.read_csv('..\LawDbWithSeniorityAndVerdictCount.csv', low_memory=False)

    if url_list[i] in url_to_word_count_dict:
        df.loc[i, 'words_in_verdict'] = url_to_word_count_dict[url_list[i]]
        continue

    page = requests.get(url_list[i])
    soup = BeautifulSoup(page.text, 'html.parser')

    list_of_words= soup.text.strip().split()
    list_of_words = [w for w in list_of_words if len(w) >1]

    word_count = len(list_of_words)
    df.loc[i , 'words_in_verdict'] = word_count
    url_to_word_count_dict[url_list[i]] = word_count
    print(i)



df.to_csv('..\LawDbWithSeniorityAndVerdictCount.csv', encoding="utf-8-sig", index=False)
