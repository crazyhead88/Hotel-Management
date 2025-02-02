import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import *
import mysql.connector as sql
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import sv_ttk

print("hello")

connector = sql.connect(host="localhost", user="root", passwd="pass")
if connector.is_connected():
    print("hello")
cursor = connector.cursor()

# for sql error
try:
    cursor.execute("create database if not exists oasis;")
    cursor.execute("use oasis")
    cursor.execute(
        "create table if not exists checkin(ID int primary key AUTO_INCREMENT, Name varchar(25), Age int(2), Contact"
        " char(10), Members char(12), adhaar char(12), CheckIN_Date date,  CheckIN_Time time, payment varchar(7),"
        " Room_NO int, Roomtype Varchar(10), CheckOut_Date date,  CheckOut_Time time, Amount decimal(7,1))")
    cursor.execute(
        "create table if not exists reservations(ID int primary key AUTO_INCREMENT, Name varchar(25), Age int, Contact"
        " char(10), Members char(13), Adhaar char(12), Room_type varchar(10), reserve_date date, checkout_date date, "
        "status varchar(10))")
    connector.commit()
except:
    messagebox.showerror("Database Error", "My Sql Not installed")

try:
    cursor.execute('show tables')
    x = cursor.fetchall()
    data = []
    for i in x:
        for j in i:
            data.append(j)

    if 'standard' not in data:
        cursor.execute("create table standard(Room_no int not null primary key, id int);")
        for i in range(1, 11):
            cursor.execute(f"insert into standard values({i}, null)")
            connector.commit()
    if 'deluxe' not in data:
        cursor.execute("create table deluxe(Room_no int not null primary key, id int);")
        for i in range(11, 21):
            cursor.execute(f"insert into deluxe values({i}, null)")
            connector.commit()
    if 'suite' not in data:
        cursor.execute("create table suite(Room_no int not null primary key, id int);")
        for i in range(21, 31):
            cursor.execute(f"insert into suite values({i}, null)")
            connector.commit()
    if 'executive' not in data:
        cursor.execute("create table executive(Room_no int not null primary key, id int);")
        for i in range(31, 41):
            cursor.execute(f"insert into executive values({i}, null)")
            connector.commit()
except:
    messagebox.showerror("Database Error", "Rooms not Created.\n"
                                           "If Error persists restart program.")


def update_content(content_frame, function_text):
    # Clear existing frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    if function_text == "Check-In":
        background(content_frame, 'in.png')
        check_in(content_frame)

    elif function_text == "Check-Out":
        background(content_frame, 'out.png')
        check_out(content_frame)
    elif function_text == "Reservation":
        background(content_frame, 'reservation.png')
        reservation(content_frame)

    elif function_text == "Reservation_for_user":
        background(content_frame, 'reservation.png')
        reservation_for_user(content_frame)

    elif function_text == "Guest List":
        background(content_frame, 'status.png')
        guest_list(content_frame)

    elif function_text == "Revenue":
        background(content_frame, 'report.png')
        revenue(content_frame)

    elif function_text == "Login":
        background(content_frame, 'report.png')
        login(content_frame)

    elif function_text == "Info":
        background(content_frame, 'status.png')
        info(content_frame)

    else:
        background(content_frame, 'report.png')
        label = ttk.Label(content_frame, text=f"Content for {function_text}", font=('TkDefaultFont', 14))
        label.pack(padx=20, pady=20)


def background(content_frame, path):
    img = tk.PhotoImage(file=path)
    back_label = ttk.Label(content_frame, image=img)
    back_label.image = img
    back_label.place(relwidth=1, relheight=1)


def disappear_click(boxname, text):
    if boxname.get() == text:
        boxname.delete(0, tk.END)


def appear_click(boxname, text):
    if not boxname.get():
        boxname.insert(0, text)


