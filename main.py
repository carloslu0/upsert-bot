import os
import telebot
import requests

API_KEY = os.getenv('TELEGRAM_TOKEN')  # Fetching the Telegram Bot Token from the environment variable
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # Only process the document if the bot is mentioned in the caption
        if message.caption and '@upsert_bot' in message.caption:
            # Only process the document if it's a PDF
            if message.document.mime_type == 'application/pdf':
                # Download file from Telegram
                file_info = bot.get_file(message.document.file_id)
                download_url = f"https://api.telegram.org/file/bot{API_KEY}/{file_info.file_path}"
                response = requests.get(download_url)
                with open('tempfile.pdf', 'wb') as file:
                    file.write(response.content)

                # Open downloaded file and upload to the API
                with open('tempfile.pdf', 'rb') as file:
                    form_data = {
                        'files': file,
                        'chunksize': (None, '1'),
                        'chunkoverlap': (None, '1'),
                        'temperature': (None, '1')
                    }

                    response = requests.post("https://flowise-08rv.onrender.com/api/v1/prediction/144cb34e-a30f-4a9c-b1f5-3325e33d4b42", files=form_data, timeout=60)
                    print(response.json())
            else:
                bot.reply_to(message, 'Only PDF files are supported.')
    except requests.exceptions.Timeout:
        bot.reply_to(message, 'Request timed out.')
    except Exception as e:
        bot.reply_to(message, str(e))

bot.polling()