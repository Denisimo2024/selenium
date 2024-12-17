from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def open_wikipedia_page(browser, query):
    """Открывает страницу Википедии по запросу."""
    url = f"https://ru.wikipedia.org/wiki/{query.replace(' ', '_')}"
    browser.get(url)
    time.sleep(2)  # Небольшая пауза для загрузки страницы


def list_paragraphs(browser):
    """Листает и выводит параграфы текущей статьи."""
    print("\nСодержимое статьи:\n")
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    for i, p in enumerate(paragraphs):
        text = p.text.strip()
        if text:
            print(f"{i + 1}. {text[:300]}...")  # Ограничим вывод 300 символами
    print("\n--- Конец содержимого статьи ---\n")


def list_internal_links(browser):
    """Собирает и возвращает внутренние ссылки статьи."""
    links = browser.find_elements(By.TAG_NAME, "a")
    internal_links = {}
    for i, link in enumerate(links):
        href = link.get_attribute("href")
        title = link.text.strip()
        if href and "/wiki/" in href and "http" in href and title:
            internal_links[i + 1] = {"title": title, "url": href}
    return internal_links


def print_internal_links(links):
    """Выводит список связанных страниц."""
    print("\nСвязанные страницы:")
    for i, data in links.items():
        print(f"{i}. {data['title']}")
    print()


def main():
    browser = webdriver.Chrome()
    print("Добро пожаловать в Википедия-поисковик!")
    print("Чтобы выйти из программы, введите 'выход'.\n")

    try:
        query = input("Введите ваш запрос для поиска на Википедии: ")
        if query.lower() == "выход":
            return

        open_wikipedia_page(browser, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи.")
            print("2. Перейти на одну из связанных страниц.")
            print("3. Выйти из программы.")
            choice = input("Ваш выбор: ")

            if choice == "1":
                list_paragraphs(browser)
            elif choice == "2":
                internal_links = list_internal_links(browser)
                if not internal_links:
                    print("Связанные страницы не найдены.")
                    continue

                print_internal_links(internal_links)
                page_choice = input("Введите номер страницы для перехода или 'назад' для возврата: ")
                if page_choice.lower() == "назад":
                    continue
                elif page_choice.isdigit() and int(page_choice) in internal_links:
                    link = internal_links[int(page_choice)]["url"]
                    browser.get(link)
                    time.sleep(2)
                    print(f"\nПерешли на страницу: {internal_links[int(page_choice)]['title']}")
                else:
                    print("Неверный ввод. Попробуйте снова.")
            elif choice == "3":
                print("Выход из программы...")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        browser.quit()
        print("Программа завершена.")


if __name__ == "__main__":
    main()

