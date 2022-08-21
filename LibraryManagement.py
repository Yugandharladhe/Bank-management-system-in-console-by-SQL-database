import sqlite3
import smtplib
import random
import datetime
from datetime import date
password="#Ladhe@Yug?"
def sent_email(email, m):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("yugandharladhe75@gmail.com",password)
    server.sendmail("yugandharladhe75@gmail.com", email, m)

def numofdays(date1,date2):
	return (date2-date1).days

def return_book():
    G=0
    email=None
    enr=input("Enter enrollemnt number: ")
    book_no=input("Enter book number: ")
    #check whether the user is valid or not
    con = sqlite3.connect("Central_Library.db")
    cur = con.cursor()
    query = "select Enrollment_No,Email from all_students where Enrollment_No='" + enr + "'"
    cur.execute(query)
    data = cur.fetchall()
    if len(data) == 0:
        print("\n\n***********invalid User************\n")
        return
    #get the email of user
    email = data[0][1]
    #check book number is valid or not
    cur = con.cursor()
    query = "select Book_No from all_issues where Enrollment_No='" + enr + "' and Return_Date='NULL'"
    cur.execute(query)
    data = cur.fetchall()
    i=0
    f=0
    while i<len(data):
        if data[i][0]==book_no:
            f=1
            break
        i+=1
    if f==0:
        print("********Invalid Book Number*********")
        return

    cur = con.cursor()
    query = "select Issue_Date from all_issues where Enrollment_No='" + enr + "' and Book_No='" + book_no + "' and Return_Date='NULL'"
    cur.execute(query)
    data = cur.fetchall()
    idate = data[0][0]
    tdate = datetime.date.today()
    idate=str(idate)
    tdate=str(tdate)
    id=idate.split("-")
    td=tdate.split("-")
    date1 = date(int(id[0]), int(id[1]), int(id[2]))
    date2 = date(int(td[0]), int(td[1]), int(td[2]))
    if numofdays(date1, date2) > 90:
        print("You got Fine of ", numofdays(date1, date2)-90, "Rupees")
        G = 1
    else:
        print(numofdays(date1, date2),"days")
        print("\n*****No fine*****\n")
    #updating all_students table for No_Of_Books and Fine
    query="update all_issues set Return_Date='"+str(datetime.date.today())+"' where Enrollment_No='"+enr+"' and Return_Date='NULL' and Book_No='"+book_no+"'"
    con.execute(query)
    con.commit()
    query="update all_students set No_Of_Books=No_Of_Books+"+"-1 where Enrollment_No='"+enr+"'"
    con.execute(query)
    con.commit()
    #sending email
    if G==1:
        query="update all_students set Fine=Fine+"+str(numofdays(date1, date2)-90)+" where Enrollment_No='"+enr+"'"
        con.execute(query)
        con.commit()
        sent_email(email, "You have returned an Item to the library.\nItem ID " + book_no + " \nFine:" + str(numofdays(date1, date2)-90))
        print("\n\nbook returned sucessfully")
    elif G==0:
        sent_email(email, "You have returned an Item to the library.\nItem ID "+book_no+" \nFine:0")
        print("\n\nbook returned sucessfully")
    cur.close()
    con.close()

def not_returned_book():
    enr = input("Enter Enrollment number of student: ")
    con=sqlite3.connect("Central_Library.db")
    cur = con.cursor()
    query = "select Enrollment_No from all_students where Enrollment_No='" + enr + "'"
    cur.execute(query)
    data = cur.fetchall()
    if len(data) == 0:
        print("\n\n***********invalid User************\n")
        return
    cur=con.cursor()
    query="select Book_No,Issue_Date,Return_date from all_issues where Enrollment_No='"+enr+"' and Return_Date='NULL'"
    cur.execute(query)
    data=cur.fetchall()
    print("book_number" + "\t\t" + "    issue_date" + "\t\t" + "Return_date")
    print("----------------------------------------------------------------")
    for i in data:
        print(i[0]+"\t\t"+"\t\t"+i[1]+"\t\t"+i[2])
        print("--------------------------------------------------")
    cur.close()
    con.close()

