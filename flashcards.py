import pandas as pd
import numpy as np 

from tkinter import *
from tkinter import ttk
from tkinter import font




# flip back and forth between chinese and english/pinyin
# centre window on start
# keep a track of missed ones and have setting to train on those

# choose on the basis of c2e/e2c (and use that for flip setting)
# show count of how many words done and how many left
# disable flip, correct/incorrect buttons respectively
# if word has more than one character, look up meanings and print them on flip
# expand window size and fit frame in it.
# adjust position of missed button to align with number entry box above
# change ending message to be accurate in case of testing missed entries only
# count shouldn't increase if correct is clicked repeatedly after test ends.
# menu to change window to data entry and facilitiy for data entry
# group all grid code together
# error message for no missed words
#repeat the ones that were incorrect in the session


data = pd.read_csv('data.csv')



root = Tk()
root.title("Flashcards")
root.geometry('+500+300') #500x100

### MAINFRAME ###

mainframe = ttk.Frame(root, width = 500, height = 100) #padding = '3 3 12 12'
mainframe.grid(column = 0, row = 0, sticky = ("nsew"))



### FLASH/ANSWER FRAME ###

# flash_answer_frame = ttk.Frame(mainframe,height = 20, width = 20, padding = (10,10,10,10)).grid(column = 0, row = 0)
flash_answer = StringVar()
flash_answer.set("Click start to begin")
flash_answer_font = font.Font(size = 30)
flash_answer_label = ttk.Label(mainframe, textvariable = flash_answer,  padding = (2,2,5,5), font = flash_answer_font)
flash_answer_label.grid(column = 0, row = 0, columnspan = 3, rowspan = 2)


### FLIP BUTTON ###

display = 'Chinese'


def flip():
    global index
    global display

    if display == 'Chinese':
        flash_answer.set(data['Pinyin'][index]+": "+data['English'][index])
        display = 'English'
    else:
        flash_answer.set(data['Mandarin'][index])
        display = 'Chinese'


    



flip_button = ttk.Button(mainframe, text = 'Flip', command = flip) #, state = 'disabled')
flip_button.grid(column = 0, row = 2, columnspan = 2, sticky = W+E+N+S)



### CORRECT BUTTON ###

def correct():
    global correct_tally
    global sample
    global index
    global data
    global display

    display = 'Chinese' #modify when C2E/E2C is enabled

    correct_tally+=1
    data['Missed'][index]='n'
    
    if len(sample)==0:

        flash_answer.set("")
        flash_answer.set('You got '+ str(correct_tally)+ ' out of '+ number + ' right.')
        data.to_csv('data.csv', index = False)

    else:
        flash_answer.set("")
        index = sample.pop()
        flash_answer.set(data["Mandarin"][index])


correct_button = ttk.Button(mainframe, text = 'correct', command = correct)
correct_button.grid(column = 0, row = 3)

### INCORRECT BUTTON ###

def incorrect():
    global correct_tally
    global sample
    global index
    global display

    display = 'Chinese' #modify when C2E/E2C is enabled
    data['Missed'][index]='y'
    
    


    if len(sample)==0:
        flash_answer.set("")
        flash_answer.set('You got '+ str(correct_tally)+ ' out of '+ number + ' right.')
        data.to_csv('data.csv', index = False)

    else:
        flash_answer.set("")
        index = sample.pop()
        flash_answer.set(data["Mandarin"][index])

incorrect_button = ttk.Button(mainframe, text = 'incorrect', command = incorrect)
incorrect_button.grid(column = 1, row = 3)

### set default to C2E

#if depending on what the value is, set display value in start funtion
direction = StringVar()
chinese_to_english = ttk.Radiobutton(mainframe, text = 'Chinese to English', variable = direction, value = 'C2E')
chinese_to_english.grid(column = 3, row = 0)
english_to_chinese = ttk.Radiobutton(mainframe, text = ' English to Chinese', variable = direction, value = 'E2C')
english_to_chinese.grid(column = 3, row = 1)

### NUMER OF CARDS ENTRY ###
number_of_cards = StringVar()
number_of_cards_entry = ttk.Entry(mainframe, width = 4, textvar = number_of_cards)
number_of_cards_entry.grid(column = 4, row = 0)

total_words = StringVar()
total_words = str(data.shape[0])
total_label_text = 'of '+ total_words
total_label = ttk.Label(mainframe, text = total_label_text)
total_label.grid(column = 5, row = 0)

### MISSED CHECKBUTTON ###

missed = StringVar()

missed_checkbutton = ttk.Checkbutton(mainframe, variable = missed, text = 'Missed')
missed_checkbutton.grid(column = 4, row = 1)

### START BUTTON ###
def start():
    global flash_answer
    global number
    global sample
    global data
    global index
    global correct_tally

    correct_tally = 0 

    number = number_of_cards.get()
    if number == "":
        number = total_words
    
    if missed.get() == '1':
        try:
            sample = list(data.index[data['Missed']=='y'])
            np.random.shuffle(sample)
            number = str(len(sample))
            index = sample.pop()
        except:
            flash_answer.set("No missed words")

    else:    
        sample = list(np.random.choice(range(int(total_words)), int(number), replace = False)) 
        index = sample.pop()

    

    flash_answer.set(data["Mandarin"][index]) ###modify for C2E vs E2C



    # extract random section of data


start_button = ttk.Button(mainframe, text = 'Start', command = start)
start_button.grid(column = 3, row = 3)

### MAINLOOP ###
root.mainloop()

