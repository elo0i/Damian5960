#Made by @elo0i (Twitter user) I don't know how to do the license thing so do whatever you want with the code.
#Sorry to all english speakers but a lot of parts of the code and its clarifications are in Spanish because I am too lazy to fully translate the English version of the code, but I have translated the system prompts that guide the modules so don't complain either.
#To change the language translante the prompts and edit "lang=en" on google_search (line 140)

# !!!!IMPORTANT!!!! You have to specify a route for a loading gif in the line 388

import sys
import openai
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QFrame, QSpacerItem, QSizePolicy, QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QMovie

import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import tkinter as tk
from tkinter import ttk

openai.api_key = "YOUR_KEY_GOES_HERE"

messages = [
    {"role": "system", "content": "Your only function is to make a very detailed list with all the steps that an AI with an internet connection would have to follow to respond to the user's request. You can't answer any other way."},
]


def chat_with_assistant(user_message):
    messages.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=300,
            temperature=0.7,
            top_p=1,
        )
        print("Solicitud de chat_with_assistant completada")
        assistant_response = response.choices[0].message['content'].strip()
        print("ASYSRESPONSE: ", assistant_response)
        messages.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        print(f"Error al llamar a la API de GPT-4: {e}")
        return None


def chat_with_assistant_v2(user_message, system_message):
    messages_v2 = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": """[
  Where does Elon Musk live?
  "latest Elon Musk news",
  "current location Elon Musk",
  "API geolocation time zone",
  "local time time zone Elon Musk",
  "Elon Musk sleep time"
  "Recent Elon Musk Twitter Activity",
  "recent posts Elon Musk",
  "Elon Musk sleep schedules",
  "Elon Musk tweets",
]"""},
    ]

    messages_v2.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages_v2,
            max_tokens=150,
            temperature=0.7,
            top_p=1,
        )
        print("Solicitud de chat_with_assistant_v2 completada")
        assistant_response = response.choices[0].message['content'].strip()
        print("***ASSISTANT-RESPONSE***", assistant_response)
        messages_v2.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        print(f"Error al llamar a la API de GPT-4: {e}")
        return None

    messages_v2.append({"role": "user", "content": user_message})
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages_v2,
        max_tokens=150,
        temperature=0.7,
        top_p=1,
    )
    print("Solicitud de chat_with_assistant_v2 completada")  # Agrega esta línea
    assistant_response = response.choices[0].message['content'].strip()
    print("***ASSISTANT-RESPONSE***", assistant_response)
    messages_v2.append({"role": "assistant", "content": assistant_response})
    return assistant_response


def chat_with_assistant_v3(user_message, system_message):
    messages_v2 = [
        {"role": "system", "content": system_message},
    ]

    # Comprobar y acortar user_message si excede los 21000 caracteres
    print(f"Las busquedas? de internet tienen: {len(user_message)} caracteres")
    if len(user_message) > 21000:
        user_message = user_message[:21000]
        print("El mensaje con los resultados de internet se ha acortado a 21000 caracteres")

    messages_v2.append({"role": "user", "content": user_message})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages_v2,
            max_tokens=600,
            temperature=0.7,
            top_p=1,
        )
        print("Solicitud de chat_with_assistant_v3 completada")  # Cambia a "_v3" en lugar de "_v2"
        assistant_response = response.choices[0].message['content'].strip()
        print("***ASSISTANT-RESPONSE***", assistant_response)
        messages_v2.append({"role": "assistant", "content": assistant_response})
        return assistant_response
    except Exception as e:
        print(f"Error al llamar a la API de GPT-4: {e}")
        return None

def pre_busqueda(assistant_response):
    system_message = "Your only function is to create a python list with the most relevant searches that could be done in google on the list of instructions that the user will give you next. You can ONLY respond with a list of at most 10 queries in python format."
    new_assistant_response = chat_with_assistant_v2(assistant_response, system_message)
    return new_assistant_response

api_key = "YOUR_KEY_GOES_HERE"  # Reemplaza con tu clave API
cse_id = "YOUR_ID_GOES_HERE""  # Reemplaza con tu ID de motor de búsqueda personalizado

SEARCH_METHOD = "RAPIDO"  # Cambiar a "LENTO" para usar el método lento

def google_search(query, num_results=2):
    service = build("customsearch", "v1", developerKey=api_key)
    result = service.cse().list(q=query, cx=cse_id, num=num_results, lr='lang_en').execute()
    links = [item['link'] for item in result['items']]
    return links


def get_visible_text(soup):
    [s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
    return ' '.join(soup.stripped_strings)

chrome_driver_path = 'D:\chromedriver.exe'

def get_page_content_slow(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("start-maximized")
    options.add_argument("disable-cache")
    options.add_argument("disable-application-cache")
    options.add_argument("disable-offline-load-stale-cache")
    options.add_argument("disk-cache-size=0")
    options.add_argument("log-level=3")
    options.add_argument("--silent")
    options.add_argument("--incognito")

    service = Service(executable_path=chrome_driver_path)
    browser = webdriver.Chrome(service=service, options=options)

    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        visible_text = get_visible_text(soup)
        return visible_text
    except Exception as e:
        print(f"Error al obtener la página {url}: {e}")
        return None
    finally:
        browser.quit()

def get_page_content_fast(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'
    }

    session = requests.Session()

    try:
        response = session.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            visible_text = get_visible_text(soup)
            truncated_text = visible_text[:1250]  # Truncate the text to the first 10,000 characters
            return truncated_text
        else:
            print(f"Error al obtener la página {url}: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print(f"Tiempo de espera agotado para la URL: {url}")
        return None
    except Exception as e:
        print(f"Error al obtener la página {url}: {e}")
        return None


def buscador(consultas):
    resultados = []

    for consulta in consultas:
        print(f"\nBuscando resultados para: {consulta}\n")
        resultados_consulta = buscar_resultados(consulta)
        resultados.append(resultados_consulta)
    print("LOS RESULTADOS DEL BUSCADOR SON: ", resultados)
    return resultados

def buscar_resultados(query):
    links = google_search(query)

    content_list = []
    for link in links:
        print(f"Obteniendo contenido de: {link}")
        if SEARCH_METHOD == "LENTO":
            content = get_page_content_slow(link)
            #print(content)
        else:
            content = get_page_content_fast(link)
            #print(content)

        if content:
            content_list.append(content)

    print("***LA CONTENT LIST ES: ", content_list)
    return content_list

def respuesta_final(resultados_input, primer_mensaje):
    user_message = str(resultados_input)
    first_message_content = messages[1]['content']
    system_message = f"The user will provide you with information taken from the internet. Give him an answer to his question ({first_message_content}) based on the information he has sought to try to solve these instructions: {primer_mensaje}"
    print("EL mensaje de SYSTEM para RESP_FINAL es: ", system_message)
    final_response = chat_with_assistant_v3(user_message, system_message)

    return final_response

def show_final_response(final_response):
    # Crea una nueva ventana
    window = tk.Toplevel()
    window.title("Respuesta Final")

    # Agrega un cuadro de texto para mostrar la respuesta
    text_box = tk.Text(window, wrap=tk.WORD)
    text_box.insert(tk.END, final_response)
    text_box.config(state=tk.DISABLED)
    text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    # Agrega una barra de desplazamiento
    scroll_bar = ttk.Scrollbar(window, command=text_box.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.config(yscrollcommand=scroll_bar.set)

    window.mainloop()


class PreBusquedaThread(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, assistant_response):
        super().__init__()
        self.assistant_response = assistant_response

    def run(self):
        pre_busqueda_response = pre_busqueda(self.assistant_response)
        self.response_ready.emit(pre_busqueda_response)


class PreBusquedaWindow(QWidget):
    def __init__(self, pre_busqueda_response):
        super().__init__()
        self.initUI(pre_busqueda_response)

    def initUI(self, pre_busqueda_response):
        self.setGeometry(100, 100, 400, 200)
        self.setWindowTitle('Resultados de Pre-búsqueda')

        layout = QVBoxLayout()

        response_label = QLabel(self)
        response_label.setWordWrap(True)
        response_label.setText(pre_busqueda_response)
        layout.addWidget(response_label)

        self.setLayout(layout)

class ResultadosWindow(QWidget):
    def __init__(self, resultados):
        super().__init__()
        self.initUI(resultados)

    def initUI(self, resultados):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Resultados de búsqueda')

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        for index, resultado in enumerate(resultados):
            consulta_label = QLabel(self)
            consulta_label.setText(f"Consulta {index + 1}:")
            consulta_label.setStyleSheet("font-weight: bold;")
            self.scroll_layout.addWidget(consulta_label)

            for texto in resultado:
                contenido_label = QLabel(self)
                contenido_label.setWordWrap(True)
                contenido_label.setText(texto)
                contenido_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
                self.scroll_layout.addWidget(contenido_label)

            spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.scroll_layout.addItem(spacer)

        self.scroll_area.setWidget(self.scroll_content)

        self.setLayout(layout)



class AssistantThread(QThread):
    response_ready = pyqtSignal(str)

    def __init__(self, user_message):
        super().__init__()
        self.user_message = user_message

    def run(self):
        assistant_response = chat_with_assistant(self.user_message)
        self.response_ready.emit(assistant_response)

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 200)
        self.setWindowTitle('Chat con GPT-3.5 Turbo')

        layout = QVBoxLayout()

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        layout.addWidget(self.scroll_area)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.message_container = QVBoxLayout()
        self.scroll_layout.addLayout(self.message_container)

        self.add_message("Assistant", messages[0]['content'], is_user=False)

        self.scroll_area.setWidget(self.scroll_content)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Escribe tu mensaje aquí")
        layout.addWidget(self.user_input)

        self.send_button = QPushButton('Enviar', self)
        layout.addWidget(self.send_button)

        self.send_button.clicked.connect(self.on_send)

        self.setLayout(layout)

        # Configurar el GIF de carga
        self.loading_movie = QMovie(r"C:\Users\Eloi\Downloads\loading-gif-transparent.gif")  # Reemplaza la ruta del archivo GIF que deseas utilizar
        self.loading_label = QLabel(self)
        self.loading_label.setMovie(self.loading_movie)
        self.loading_label.hide()

    def add_message(self, user_name, message_text, is_user=True):
        message_frame = QFrame(self.scroll_content)
        message_frame.setFrameShape(QFrame.StyledPanel)
        message_frame.setFrameShadow(QFrame.Raised)
        message_frame.setAutoFillBackground(True)

        message_frame.setStyleSheet("""            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 5px;
            }
        """)

        message_label = QLabel(message_frame)
        message_label.setWordWrap(True)
        message_label.setMargin(5)
        message_text = message_text.replace("\n", "<br>")  # Reemplazar saltos de línea con etiquetas HTML <br>
        message_label.setText(f'<b>{user_name}:</b> {message_text}')
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)  # Permitir seleccionar y copiar el texto

        frame_layout = QVBoxLayout(message_frame)
        frame_layout.addWidget(message_label)
        frame_layout.setContentsMargins(10, 5, 10, 5)

        self.message_container.addWidget(message_frame)

        if not is_user:
            spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.message_container.addItem(spacer)

        if hasattr(self, "bottom_spacer"):
            self.message_container.removeItem(self.bottom_spacer)

        self.bottom_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.message_container.addItem(self.bottom_spacer)

    def on_send(self):
        user_message = self.user_input.text()
        if user_message.strip() == "":
            return

        self.user_input.clear()
        self.add_message("Usuario", user_message, is_user=True)

        QApplication.processEvents()

        # Mostrar y centrar el GIF de carga
        self.loading_label.setAlignment(Qt.AlignHCenter)
        self.message_container.addWidget(self.loading_label)
        self.loading_label.show()
        self.loading_movie.start()

        self.assistant_thread = AssistantThread(user_message)
        self.assistant_thread.response_ready.connect(self.update_chat)
        self.assistant_thread.start()

    def update_chat(self, assistant_response):
        self.add_message("Assistant", assistant_response, is_user=False)
        self.loading_label.hide()  # Oculta el GIF cuando llega la respuesta del asistente

        self.pre_busqueda_thread = PreBusquedaThread(assistant_response)
        self.pre_busqueda_thread.response_ready.connect(self.show_pre_busqueda)
        self.pre_busqueda_thread.start()

    def show_pre_busqueda(self, pre_busqueda_response):
        self.pre_busqueda_window = PreBusquedaWindow(pre_busqueda_response)
        self.pre_busqueda_window.show()

        # Convertir la respuesta de pre_busqueda en una lista
        consultas = eval(pre_busqueda_response)

        # Llamar a la función buscador con la lista de consultas
        resultados = buscador(consultas)
        print("buscadorconsultas********es: ", resultados)

        # Mostrar los resultados en una ventana con desplazamiento vertical
        self.resultados_window = ResultadosWindow(resultados)
        self.resultados_window.show()

        # Probando para respuesta final a ver si vai ben
        second_message_content = messages[2]['content']
        print("*******PRIMERMENSAJE????????: ", second_message_content)

        # Hacer algo con los resultados, como mostrarlos en una ventana
        final_response = respuesta_final(resultados, second_message_content)
        print("*****Respuesta final:", final_response)

        show_final_response(final_response)


if __name__ =='__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
