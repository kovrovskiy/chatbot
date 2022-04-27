#webinar skillbox python and chatbot

import json, os, nltk, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

os.chdir("C:\\Project\\chatbot\\")

config_file = open("big_bot_config.json", "r")
BOT_CONFIG = json.load(config_file)
#BOT_CONFIG["intents"].keys()
#BOT_CONFIG["intents"]["About sport"]


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

def get_intent(text):
  for intent in BOT_CONFIG["intents"]:
    for example in BOT_CONFIG["intents"][intent]["examples"]:
      if match(text, example):
        return intent

def bot(text):
  intent = get_intent(text)  # Пытаемся сходу понять намерение

  if not intent:  # Если не получилось, привлекаем модель МО
    transformed_text = vectorizer.transform([text])
    intent = model.predict(transformed_text)[0]

  if intent:  # Если намерение найдено - выдаем случайный ответ
    return random.choice(BOT_CONFIG["intents"][intent]["examples"])

  # Если не найдено
  return random.choice(BOT_CONFIG["failure_phrases"])

# X - тексты (примеры)
x = []
# y - названия интентов (классы)
y = [] 

for name, data in BOT_CONFIG["intents"].items():
  for example in data['examples']:
    x.append(example)
    y.append(name)

#len(X)
#len(BOT_CONFIG["intents"])

# Векторайзер превращает тексты в вектора (наборы чисел)

# Мама круто мыла раму => [1,2,3,4]
# круто мама раму мыла => [2,1,4,3]
# мыла  => [3,0,0,0]

# "мама" = 1, "круто" = 2, "мыла" = 3, "раму" = 4

vectorizer = CountVectorizer()
vectorizer.fit(x)  # Учится вот эти конкретные тексты преобразовывать в вектора
vecX = vectorizer.transform(x)
#len(list(vecX.toarray()[0]))

# 3. Обучить модель (алгоритм, настройки)
#model = LogisticRegression() # Настройки
#model.fit(vecX, y)
#test = vectorizer.transform(["меньше чем за миллион я не согласился бы"])
#model.predict(test)
# 4. Проверить качество модели
#model.score(vecX, y)

#y_pred = model.predict(vecX)

model = RandomForestClassifier(n_estimators = 500, min_samples_split=3)
model.fit(vecX, y)
print(model.score(vecX, y))

print("Поговори со мной...")
question = "" # Вопрос который задает пользователь
while question != "Выйти":
  question = input()
  answer = bot(question)
  print(f"[Юзер]: {question}")
  print(f"[Бот]: {answer}")