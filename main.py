import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import random
import os

global df
df = pd.read_csv('data.csv')
#cart = pd.DataFrame(columns=["name", "price", "ram", "storage", "battery", "quantity"])

app = Flask(__name__)

global customer_name

@app.route('/', methods=['POST', 'GET'])
def name():
    global customer_name
    if request.method == 'POST':
        customer_name = request.form.get("name")
        return redirect(url_for('home'))
    return render_template('index.html', redirect_url="/home")

@app.route('/home')
def home():
    rand_ind = random.sample(range(len(df)), 3)
    mobile_names = df.iloc[rand_ind][["phone_model", "price_usd", "ram", "storage", "battery"]].values.tolist()
    print(mobile_names)

    max_row = df.loc[df['price_usd'].idxmax()]
    min_row = df.loc[df['price_usd'].idxmin()]
    result = [[max_row['phone_model'], max_row['price_usd'], max_row['ram'], max_row['storage'], max_row['battery'], "most expensive", "warning"],
              [min_row['phone_model'], min_row['price_usd'], min_row['ram'], min_row['storage'], min_row['battery'], "cheapest deal", "success"]]
             
    print(result)
    return render_template('home.html', rand_mobs=mobile_names, heir_mobs=result)

@app.route('/search', methods=['POST', 'GET'])
def search():
    df_filtered = None
    if request.method == 'POST':
        phone_brand = request.form.get('brand')
        price_range = request.form.get('price')
        sort_by = request.form.get('sort')
        
        df_filtered = df[df['phone_brand'] == phone_brand]
        # print(df_filtered)

        price_range_values = price_range.split('-')
        min_price = int(price_range_values[0])
        max_price = int(price_range_values[1])
        df_filtered = df_filtered[(df_filtered['price_usd'] >= min_price) & (df_filtered['price_usd'] <= max_price)]
        # print(df_filtered)

        if sort_by == 'asc':
            df_filtered = df_filtered.sort_values(by='price_usd', ascending=True)
        elif sort_by == 'desc':
            df_filtered = df_filtered.sort_values(by='price_usd', ascending=False)
        
        df_filtered = df_filtered.loc[:, ["phone_model", "price_usd", "ram", "storage", "battery"]].values.tolist()




    brands = df['phone_brand'].unique()
    if df_filtered is None:
       return render_template('search.html', brand_names=brands)
    else:
       return render_template('search.html', brand_names=brands, phones=df_filtered)

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
    cart.loc[len(cart)] = item
    return redirect(url_for('home'))


@app.route('/add', methods=['POST'])
def add():
    print('check')
    item = {
        "name": request.form.get("name"),
        "price": request.form.get("price"),
        "ram": int(request.form.get("ram")),
        "storage": int(request.form.get("storage")),
        "battery": int(request.form.get("battery")),
        "quantity":int(request.form.get("quantity"))
    }
    cart.loc[len(cart)] = item
    return redirect(url_for('search'))


@app.route('/cart')
def mycart():
    print(cart)
    cart_names = cart.loc[:, ["name", "price", "ram", "storage", "battery", "quantity"]].values
    subtotal = 0
    total = 0
    shipping = 0

    for name, price, ram, storage, battery, quantity in cart_names:
        subtotal += float(price)*int(quantity)
        shipping += 10*int(quantity)
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


@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    global cart

    phone_name = request.form.get('phone_name')
    new_quantity = int(request.form.get('quantity'))
    if phone_name in cart['name'].values:
        cart.loc[cart['name'] == phone_name, 'quantity'] = new_quantity
    return redirect(url_for('mycart'))



@app.route('/thanks')
def thanks():
  global cart
  cart = cart.iloc[0:0]
  print(cart)
  return render_template('thankyou.html', cust=customer_name)

if __name__ =='__main__':  
    app.run(debug = True)  
