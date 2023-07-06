    try:
        product_description_element = soup.find('div', {'id': 'productDescription'})
        paragraphs = product_description_element.find_all('p')
        product_description = ' '.join([p.get_text().strip() for p in paragraphs]) if paragraphs else None
    except AttributeError:
        product_description = None