def check_in(content_frame):
    def roomno(roomtype):
        connector = sql.connect(host="localhost", user="root", passwd="pass")
        cursor = connector.cursor()
        cursor.execute("use oasis")

        if roomtype in ["Standard", "Deluxe", "Suite", "Executive"]:
            cursor.execute(f"select room_no from {roomtype.lower()} where id is null")
            x = cursor.fetchone()
            l = list(x)
            return l[0]

    def execute(name, age, cont, member, adhar, pay, roomtype):
        # get date and time ["Standard ₹1100", "Deluxe ₹1900", "Suite ₹2700", "Executive ₹4500"]
        roomt = ""
        if roomtype == "Standard ₹1100":
            roomt = "Standard"
        elif roomtype == "Deluxe ₹1900":
            roomt = 'Deluxe'
        elif roomtype == "Suite ₹2700":
            roomt = "Suite"
        else:
            roomt = "Executive"

        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        key = roomno(roomt)

        query = f"null, '{name.title()}', {age}, {cont}, '{member}', {adhar}, '{date}', '{time}', '{pay}', {key}, '{roomt}'," \
                f" null, null, null "

        def key_editor(roomtype, key):
            cursor.execute(f"select ID from checkin order by id desc limit 1")
            id = cursor.fetchone()
            new_id = list(id)[0]
            cursor.execute(f"update {roomtype} set id = {new_id} where room_no = {key}")
            connector.commit()
            room_details(content_frame, key, new_id)

        try:
            cursor.execute(f"insert into checkin values({query})")
            connector.commit()
            key_editor(roomt, key)
        except:
            messagebox.showerror("Invalid Entry", "Enter all Fields Correctly")

    label = ttk.Label(content_frame, text="Check In ", font=("harlow solid italic", 70), foreground="#a1dbcd",
                      background="#019cb3")
    label.pack(padx=20, pady=20)

    name = ttk.Entry(content_frame, font=("Helvetica", 18))
    name.insert(0, "Name")
    name.bind("<FocusIn>", lambda event: disappear_click(name, "Name"))
    name.bind("<FocusOut>", lambda event: appear_click(name, "Name"))

    age = ttk.Entry(content_frame, font=("Helvetica", 18))
    age.insert(0, "Age")
    age.bind("<FocusIn>", lambda event: disappear_click(age, "Age"))
    age.bind("<FocusOut>", lambda event: appear_click(age, "Age"))

    contact = ttk.Entry(content_frame, font=("Helvetica", 18))
    contact.insert(0, "Contact")
    contact.bind("<FocusIn>", lambda event: disappear_click(contact, "Contact"))
    contact.bind("<FocusOut>", lambda event: appear_click(contact, "Contact"))

    adhar = ttk.Entry(content_frame, font=("Helvetica", 18))
    adhar.insert(0, "Adhaar Number")
    adhar.bind("<FocusIn>", lambda event: disappear_click(adhar, "Adhaar Number"))
    adhar.bind("<FocusOut>", lambda event: appear_click(adhar, "Adhaar Number"))

    members = ttk.Combobox(content_frame, values=["1", "2", "3", "4", "More than 4"], font=("Helvetica", 16),
                           style='Custom.TMenubutton')
    members.set(" No. of Members")
    members.bind("<<ComboboxSelected>>")

    room_type = ttk.Combobox(content_frame, values=["Standard ₹1100", "Deluxe ₹1900", "Suite ₹2700", "Executive ₹4500"],
                             font=("Helvetica", 16),
                             style='Custom.TMenubutton')
    room_type.set(" Room Type")
    room_type.bind("<<ComboboxSelected>>")

    pay = ttk.Combobox(content_frame, values=["Cash", "Card", "Online"], font=("Helvetica", 16),
                       style='Custom.TMenubutton')
    pay.set(" Payment Type")
    pay.bind("<<ComboboxSelected>>")

    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    submit_button = ttk.Button(content_frame, text="Submit",
                               command=lambda: execute(name.get(), age.get(), contact.get(), members.get(), adhar.get(),
                                                       pay.get(), room_type.get()))

    name.pack(pady=10)
    age.pack(pady=10)
    contact.pack(pady=10)
    adhar.pack(pady=10)
    members.pack(pady=10)
    room_type.pack(pady=10)
    pay.pack(pady=10)
    submit_button.pack(pady=10)

    key_label = None

    def room_details(content_frame, room, ID):
        label1 = ttk.Label(content_frame, text=f"ID: {ID} \nRoom no: {room}", font=("Century Gothic", 30))
        label1.pack(pady=20)

        clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
        clear_button.pack(pady=16)

        def clear():
            update_content(content_frame, "Check-In")


