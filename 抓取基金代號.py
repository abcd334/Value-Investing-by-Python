from bs4 import BeautifulSoup

url=
soup = BeautifulSoup(chrome.page_source, "lxml")
df = soup.find_all('span')