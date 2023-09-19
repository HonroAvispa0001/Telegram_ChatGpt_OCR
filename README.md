# Telegram_ChatGpt_OCR
El código es un script de Python que utiliza varias bibliotecas para crear un bot de Telegram con capacidad para procesar y responder mensajes de texto e imágenes. A continuación, se describe el código paso por paso:

1. **Importación de módulos y configuración de logging:**
    - Se importan varios módulos necesarios, incluyendo `openai` para interactuar con el modelo GPT-3.5-turbo y `telegram` para interactuar con la API de Telegram.
    - Se configura el logger para registrar eventos con una estructura específica.

2. **Función `process_message_and_generate_response`:**
    - Esta función es el punto de entrada para procesar los mensajes que recibe el bot. Según el contenido del mensaje (texto o imagen), delega el procesamiento a otras funciones.

3. **Función `process_image_and_generate_response`:**
    - Si el mensaje recibido es una imagen, se ejecuta esta función. 
    - Descarga la imagen y guarda con un nombre basado en la fecha y hora actual.
    - Llama a la función `process_image` para obtener el texto de la imagen mediante OCR y a `generate_response` para obtener una respuesta de GPT-3.
    - Envia la respuesta generada al usuario y elimina la imagen del servidor (nota que la eliminación de la imagen está comentada).

4. **Función `process_image`:**
    - Convierte la imagen a base64 y envía una solicitud POST a la API de Google Cloud Vision para realizar la detección de texto (OCR).
    - Limpia el texto obtenido, reemplazando ciertos caracteres y corrigiendo posibles errores de OCR.
    - Devuelve el texto limpio.

5. **Función `generate_response`:**
    - Configura la clave de API y el ID de organización para la API de OpenAI.
    - Crea un chat de completitud utilizando el modelo GPT-3.5-turbo y los mensajes especificados.
    - Extrae y devuelve la respuesta generada por el modelo.

6. **Main script:**
    - Define el token de API para el bot de Telegram.
    - Crea un handler para procesar todos los mensajes recibidos con la función `process_message_and_generate_response`.
    - Inicia el polling para comenzar a recibir y procesar mensajes.

**Aspectos destacados:**
- El script está diseñado para actuar como un bot que asiste en la resolución de problemas, proporcionando respuestas cortas y concisas a las preguntas que se le presentan, tanto en forma de texto como de imágenes.
- Utiliza el OCR de Google Cloud Vision para extraer texto de las imágenes.
- Utiliza GPT-3.5-turbo para generar respuestas a las preguntas.
- Está configurado para ejecutarse de manera asincrónica, lo que permite un mejor rendimiento en entornos con muchas solicitudes simultáneas.

## Ejemplo de uso
![Captura de pantalla 2023-09-18 234519](https://github.com/HonroAvisp/Telegram_ChatGpt_OCR/assets/73007200/3705afc8-f337-46e9-bc69-1e7a152a8405)