def check_out(content_frame):
    def execute(name, roomno):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        def price_update(final_price, guest):
            cursor.execute(f"update checkin set amount = {final_price} where id = {guest}")
            connector.commit()

        try:
            id = []
            cursor.execute(
                f"select id from checkin where room_no = {roomno} and name = '{name}' and checkout_date is null ")
            data = cursor.fetchall()
            id = []
            for i in data:
                for j in i:
                    id.append(j)

            cursor.execute(
                f"update checkin set checkout_date = '{date}', checkout_time = '{time}' where room_no = {roomno} and"
                f" name = '{name}' and checkout_date is null")
            connector.commit()

            cursor.execute(f"select checkin_date, checkout_date from checkin where Id = {id[0]}")
            x = cursor.fetchall()
            c = []
            for i in x:
                for j in i:
                    c.append(j)
            d = c[1] - c[0]
            days = d.days

            standard_price = 1100
            deluxe_price = 1900
            suite_price = 2700
            executive_price = 4500

            guest = id[0]

            cursor.execute(f"select roomtype from checkin where Id = {id[0]}")
            room = cursor.fetchall()
            roomname = ""
            for i in room:
                for j in i:
                    roomname += j

            if roomname.lower() == "standard":
                price = days * standard_price
                tax = int(price) * 0.18
                total = price + tax
                if total == 0 and price == 0:
                    price = standard_price * 0.6
                    tax = price * 0.18
                    total = price + tax
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Standard) ₹{standard_price}/-\nDays"
                                           f" stayed: \t\t 0,[half] \nTax: \t\t\t₹{tax} \nPayable Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)
                    cursor.execute(f"update standard set id = null where room_no = {roomno}")
                    connector.commit()
                else:
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Standard) ₹{standard_price}/-\nDays"
                                           f" stayed: \t\t{days} \nTotal: \t\t\t₹{price} \nTax: \t\t\t₹{tax} \nPayable"
                                           f" Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)

                    cursor.execute(f"update standard set id = null where room_no = {roomno}")
                    connector.commit()

            elif roomname.lower() == "deluxe":
                price = days * deluxe_price
                tax = int(price) * 0.18
                total = price + tax
                if total == 0 and price == 0:
                    price = deluxe_price * 0.6
                    tax = price * 0.18
                    total = price + tax
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Deluxe) ₹{deluxe_price}/-\nDays "
                                           f"stayed: \t\t 0,[half] \nTax: \t\t\t₹{tax} \nPayable Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)
                    cursor.execute(f"update deluxe set id = null where room_no = {roomno}")
                    connector.commit()
                else:
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\tDeluxe ₹{deluxe_price}/-\nDays stayed:"
                                           f" \t\t{days} \nTotal: \t\t\t₹{price} \nTax: \t\t\t₹{tax} \nPayable Amount: "
                                           f"\t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)

                    cursor.execute(f"update deluxe set id = null where room_no = {roomno}")
                    connector.commit()

            elif roomname.lower() == "suite":
                price = days * deluxe_price
                tax = int(price) * 0.18
                total = price + tax
                if total == 0 and price == 0:
                    price = suite_price * 0.6
                    tax = price * 0.18
                    total = price + tax
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Suite) ₹{suite_price}/-\nDays "
                                           f"stayed: \t\t 0,[half] \nTax: \t\t\t₹{tax} \nPayable Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)
                    cursor.execute(f"update suite set id = null where room_no = {roomno}")
                    connector.commit()
                else:
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Suite) ₹{suite_price}/-\nDays "
                                           f"stayed: \t\t{days} \nTotal: \t\t\t₹{price} \nTax: \t\t\t₹{tax} \n"
                                           f"Payable Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)

                    cursor.execute(f"update suite set id = null where room_no = {roomno}")
                    connector.commit()

            else:
                price = days * deluxe_price
                tax = int(price) * 0.18
                total = price + tax

                if total == 0 and price == 0:
                    price = executive_price * 0.6
                    tax = price * 0.18
                    total = price + tax
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Executive) ₹{executive_price}/-\nDays "
                                           f"stayed: \t\t 0,[half] \nTax: \t\t\t₹{tax} \nPayable "
                                           f"Amount: \t\t₹{price + tax}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)
                    cursor.execute(f"update executive set id = null where room_no = {roomno}")
                    connector.commit()
                else:
                    price_update(total, guest)
                    label = ttk.Label(content_frame,
                                      text=f"Name: \t\t\t{name} \nRoom Type: \t\t(Executive) ₹{executive_price}/-\nDays "
                                           f"stayed: \t\t{days} \nTotal: \t\t\t₹{price} \nTax: \t  \t\t₹{tax} \nPayable"
                                           f" Amount: \t\t₹{total}",
                                      font=("Century Gothic", 20))
                    label.pack(pady=20)

                    cursor.execute(f"update executive set id = null where room_no = {roomno}")
                    connector.commit()
        except:
            messagebox.showerror("Invalid Input", "Enter Correct details")

        clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
        clear_button.pack(pady=5)

        def clear():
            update_content(content_frame, "Check-Out")

    label = ttk.Label(content_frame, text="Check Out ", font=("harlow solid italic", 70), foreground="#e0d1b9",
                      background="#0281d0")
    label.pack(padx=20, pady=20)

    name = ttk.Entry(content_frame, font=("Helvetica", 18))
    name.insert(0, "Name")
    name.bind("<FocusIn>", lambda event: disappear_click(name, "Name"))
    name.bind("<FocusOut>", lambda event: appear_click(name, "Name"))

    room_no = ttk.Entry(content_frame, font=("Helvetica", 18))
    room_no.insert(0, "Room No")
    room_no.bind("<FocusIn>", lambda event: disappear_click(room_no, "Room No"))
    room_no.bind("<FocusOut>", lambda event: appear_click(room_no, "Room No"))

    submit_button = ttk.Button(content_frame, text="Submit", command=lambda: execute(name.get().title(), room_no.get()))

    name.pack(pady=10)
    room_no.pack(pady=10)
    submit_button.pack(pady=10)


