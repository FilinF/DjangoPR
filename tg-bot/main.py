from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests
import os
import pandas as pd

TOKEN = '6182777381:AAHymrY0WtjhiRhlk_Hag4jQH4SeXnQRuyM'
UPLOAD_DIR = 'temp'

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        ["Загрузить файл", "Показать файлы", "Удалить файлы"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        'Привет! Выберите одно из действий:',
        reply_markup=reply_markup
    )

async def handle_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    file = await context.bot.get_file(document.file_id)
    file_path = os.path.join(UPLOAD_DIR, document.file_name)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    await file.download_to_drive(file_path)

    with open(file_path, 'rb') as f:
        response = requests.post('http://proxy:8000/upload_excel/', files={'file': f})

    if response.status_code == 200:
        json_data = response.json()
        formatted_data = format_data(json_data)
        await update.message.reply_text(f'Файл успешно загружен и обработан:\n{formatted_data}', parse_mode='Markdown')
    else:
        await update.message.reply_text('Произошла ошибка при обработке файла.')

def format_data(json_data):
    if isinstance(json_data, list):
        df = pd.DataFrame(json_data)
        return df.to_markdown(index=False)
    return "Не удалось отформатировать данные"

async def list_files(update: Update, context: CallbackContext) -> None:
    response = requests.get('http://proxy:8000/api/list_files/')
    if response.status_code == 200:
        file_list = response.json().get('files', [])
        if file_list:
            files_text = "\n".join(file_list)
            await update.message.reply_text(f"Загруженные файлы:\n{files_text}")
        else:
            await update.message.reply_text("Нет загруженных файлов.")
    else:
        await update.message.reply_text("Произошла ошибка при получении списка файлов.")

async def handle_button(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Загрузить файл":
        await update.message.reply_text("Отправьте мне файл Excel.")
    elif text == "Показать файлы":
        await list_files(update, context)
    elif text == "Удалить файлы":
        await delete_files(update, context)
    else:
        await update.message.reply_text("Пожалуйста, используйте кнопки для навигации.")

async def delete_files(update: Update, context: CallbackContext) -> None:
    response = requests.post('http://proxy:8000/delete-files/')
    if response.status_code == 200:
        message = response.json().get('message', 'Все файлы успешно удалены.')
        await update.message.reply_text(message)
    else:
        await update.message.reply_text("Произошла ошибка при удалении файлов.")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("delete", delete_files))
    application.add_handler(MessageHandler(filters.Document.ALL & filters.Document.MimeType(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"), handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_button))

    application.run_polling()

if __name__ == '__main__':
    main()