from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

#actually its a getter from sql database for display on datagridview(Treeview)
def update(rows):
    trv.delete(*trv.get_children())
    for i in rows:
        trv.insert('', 'end', values=i)

def search():
    q2 = q.get()
    query = "SELECT id, cariadi, vno, vergidairesi, adres, telefon, sehir FROM musteri WHERE id LIKE '%"+q2+"%' OR cariadi LIKE '%"+q2+"%' "
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def clear():
    query = "SELECT id, cariadi, vno, vergidairesi, adres, telefon, sehir FROM musteri"
    cursor.execute(query)
    rows = cursor.fetchall()
    update(rows)

def getrow(event):
    rowid = trv.identify_row(event.y)
    item = trv.item(trv.focus())
    t1.set(item['values'][0])
    t2.set(item['values'][1])
    t3.set(item['values'][2])
    t4.set(item['values'][3])
    t5.set(item['values'][4])
    t6.set(item['values'][5])
    t7.set(item['values'][6])

def add_data():
    cariadi = t2.get()
    vno = t3.get()
    vergidairesi = t4.get()
    adres = t5.get()
    telefon = t6.get()
    sehir = t7.get()
    query = "INSERT INTO musteri(id, cariadi, vno, vergidairesi, adres, telefon, sehir) VALUES(NULL, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (cariadi, vno, vergidairesi, adres, telefon, sehir))
    mydb.commit()
    clear()
    messagebox.showinfo("done","well done you've added")

def update_data():
    id = t1.get()
    cariadi = t2.get()
    vno = t3.get()
    vergidairesi = t4.get()
    adres = t5.get()
    telefon = t6.get()
    sehir = t7.get()
    
    if messagebox.askyesno("are you sure","Please be sure that you've double clicked the data unless action won't happen!"):
        query = "UPDATE musteri SET cariadi = %s, vno = %s, vergidairesi = %s, adres = %s, telefon = %s, sehir = %s WHERE id =" + id
        cursor.execute(query, ( cariadi, vno, vergidairesi, adres, telefon, sehir))
        mydb.commit()
        clear()
    else: 
        return True

def delete_data():
    data_id = t1.get()
    if(messagebox.askyesno("Are you confirm?", "Please be sure that you've double clicked the data unless action won't happen!")):
        query = "DELETE FROM musteri WHERE id =" + data_id
        cursor.execute(query)
        mydb.commit()
        clear()
        
    else:
        return True

def purify():
    input_id.delete(0, END)
    input_cariadi.delete(0, END)
    input_vno.delete(0, END)
    input_vergidairesi.delete(0, END)
    input_adres.delete(0, END)
    input_telefon.delete(0, END)
    input_sehir.delete(0, END)

#setting connection configurations via mysql.connector
mydb = mysql.connector.connect(host="####", user="###", password="####", database="###")
#i don't know the official term of it but it's our hitman for query commands
cursor = mydb.cursor()

#creating windows 1-2 step (like ardiuno loops)
root = Tk()
q = StringVar()
t1, t2, t3, t4, t5, t6, t7 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

#our panels 
wrapper1 = LabelFrame(root, text="Data List")
wrapper2 = LabelFrame(root, text="Search")
wrapper3 = LabelFrame(root, text="Product Data")
# panel cooridantes and etc
wrapper1.pack(fill="both", expand="yes", padx="10", pady="30")
wrapper2.pack(fill="both", expand="yes", padx="70", pady="30")
wrapper3.pack(fill="both", expand="yes", padx="70", pady="30")

# defining python version of datagridviewview 
trv = ttk.Treeview(wrapper1, columns=(1,2,3,4,5,6,7), show="headings", height="14" )

#ttk için barbie giydirmeceden başka bir şey değil ya
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="siver", foreground="black", rowheight=25, fieldbackground="silver")
style.map('Treeview', background=[('selected','green')])

trv.pack()

#our column names
trv.heading(1, text="ID")
trv.heading(2, text="Cari Adi")
trv.heading(3, text="VNO")
trv.heading(4, text="Vergi Dairesi")
trv.heading(5, text="Adres")
trv.heading(6, text="Telefon")
trv.heading(7, text="Sehir")