def reservation_for_user(content_frame):
    label = ttk.Label(content_frame, text="  Reservation  ", font=("harlow solid italic", 50), foreground="#415433",
                      background="#CBCDDA")
    label.pack(padx=20, pady=10)

    def room_available(room_type):
        query = f"SELECT COUNT(*) FROM reservations WHERE room_type = '{room_type}' AND status = 'active'"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        # 4 reservations per room per day
        return count < 4

    def execute_reservation(name, age, contact, members, adhar, roomt, days):
        def dategive():
            date = reservation_date1.get_date()
            return date.strftime("%Y-%m-%d")
        reservation_date = dategive()
        room_type = ""
        if roomt == "Standard ₹1100":
            room_type = "Standard"
        elif roomt == "Deluxe ₹1900":
            room_type = 'Deluxe'
        elif roomt == "Suite ₹2700":
            room_type = "Suite"
        else:
            room_type = "Executive"
        try:
            def clear():
                update_content(content_frame, "Reservation_for_user")

            if room_available(room_type):
                reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d")
                checkout_date = reservation_date_obj + timedelta(days=int(days))

                cursor.execute(
                    f"INSERT INTO reservations values(null ,'{name}', {age}, {contact}, '{members}', {adhar}, "
                    f"'{room_type}', '{reservation_date}', '{checkout_date}', 'active')")
                connector.commit()

                success_label = ttk.Label(content_frame,
                                          text=f"\n \nReservation successful for {name} in {room_type} room from "
                                               f"{reservation_date} to {checkout_date}\n \n",
                                          font=("Century Gothic", 10))
                success_label.pack(pady=20)

                clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
                clear_button.pack(pady=16)

            else:
                error_label = ttk.Label(content_frame,
                                        text=f"Sorry, {room_type} room is not available for reservation "
                                             f"on {reservation_date}",
                                        font=("Century Gothic", 10), foreground="red")
                error_label.pack(pady=20)

                clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
                clear_button.pack(pady=16)
        except:
            messagebox.showerror("Invalid Entry", "Enter all Fields Correctly")

    frame2 = ttk.Frame(content_frame)
    frame2.pack(side='top', anchor='n')

    name = ttk.Entry(content_frame, font=("Helvetica", 18))
    name.insert(0, "Name")
    name.bind("<FocusIn>", lambda event: disappear_click(name, "Name"))
    name.bind("<FocusOut>", lambda event: appear_click(name, "Name"))

    age = ttk.Entry(content_frame, font=("Helvetica", 18))
    age.insert(0, "Age")
    age.bind("<FocusIn>", lambda event: disappear_click(age, "Age"))
    age.bind("<FocusOut>", lambda event: appear_click(age, "Age"))

    contact = ttk.Entry(content_frame, font=("Helvetica", 18))
    contact.insert(0, "Contact")
    contact.bind("<FocusIn>", lambda event: disappear_click(contact, "Contact"))
    contact.bind("<FocusOut>", lambda event: appear_click(contact, "Contact"))

    members = ttk.Combobox(content_frame, values=["1", "2", "3", "4", "More than 4"], font=("Helvetica", 16),
                           style='Custom.TMenubutton')
    members.set(" No. of Members")
    members.bind("<<ComboboxSelected>>")

    adhar = ttk.Entry(content_frame, font=("Helvetica", 18))
    adhar.insert(0, "Adhaar Number")
    adhar.bind("<FocusIn>", lambda event: disappear_click(adhar, "Adhaar Number"))
    adhar.bind("<FocusOut>", lambda event: appear_click(adhar, "Adhaar Number"))

    room_type = ttk.Combobox(content_frame, values=["Standard ₹1100", "Deluxe ₹1900", "Suite ₹2700", "Executive ₹4500"],
                             font=("Helvetica", 16),
                             style='Custom.TMenubutton')
    room_type.set(" Room Type")
    room_type.bind("<<ComboboxSelected>>")

    reservation_date1 = DateEntry(content_frame, font=("Helvetica", 16),date_pattern='dd-MM-yyyy',selectmode='day')
    reservation_date1.insert(0, "")
    reservation_date1.bind("<FocusIn>", lambda event: disappear_click(reservation_date1, "Reservation Date"))
    reservation_date1.bind("<FocusOut>", lambda event: appear_click(reservation_date1, "Reservation Date"))

    days = ttk.Entry(content_frame, font=("Helvetica", 18))
    days.insert(0, "Number of Days")
    days.bind("<FocusIn>", lambda event: disappear_click(days, "Number of Days"))
    days.bind("<FocusOut>", lambda event: appear_click(days, "Number of Days"))

    submit_button = ttk.Button(content_frame, text="Submit",
                               command=lambda: execute_reservation(name.get().title(), age.get(), contact.get(), members.get(),
                                                                   adhar.get(), room_type.get(), days.get()))
    name.pack(pady=10)
    age.pack(pady=10)
    contact.pack(pady=10)
    members.pack(pady=10)
    adhar.pack(pady=10)
    room_type.pack(pady=10)
    reservation_date1.pack(pady=10)
    days.pack(pady=10)
    submit_button.pack(pady=10)