def search_student():
    enr = input("Enter Enrollment number of student: ")
    print()
    con=sqlite3.connect("Central_Library.db")
    cur = con.cursor()
    query = "select Enrollment_No from all_students where Enrollment_No='" + enr + "'"
    cur.execute(query)
    data = cur.fetchall()
    if len(data) == 0:
        print("\n\n***********invalid User************\n")
        return
    cur=con.cursor()
    query="select Book_No,Issue_Date,Due_Date,Return_Date from all_issues where Enrollment_No='"+enr+"'"
    cur.execute(query)
    data=cur.fetchall()
    print("book_number" + "\t\t" + "issue_date" + "\t\t" + "     due_date"+"\t\t\tReturn_date")
    print("--------------------------------------------------------------------------------")
    for i in data:
        print(i[0]+"\t\t\t"+i[1]+"\t\t\t"+i[2]+"\t\t\t"+i[3])
        print("------------------------------------------------------------------------------")
    cur.close()
    con.close()


ls = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def book_history():
    bh = input("Enter book ID for which you want to check history: ")
    con=sqlite3.connect("Central_Library.db")
    cur=con.cursor()
    query="select Book_No from all_books where Book_No='"+bh+"'"
    cur.execute(query)
    data=cur.fetchall()
    if len(data)==0:
        print("\nINVALID BOOK NUMBER\nNo such book present in Library\n")
        return
    else:
        cur=con.cursor()
        query="select Enrollment_No,Issue_Date,Due_Date from all_issues where Book_No='"+bh+"' and Return_Date='NULL'"
        cur.execute(query)
        data=cur.fetchall()
        print("Enrollment number\t\tIssue Date\t\tDue Date")
        print("-------------------------------------------------------------------")
        n=1
        for i in data:
            print(str(n)+")",i[0],"    \t\t",i[1],"   \t\t",i[2])
            print("----------------------------------------------------------------")
            n+=1
    cur.close()
    con.close()


def student_history():
    enr = input("Enter Enrollment number of student: ")
    con=sqlite3.connect("Central_Library.db")
    #if wrong detail submmited then
    cur=con.cursor()
    query="select Enrollment_No from all_students where Enrollment_No='"+enr+"'"
    cur.execute(query)
    data=cur.fetchall()
    if len(data)==0:
        print("\n\n***********invalid User************\n")
        return
    #If details are Correct then
    cur.execute(query)
    query="select Book_No,Issue_Date,Return_Date from all_issues where Enrollment_No='"+enr+"'"
    data=cur.execute(query)
    #printing data of student history
    print("Student History Is As Follows: \n")
    print("Book_id\t\tIssued_Date\t\tReturned_Date")
    print("------------------------------------------")
    for i in data:
        print(i[0]+"\t\t"+i[1]+"\t\t"+i[2])
        print("--------------------------------------------")
    cur.close()
    con.close()

def issue_book():
    bno = input("Enter book number: ")
    enr = input("enter enrollment of student: ")
    email = None
    con=sqlite3.connect("Central_Library.db")
    cur=con.cursor()
    query="select Book_No from all_issues where Return_Date='NULL'"
    cur.execute(query)
    data=cur.fetchall()
    #if taken book is repeatately issued
    for i in data:
        if bno==i[0]:
            print("\nSomething wents wrong \n")
            print("Book can't be issue to " + enr)
            return
    cur.close()
    con.close()
    #check if student have taken more than 5 book or not
    con=sqlite3.connect("Central_Library.db")
    cur=con.cursor()
    query="select No_Of_Books from all_students where Enrollment_No='"+enr+"'"
    cur.execute(query)
    data=cur.fetchall()
    if len(data)==0:
        print("Wrong details submitted")
        return
    No_Of_Books=data[0][0]
    if No_Of_Books==5:
        print("something wents wrong")
        print("you have taken 5 book already")
        return
    cur.close()
    con.close()
    #searching students email to issue book
    con=sqlite3.connect("Central_Library.db")
    message = "An item has been issued to you Item ID " + bno + "\nDue date:-" + str(datetime.date.today() + datetime.timedelta(days=90))
    d = str(datetime.date.today())
    query="select Email from all_students where Enrollment_No='"+enr+"'"
    cur = con.cursor()
    cur.execute(query)
    data=cur.fetchall()
    email=data[0][0]
    query="insert into all_issues values('"+enr+"','"+bno+"','"+str(datetime.date.today())+"','"+str(datetime.date.today() + datetime.timedelta(days=90))+"',"+"'NULL'"+")"
    con=sqlite3.connect("Central_Library.db")
    con.execute(query)
    con.commit()
    cur.close()
    con.close()
    #updating all student table for keeping records of numbers of books taken by student
    con=sqlite3.connect("Central_Library.db")
    query="update all_students set No_Of_Books="+str(No_Of_Books+1)+" where Enrollment_No='"+enr+"'"
    con.execute(query)
    con.commit()
    sent_email(email, message)
    print("book issued sucessfully........... ")
    cur.close()
    con.close()


