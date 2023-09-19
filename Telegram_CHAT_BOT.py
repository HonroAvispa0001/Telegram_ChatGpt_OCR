import datetime
import json
import logging
import os
import re
import base64


import openai
import requests
from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackContext, MessageHandler, filters)

logger = logging.getLogger(__name__)


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def process_message_and_generate_response(update: Update, context: CallbackContext):
    # Si el mensaje es una imagen, utiliza la función process_image_and_generate_response
    if update.message.photo:
        await process_image_and_generate_response(update, context)
    # Si el mensaje es un texto, utiliza ChatGPT para generar una respuesta
    elif update.message.text:
        # Obtiene el texto del mensaje
        text = update.message.text
        #logger.info(f"Received message: {text}")

        # Genera la respuesta con ChatGPT
        assistant_reply = await generate_response(text)

        # Envía la respuesta al usuario
        await context.bot.send_message(chat_id=update.effective_chat.id, text=assistant_reply)



async def process_image_and_generate_response(update: Update, context: CallbackContext):
    #print("INICIADO")
    # Descarga la imagen
    photo_file = await context.bot.get_file(update.message.photo[-1].file_id)
    photo_path = os.path.join('img_sources', f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')}.jpg")
    await photo_file.download(photo_path)

    # Procesa la imagen con OCR y GPT-3
    text_photo = await process_image(photo_path)
    assistant_reply = await generate_response(text_photo)
    messsage = text_photo + "\n" + "\n" + assistant_reply

    # Envía la respuesta al usuario
    await context.bot.send_message(chat_id=update.effective_chat.id, text=messsage)

    # Elimina la imagen
    #os.remove(photo_path)


async def process_image(photo_path: str):
    # Convierte la imagen a formato base64
    with open(photo_path, 'rb') as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode('utf-8')

    # Especifica la URL de la API de Google Cloud Vision
    url = 'https://vision.googleapis.com/v1/images:annotate?key=AIzaS...'

    # Especifica los parámetros de la petición
    data = {
      "requests": [
        {
          "image": {
            "content": img_base64
          },
          "features": [
            {
              "type": "TEXT_DETECTION"
            },
            {
              "type": "DOCUMENT_TEXT_DETECTION"
            },
            {
              "type": "TEXT_DETECTION",
              "model": "builtin/stable:ocr_math"
            }
          ]
        }
      ]
    }

    # Realiza la petición a la API
    response = requests.post(url, data=json.dumps(data))

    # Verifica si la respuesta incluye la clave 'responses'
    if 'responses' in response.json():
        text = response.json()['responses'][0]['fullTextAnnotation']['text']
    else:
        text = ''

    # Limpia el texto
    text = re.sub(r'\bO\b', '', text)
    text = re.sub(r'OA\)', 'A)', text)
    text = re.sub(r'OB\)', 'B)', text)
    text = re.sub(r'OC\)', 'C)', text)
    text_photo = re.sub(r'OD\)', 'D)', text)

    return text_photo

async def generate_response(text_photo):

    openai.api_key = "sk-lXZa..."
    openai.organization = "org-YD..."

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "system", "content": "Vas a ser un excelente ayudante de resolucion de examenes, La respuesta que des sobre la pregunta tiene que ser corta, por ejemplo: Opción a), Opción B), etc. Si no hay opciones en la pregunta Igual tienes que dar una respuesta lo mas corto y concisa posible"},
            {"role": "user", "content": text_photo}
        ]
    )

    assistant_reply = completion['choices'][0]['message']['content']

    return assistant_reply


if __name__ == '__main__':
    application = ApplicationBuilder().token('60596....:AAHd...').build()

    message_handler = MessageHandler(filters.ALL, process_message_and_generate_response)

    application.add_handler(message_handler)

    application.run_polling()