def reservation(content_frame):
    def room_available(room_type):
        query = f"SELECT COUNT(*) FROM reservations WHERE room_type = '{room_type}' AND status = 'active'"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        # 4 reservations per room per day
        return count < 4

    def execute_reservation(name, age, contact, members, adhar, roomt, days):
        def dategive():
            date = reservation_date1.get_date()
            return date.strftime("%Y-%m-%d")
        reservation_date = dategive()
        room_type = ""
        if roomt == "Standard ₹1100":
            room_type = "Standard"
        elif roomt == "Deluxe ₹1900":
            room_type = 'Deluxe'
        elif roomt == "Suite ₹2700":
            room_type = "Suite"
        else:
            room_type = "Executive"
        try:
            def clear():
                update_content(content_frame, "Reservation")

            if room_available(room_type):
                reservation_date_obj = datetime.strptime(reservation_date, "%Y-%m-%d")
                checkout_date = reservation_date_obj + timedelta(days=int(days))

                cursor.execute(
                    f"INSERT INTO reservations values(null ,'{name}', {age}, {contact}, '{members}', {adhar}, "
                    f"'{room_type}', '{reservation_date}', '{checkout_date}', 'active')")
                connector.commit()

                success_label = ttk.Label(content_frame,
                                          text=f"\n \nReservation successful for {name} in {room_type} room from"
                                               f" {reservation_date} to {checkout_date}\n \n",
                                          font=("Century Gothic", 10))
                success_label.pack(pady=20)

                clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
                clear_button.pack(pady=5)

            else:
                error_label = ttk.Label(content_frame,
                                        text=f"Sorry, {room_type} room is not available for reservation "
                                             f"on {reservation_date}",
                                        font=("Century Gothic", 10), foreground="red")
                error_label.pack(pady=20)

                clear_button = ttk.Button(content_frame, text="Clear", command=lambda: clear())
                clear_button.pack(pady=5)
        except:
            messagebox.showerror("Invalid Entry", "Enter all Fields Correctly")

    frame2 = ttk.Frame(content_frame)
    frame2.pack(side='top', anchor='n')

    name = ttk.Entry(content_frame, font=("Helvetica", 18))
    name.insert(0, "Name")
    name.bind("<FocusIn>", lambda event: disappear_click(name, "Name"))
    name.bind("<FocusOut>", lambda event: appear_click(name, "Name"))

    age = ttk.Entry(content_frame, font=("Helvetica", 18))
    age.insert(0, "Age")
    age.bind("<FocusIn>", lambda event: disappear_click(age, "Age"))
    age.bind("<FocusOut>", lambda event: appear_click(age, "Age"))

    contact = ttk.Entry(content_frame, font=("Helvetica", 18))
    contact.insert(0, "Contact")
    contact.bind("<FocusIn>", lambda event: disappear_click(contact, "Contact"))
    contact.bind("<FocusOut>", lambda event: appear_click(contact, "Contact"))

    members = ttk.Combobox(content_frame, values=["1", "2", "3", "4", "More than 4"], font=("Helvetica", 16),
                           style='Custom.TMenubutton')
    members.set(" No. of Members")
    members.bind("<<ComboboxSelected>>")

    adhar = ttk.Entry(content_frame, font=("Helvetica", 18))
    adhar.insert(0, "Adhaar Number")
    adhar.bind("<FocusIn>", lambda event: disappear_click(adhar, "Adhaar Number"))
    adhar.bind("<FocusOut>", lambda event: appear_click(adhar, "Adhaar Number"))

    room_type = ttk.Combobox(content_frame, values=["Standard ₹1100", "Deluxe ₹1900", "Suite ₹2700", "Executive ₹4500"],
                             font=("Helvetica", 16),
                             style='Custom.TMenubutton')
    room_type.set(" Room Type")
    room_type.bind("<<ComboboxSelected>>")

    reservation_date1 = DateEntry(content_frame, font=("Helvetica", 16), date_pattern='dd-MM-yyyy', selectmode='day')
    reservation_date1.insert(0, "")
    reservation_date1.bind("<FocusIn>", lambda event: disappear_click(reservation_date1, "Reservation Date"))
    reservation_date1.bind("<FocusOut>", lambda event: appear_click(reservation_date1, "Reservation Date"))

    days = ttk.Entry(content_frame, font=("Helvetica", 18))
    days.insert(0, "Number of Days")
    days.bind("<FocusIn>", lambda event: disappear_click(days, "Number of Days"))
    days.bind("<FocusOut>", lambda event: appear_click(days, "Number of Days"))

    submit_button = ttk.Button(content_frame, text="Submit",
                               command=lambda: execute_reservation(name.get().title(), age.get(), contact.get(), members.get(),
                                                                   adhar.get(), room_type.get(), days.get()))

    name.pack(pady=10)
    age.pack(pady=10)
    contact.pack(pady=10)
    members.pack(pady=10)
    adhar.pack(pady=10)
    room_type.pack(pady=10)
    reservation_date1.pack(pady=10)
    days.pack(pady=10)
    submit_button.pack(pady=10)

    # reservation table
    def roomno(roomtype):
        connector = sql.connect(host="localhost", user="root", passwd="pass")
        cursor = connector.cursor()
        cursor.execute("use oasis")

        if roomtype in ["Standard", "Deluxe", "Suite", "Executive"]:
            cursor.execute(f"select room_no from {roomtype.lower()} where id is null")
            x = cursor.fetchone()
            l = list(x)
            return l[0]

    def execute(id_d, name, age, cont, member, adhar, roomt):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        key = roomno(roomt)

        query = f"null, '{name}', {age}, {cont}, '{member}', {adhar}, '{date}', '{time}', 'online', {key}, '{roomt}'," \
                f" null, null, null "

        def key_editor(roomtype, key):
            cursor.execute(f"select ID from checkin order by id desc limit 1")
            id = cursor.fetchone()
            ID = list(id)[0]
            cursor.execute(f"update {roomtype} set id = {ID} where room_no = {key}")
            connector.commit()

        try:
            cursor.execute(f"insert into checkin values({query})")
            key_editor(roomt, key)
            connector.commit()
            cursor.execute(f"update reservations set status = 'inactive' where id = {id_d};")
            connector.commit()
            update_content(content_frame, "Reservation")
        except:
            messagebox.showerror("Invalid Input", "Enter all the fields.")

    label_r = ttk.Label(frame2, text="  Reservation  ", font=("harlow solid italic", 35), foreground="#ffffff",
                        background="#1c1c1c")
    label_r.pack(padx=1, pady=1)

    columns = (
        'Id', 'Name', 'Age', 'Contact', 'Members', 'Adhaar', 'Roomtype', 'Reserve_date', 'Checkout_date', 'Status')

    scroll = ttk.Scrollbar(frame2, orient=tk.VERTICAL)
    scroll.pack(side="right", fill="y")

    tree2 = ttk.Treeview(frame2, columns=columns, show='headings', yscrollcommand=scroll.set)

    scroll.configure(command=tree2.yview)
    for i in columns:
        tree2.heading(i, text=i)
        tree2.column(i, minwidth=10, width=120)

    cursor.execute("select * from reservations")
    data = cursor.fetchall()

    tree2.tag_configure('green', background='green')
    tag = 'normal'
    for value in data:
        tag = 'green' if value[9] == 'active' else 'normal'
        tree2.insert('', tk.END, values=value, tags=tag)

    def item():
        for selected_item in tree2.selection():
            item = tree2.item(selected_item)
            record = item['values']
            messagebox.showinfo(title='Information', message=','.join(record))

    tree2.bind('<<TreeviewSelect>>', item)
    tree2.pack(expand=True, fill="both")

    def checkin_record():
        selected = tree2.focus()
        values = tree2.item(selected, 'values')
        execute(values[0], values[1], values[2], values[3], values[4], values[5], values[6])

    select_record = ttk.Button(frame2, text='Checkin', command=checkin_record)
    select_record.pack(padx=305, side='left')

    def toggle_record():
        selected = tree2.focus()
        values = tree2.item(selected, 'values')
        if values[9] == "active":
            cursor.execute(f"update reservations set status = 'inactive' where id = {values[0]}")
            connector.commit()
        else:
            cursor.execute(f"update reservations set status = 'active' where id = {values[0]}")
            connector.commit()
        update_content(content_frame, "Reservation")

    toggle_record = ttk.Button(frame2, text='Toggle Record', command=toggle_record)
    toggle_record.pack(padx=5, side='left')

    def cancel_record():
        selected = tree2.focus()
        values = tree2.item(selected, 'values')
        cursor.execute(f"update reservations set status = 'cancelled' where id = {values[0]}")
        connector.commit()
        update_content(content_frame, "Reservation")

    cancel_record = ttk.Button(frame2, text='Cancel Record', command=cancel_record)
    cancel_record.pack(padx=300, side='left')


