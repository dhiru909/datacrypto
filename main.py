import json
import sqlite3
from tkinter import *
from tkinter import messagebox, Menu
import requests

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
# pycrypto.iconbitmap("D:\\cprograms\\12 11 21\\python\\pycrypto\\favicon.ico")
# database info 
con = sqlite3.connect("coin.db")
cobj = con.cursor()

cobj.execute(
    "create table if not exists coin(id integer primary key,symbol TEXT,amount REAL,price REAL)")
con.commit()

# cobj.execute("Insert into coin values(?,?,?,?)",(2,"BTC",0.1,32000))
# con.commit()
# cobj.execute("Insert into coin values(?,?,?,?)",(3,"XMR",0.1,12))
# con.commit()
# cobj.execute("Insert into coin values(?,?,?,?)",(4,"ETH",5,320))
# con.commit()
# cobj.execute("Insert into coin values(?,?,?,?)",(5,"LTC",78,320))
# con.commit()


def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_nav()

    app_header()
    my_portfolio()


def app_nav():

    def clear_all():
        cobj.execute("delete from coin")
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add New Coins")
        reset()

    def close_app():
        pycrypto.destroy()
    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App', command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)


def my_portfolio():
    api_info = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=cf555eb5-3e86-4aeb-aa59-2619ff63d9c6")
    data = json.loads(api_info.content)

    cobj.execute("SELECT * FROM coin")
    coins = cobj.fetchall()

    def insert_coin():
        cobj.execute("insert into coin(symbol,amount,price) values(?,?,?)",
                     (sym_txt.get(), amount_txt.get(), price_txt.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notice", "Coin Added Successfully!")

    def update_coin():
        cobj.execute("update coin set symbol=?,price=?,amount=? where id=?", (sym_update.get(
        ), price_update.get(), amount_update.get(), id_update.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notice", "Coin Updated Successfully!")

    def delete_coin():
        cobj.execute("delete from coin where id=?", (id_delete.get(),))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notice", "Coin Deleted Successfully!")
    total_pl = 0
    coin_row = 1
    total_paid = 0
    total_cv = 0
    c_count = 0
    for i in range(300):
        for coin in coins:
            if data["data"][i]["symbol"] == coin[1]:
                c_count += 1
                n_of_coin_owned = coin[2]
                current_value = data["data"][i]["quote"]["USD"]["price"] * \
                    n_of_coin_owned
                t_paid = coin[2]*coin[3]
                data["data"][i]["quote"]["USD"]["price"] = round(
                    data["data"][i]["quote"]["USD"]["price"], 3)
                pl_per_coin = data["data"][i]["quote"]["USD"]["price"] - \
                    coin[3]
                total_pl_with_coin = pl_per_coin * n_of_coin_owned
                total_pl += total_pl_with_coin
                total_paid += t_paid
                total_cv += current_value
                portfolio_id = Label(pycrypto, text=coin[0], fg="black", bg="lightgray",
                                     font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                portfolio_id.grid(row=coin_row, column=0, sticky=N+S+E+W)

                coin_name = Label(pycrypto, text=data["data"][i]["name"], fg="black", bg="lightgray",
                                  font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                coin_name.grid(row=coin_row, column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text="${0:.3f}".format(data["data"][i]["quote"]["USD"]["price"]), fg="black",
                              bg="lightgray", highlightbackground="cyan", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                price.grid(row=coin_row, column=2, sticky=N+S+E+W)

                no_coins = Label(pycrypto, text=coin[2], fg="black", bg="lightgray",
                                 font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                no_coins.grid(row=coin_row, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:.3f}".format(
                    t_paid), fg="black", bg="lightgray", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                amount_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

                currenr_val = Label(pycrypto, text="${0:.3f}".format(
                    current_value), fg="black", bg="lightgray", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                currenr_val.grid(row=coin_row, column=5, sticky=N+S+E+W)

                if pl_per_coin >= 0:
                    pl_coin = Label(pycrypto, text="${0:.3f}".format(
                        pl_per_coin), fg="black", bg="green", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                    pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)
                else:
                    pl_coin = Label(pycrypto, text="${0:.3f}".format(
                        pl_per_coin), fg="black", bg="red", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                    pl_coin.grid(row=coin_row, column=6, sticky=N+S+E+W)

                if total_pl_with_coin >= 0:
                    tatal_pl = Label(pycrypto, text="${0:.3f}".format(
                        total_pl_with_coin), fg="black", bg="green", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                    tatal_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)
                else:
                    tatal_pl = Label(pycrypto, text="${0:.3f}".format(
                        total_pl_with_coin), fg="black", bg="red", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
                    tatal_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)
                coin_row += 1
        if total_pl >= 0:

            tatal_pl = Label(pycrypto, text="${0:.3f}".format(
                total_pl), fg="black", bg="green", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
            tatal_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)
        else:
            tatal_pl = Label(pycrypto, text="${0:.3f}".format(
                total_pl), fg="black", bg="red", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
            tatal_pl.grid(row=coin_row, column=7, sticky=N+S+E+W)
        if c_count > len(coins):
            break

    tatal_paid = Label(pycrypto, text="${0:.3f}".format(
        total_paid), fg="black", bg="lightgray", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    tatal_paid.grid(row=coin_row, column=4, sticky=N+S+E+W)

    tatal_cv = Label(pycrypto, text="${0:.3f}".format(
        total_cv), fg="black", bg="lightgray", font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    tatal_cv.grid(row=coin_row, column=5, sticky=N+S+E+W)
    # insert coin
    sym_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    sym_txt.grid(row=coin_row+1, column=1)
    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=coin_row+1, column=2)
    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=coin_row+1, column=3)

    add_coin = Button(pycrypto, text="Add Coin", fg="white", command=insert_coin, bg="#142E54",
                      font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    add_coin.grid(row=coin_row+1, column=4, sticky=N+S+E+W)
# UPDATE COIN
    sym_update = Entry(pycrypto, borderwidth=2, relief="groove")
    sym_update.grid(row=coin_row+2, column=1)
    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=coin_row+2, column=2)
    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=coin_row+2, column=3)
    id_update = Entry(pycrypto, borderwidth=2, relief="groove")
    id_update.grid(row=coin_row+2, column=0)
    update_coin = Button(pycrypto, text="Update Coin", fg="white", command=update_coin, bg="#142E54",
                         font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    update_coin.grid(row=coin_row+2, column=4, sticky=N+S+E+W)
    # delete coin
    id_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    id_delete.grid(row=coin_row+3, column=0)
    delete_coin = Button(pycrypto, text="Delete Coin", fg="white", command=delete_coin, bg="#142E54",
                         font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    delete_coin.grid(row=coin_row+3, column=4, sticky=N+S+E+W)
    # refresh....
    data = ""
    Refresh = Button(pycrypto, text="Refresh", fg="white", command=reset, bg="#142E54",
                     font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    Refresh.grid(row=coin_row+1, column=7, sticky=N+S+E+W)


def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", fg="white", bg="#142E54",
                         font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    portfolio_id.grid(row=0, column=0, sticky=N+S+E+W)

    coin_name = Label(pycrypto, text="COIN NAME", fg="white", bg="#142E54",
                      font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    coin_name.grid(row=0, column=1, sticky=N+S+E+W)

    price = Label(pycrypto, text="PRICE", fg="white", bg="#142E54",
                  font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    price.grid(row=0, column=2, sticky=N+S+E+W)

    no_coins = Label(pycrypto, text="Coins Owned", fg="white", bg="#142E54",
                     font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    no_coins.grid(row=0, column=3, sticky=N+S+E+W)

    amount_paid = Label(pycrypto, text="Amount Paid", fg="white", bg="#142E54",
                        font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    amount_paid.grid(row=0, column=4, sticky=N+S+E+W)

    currenr_val = Label(pycrypto, text="Current Value", fg="white", bg="#142E54",
                        font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    currenr_val.grid(row=0, column=5, sticky=N+S+E+W)

    pl_coin = Label(pycrypto, text="P/L per Coin", fg="white", bg="#142E54",
                    font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    pl_coin.grid(row=0, column=6, sticky=N+S+E+W)

    tatal_pl = Label(pycrypto, text="Total P/L for Coin", fg="white", bg="#142E54",
                     font="Lato 12 bold", borderwidth=2, relief="groove", padx=5, pady=5)
    tatal_pl.grid(row=0, column=7, sticky=N+S+E+W)


app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cobj.close()
con.close()
