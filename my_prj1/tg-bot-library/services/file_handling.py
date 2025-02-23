import os
import sys

PAGE_SIZE = 1050
books: dict[str, dict[int, str]] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    punctuations = ',.!:;?'
    finaly_size = size
    end = size + start
    if len(text) <= end:
        finaly_size = len(text) - start
    else:
        for i in range(end - 1, start, -1):
            if text[i] in punctuations and text[i + 1] not in punctuations:
                break
            finaly_size -= 1
    finaly_end = start + finaly_size
    fi_text = text[start:finaly_end]
    return fi_text, finaly_size

# Функция, формирующая словарь книги
def prepare_book(book_id: str, path: str) -> None:
    with open(file=path, mode='r', encoding='utf-8') as file:
        text = file.read()
    str_text = 0
    str_page = 1
    book_pages = {}
    while str_text < len(text):
        page_text, page_size = _get_part_text(text, str_text, PAGE_SIZE)
        book_pages[str_page] = page_text.lstrip()
        str_text += page_size
        str_page += 1
    books[book_id] = book_pages

# Пример загрузки нескольких книг
book_paths = {
    'book1': 'books/book1.txt',
    'book2': 'books/book2.txt',
    'book3': 'books/book3.txt',
    'book4': 'books/book4.txt',
}

# Загрузка всех книг
for book_id, path in book_paths.items():
    prepare_book(book_id, os.path.join(sys.path[0], os.path.normpath(path)))

# Пример обращения к книгам
# books['book1'][1] - Получить первую страницу первой книги
# books['book2'][5] - Получить пятую страницу второй книги

