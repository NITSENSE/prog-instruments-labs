import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import sqlite3
image1 = 'library.png'
image2 = 'image2.png'
image3 = 'finance.png'


class Menu:
    """Класс главного меню библиотечного приложения."""

    def __init__(self):
        """Инициализирует главное окно приложения и создает базу данных."""
        self.root = tk.Tk()
        self.root.title('Menu')
        self.root.state('zoomed')
        connection = sqlite3.connect('test.db')
        connection.execute('''create table if not exists book_info
        (ID VARCHAR PRIMARY KEY NOT NULL,
        TITLE VARTEXT NOT NULL,
        AUTHOR VARTEXT NOT NULL,
        GENRE VARTEXT NOT NULL,
        COPIES VARINT NOT NULL,
        LOCATION VARCHAR NOT NULL);''')
        connection.commit()
        connection.execute('''create table if not exists book_issued
        (BOOK_ID VARCHAR NOT NULL,
        STUDENT_ID VARCHAR NOT NULL,
        ISSUE_DATE DATE NOT NULL,
        RETURN_DATE DATE NOT NULL,
        PRIMARY KEY (BOOK_ID,STUDENT_ID));''')
        connection.commit()
        connection.close()
        self.content_frame = self.create_canvas(image1)
        btn_book_data = tk.Button(self.content_frame, text='BOOK DATA', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10, borderwidth=0, command=self.book).place(x=100, y=500)
        btn_student_data = tk.Button(self.content_frame, text='STUDENT DATA', font='Papyrus 22 bold', fg='Yellow', bg='Black', width=19, padx=10, borderwidth=0, command=self.student).place(x=800, y=500)
        self.root.mainloop()
        
    def create_canvas(self, images):
        """Создает холст с фоновым изображением на весь экран."""
        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        photo = Image.open(images)
        photo1 = photo.resize((w, h), Image.ANTIALIAS)
        photo2 = ImageTk.PhotoImage(photo1)
        self.canvas = tk.Canvas(self.root, width='%d' % w, height='%d' % h)
        self.canvas.grid(row=0, column=0)
        self.canvas.grid_propagate(0)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo2)
        self.canvas.image = photo2
        return self.canvas
    
    def book(self):
        """Открывает меню управления книгами."""
        self.content_frame.destroy()
        self.content_frame = self.create_canvas(image2)
        btn_add_books = tk.Button(self.content_frame, text='Add Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.add_book).place(x=12, y=100)
        btn_search_books = tk.Button(self.content_frame, text='Search Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.search).place(x=12, y=200)
        btn_all_books = tk.Button(self.content_frame, text='All Books', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.view_all_books).place(x=12, y=300)
        btn_main_menu = tk.Button(self.content_frame, text='<< Main Menu', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.main_menu).place(x=12, y=500)

    def add_book(self):
        """Создает окно для добавления новой книги."""
        self.aid = tk.StringVar()
        self.aauthor = tk.StringVar()
        self.aname = tk.StringVar()
        self.acopies = tk.IntVar()
        self.agenre = tk.StringVar()
        self.aloc = tk.StringVar()
        self.f1 = tk.Frame(self.content_frame, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        label_book_id = tk.Label(self.f1, text='Book ID : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1).place(x=50, y=50)
        entry_book_id = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aid).place(x=150, y=50)
        label_title = tk.Label(self.f1, text='Title : ', font='Papyrus 12 bold', fg='Orange', bg='Black', pady=1).place(x=50, y=100)
        entry_title = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aname).place(x=150, y=100)
        label_author = tk.Label(self.f1, text='Author : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50, y=150)
        entry_author = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aauthor).place(x=150, y=150)
        label_genre = tk.Label(self.f1, text='Genre : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50, y=200)
        entry_genre = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.agenre).place(x=150, y=200)
        label_copies = tk.Label(self.f1, text='Copies : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50, y=250)
        entry_copies = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.acopies).place(x=150, y=250)
        label_location = tk.Label(self.f1, text='Location : ', font='Papyrus 12 bold', fg='orange', bg='Black', pady=1).place(x=50, y=300)
        entry_location = tk.Entry(self.f1, width=45, bg='orange', fg='black', textvariable=self.aloc).place(x=150, y=300)
        self.f1.grid_propagate(0)
        btn_add = tk.Button(self.f1, text='Add', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3, command=self.add_data).place(x=150, y=400)
        btn_back = tk.Button(self.f1, text='Back', font='Papyrus 10 bold', fg='black', bg='orange', width=15, bd=3, command=self.go_back).place(x=350, y=400)

    def go_back(self):
        """Закрывает текущее окно и возвращается к предыдущему."""
        self.f1.destroy()

    def main_menu(self):
        """Возвращает пользователя в главное меню."""
        self.root.destroy()
        a = Menu()

    def add_data(self):
        """Добавляет новую книгу в базу данных."""
        book_id = self.aid.get()
        book_title = self.aname.get()
        author = self.aauthor.get()
        genre = self.agenre.get()
        copies = self.acopies.get()
        location = self.aloc.get()
        connection = sqlite3.connect('test.db')
        try:
            if (book_id and book_title and author and genre and location) == "":
                messagebox.showinfo("Error", "Fields cannot be empty.")
            else:
                connection.execute("insert into book_info \
                values (?,?,?,?,?,?)", (book_id.capitalize(), book_title.capitalize(), author.capitalize(), genre.capitalize(), copies, location.capitalize(),))
                connection.commit()
                messagebox.showinfo("Success", "Book added successfully")
        except sqlite3.IntegrityError:
            messagebox.showinfo("Error", "Book is already present.")
        connection.close()

    def search(self):
        """Создает окно поиска книг."""
        self.sid = tk.StringVar()
        self.f1 = tk.Frame(self.content_frame, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        label_search = tk.Label(self.f1, text='Book ID/Title/Author/Genre: ', font=('Papyrus 10 bold'), bd=2, fg='orange', bg='black').place(x=20, y=40)
        entry_search = tk.Entry(self.f1, width=25, bd=5, bg='orange', fg='black', textvariable=self.sid).place(x=260, y=40)
        btn_search = tk.Button(self.f1, text='Search', bg='orange', font='Papyrus 10 bold', width=9, bd=2, command=self.search_book).place(x=500, y=37)
        btn_back = tk.Button(self.f1, text='Back', bg='orange', font='Papyrus 10 bold', width=10, bd=2, command=self.go_back).place(x=250, y=450)

    def create_tree(self, plc, lists):
        """Создает таблицу Treeview для отображения данных."""
        self.tree = ttk.Treeview(plc, height=13, column=(lists), show='headings')
        n = 0
        while n is not len(lists):
            self.tree.heading("#" + str(n + 1), text=lists[n])
            self.tree.column("" + lists[n], width=100)
            n = n + 1
        return self.tree

    def search_book(self):
        """Выполняет поиск книги по ID, названию, автору или жанру."""
        search_query = self.sid.get()
        if search_query != "":
            self.list4 = ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "COPIES", "LOCATION")
            self.trees = self.create_tree(self.f1, self.list4)
            self.trees.place(x=25, y=150)
            connection = sqlite3.connect('test.db')
            cursor = connection.execute("select * from book_info where ID=? OR TITLE=? OR AUTHOR=? OR GENRE=?", (search_query.capitalize(), search_query.capitalize(), search_query.capitalize(), search_query.capitalize(),))
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    self.trees.insert("", tk.END, values=row)
                connection.commit()
                connection.close()
                self.trees.bind('<<TreeviewSelect>>')
                self.variable = tk.StringVar(self.f1)
                self.variable.set("Select Action:")
                self.cm = ttk.Combobox(self.f1, textvariable=self.variable, state='readonly', font='Papyrus 15 bold', height=50, width=15,)
                self.cm.config(values=('Add Copies', 'Delete Copies', 'Delete Book'))
                self.cm.place(x=50, y=100)
                self.cm.pack_propagate(0)
                self.cm.bind("<<ComboboxSelected>>", self.combo)
                self.cm.selection_clear()
            else:
                messagebox.showinfo("Error", "Data not found")
        else:
            messagebox.showinfo("Error", "Search field cannot be empty.")

    def combo(self, event):
        """Обрабатывает выбор действия из выпадающего списка."""
        self.var_Selected = self.cm.current()
        if self.var_Selected == 0:
            self.copies(self.var_Selected)
        elif self.var_Selected == 1:
            self.copies(self.var_Selected)
        elif self.var_Selected == 2:
            self.delete_item()

    def delete_item(self):
        """Подготавливает удаление выбранной книги."""
        try:
            self.curItem = self.trees.focus()
            self.c1 = self.trees.item(self.curItem, "values")[0]
            btn_update = tk.Button(self.f1, text='Update', font='Papyrus 10 bold', width=9, bd=3, command=self.delete2).place(x=500, y=97)

        except:
            messagebox.showinfo("Empty", "Please select something.")

    def delete2(self):
        """Удаляет книгу из базы данных, если она не выдана студенту."""
        connection = sqlite3.connect('test.db')
        cursor = connection.execute("select * from book_issued where BOOK_ID=?", (self.c1,))
        issued_records = cursor.fetchall()
        if issued_records != 0:
            connection.execute("DELETE FROM book_info where ID=?", (self.c1,))
            connection.commit()
            messagebox.showinfo("Successful", "Book Deleted sucessfully.")
            self.trees.delete(self.curItem)
        else:
            messagebox.showinfo("Error", "Book is Issued.\nBook cannot be deleted.")
        connection.commit()
        connection.close()

    def copies(self, varr):
        """Создает интерфейс для добавления или удаления копий книги."""
        try:
            curItem = self.trees.focus()
            self.c1 = self.trees.item(curItem, "values")[0]
            self.c2 = self.trees.item(curItem, "values")[4]
            self.scop = tk.IntVar()
            self.e5 = tk.Entry(self.f1, width=20, textvariable=self.scop)
            self.e5.place(x=310, y=100)
            if varr == 0:
                btn_update = tk.Button(self.f1, text='Update', font='Papyrus 10 bold', bg='orange', fg='black', width=9, bd=3, command=self.add_copies).place(x=500, y=97)
            if varr == 1:
                btn_update = tk.Button(self.f1, text='Update', font='Papyrus 10 bold', bg='orange', fg='black', width=9, bd=3, command=self.delete_copies).place(x=500, y=97)
        except:
            messagebox.showinfo("Empty", "Please select something.")

    def add_copies(self):
        """Добавляет указанное количество копий книги."""
        no = self.e5.get()
        if int(no) >= 0:
            connection = sqlite3.connect('test.db')
            connection.execute("update book_info set COPIES=COPIES+? where ID=?", (no, self.c1,))
            connection.commit()
            messagebox.showinfo("Updated", "Copies added sucessfully.")
            self.search_book()
            connection.close()

        else:
            messagebox.showinfo("Error", "No. of copies cannot be negative.")

    def delete_copies(self):
        """Удаляет указанное количество копий книги."""
        no1 = self.e5.get()
        if int(no1) >= 0:
            if int(no1) <= int(self.c2):
                connection = sqlite3.connect('test.db')
                connection.execute("update book_info set COPIES=COPIES-? where ID=?", (no1, self.c1,))
                connection.commit()
                connection.close()
                messagebox.showinfo("Updated", "Deleted sucessfully")
                self.search_book()
            else:
                messagebox.showinfo("Maximum", "No. of copies to delete exceed available copies.")
        else:
            messagebox.showinfo("Error", "No. of copies cannot be negative.")

    def view_all_books(self):
        """Отображает список всех книг в базе данных."""
        self.f1 = tk.Frame(self.content_frame, height=500, width=650, bg='black')
        self.f1.place(x=500, y=100)
        btn_back = tk.Button(self.f1, text='Back', bg='orange', fg='black', width=10, bd=3, command=self.go_back).place(x=250, y=400)
        connection = sqlite3.connect('test.db')
        self.list3 = ("BOOK ID", "TITLE", "AUTHOR", "GENRE", "COPIES", "LOCATION")
        self.treess = self.create_tree(self.f1, self.list3)
        self.treess.place(x=25, y=50)
        cursor = connection.execute("select * from book_info")
        results = cursor.fetchall()
        if len(results) != 0:
            for row in results:
                self.treess.insert('', tk.END, values=row)
        connection.commit()
        connection.close()

    def student(self):
        """Открывает меню управления студентами и выданными книгами."""
        self.content_frame.destroy()
        self.content_frame = self.create_canvas(image2)
        btn_issue_book = tk.Button(self.content_frame, text='Issue book', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.issue).place(x=12, y=100)
        btn_return_book = tk.Button(self.content_frame, text='Return Book', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.return_book_menu).place(x=12, y=200)
        btn_student_activity = tk.Button(self.content_frame, text='Student Activity', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.activity).place(x=12, y=300)
        btn_main_menu = tk.Button(self.content_frame, text='<< Main Menu', font='Papyrus 22 bold', fg='Orange', bg='Black', width=15, padx=10, command=self.main_menu).place(x=12, y=600)

    def issue(self):
        """Создает окно для выдачи книги студенту."""
        self.aidd = tk.StringVar()
        self.astudentt = tk.StringVar()
        self.f1 = tk.Frame(self.content_frame, height=550, width=500, bg='black')
        self.f1.place(x=500, y=100)
        label_book_id = tk.Label(self.f1, text='Book ID : ', font='papyrus 15 bold', bg='black', fg='orange').place(x=50, y=100)
        entry_book_id = tk.Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.aidd).place(x=180, y=100)
        label_student_id = tk.Label(self.f1, text='Student Id : ', font='papyrus 15 bold', bg='black', fg='orange').place(x=50, y=150)
        entry_student_id = tk.Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.astudentt).place(x=180, y=150)
        btn_back = tk.Button(self.f1, text='Back', font='Papyrus 10 bold', fg='black', bg='orange', width=10, bd=3, command=self.go_back).place(x=50, y=250)
        btn_issue = tk.Button(self.f1, text='Issue', font='Papyrus 10 bold', fg='black', bg='orange', width=10, bd=3, command=self.issue_book).place(x=200, y=250)

    def issue_book(self):
        """Обрабатывает выдачу книги студенту и обновляет базу данных."""
        bookid = self.aidd.get()
        studentid = self.astudentt.get()
        connection = sqlite3.connect('test.db')
        cursor = connection.cursor()
        cursor.execute("select ID,COPIES from book_info where ID=?", (bookid.capitalize(),))
        an = cursor.fetchall()
        if (bookid and studentid != ""):
            if an != []:
                for i in an:
                    if i[1] > 0:
                        try:
                            connection.execute("insert into book_issued \
                            values (?,?,date('now'),date('now','+7 day'))", (bookid.capitalize(), studentid.capitalize(),))
                            connection.commit()
                            connection.execute("update book_info set COPIES=COPIES-1 where ID=?", (bookid.capitalize(),))
                            connection.commit()
                            connection.close()
                            messagebox.showinfo("Updated", "Book Issued sucessfully.")
                        except:
                            messagebox.showinfo("Error", "Book is already issued by student.")

                    else:
                        messagebox.showinfo("Unavailable", "Book unavailable.\nThere are 0 copies of the book.")
            else:
                messagebox.showinfo("Error", "No such Book in Database.")
        else:
            messagebox.showinfo("Error", "Fields cannot be blank.")

    def return_book_menu(self):
        """Создает окно для возврата книги от студента."""
        self.aidd = tk.StringVar()
        self.astudentt = tk.StringVar()
        self.f1 = tk.Frame(self.content_frame, height=550, width=500, bg='black')
        self.f1.place(x=500, y=100)
        label_book_id = tk.Label(self.f1, text='Book ID : ', font='papyrus 15 bold', fg='orange', bg='black').place(x=50, y=100)
        entry_book_id = tk.Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.aidd).place(x=180, y=100)
        label_student_id = tk.Label(self.f1, text='Student Id : ', font='papyrus 15 bold', fg='orange', bg='black').place(x=50, y=150)
        entry_student_id = tk.Entry(self.f1, width=25, bd=4, bg='orange', textvariable=self.astudentt).place(x=180, y=150)
        btn_back = tk.Button(self.f1, text='Back', font='Papyrus 10 bold', bg='orange', fg='black', width=10, bd=3, command=self.go_back).place(x=50, y=250)
        btn_return = tk.Button(self.f1, text='Return', font='Papyrus 10 bold', bg='orange', fg='black', width=10, bd=3, command=self.process_return_book).place(x=200, y=250)
        self.f1.grid_propagate(0)

    def process_return_book(self):
        """Обрабатывает возврат книги и обновляет базу данных."""
        book_id = self.aidd.get()
        student_id = self.astudentt.get()
        connection = sqlite3.connect('test.db')
        cursor = connection.execute("select ID from book_info where ID=?", (book_id.capitalize(),))
        book_check = cursor.fetchall()
        connection.commit()
        if book_check != None:
            cursor = connection.execute("select * from book_issued where BOOK_ID=? and STUDENT_ID=?", (book_id.capitalize(), student_id.capitalize(),))
            issued_records = cursor.fetchall()
            connection.commit()
            if len(issued_records) != 0:
                cursor.execute("DELETE FROM book_issued where BOOK_ID=? and STUDENT_ID=?", (book_id.capitalize(), student_id.capitalize(),))
                connection.commit()
                connection.execute("update book_info set COPIES=COPIES+1 where ID=?", (book_id.capitalize(),))
                connection.commit()
                messagebox.showinfo("Success", "Book Returned sucessfully.")
            else:
                messagebox.showinfo("Error", "Data not found.")
        else:
            messagebox.showinfo("Error", "No such book.\nPlease add the book in database.")
        connection.commit()
        connection.close()

    def activity(self):
        """Создает окно для просмотра активности студентов и выданных книг."""
        self.aidd = tk.StringVar()
        self.astudentt = tk.StringVar()
        self.f1 = tk.Frame(self.content_frame, height=550, width=500, bg='black')
        self.f1.place(x=500, y=80)
        self.list2 = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)
        label_search = tk.Label(self.f1, text='Book/Student ID : ', font='Papyrus 15 bold', fg='Orange', bg='black').place(x=50, y=30)
        entry_search = tk.Entry(self.f1, width=20, bd=4, bg='orange', textvariable=self.aidd).place(x=280, y=35)
        btn_back = tk.Button(self.f1, text='Back', bg='orange', font='Papyrus 10 bold', width=10, bd=3, command=self.go_back).place(x=340, y=450)
        btn_search = tk.Button(self.f1, text='Search', bg='orange', font='Papyrus 10 bold', width=10, bd=3, command=self.search_activity).place(x=40, y=450)
        btn_all = tk.Button(self.f1, text='All', bg='orange', font='Papyrus 10 bold', width=10, bd=3, command=self.search_all).place(x=190, y=450)
        self.f1.grid_propagate(0)

    def search_activity(self):
        """Выполняет поиск выданных книг по ID книги или студента."""
        self.list2 = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)
        connection = sqlite3.connect('test.db')
        bid = self.aidd.get()
        try:
            cursor = connection.execute("select * from book_issued where BOOK_ID=? or STUDENT_ID=?", (bid.capitalize(), bid.capitalize(),))
            results = cursor.fetchall()
            if len(results) != 0:
                for row in results:
                    self.trees.insert("", tk.END, values=row)
            else:
                messagebox.showinfo("Error", "Data not found.")
            connection.commit()
        except Exception as e:
            messagebox.showinfo(e)
        connection.close()

    def search_all(self):
        """Отображает все выданные книги в базе данных."""
        self.list2 = ("BOOK ID", "STUDENT ID", "ISSUE DATE", "RETURN DATE")
        self.trees = self.create_tree(self.f1, self.list2)
        self.trees.place(x=50, y=150)
        connection = sqlite3.connect('test.db')
        try:
            cursor = connection.execute("select * from book_issued")
            results = cursor.fetchall()
            for row in results:
                self.trees.insert("", tk.END, values=row)
            connection.commit()
        except Exception as e:
            messagebox.showinfo(e)
        connection.close()