def guest_list(content_frame):
    label = ttk.Label(content_frame, text="  Guest list  ", font=("harlow solid italic", 50), foreground="#ffffff",
                      background="#c49787")
    label.pack(padx=20, pady=10)

    frame1 = ttk.Frame(content_frame)
    frame1.pack()

    columns = (
        'Id', 'Name', 'Age', 'Contact', 'Members', 'Adhaar', 'Checkin_date', 'Checkin_time', 'Payment', 'Room_No',
        'Roomtype', 'Checkout_date', 'Checkout_time')

    scroll = ttk.Scrollbar(frame1, orient=tk.VERTICAL)
    scroll.pack(side="right", fill="y")

    tree = ttk.Treeview(frame1, columns=columns, show='headings', yscrollcommand=scroll.set)

    scroll.configure(command=tree.yview)
    for i in columns:
        tree.heading(i, text=i)
        tree.column(i, minwidth=10, width=120)

    cursor.execute("select * from checkin")
    data = cursor.fetchall()
    for value in data:
        tree.insert('', tk.END, values=value)

    def item():
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            messagebox.showinfo(title='Information', message=','.join(record))

    tree.bind('<<TreeviewSelect>>', item)
    tree.pack(expand=True, fill="both")

    # for all room information
    frame_room = ttk.Frame(content_frame)
    frame_room.pack(pady=10)
    for room in ['standard', 'deluxe', 'suite', 'executive']:
        frame = ttk.Frame(frame_room)
        frame.pack(pady=5, side='left')
        label = ttk.Label(frame, text=f"  {room}  ", font=("harlow solid italic", 30), foreground="#a1dbcd",
                          background="#1c1c1c")
        label.pack(padx=1, pady=1)

        column = ('Room NO', 'ID')
        tree = ttk.Treeview(frame, columns=column, show='headings')
        for i in column:
            tree.heading(i, text=i)
            tree.column(i, minwidth=10, width=120)

        cursor.execute(f"select * from {room}")
        standard_data = cursor.fetchall()

        tree.tag_configure('green', background='green')
        tree.tag_configure('red', background='red')
        tag = 'normal'

        for value in standard_data:
            tag = 'green' if value[1] is None else 'red'
            tree.insert('', tk.END, values=value, tags=tag)
        tree.bind('<<TreeviewSelect>>', item)
        tree.pack(expand=True, fill="both")


