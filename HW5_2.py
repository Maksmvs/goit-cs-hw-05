import string
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
import requests
import matplotlib.pyplot as plt

# Функція для завантаження тексту з URL
def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(f"Помилка: {e}")
        return None

# Функція для видалення знаків пунктуації з тексту
def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))

# Мапувальна функція для підрахунку кількості входжень кожного слова у тексті
def map_function(word):
    return word, 1

# Функція Shuffle для групування мапованих значень за ключами
def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()

# Функція редукції для підсумовування кількості входжень кожного слова
def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Основна функція для виконання MapReduce
def map_reduce(text):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Мапування кожного слова на пару (слово, 1)
    mapped_values = map(map_function, words)

    # Shuffle - групування мапованих значень за ключами (словами)
    shuffled_values = shuffle_function(mapped_values)

    # Редукція - підсумовування кількості входжень кожного слова
    reduced_values = map(reduce_function, shuffled_values)

    # Повернення результату у вигляді словника
    return dict(reduced_values)

# Функція для візуалізації топ N слів
def visualize_top_words(word_counts, n=10):
    # Сортування словника за значеннями (кількістю входжень)
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    top_words = [pair[0] for pair in sorted_word_counts[:n]]
    top_counts = [pair[1] for pair in sorted_word_counts[:n]]
    
    # Візуалізація топ слів за допомогою горизонтального стовпчикового графіка
    plt.figure(figsize=(10, 6))
    plt.barh(top_words, top_counts, color='skyblue')
    plt.xlabel('Кількість')
    plt.ylabel('Слова')
    plt.title(f'Топ {n} слів')
    plt.gca().invert_yaxis()  # Реверсуємо ось y, щоб найбільш вживані слова були наверху
    plt.show()

if __name__ == "__main__":
    # URL-адреса для завантаження тексту
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"

    # Отримання тексту з URL
    text = get_text(url)

    if text:
        # Виконання MapReduce на тексті
        word_counts = map_reduce(text)

        # Візуалізація топ-слів з найвищою частотою використання
        visualize_top_words(word_counts)
