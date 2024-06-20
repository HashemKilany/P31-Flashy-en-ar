from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
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
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_lang, text="Arabic", fill="white")
    canvas.itemconfig(card_word, text=current_card["Arabic"], fill="white")
    canvas.itemconfig(img_bg, image=back_img)


def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pd.DataFrame(to_learn)
    data.to_csv("data/words_to_learn",index=False)


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
