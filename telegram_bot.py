import telebot
from class_replicate import Replicate_API
from class_chatgpt import Gpt_API
from water_mark import Water_Mark
import os
from dotenv import load_dotenv
load_dotenv()

##Your telegram bot token here
BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(BOT_TOKEN)

from flask import Flask, request
app = Flask(__name__)
@bot.message_handler(commands=['ask'])
def ask(message):
    if len(message.text)<5 or message.text[4]=='@':
        bot.reply_to(message, f"Please type your query after the command by having a space between them, like this:\n/ask Who is Joe Biden?")
    else:
        sender = message.from_user
        bot.reply_to(message, f"Processing command by <a href=\"tg://user?id={sender.id}\">{sender.full_name}</a>...", parse_mode = "HTML")
        prompt = message.text[5:]
        gpt_obj = Gpt_API(prompt)
        result = gpt_obj.get_result()
        bot.send_message(message.chat.id, f"{result}",reply_to_message_id= message.message_id)
        bot.delete_message(chat_id= message.chat.id,message_id = message.message_id+1)

@bot.message_handler(commands=['gen'])
def generate_image(message):
    if len(message.text)<5 or message.text[4]=='@':
        bot.reply_to(message, f"Please type your prompt after the command by having a space between them, like this:\n/gen A fox looking at the sky, hd, dramatic lighting")
    else:
        sender = message.from_user
        bot.reply_to(message, f"Processing command by <a href=\"tg://user?id={sender.id}\">{sender.full_name}</a>...", parse_mode="HTML")
        #bot.send_message(chat_id=message.chat.id,text=f"Process command by <a href=\"tg://user?id={sender.id}\">{sender.full_name}</a>...", parse_mode="HTML",reply_to_message_id=message.message_id)
        prompt = message.text[5:]
        #print(prompt)
        obj = Replicate_API(prompt)
        url = obj.get_result()[0]
        print("Got result")
        obj_watermark= Water_Mark(url)
        obj_watermark.get_result()
        print("Image saved")
        photo = open('result.png', 'rb')
        print("photo opened")
        bot.delete_message(chat_id=message.chat.id,message_id=message.message_id+1)
        bot.send_photo(chat_id = message.chat.id,photo=photo,caption = f"Image generated by <a href=\"tg://user?id={sender.id}\">{sender.full_name}</a>: <code>{message.text}</code>\n\n&gt; <a href=\"https://genaitoken.com/\">Join GenAi</a> | <a href=\"https://genaitoken.com/\">Website</a> | <a href=\"https://genaitoken.com/\">Buy </a>&lt;", parse_mode="HTML",reply_to_message_id=message.message_id)
        print("Photo sent")
    
    #bot.reply_to(message, f"Hello @{sender.username}! , your prompt was \"{prompt}\"")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, f"You will have two features in this bot.\n1. Image generation\n2.Text Generation\n\nBy typing,  /ask<space><your query> , you can ask the bot anything, and you will get answer.\n\nBy typing,  /gen<space><your prompt> , you can generate images with based on your prompt.")

bot.polling()
    
@app.route('/')
def home():
    return 'All is well...'

if __name__ == '__main__':
    app.run(debug=True)
