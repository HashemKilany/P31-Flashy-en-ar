from tkinter import *
import pandas as pd
import random
import pygame
import os
from gtts import gTTS

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Initialize pygame mixer
pygame.mixer.init()

# Ensure the audio directory exists
if not os.path.exists("./audio"):
    os.makedirs("./audio")


def download_sound(word):
    tts = gTTS(text=word, lang='en')
    file_path = f"./audio/{word}.mp3"
    tts.save(file_path)
    print(f"Downloaded audio for '{word}'")


def play_sound(word):
    # Construct the file path
    file_path = f"./audio/{word}.mp3"
    if not os.path.exists(file_path):
        download_sound(word)
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()


# ---------------------------- cards mechanism ------------------------------- #
try:
    data = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("./data/en_ar_word.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_lang, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["ENGLISH"], fill="black")
    canvas.itemconfig(img_bg, image=front_img)
    play_sound(current_card["ENGLISH"])  # Play the sound
    flip_timer = window.after(5000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_lang, text="Arabic", fill="white")
    canvas.itemconfig(card_word, text=current_card["Arabic"], fill="white")
    canvas.itemconfig(img_bg, image=back_img)


def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn", index=False)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashy Arabic")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
front_img = PhotoImage(file="./images/card_front.png")
back_img = PhotoImage(file="./images/card_back.png")
img_bg = canvas.create_image(400, 263, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card_lang = canvas.create_text(400, 150, text="", font=("Ariel", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "italic"))
right_img = PhotoImage(file="./images/right.png")

right_BT = Button(image=right_img, highlightthickness=0, bg=BACKGROUND_COLOR,
                  command=is_known)
right_BT.grid(row=1, column=1)

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_BT = Button(image=wrong_img, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
wrong_BT.grid(row=1, column=0)

next_card()
window.mainloop()
