from flask import Flask ,render_template, request
import numpy as np
import pandas as pd 



# app = Flask(__name__)
# on start button being clicked, get preferences from C2E, Missed
# create


data = pd.read_csv('data.csv')

app = Flask(__name__)
@app.route('/')
def main_function():
    return render_template('flashcards.html')

@app.route('/start')
def start():   
    missed = request.args.get('missed',0)
    number = request.args.get('number',0)
    
    characters = get_characters(missed, number)

    return characters.to_json(orient = 'index')

def get_characters(missed, number):

    total = len(data.index)
    print('total',total)

    if number == 'empty':
        number = total
    else:
        number = int(number)
    
    if missed == 'true':
        return data[data["Missed"]=='y']
    else:
        index = np.random.choice(range(total), size = number, replace=False)
        return data.iloc[index]
    