def info(content_frame):
    def id_information(new_id):
        try:
            update_content(content_frame, "Info")

            cursor.execute(f'select * from checkin where id = {new_id}')
            j = cursor.fetchall()
            x = list(j[0])
            label = ttk.Label(content_frame,
                              text=f"Name: {x[1]}\nAge: {x[2]}\nContact: {x[3]}\nMembers: {x[4]}\nAdhaar: "
                                   f"{x[5]}\nCheckin Date: {x[6]}\nCheckin Time: {x[7]}\n ",
                              font=("Century Gothic", 20))
            label.pack(pady=20)

        except:
            label = ttk.Label(content_frame, text="No Records Found", font=("Century Gothic", 20))
            label.pack(pady=20)

    label = ttk.Label(content_frame, text="Information ", font=("harlow solid italic", 70), foreground="#e0d1b9",
                      background="#0281d0")
    label.pack(padx=20, pady=20)

    given_id = ttk.Entry(content_frame, font=("Helvetica", 18))
    given_id.insert(0, "ID")
    given_id.bind("<FocusIn>", lambda event: disappear_click(given_id, "ID"))
    given_id.bind("<FocusOut>", lambda event: appear_click(given_id, "ID"))
    submit_button = ttk.Button(content_frame, text="Submit", command=lambda: id_information(given_id.get()))
    given_id.pack(pady=10)
    submit_button.pack(pady=10)


def revenue(content_frame):
    label = ttk.Label(content_frame, text="  Revenue  ", font=("harlow solid italic", 50), foreground="#16c0d4",
                      background="#e0e2e4")
    label.pack(padx=20, pady=10)
    cursor.execute("select * from checkin")
    data = cursor.fetchall()

    # REVENUE
    dates = []
    price = []
    for i in data:
        if str(i[11]) in dates:
            last_value = price.pop()
            if last_value is None:
                pass
            else:
                new = i[13] + last_value
                price.append(new)  # price
        else:
            dates.append(str(i[11]))  # date
            price.append(i[13])  # price

    # Customers
    date = []
    single_date = []
    customer = []

    for i in data:
        date.append(str(i[6]))
    for i in date:
        if i in single_date:
            x = customer.pop()
            customer.append(x + 1)
        else:
            single_date.append(i)
            val = 1
            customer.append(val)

    frame = ttk.Frame(content_frame)
    frame.pack(pady=5)

    def show_image_line(x_coordinate, y_coordinate):
        fig, ax = plt.subplots()
        ax.plot(x_coordinate, y_coordinate, label='Revenue')
        ax.set_ylabel('Customer')
        ax.set_xlabel('Date')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_wid = canvas.get_tk_widget()
        canvas_wid.pack(side='left')

    def show_image_bar(x_coordinate, y_coordinate):
        fig, ax = plt.subplots()
        ax.bar(x_coordinate, y_coordinate, label='Revenue')
        ax.set_ylabel('Amount')
        ax.set_xlabel('Date')
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_wid = canvas.get_tk_widget()
        canvas_wid.pack(side='left', fill='both')
    try:
        show_image_bar(dates, price)
        show_image_line(single_date, customer)
    except:
        messagebox.showerror("No Data Available", "No Revenue has been Generated.")


second_screen_buttons = []


def second_screen():
    content_frame = content_frame1[0]
    sidebar_frame = button_in_frame1[0]
    functions = ["Check-In", "Check-Out", "Reservation", "Guest List", "Revenue", 'Log Out']
    common_button_width = 30  # Set a common width for all buttons
    for i, function_text in enumerate(functions):
        button = ttk.Button(sidebar_frame, text=function_text, width=common_button_width)
        button.grid(row=i, column=0, padx=20, pady=10, sticky="w")
        second_screen_buttons.append(button)
        if function_text == "Check-In":
            button.configure(command=lambda: update_content(content_frame, "Check-In"))
        elif function_text == "Check-Out":
            button.configure(command=lambda: update_content(content_frame, "Check-Out"))
        elif function_text == "Reservation":
            button.configure(command=lambda: update_content(content_frame, "Reservation"))
        elif function_text == "Guest List":
            button.configure(command=lambda: update_content(content_frame, "Guest List"))
        elif function_text == "Revenue":
            button.configure(command=lambda: update_content(content_frame, "Revenue"))
        elif function_text == "Log Out":
            button.configure(command=lambda: first_screen())
        else:
            button.configure(command=lambda text=function_text: first_screen)
    update_content(content_frame, "Check-In")


