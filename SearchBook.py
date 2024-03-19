import requests
def search(search_query):
    api_url = 'https://www.googleapis.com/books/v1/volumes?q=' + search_query
    response = requests.get(api_url)
    if response.status_code == 200:
        books_data = response.json()
        items = books_data.get('items', [])
        books = []
        for item in items:
            volume_info = item.get('volumeInfo', {})
            title = volume_info.get('title')
            authors = volume_info.get('authors')
            genre = volume_info.get('categories') if 'categories' in volume_info else None
            synopsis = volume_info.get('description')
            publisher = volume_info.get('publisher')
            published_date = volume_info.get('publishedDate')
            page_count = volume_info.get('pageCount')
            image_link = volume_info.get('imageLinks', {}).get('smallThumbnail') if 'imageLinks' in volume_info else None

            # Verificar que todos los campos existen
            if all([title, authors, genre, synopsis, publisher, published_date, page_count, image_link]):
                book_info = {
                    'title': title,
                    'authors': ', '.join(authors),
                    'genre': ', '.join(genre),
                    'synopsis': synopsis,
                    'publisher': publisher,
                    'published_date': published_date,
                    'page_count': page_count,
                    'image_link': image_link
                }
                books.append(book_info)
        return books
    else:
        return 'Error: ' + str(response.status_code), 400