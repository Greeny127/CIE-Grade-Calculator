import os
import requests
from bs4 import BeautifulSoup

for year in range(10, 24):
    URL = f"website-url"
    request = requests.get(URL)

    soup = BeautifulSoup(request.content, "lxml")
    files = soup.find_all('a', class_="name")

    for file in files:
        filename = file.attrs["href"]
        if "gt" in filename:
            print(filename)
            pdfurl = f"website-url/20{year}/{filename}"
            pdf = requests.get(pdfurl)
            code = 9700
            os.makedirs(
                f"dir\\data\\{code}\\", exist_ok=True)
            with open(f"data/{code}/{filename}", "wb") as f:
                f.write(pdf.content)
