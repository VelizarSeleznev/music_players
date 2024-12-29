# Смотри эта версия при копировании ссылки выдает название песни, может это нам лучше подойдет?

import pyperclip
import time
import requests
from bs4 import BeautifulSoup
from threading import Thread


def get_title_from_url(url):
    """
    Универсальная функция для извлечения заголовка из любого URL.
    """
    try:
        # Отправляем GET-запрос к URL
        response = requests.get(url, allow_redirects=True)
        response.raise_for_status()  # Проверка на ошибки HTTP

        # Получаем конечный URL (на случай редиректа)
        final_url = response.url

        # Загружаем контент страницы
        page = requests.get(final_url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, 'html.parser')

        # Пробуем получить заголовок из мета-тега og:title
        title_tag = soup.find("meta", property="og:title")
        if title_tag and title_tag["content"]:
            return title_tag["content"]

        # Если мета-тег отсутствует, пробуем взять <title>
        if soup.title:
            return soup.title.string

        return "Название не найдено"
    except Exception as e:
        return f"Ошибка: {e}"


def monitor_clipboard():
    """
    Функция для мониторинга буфера обмена и обработки ссылок.
    """
    last_text = ""
    print("Мониторинг буфера обмена запущен. Скопируйте любую ссылку.")
    try:
        while True:
            clipboard_text = pyperclip.paste()  # Получаем текущий текст из буфера
            if clipboard_text != last_text and clipboard_text.startswith("http"):
                last_text = clipboard_text
                print(f"Обнаружена ссылка: {clipboard_text}")
                title = get_title_from_url(clipboard_text)
                print(f"Заголовок страницы: {title}")
            time.sleep(1)  # Проверка каждую секунду
    except KeyboardInterrupt:
        print("\nМониторинг завершен. До свидания!")


def run_monitor_in_thread():
    """
    Запуск мониторинга в отдельном потоке для безопасного завершения.
    """
    monitor_thread = Thread(target=monitor_clipboard, daemon=True)
    monitor_thread.start()

    try:
        # Основной поток продолжает работать
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nПрограмма завершена.")


if __name__ == "__main__":
    run_monitor_in_thread()