def add_new_book():
    title = input("enter book title: ")
    author = input("Enter author name: ")
    pub = input("Enter publication of the book: ")
    book_no = "L"
    con=sqlite3.connect("Central_Library.db")
    LS = None

    #logic to give unique book number to the new book
    while 1:
        g = 0
        for i in range(6):
            book_no = book_no + random.choice(ls)
        query="select Book_No from all_books"
        cur=con.cursor()
        cur.execute(query)
        data=cur.fetchall()
        for i in data:
            if data[0]!=book_no:
                g=1
        if g == 1:
            break
    query="insert into all_books values('"+book_no+"','"+title+"','"+author+"','"+pub+"')"
    con.execute(query)
    con.commit()
    cur.close()
    con.close()
    print("Added new book number is ", book_no)
    print("NEW BOOK ADDED SUCESSFULLY.............")


def add_new_student():
    stud_enr = input("Enter student's enrollment: ")
    stud_nm = input("Enter name of student: ")
    stud_mob = input("Enter mobile number of student: ")
    stud_email = input("Enter email of student: ")
    con=sqlite3.connect("Central_Library.db")
    query="select Enrollment_No from all_students"
    cur=con.cursor()
    data=cur.execute(query)
    for i in data:
        if i[0]==stud_enr:
            print("student is already registered")
            return
    otp = random.choice(ls)
    for i in range(5):
        otp = otp + random.choice(ls)
    sent_email(stud_email, otp + " is your one time OTP for verification")
    print("Email sent to " + stud_email)
    chance=2
    while 1:
        OTP = input("\nEnter OTP Recieved on your E-mail: \n")
        if otp == OTP:
            break
        elif chance==0:
            print(" Limit Exceed\nRe-Enter all Detailed")
            return
        else:
            chance-=1
            print("\nWrong otp please enter correct otp\n")
            print("                                                             chances remain is ", chance)

    query="insert into all_students (Enrollment_No,Name,Mobile_No,Email) values("+"'"+stud_enr+"',"+"'"+stud_nm+"',"+stud_mob+","+"'"+stud_email+"')"
    con.execute(query)
    con.commit()
    sent_email(stud_email, stud_nm + " has registered sucessfully for library")
    print("NEW STUDENT DATA SAVED SUCESSFULLY.................\n")
    cur.close()
    con.close()


def search_book():
    b = input("Enter name of the book you want to search: ")
    con=sqlite3.connect("Central_Library.db")
    cur=con.cursor()
    query="select Name_Of_Book from all_books where Name_Of_Book='"+b+"'"
    cur.execute(query)
    data=cur.fetchall()
    if len(data)==0:
        print("no such found in library")
        return
    else:
        print(b + "\n********book is present in library*******")
    cur.close()
    con.close()


print("\n\n+++++++++++++++++++++++++LIBRARY MANAGEMENT APPLICATION++++++++++++++++++++++++++++++++")
while 1:
    print("\n\n1-issue book")
    print("2-return book")
    print("3-add new book")
    print("4-Register new student")
    print("5-book history")
    print("6-student history")
    print("7-search book")
    print("8-search student")
    print("9-Not returned books")
    print("0-Exit")
    print("Provide your choice")
    ch = int(input())
    if ch == 1:
        issue_book()
    elif ch == 2:
        return_book()
    elif ch == 3:
        add_new_book()
    elif ch == 4:
        add_new_student()
    elif ch == 5:
        book_history()
    elif ch == 6:
        student_history()
    elif ch == 7:
        search_book()
    elif ch == 8:
        search_student()
    elif ch == 9:
        not_returned_book()
    elif ch == 0:
        exit(0)
