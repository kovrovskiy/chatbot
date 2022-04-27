#webinar skillbox python and chatbot

from cgitb import handler
import json, os, nltk, random #, pickle
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from telegram import Update   
from telegram.ext import Updater, MessageHandler, Filters
#from sklearn.model_selection import GridSearchCV

os.chdir("C:\\Project\\chatbot\\")

config_file = open("big_bot_config.json", "r")
BOT_CONFIG = json.load(config_file)
BOT_KEY = "5353279424:AAERubY7iIPI8G-wI38824W2_TdP6syVNVw"

def botReactOnMessage(update: Update, context):
  text = update.message.text #то что пользователь нам написал
  print(f"[user]: {text}")
  reply = bot(text)
  update.message.reply_text(reply)

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

#model = RandomForestClassifier(n_estimators = 500, min_samples_split=3)
model = RandomForestClassifier()
model.fit(vecX, y)

#запись модели в файл для сохранения
#f = open("bot_model.class", "wb")
#pickle.dump(model, f)

#поиск идеальной модели
#ideal_model = RandomForestClassifier()
#param = {
#    "n_estimators": [60, 140],
#    "criterion": ["gini", "entropy"],
#}

#cv = GridSearchCV(ideal_model, param)
#cv.fit(vecX, y)

print(model.score(vecX, y))

upd = Updater(BOT_KEY)
handler = MessageHandler(Filters.text, botReactOnMessage)
upd.dispatcher.add_handler(handler)
upd.start_polling()
upd.idle()

print("Поговори со мной...")
question = "" # Вопрос который задает пользователь
while question != "Выйти":
  question = input()
  answer = bot(question)
  print(f"[Юзер]: {question}")
  print(f"[Бот]: {answer}")