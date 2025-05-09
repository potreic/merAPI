import requests
from bs4 import BeautifulSoup

def magmalevelonly():
    result = {}
    web = requests.get('https://magma.esdm.go.id/v1/gunung-api/tingkat-aktivitas').text
    HTMLResult = ((BeautifulSoup(web, "html.parser").find_all('div',  class_= "table-responsive")[0]).find('tbody'))
    linkcheck = 0
    judul2 = ""
    url = []
    def ceking(HTMLResult):
            for ip in HTMLResult.find_all('a', class_="tx-inverse tx-14 tx-medium d-block"):
                judul = ip.get_text(strip=True)
                if judul in j.get_text(strip=True):
                    return False, judul
            return True, judul2
    def checkinglink(k):
        for l in k.find_all('a', href=True, class_=False):
            url.append(l['href'])
    for i in HTMLResult.find_all('tr'):
        for j in i.find_all('td'):
            tes, judul = ceking(HTMLResult)
            checkinglink(j)
            judul2 = judul
            if tes and not (j.get_text(strip=True)).isnumeric():
                gunung = (j.get_text(strip=True)).replace("Lihat laporan","").split(" - ")
                result[judul2][gunung[0]] = {"location":gunung[1],"link":url[linkcheck]}
                linkcheck += 1
            elif tes == False:
                result[judul2] = {}
    return result

def main():
    levels = magmalevelonly()
    print(levels)

if __name__ == "__main__":
    main()
