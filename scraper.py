from bs4 import BeautifulSoup
import requests
from pandas import DataFrame

# get web page html
page = requests.get('https://www.newegg.com/p/pl?N=100007709&srchInDesc=rx%202070&hisInDesc=rx%202070&ActiveSearchResult=True&PageSize=96')
soup = BeautifulSoup(page.content, 'lxml')
result_list = soup.find('div', class_='items-view is-grid')
containers = result_list.find_all('div', {'class': 'item-container'}) # Create list of all individual results

field_names = ['brands', 'product names', 'prices', 'shipping costs', 'promotions', 'urls']
brands = []
product_names = []
prices = []
shipping_costs = []
promotions = [] 
urls = []

for container in containers: 
    # Retrieve Desired Fields
    # clean brand name
    if container.find('a', class_='item-brand'):
        brands.append(container.find('a', class_='item-brand').img['title'])
    else: 
        brands.append('Brand Not Available')

    # Retrieve item name
    product_names.append(container.find('a', class_='item-title').text)

    # clean pricing 
    if container.find('li', class_='price-current').strong and container.find('li', class_='price-current').sup:
        prices.append(container.find('li', class_='price-current').strong.text + container.find('li', class_='price-current').sup.text)
    else:
        if container.find('li', class_='price-current').text.strip() == '':
            prices.append('unknown')
        else:
            prices.append(container.find('li', class_='price-current').text.strip())

    # clean shipping costs
    if container.find('li', class_='price-ship').text.replace('Shipping', '').replace('$', '').strip() == 'Free':
        shipping_costs.append(0)
    else:
        shipping_costs.append(container.find('li', class_='price-ship').text.replace('Shipping', '').replace('$', '').strip())

    # clean promotions
    if len(container.find('p', class_='item-promo').text.strip()) > 0:
        promotions.append(container.find('p', class_='item-promo').text.strip())
    else:
        promotions.append('no promo')

    # get urls for each result
    urls.append(container.a['href'])

# turn lists into dictionary
data_set = dict(zip(field_names, [brands, product_names, prices, shipping_costs, promotions, urls]))
df = DataFrame(data_set, columns=field_names)

df.to_csv('scraper_results.csv', header=True)
print(df)