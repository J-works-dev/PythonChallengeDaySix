import os
import requests
from bs4 import BeautifulSoup
from babel.numbers import format_currency

os.system("clear")
url = "https://www.iban.com/currency-codes"

print("Hello! Welcome to Currency Converter")

iban=requests.get(url)

indeed_soup = BeautifulSoup(iban.text, "html.parser")

pagination = indeed_soup.find("tbody")
c_list = pagination.find_all("td")

data = []
temp = []
# country_from = 0
# country_to = 0

for i in c_list:
  temp.append(i.string)

dic={}
x=0
num=0
for i in temp:
  x += 1
  if x%4 == 1:
    dic['country'] = i.capitalize()
  elif x%4 == 2:
    dic['currency'] = i
  elif x%4 == 3:
    dic['code'] = i
  else: # x%4 == 0:
    x = 0
    if "No universal currency" in dic['currency']:
      dic = {}
      pass
    else:
      num += 1
      dic['number'] = num
      data.append(dic)
      dic = {}

for i in data:
  print(f"# {i['number']} {i['country']}")

def get_country_from():
  print("\nWhere are you from? Choose a country by number")
  got = input("#: ")
  try:
    global country_from
    country_from = int(got)
    country_from -= 1
    if 0 <= country_from < len(data):
      print(data[country_from]['country'])
    else:
      print("Choose a number from the list.")
      get_country_from()
  except ValueError:
    print("That wasn't a number.")
    get_country_from()

def get_country_to():
  print("\nNow choose another country.")
  got = input("#: ")
  try:
    global country_to
    country_to = int(got)
    country_to -= 1
    if 0 <= country_to < len(data):
      print(data[country_to]['country'])
    else:
      print("Choose a number from the list.")
      get_country_to()
  except ValueError:
    print("That wasn't a number.")
    get_country_to()

def convert_currency():
  print(f"\nHow many {data[country_from]['code']} do you want to convert to {data[country_to]['code']}")
  got = input()
  try:
    amount = int(got)

    temp=requests.get(f"https://transferwise.com/gb/currency-converter/{data[country_from]['code'].lower()}-to-{data[country_to]['code'].lower()}-rate?amount={amount}")
    soup = BeautifulSoup(temp.text, "html.parser")
    table = soup.find("input", id="rate")
    if table is None:
      print("There is no country data on the Server. Please try again...\n")
      main()
    rate = table.get("value")
    result = int(amount)*float(rate)
    print(f'{format_currency(amount, data[country_from]["code"], locale="ko_KR")} is {format_currency(result, data[country_to]["code"], locale="ko_KR")}')
  except ValueError:
    print("That wasn't a number.")
    convert_currency()

def main():
  get_country_from()
  get_country_to()
  convert_currency()

main()

"""
Use the 'format_currency' function to format the output of the conversion
format_currency(AMOUNT, CURRENCY_CODE, locale="ko_KR" (no need to change this one))
"""

# print(format_currency(5000, "KRW", locale="ko_KR", format_type='name'))