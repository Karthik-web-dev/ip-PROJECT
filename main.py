import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template

df = pd.read_csv('data.csv')
cart = pd.DataFrame()
print(df)

app = Flask(__name__)


@app.route('/home')
def home():
    #selected = df['phone_model'].sample(n=6).tolist()
    mobile_names = df['phone_model'].sample(n=6).tolist()

    return render_template('home.html', mobile_names=mobile_names)

@app.route('/cart')
def cart():
    
    return render_template('cart.html')

if __name__ =='__main__':  
    app.run(debug = True)  
