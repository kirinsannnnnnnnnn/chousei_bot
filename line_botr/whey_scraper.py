from urllib import (request, parse)
from bs4 import BeautifulSoup
import re

URL_WHEY = "https://www.myprotein.jp/sports-nutrition/impact-whey-protein/10530943.html"

def is_whey_page(soup_whey):
  if soup_whey.find("h1").text == "Impact ホエイ プロテイン":
    return True
  else:
    return False

def get_off_rate(soup_whey):
  off_rate_line = soup_whey.findAll('span', text=re.compile(".*\%.*"))
  if len(off_rate_line) == 0:
    return ""
  if len(off_rate_line) > 1:
    for line in off_rate_line:
      if "オフコード" in line:
        off_rate_line = [line]
  text = "今日のmyproteinのホエイプロテインの割引↓\n{}".format(off_rate_line[0].text)
  return text

def get_whey_off_rate():
  try:
    source_whey = request.urlopen(URL_WHEY)
    soup_whey = BeautifulSoup(source_whey, "lxml")
    if not is_whey_page(soup_whey):
      return "ERROR: ホエイプロテインのURLもしくはタグが変わったようです"
    else:
      return get_off_rate(soup_whey)
  except:
    return "500: 何らかのエラーが発生しました(つまり分かりません)"

if __name__ == "__main__":
  print(get_whey_off_rate())
