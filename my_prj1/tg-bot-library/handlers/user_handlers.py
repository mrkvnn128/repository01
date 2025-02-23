from copy import deepcopy
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message
from database.database import user_dict_template, users_db
from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
from keyboards.bookmarks_kb import create_books_keyboard, create_bookmarks_keyboard, create_edit_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from lexicon1.lexicon1 import LEXICON
from services.file_handling import books

router = Router()


@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(LEXICON[message.text])
    if message.from_user.id not in users_db:
        users_db[message.from_user.id] = deepcopy(user_dict_template)

@router.message(Command(commands='choose_book'))
async def process_choose_book_command(message: Message):
    await message.answer("Выберите книгу:", reply_markup=create_books_keyboard())

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(LEXICON[message.text])


@router.message(Command(commands='beginning'))
async def process_beginning_command(message: Message):
    user_id = message.from_user.id
    current_book = users_db[user_id]['current_book']
    if current_book:
        users_db[user_id]['page'] = 1
        text = books[current_book][users_db[user_id]['page']]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )


@router.message(Command(commands='continue'))
async def process_continue_command(message: Message):
    user_id = message.from_user.id
    current_book = users_db[user_id]['current_book']
    if current_book:
        text = books[current_book][users_db[user_id]['page']]
        await message.answer(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )

@router.message(Command(commands='bookmarks'))
async def process_bookmarks_command(message: Message):
    user_id = message.from_user.id
    current_book = users_db[user_id].get('current_book')
    if not current_book:
        await message.answer("Выберите книгу перед использованием закладок.")
        return
    if users_db[user_id]["bookmarks"]:
        await message.answer(
            text="Ваши закладки:",
            reply_markup=create_bookmarks_keyboard(
                users_db[user_id]["bookmarks"], current_book
            )
        )
    else:
        await message.answer("У вас пока нет закладок.")



@router.callback_query(lambda callback: callback.data.startswith("book_"))
async def process_book_select(callback: CallbackQuery):
    book_id = callback.data.split("_")[1]
    if book_id in books:
        users_db[callback.from_user.id]['current_book'] = book_id
        users_db[callback.from_user.id]['page'] = 1  # Сброс на первую страницу
        await callback.message.answer(
            text=f"Вы выбрали книгу: {book_id}",
            reply_markup=create_pagination_keyboard(
                'backward',
                f'1/{len(books[book_id])}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'forward')
async def process_forward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id]['current_book']
    if current_book and users_db[user_id]['page'] < len(books[current_book]):
        users_db[user_id]['page'] += 1
        text = books[current_book][users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )
    await callback.answer()


@router.callback_query(F.data == 'backward')
async def process_backward_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id]['current_book']
    if current_book and users_db[user_id]['page'] > 1:
        users_db[user_id]['page'] -= 1
        text = books[current_book][users_db[user_id]['page']]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )
    await callback.answer()

@router.callback_query(lambda x: '/' in x.data and x.data.split('/')[0].isdigit())
async def process_page_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id].get('current_book')
    
    if current_book:
        page = int(callback.data.split('/')[0])
        users_db[user_id]['page'] = page
        
        # Добавляем закладку
        if 'bookmarks' not in users_db[user_id]:
            users_db[user_id]['bookmarks'] = set()
        users_db[user_id]['bookmarks'].add(page)
        
        # Получаем текст страницы
        text = books[current_book][page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )
        await callback.answer('Страница добавлена в закладки!')
    else:
        await callback.answer("Выберите книгу перед добавлением закладки.")



@router.callback_query(IsDigitCallbackData())
async def process_bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id]['current_book']
    if current_book:
        page = int(callback.data)
        users_db[user_id]['page'] = page
        text = books[current_book][page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{users_db[user_id]["page"]}/{len(books[current_book])}',
                'forward'
            )
        )


@router.callback_query(F.data == 'edit_bookmarks')
async def process_edit_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.message.edit_text(
        text=LEXICON[callback.data],
        reply_markup=create_edit_keyboard(
            *users_db[user_id]["bookmarks"]
        )
    )


@router.callback_query(F.data == 'cancel')
async def process_cancel_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['cancel_text'])


@router.callback_query(IsDelBookmarkCallbackData())
async def process_del_bookmark_press(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id].get('current_book')

    # Проверяем, выбрана ли текущая книга
    if not current_book:
        await callback.answer("Книга не выбрана. Удаление невозможно.", show_alert=True)
        return

    # Извлекаем номер закладки из callback_data
    try:
        page = int(callback.data[:-3])
        users_db[user_id]['bookmarks'].remove(page)

        # Если остались закладки, обновляем клавиатуру
        if users_db[user_id]['bookmarks']:
            await callback.message.edit_text(
                text="Ваши закладки:",
                reply_markup=create_bookmarks_keyboard(
                    users_db[user_id]['bookmarks'],
                    current_book
                )
            )
        else:
            # Если закладок не осталось, отправляем сообщение
            await callback.message.edit_text("У вас больше нет закладок.")
    except ValueError:
        await callback.answer("Ошибка удаления закладки!", show_alert=True)

@router.callback_query(F.data == "delete_all_bookmarks")
async def process_delete_all_bookmarks(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Удаляем все закладки
    users_db[user_id]['bookmarks'].clear()

    # Обновляем сообщение с пустым списком
    await callback.message.edit_text("Все закладки удалены.")

@router.callback_query(lambda cb: cb.data.startswith("goto_"))
async def process_goto_bookmark(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_book = users_db[user_id].get('current_book')

    # Проверяем, выбрана ли текущая книга
    if not current_book:
        await callback.answer("Книга не выбрана. Действие невозможно.", show_alert=True)
        return

    # Переходим на выбранную страницу
    try:
        page = int(callback.data.split('_')[1])  # Пример: 'goto_12' -> 12
        users_db[user_id]['page'] = page

        text = books[current_book][page]
        await callback.message.edit_text(
            text=text,
            reply_markup=create_pagination_keyboard(
                'backward',
                f'{page}/{len(books[current_book])}',
                'forward'
            )
        )
    except (ValueError, KeyError):
        await callback.answer("Ошибка при переходе к закладке!", show_alert=True)


