import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
 
 def scrape_page(url, session):
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table_rows = soup.find_all('tr')

    page_data = []
    for row in table_rows:
        shlok = row.find('td', {'class': 'shlok'})
        arth = row.find('td', {'class': 'arth'})
        if shlok and arth:
            shlok_text = shlok.get_text(strip=True)
            arth_text = arth.get_text(strip=True)
            page_data.append({
                'Shlok': shlok_text,
                'Arth': arth_text
            })

    return page_data

def scrape_all_pages():
    all_data = []
    base_url = "https://satsangdhara.net/vara/"

    urls = []
    for i in range(0, 76):  
        if i < 10:
            url = f"{base_url}k3s00{i}.htm"
        elif i < 100:
            url = f"{base_url}k3s0{i}.htm"
        else:
            url = f"{base_url}k3s{i}.htm"
        urls.append(url)

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_page, url, session) for url in urls]
            for future in futures:
                page_data = future.result()
                print(f"Scraped data from page: {urls[futures.index(future)]}")
                all_data.extend(page_data)

    df = pd.DataFrame(all_data)
    df.to_excel('data/xyz.xlsx', index=False)

scrape_all_pages()
