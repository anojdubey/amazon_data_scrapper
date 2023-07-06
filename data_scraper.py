import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_product_listing_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = []
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    for result in results:
        try:
            product_url = "https://www.amazon.in" + result.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
            product_name = result.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
            product_price = result.find('span', {'class': 'a-price-whole'}).text.strip()
            rating_element = result.find('span', {'class': 'a-icon-alt'})
            rating = rating_element.text.strip().split()[0] if rating_element else None
            num_reviews_element = result.find('span', {'class': 'a-size-base s-underline-text'})
            num_reviews = num_reviews_element.text.strip() if num_reviews_element else None

            products.append({
                'Product URL': product_url,
                'Product Name': product_name,
                'Product Price': product_price,
                'Rating': rating,
                'Number of Reviews': num_reviews
            })
        except Exception as e:
            print('Error:', e)

    return products

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    asin = None
    product_description = None
    manufacturer = None

    product_details = soup.find('div', {'id': 'detailBullets_feature_div'})
    if product_details:
        ul_elements = product_details.find_all('ul')
        for ul_element in ul_elements:
            li_elements = ul_element.find_all('li')
            for li_element in li_elements:
                if 'ASIN' in li_element.text:
                    asin = li_element.find('span',class_=False,id=False).text.strip()
                    break
            if asin:
                break

    product_description_element = soup.find('div', {'id': 'productDescription'})
    if product_description_element:
        product_description = product_description_element.text.strip()

    product_details = soup.find('div', {'id': 'detailBullets_feature_div'})
    if product_details:
        ul_elements = product_details.find_all('ul')
        for ul_element in ul_elements:
            li_elements = ul_element.find_all('li')
            for li_element in li_elements:
                if 'Manufacturer' in li_element.text:
                    manufacturer = li_element.find('span',class_=False,id=False).text.strip()
                    break
            if manufacturer:
                break

    return {
        'ASIN': asin,
        'Product Description': product_description,
        'Manufacturer': manufacturer
    }

def scrape_amazon_products():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    max_pages = 20
    product_list = []

    for page in range(1, max_pages+1):
        print(f"Scraping page {page}...")
        url = base_url + str(page)
        products = scrape_product_listing_page(url)
        product_list.extend(products)
        time.sleep(2)

    with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'ASIN',
                      'Product Description', 'Manufacturer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for product in product_list:
            url = product['Product URL']
            details = scrape_product_details(url)
            product.update(details)
            writer.writerow(product)

    print('Scraping completed. Data saved to amazon_products.csv.')

scrape_amazon_products()
