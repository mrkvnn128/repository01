from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon1.lexicon1 import LEXICON
from services.file_handling import books  # books вместо book

'''
def create_books_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for book_id, pages in books.items():
        kb_builder.row(InlineKeyboardButton(
            text=f"Книга: {book_id}",
            callback_data=f"book_{book_id}"
        ))
    return kb_builder.as_markup()
'''
'''
def create_books_keyboard() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for book_id, pages in books.items():
        kb_builder.row(InlineKeyboardButton(
            text=f"Книга: {book_id}",
            callback_data=f"book_{book_id}" 
        ))
    return kb_builder.as_markup()
'''
def create_books_keyboard() -> InlineKeyboardMarkup:
    # Сопоставление идентификаторов книг с названиями
    book_titles = {
        "book1": "Р.Бредбери, Марсианские хроники",
        "book2": "Д.Роулинг, Гарри Поттер и философский камень",
        "book3": "Ф.Достоевский, Преступление и наказание",
        "book4": "С.Кинг, Оно"
    }
    kb_builder = InlineKeyboardBuilder()
    for book_id, pages in books.items():
        # Получаем название книги из словаря book_titles, если оно существует, иначе используем book_id
        title = book_titles.get(book_id, f"Без названия ({book_id})")
        # Создаём кнопку с текстом "book_id - title"
        kb_builder.row(InlineKeyboardButton(
            text=f"{title}",
            callback_data=f"book_{book_id}"
        ))
    return kb_builder.as_markup()
'''
def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{button} - {books["current_book"][button][:100]}',
            callback_data=str(button)
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['edit_bookmarks_button'],
            callback_data='edit_bookmarks'
        ),
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()
'''

'''
def create_bookmarks_keyboard(bookmarks: set, current_book: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для работы с закладками.
    Каждая закладка имеет кнопку с возможностью её удаления.
    """
    if not current_book:
        raise ValueError("Текущая книга не выбрана!")

    kb_builder = InlineKeyboardBuilder()
    
    # Создаем кнопки для каждой закладки
    for bookmark in sorted(bookmarks):
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{bookmark} - {books[current_book][bookmark][:100]}',
                callback_data=f"{bookmark}_del"  # Уникальное значение для удаления
            )
        )
    
    # Кнопка для выхода из режима редактирования
    kb_builder.row(
        InlineKeyboardButton(
            text="Отменить",
            callback_data="cancel"
        )
    )
    return kb_builder.as_markup()
'''

def create_bookmarks_keyboard(bookmarks: set, current_book: str) -> InlineKeyboardMarkup:
    if not current_book:
        raise ValueError("Текущая книга не выбрана!")

    kb_builder = InlineKeyboardBuilder()

    # Кнопки для перехода к закладкам
    for bookmark in sorted(bookmarks):
        kb_builder.row(
            InlineKeyboardButton(
                text=f'{bookmark} - {books[current_book][bookmark][:100]}',
                callback_data=f"goto_{bookmark}"  # Уникальная команда для перехода
            )
        )
    
    # Кнопка для удаления всех закладок
    kb_builder.row(
        InlineKeyboardButton(
            text="❌ Удалить все закладки",
            callback_data="delete_all_bookmarks"
        )
    )

    # Кнопка для выхода из режима редактирования
    kb_builder.row(
        InlineKeyboardButton(
            text="Отмена",
            callback_data="cancel"
        )
    )

    return kb_builder.as_markup()


def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    for button in sorted(args):
        kb_builder.row(InlineKeyboardButton(
            text=f'{LEXICON["del"]} {button} - {books["current_book"][button][:100]}',
            callback_data=f'{button}del'
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON['cancel'],
            callback_data='cancel'
        )
    )
    return kb_builder.as_markup()
