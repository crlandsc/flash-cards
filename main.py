from tkinter import *
import pandas as pd
import random


# ---------------------------- Functionality ------------------------------- #
current_card = {}
dict_to_learn = {}

# Try to load the 'words_to_learn file.csv'. If it doesn't exist, then create it and populate it with the french csv
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/test.csv")
    # data.to_csv("data/words_to_learn.csv", index=False)
    dict_to_learn = original_data.to_dict(orient="records")
else:
    dict_to_learn = data.to_dict(orient="records")
    # print(dict_to_learn)

# print(data)

def flip_card():
    random_english_word = current_card['English']
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(french_word, text=f"{random_english_word}", fill="white")
    canvas.itemconfig(language, text="English", fill="white")

def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(dict_to_learn)
    # print(dict_to_learn[0])
    random_french_word = current_card['French']
    canvas.itemconfig(french_word, text=f"{random_french_word}", fill="black")
    canvas.itemconfig(language, text="French", fill="black")
    canvas.itemconfig(canvas_image, image=card_front_img)
    # print(random_word)
    flip_timer = window.after(3000, flip_card)
    # card_back()

def correct():
    if len(dict_to_learn) > 1:
        print(len(dict_to_learn))
        print(dict_to_learn)
        # Remove from list to learn if correct
        dict_to_learn.remove(current_card)
        # print(dict_to_learn)
        data_frame = pd.DataFrame(dict_to_learn)
        data_frame.to_csv("data/words_to_learn.csv", index=False)
        next_card()
    else:
        print(dict_to_learn)
        canvas.itemconfig(french_word, text="Congratulations!", fill="black")
        canvas.itemconfig(language, text="You Finished All Of The Words!", fill="black")
        canvas.itemconfig(canvas_image, image=card_front_img)

def incorrect():
    if dict_to_learn:
        next_card()


# ---------------------------- UI SETUP ------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
LANGUAGE_FONT_SIZE = 40
WORD_FONT_SIZE = 60

window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.minsize(width=900, height=626)  # minimum size the window can shrink to

flip_timer = window.after(3000, flip_card)

# --- Canvas ---
# Card Front Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)  # create canvas
card_front_img = PhotoImage(file="images\card_front.png")  # import photo image
card_back_img = PhotoImage(file="images\card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_img)  # place image - (x,y) starting coordinates
language = canvas.create_text(400, 150, text="", font=(FONT_NAME, LANGUAGE_FONT_SIZE, "italic")) # Card title
french_word = canvas.create_text(400, 263, text="", font=(FONT_NAME, WORD_FONT_SIZE, "bold")) # Card word
canvas.grid(column=0, row=0, columnspan=2)


# ---------------------------- Buttons ------------------------------- #
# Wrong Button
wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=incorrect)
wrong_button.grid(column=0, row=1)

# Right Button
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=correct)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()