def first_screen():
    content_frame = content_frame1[0]
    sidebar_frame = button_in_frame1[0]
    try:
        for i in range(len(second_screen_buttons)):
            second_screen_buttons[i].destroy()
    except:
        pass
    functions = ["Check-In", "Reservation", "Check-Out", "Info", "Login"]
    common_button_width = 30  # Set a common width for all buttons
    for i, function_text in enumerate(functions):
        button = ttk.Button(sidebar_frame, text=function_text, width=common_button_width)
        button.grid(row=i, column=0, padx=20, pady=10, sticky="w")

        button_in_frame1.append(button)

        if function_text == "Check-In":
            button.configure(command=lambda: update_content(content_frame, "Check-In"))
        elif function_text == "Check-Out":
            button.configure(command=lambda: update_content(content_frame, "Check-Out"))
        elif function_text == "Reservation":
            button.configure(command=lambda: update_content(content_frame, "Reservation_for_user"))
        elif function_text == "Login":
            button.configure(command=lambda: update_content(content_frame, "Login"))
        elif function_text == "Info":
            button.configure(command=lambda: update_content(content_frame, "Info"))
        else:
            button.configure(command=lambda text=function_text: update_content(content_frame, text))

    update_content(content_frame, "Check-In")


def login(content_frame):
    label = ttk.Label(content_frame, text="  Login  ", font=("harlow solid italic", 50), foreground="#16c0d4",
                      background="#e0e2e4")
    label.pack(padx=20, pady=40)

    user = ttk.Entry(content_frame, font=("Helvetica", 18))
    user.insert(0, "Username")
    user.bind("<FocusIn>", lambda event: disappear_click(user, "Username"))
    user.bind("<FocusOut>", lambda event: appear_click(user, "Username"))

    passwd = ttk.Entry(content_frame, font=("Helvetica", 18))
    passwd.insert(0, "Password")
    passwd.bind("<FocusIn>", lambda event: disappear_click(passwd, "Password"))
    passwd.bind("<FocusOut>", lambda event: appear_click(passwd, "Password"))

    def log(username, password):
        users = {'parth': '2121', 'krishna': '1919', 'mahin': '2020'}
        if username in users and users[username] == password:
            return True
        else:
            return False

    def checkin1():
        if log(user.get(), passwd.get()):
            second_screen()
        else:
            messagebox.showerror("Wrong Username", "Invalid Credentials")

    login = ttk.Button(content_frame, text="Login", command=lambda: checkin1())

    user.pack(pady=10)
    passwd.pack(pady=10)
    login.pack(pady=10)


button_in_frame1 = []
content_frame1 = []


def main():
    root = tk.Tk()
    root.title("Hotel Management App")
    sv_ttk.set_theme("dark")
    root.state("zoomed")

    #recent added
    #root.tk.call('tk', 'scaling', 0.8)

    # grid weights resizing
    root.grid_columnconfigure(0, weight=0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=7)

    # Sidebar Frame
    sidebar_frame = ttk.Frame(root, style="Sidebar.TFrame", width=200)
    sidebar_frame.grid(row=0, column=0, sticky="nsw")
    style = ttk.Style()  # for changing background color

    #recent added
    #style.configure('.', font=('Helvetica', int(15)))

    style.configure("Sidebar.TFrame", background="#0d1c2a")

    button_in_frame1.append(sidebar_frame)
    functions = ["Check-In", "Reservation", "Check-Out", "Info", "Login"]
    common_button_width = 30  # Set a common width for all buttons
    for i, function_text in enumerate(functions):
        button = ttk.Button(sidebar_frame, text=function_text, width=common_button_width)
        button.grid(row=i, column=0, padx=20, pady=10, sticky="w")
        # added two lines for scaling in laptop
        button_in_frame1.append(button)

        if function_text == "Check-In":
            button.configure(command=lambda: update_content(content_frame, "Check-In"))
        elif function_text == "Check-Out":
            button.configure(command=lambda: update_content(content_frame, "Check-Out"))
        elif function_text == "Reservation":
            button.configure(command=lambda: update_content(content_frame, "Reservation_for_user"))
        elif function_text == "Login":
            button.configure(command=lambda: update_content(content_frame, "Login"))
        elif function_text == "Info":
            button.configure(command=lambda: update_content(content_frame, "Info"))
        else:
            button.configure(command=lambda text=function_text: update_content(content_frame, text))

    content_frame = ttk.Frame(root, style="Content.TFrame")
    content_frame.grid(row=0, column=1, sticky="nsew")
    content_frame1.append(content_frame)
    root.columnconfigure(1, weight=7)

    update_content(content_frame, "Check-In")
    root.mainloop()


if __name__ == "__main__":
    main()
