#webinar skillbox python and chatbot
import random, nltk

# Группируем фразу по "сути/смыслу" - intent "намерение"
BOT_CONFIG = {
    "hello": {  
        "examples": ["Хеллоу", "Привет", "Шалом", "Здравствуйте"],
        "responses": ["Приветик", "Шалом", "Здравствуйте", "Салютики", "Охае", ],
    },
    "how-do-you-do": {  
        "examples": ["Как дела", "Чем занят", "Чо как", "Йо"],
        "responses": ["Отдыхаю", "Кайфую", "Веду интенсивы"],
    },
    "bye": {
        "examples": ["Пока", "Бай", "До Свидания"],
        "responses": ["Пока", "Бай", "До Свидания", "Аливидерчи", "Чао Какао", "айдиос амигос", "код не верно пишешь"],
    }
}
# Убрать из текста лишние символы
def filter(text):
  alphabet = 'абвгджзеёийклмнопрстуфхцчшщьыъэюя -'
  result = [c for c in text if c in alphabet]  # Фильтрует символы не входящие в список
  return ''.join(result)

# Если текст похож на example то вернуть "True", "False"
def match(text, example):
    text = filter(text.lower())
    example = example.lower()

    distance = nltk.edit_distance(text, example) / len(example)  #  0..1+
    return distance < 0.6

def get_answer(text):
  for intent in BOT_CONFIG:
    for example in BOT_CONFIG[intent]["examples"]:
      if match(text, example):
        return random.choice(BOT_CONFIG[intent]["responses"])

text = input()  # То что нам написал юзер 
answer = get_answer(text)
print(answer)