# i want to get the data when i double-click
trv.bind('<Double 1>', getrow)

#our query and executions for sql
query = "SELECT id, cariadi, vno, vergidairesi, adres, telefon, sehir FROM musteri"
cursor.execute(query)
rows = cursor.fetchall()
update(rows)

#Search Section
label_search = Label(wrapper2, font=('Arial', 15), text="Search")
label_search.pack(side=tk.LEFT, padx=10)
input_label = Entry(wrapper2, width=25, font=("Helvatica",15), textvariable=q)
input_label.pack(side=tk.LEFT, padx=6)
button_search = Button(wrapper2, text=" Search", font=('Arial', 15), bg="#F4FE82", command=search)
button_search.pack(side=tk.LEFT, padx=6)
button_clear = Button(wrapper2, text="Clear", font=('Arial', 15), command=clear)
button_clear.pack(side=tk.LEFT, padx=6)

#Data Section
label_id = Label(wrapper3, font=('Arial', 15), text="Cariadi")
label_id.grid(row=0, column=0, padx=5, pady=3)
input_id = Entry(wrapper3, width=25, font=("Helvatica",15),  state=DISABLED, textvariable=t1)
input_id.grid(row=0, column=1, padx=5, pady=3)

label_cariadi = Label(wrapper3, font=('Arial', 15), text="Cariadi")
label_cariadi.grid(row=1, column=0, padx=5, pady=3)
input_cariadi = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t2)
input_cariadi.grid(row=1, column=1, padx=5, pady=3)

label_vno = Label(wrapper3, font=('Arial', 15), text="VNO: ")
label_vno.grid(row=2, column=0, padx=5, pady=3)
input_vno = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t3)
input_vno.grid(row=2, column=1, padx=5, pady=3)

label_vergidairesi = Label(wrapper3, font=('Arial', 15), text="Vergi Dairesi: ")
label_vergidairesi.grid(row=3, column=0, padx=5, pady=3)
input_vergidairesi = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t4)
input_vergidairesi.grid(row=3, column=1, padx=5, pady=3)

label_adres = Label(wrapper3, font=('Arial', 15), text="Adres: ")
label_adres.grid(row=4, column=0, padx=5, pady=3)
input_adres = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t5)
input_adres.grid(row=4, column=1, padx=5, pady=3)

label_telefon = Label(wrapper3, font=('Arial', 15), text="Telefon: ")
label_telefon.grid(row=5, column=0, padx=5, pady=3)
input_telefon = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t6)
input_telefon.grid(row=5, column=1, padx=5, pady=3)

label_sehir = Label(wrapper3, font=('Arial', 15), text="Sehir: ")
label_sehir.grid(row=6, column=0, padx=5, pady=3)
input_sehir = Entry(wrapper3, width=25, font=("Helvatica",15), textvariable=t7)
input_sehir.grid(row=6, column=1, padx=5, pady=3)

button_add = Button(wrapper3, text="Add", font=('Arial', 15), bg="#84F894", command=add_data)
button_add.grid(row=7, column=0, padx=10, pady=8)
button_update = Button(wrapper3, text="Update", font=('Arial', 15), bg="#84E8F8", command=update_data)
button_update.grid(row=7, column=1, padx=10, pady=8)
button_delete = Button(wrapper3, text="Delete", font=('Arial', 15), bg="#FF9999", command=delete_data)
button_delete.grid(row=7, column=2, padx=10, pady=8)
button_purify = Button(wrapper3, text="Purify", font=('Arial', 15), bg="#F398FF", command=purify)
button_purify.grid(row=7, column=3, padx=100, pady=8)







#creating windows 2-2 step
root.title("DATA APPLICATION")
root.geometry("1600x1000")
root.mainloop()



# label_bruh = Label(wrapper3, text="bruh")
# label_bruh.grid(row=6, column=0, padx=5, pady=3)
# input_bruh = Entry(wrapper3, textvariable=t1)
# input_bruh.grid(row=6, column=1, padx=5, pady=3)
