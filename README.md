# 🏠 Telegram Bot Número Star – Consulta de Posición en Lista de Viviendas

Este bot de Telegram permite a los usuarios de una promoción de viviendas consultar su **posición en la lista de adjudicación** mediante el número `star` asignado por la promotora. Su objetivo es proporcionar información clara y accesible a cada usuario de forma automatizada y segura.

---

## Creación del bot

En la primera fase este bot fue creado originalmente por el usuario [alfonsoelmas](https://github.com/alfonsoelmas) \\ (https://github.com/tecnosor/python-telegram-bot-with-ddd)  
Para las fases posteriores se modificó para ponerlo en funcionamiento. La última versión del bot, con la que actualmente está funcionando, se encuentra en este repositorio.

---

## ⚙️ Funcionalidades

- 🔎 Consulta personalizada de posición ingresando el número `star`.  
- 🧾 Almacenamiento de los códigos y posiciones en un archivo JSON estructurado.  
- 📲 Integración sencilla con la API de Telegram.  
- 🔐 Registro previo del número Star con su fecha para consultas seguras y personalizadas.

---

## 🛠️ Comandos principales disponibles

El bot ofrece una serie de comandos para que puedas gestionar tu registro y consultar tu posición de forma sencilla:

- `/registrar` — Para añadirte como Star y registrarte en la lista.
- `/actualizar` — Para modificar o actualizar tu información de Star.
- `/borrar` — Para eliminar tu registro de la lista.
- `/miposicion` — Para consultar tu posición actual en la lista de Stars.

Además, cuando inicies por primera vez, el bot te enviará un mensaje de bienvenida personalizado explicándote cómo usar estos comandos para que no te pierdas.

---
## 🗂️ Estructura del Proyecto

- `src/`: Código fuente del bot.  
- `.secrets/`: Carpeta que contiene el archivo `secrets.json` donde se guarda la API Key del bot de Telegram, la ruta al JSON de usuarios y otros secretos necesarios para el funcionamiento seguro de la aplicación.  
- `persistentmemorydb/`: Carpeta con la base de datos JSON que almacena los usuarios y sus posiciones.  

---

## 🚀 Cómo obtener la API Key de un bot de Telegram

1. **Abre Telegram y busca el bot [@BotFather](https://t.me/BotFather)**  
   Es el bot oficial para crear y gestionar bots en Telegram.

2. **Inicia una conversación con @BotFather**  
   Pulsa "Start" o escribe `/start` para comenzar.

3. **Crea un nuevo bot**  
   Envía el comando `/newbot`.

4. **Sigue las instrucciones:**  
   - Elige un nombre para tu bot (visible para los usuarios).  
   - Elige un **username único** para el bot (debe terminar en `bot`, por ejemplo: `mi_promocion_bot`).

5. **Recibe el token de autenticación (API Key)**  
   @BotFather te enviará un mensaje con un token único similar a este:  
   `123456789:ABCDefGHIjklMNOpQRsTuvWXyz1234567890`

6. **Guarda el token en un lugar seguro**  
   Este token es la clave que permite a tu código controlar el bot, no lo compartas públicamente.

7. **Configura tu bot con este token en tu proyecto**  
   Por ejemplo, colócalo en tu archivo de secretos `.secrets/secrets.json` para que tu aplicación lo utilice.

---

Si tienes alguna duda o quieres colaborar, no dudes en abrir un issue o hacer un pull request.  
¡Gracias por usar el Bot Número Star!


## Top Contributors
- @alfonsoplusplus | Creación del bot y definición de arquitectura y mínimos.
- @roberto22palomar | Evolución del bot y documentación
