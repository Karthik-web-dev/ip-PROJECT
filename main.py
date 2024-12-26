import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import random

df = pd.read_csv('data.csv')
#cart = pd.DataFrame(columns=["name", "price", "ram", "storage", "battery", "quantity"])

app = Flask(__name__)


@app.route('/home')
def home():
    rand_ind = random.sample(range(len(df)), 3)
    mobile_names = df.iloc[rand_ind][["phone_model", "price_usd", "ram", "storage", "battery"]].values.tolist()
    print(mobile_names)

    max_row = df.loc[df['price_usd'].idxmax()]
    min_row = df.loc[df['price_usd'].idxmin()]
    result = [[max_row['phone_model'], max_row['price_usd'], max_row['ram'], max_row['storage'], max_row['battery'], "most expensive", "warning"],
              [min_row['phone_model'], min_row['price_usd'], min_row['ram'], min_row['storage'], min_row['battery'], "cheapest deal", "success"]]
             

    return render_template('home.html', rand_mobs=mobile_names, heir_mobs=result)



global cart 
cart = pd.DataFrame(columns=["name", "price", "ram", "storage", "battery", "quantity"])

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = {
        "name": request.form.get("name"),
        "price": request.form.get("price"),
        "ram": int(request.form.get("ram")),
        "storage": int(request.form.get("storage")),
        "battery": int(request.form.get("battery")),
        "quantity":1
    }
    # Append item to the cart DataFra
    cart.loc[len(cart)] = item
    return redirect(url_for('home'))

@app.route('/cart')
def mycart():
    print(cart)
    cart_names = cart.loc[:, ["name", "price", "ram", "storage", "battery", "quantity"]].values
    subtotal = 0
    shipping = 10
    total = 0

    for name, price, ram, storage, battery, quantity in cart_names:
        subtotal += float(price)
    subtotal = round(subtotal, 2)
    discount = round(0.1*subtotal, 2)
    total = round(subtotal + shipping - discount, 2)
    
    print(cart)
    print(cart_names)
    return render_template('cart.html', cart_mobs=cart_names, subtotal=subtotal, shipping=shipping, total=total, discount=discount)

@app.route('/remove_item', methods=['POST'])
def remove_item():
    global cart
    phone_name = request.form.get('phone_name')
    if phone_name in cart['name'].values:
        cart = cart.loc[cart['name'] != phone_name]

    return redirect(url_for('mycart'))

if __name__ =='__main__':  
    app.run(debug = True)  