def create_canvas(images, w, h):
    """Создает холст с фоновым изображением для окна входа."""
    photo = Image.open(images)
    photo1 = photo.resize((w, h), Image.ANTIALIAS)
    photo2 = ImageTk.PhotoImage(photo1)
    canvas = tk.Canvas(root, width='%d' % w, height='%d' % h)
    canvas.grid(row=0, column=0)
    canvas.grid_propagate(0)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo2)
    canvas.image = photo2
    return canvas


def init_database():
    """Инициализирует базу данных для входа и создает таблицу пользователей."""
    global conn, cursor
    conn = sqlite3.connect("python1.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `login` (mem_id INTEGER NOT NULL PRIMARY KEY  AUTOINCREMENT, username TEXT, password TEXT)")
    cursor.execute("SELECT * FROM `login` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `login` (username, password) VALUES('Prakarsha', 'root')")
        conn.commit()


def login_process(event=None):
    """Обрабатывает процесс входа пользователя в систему."""
    init_database()
    if username_var.get() == "" or password_var.get() == "":
        messagebox.showinfo("Error", "Please complete the required field!")
        lbl_text.config(text="Please complete the required field!", fg="red")
    else:
        cursor.execute("SELECT * FROM `login` WHERE `username` = ? AND `password` = ?", (username_var.get(), password_var.get()))
        if cursor.fetchone() is not None:
            root.destroy()
            a = Menu()
        else:
            messagebox.showinfo("Error", "Invalid username or password.")
            username_var.set("")
            password_var.set("")
    cursor.close()
    conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("LOGIN")
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    canvas = create_canvas(image3, w, h)
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    lbl_title = tk.Label(canvas, text="ADMIN   LOGIN", font=('Papyrus', 30, 'bold',), bg='black', fg='orange')
    lbl_title.place(x=500, y=100)
    lbl_username = tk.Label(canvas, text="Username:", font=('Papyrus', 15, 'bold'), bd=4, bg='black', fg='orange')
    lbl_username.place(x=500, y=230)
    lbl_password = tk.Label(canvas, text="Password :", font=('Papyrus', 15, 'bold'), bd=3, bg='black', fg='orange')
    lbl_password.place(x=500, y=330)
    lbl_text = tk.Label(canvas)
    lbl_text.place(x=450, y=500)
    lbl_text.grid_propagate(0)
    username = tk.Entry(canvas, textvariable=username_var, font=(14), bg='black', fg='orange', bd=6)
    username.place(x=650, y=230,)
    password = tk.Entry(canvas, textvariable=password_var, show="*", font=(14), bg='black', fg='orange', bd=6)
    password.place(x=650, y=330)
    btn_login = tk.Button(canvas, text="LOGIN", font=('Papyrus 15 bold'), width=25, command=login_process, bg='black', fg='orange')
    btn_login.place(x=500, y=400)
    btn_login.bind('<Return>', login_process)
    root.mainloop()