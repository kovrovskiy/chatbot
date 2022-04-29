#webinar skillbox python and chatbot

from cgitb import handler
import json, os, nltk, random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from telegram import Update   
from telegram.ext import Updater, MessageHandler, Filters

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

# If the text is similar to example then return "True", "False"
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

# X - texts
x = []
# y - name of intents
y = [] 

for name, data in BOT_CONFIG["intents"].items():
  for example in data['examples']:
    x.append(example)
    y.append(name)

vectorizer = CountVectorizer()
vectorizer.fit(x)  
vecX = vectorizer.transform(x)

model = RandomForestClassifier(n_estimators = 500, min_samples_split=3)
model.fit(vecX, y)

print(model.score(vecX, y))

upd = Updater(BOT_KEY)
handler = MessageHandler(Filters.text, botReactOnMessage)
upd.dispatcher.add_handler(handler)
upd.start_polling()
upd.idle()

question = "" # The question asked by the user
while question != "Exit":
  question = input()
  answer = bot(question)
  print(f"User]: {question}")
  print(f"[Bot]: {answer}")