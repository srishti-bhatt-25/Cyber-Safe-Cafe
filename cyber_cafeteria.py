import mysql.connector as sqltor
from tabulate import tabulate
import random

def system():
    while True:
        print("+----------------------------CYBER CAFE MANAGEMENT SYSTEM----------------------------------+")
        print("| 1. Manage customers                                                                      |")
        print("| 2. Manage computers                                                                      |")
        print("| 3. Charge                                                                                |")
        print("| 4. Change password                                                                       |")
        print("| 5. Exit                                                                                  |")
        print("+------------------------------------------------------------------------------------------+")
        option = input("Enter your choice(1-5)::")
        if option == "1":
            while True:
                print("========================================")
                print("|| 1. View customer records           ||")
                print("|| 2. View LIVE customers             ||")
                print("|| 3. Add a customer record           ||")
                print("|| 4. Remove a customer record        ||")
                print("|| 5. Edit a customer record          ||")
                print("|| 6. Search a customer record.       ||")
                print("|| 7. Return to the main menu         ||")
                print("========================================")
                choice = input("Enter your choice(1-7)::")
                cursor.execute("DELETE FROM CustomersLIVE WHERE (End_Time < curtime() OR Date<curdate())")
                mycon.commit()
                if choice == "1":
                    cursor.execute("SELECT * FROM Customers ORDER BY Date,Start_Time")
                    data = cursor.fetchall()
                    if not data:
                        print("No records available.")
                    else:
                        header = ["Cust_ID","Name","Cubicle_No","Date","Start_Time","End_Time","BILL(in rupees)"]
                        print(tabulate(data, header, tablefmt = "psql"))
                elif choice == "2":
                    cursor.execute("SELECT * FROM CustomersLIVE ORDER BY Start_Time")
                    data = cursor.fetchall()
                    if not data:
                        print("No user is present at the cafe as of now...")
                    else:
                        header = ["Cust_ID", "Name", "Cubicle_No", "Date", "Start_Time", "End_Time"]
                        print(tabulate(data, header, tablefmt="psql"))
                elif choice == "3":
                    try:
                        cursor.execute("SELECT Cubicle_No from Computers")
                        data = cursor.fetchall()
                        if not data:
                            print("All the cubicles are empty...")
                            break
                        cursor.execute("select Cust_ID from Customers")
                        data = cursor.fetchall()
                        cust_id = random.randint(100, 9999)
                        while (cust_id,) in data:
                            cust_id = random.randint(100, 9999)
                        cursor.execute("SELECT Cubicle_No  FROM Computers WHERE Status='Working' OR 'working'")
                        working = cursor.fetchall()
                        cursor.execute("SELECT Cubicle_No FROM CustomersLIVE")
                        occupied_cubicle = cursor.fetchall()
                        cubicle = -1
                        for a in working:
                            if a in working and a not in occupied_cubicle:
                                for b in a:
                                    cubicle = b
                                break
                        if cubicle == -1:
                            print("No cubicle is vacant...")
                            break
                        name = input("Enter name of the customer::")
                        start = input("Enter the start time(HH:MM)::")
                        end = input("Enter the end time(HH:MM)::")
                        cursor.execute("INSERT INTO CustomersLIVE(Cust_ID, Name, Cubicle_No,Start_Time,End_Time)"
                                       " VALUES({},'{}',{},'{}','{}')".format(cust_id, name, cubicle, start, end))
                        cursor.execute("INSERT INTO Customers(Cust_ID,Name,Cubicle_No,Start_Time,End_Time)"
                                       " VALUES({},'{}',{},'{}','{}')".format(cust_id, name, cubicle,start, end))
                        cursor.execute("UPDATE Customers SET BILL = (TIME_TO_SEC(End_Time)-TIME_TO_SEC(Start_Time))/60 * {}"
                                       "2, Date=curdate() WHERE Cust_ID={}".format(float(charge_pass[1][1]),cust_id))
                        cursor.execute("UPDATE CustomersLIVE SET Date=curdate() WHERE Cust_ID={}".format(cust_id))
                        mycon.commit()
                        print("Record added successfully.")
                    except:
                        print("Incorrect input...")
                elif choice == "4":
                    cursor.execute("SELECT * FROM Customers")
                    data = cursor.fetchall()
                    if not data:
                        print("No records available to remove.")
                    else:
                        cursor.execute("SELECT Cust_ID from Customers")
                        data = cursor.fetchall()
                        remove_cust = int(input("Enter the customer ID::"))
                        while (remove_cust,) not in data:
                            remove_cust = int(input("Customer ID not found...Please try again::"))
                        cursor.execute("DELETE FROM Customers WHERE Cust_ID ={}".format(remove_cust,))
                        mycon.commit()
                        print("Customer's record removed successfully...")
                elif choice == "5":
                    cursor.execute("SELECT Cust_ID from Customers")
                    data = cursor.fetchall()
                    if not data:
                        print("No records available to edit...")
                    else:
                        cust_id = int(input("Enter customer's ID::"))
                        cursor.execute("SELECT Cust_ID FROM Customers")
                        data = cursor.fetchall()
                        while (cust_id,) not in data:
                            cust_id = int(input("Customer ID not present. Please try again::"))
                        while True:
                            print("============================================================")
                            print("|| 1. Edit customer's name                                ||")
                            print("|| 2. Edit customer's start time                          ||")
                            print("|| 3. Edit customer's end time                            ||")
                            print("|| 4. Return to the customers menu                        ||")
                            print("============================================================")
                            choice = input("Enter your choice(1-4)::")
                            if choice == "1":
                                cust_name = input("Enter customer's name::")
                                cursor.execute(
                                    "UPDATE Customers SET Name ='{}' WHERE Cust_ID = {}".format(cust_name, cust_id))
                                mycon.commit()
                                print("Customer's name changed successfully...")
                            elif choice == "2":
                                start = input("Enter start time(HH:MM)::")
                                cursor.execute("UPDATE Customers SET Start_Time ='{}' WHERE Cust_ID={}".format(start, cust_id))
                                cursor.execute(
                                    "UPDATE Customers SET BILL = (TIME_TO_SEC(End_Time)-TIME_TO_SEC(Start_Time))/60 * {}".format(float(charge_pass[1][1])))
                                cursor.execute("SELECT * FROM CustomersLIVE WHERE Cust_ID={}".format(cust_id))
                                if not cursor.fetchone():
                                    cursor.execute("INSERT IGNORE INTO CustomersLIVE SELECT Cust_ID,Name,Cubicle_No,Date,"
                                               "Start_Time,End_Time FROM Customers WHERE Cust_ID={}".format(cust_id))
                                else:
                                    cursor.execute(("UPDATE IGNORE CustomersLIVE SET Start_Time='{}' WHERE Cust_ID={}".format(start,cust_id)))
                                mycon.commit()
                                print("Customer's start time changed successfully...")
                            elif choice == "3":
                                end = input("Enter end time(HH:MM)::")
                                cursor.execute("UPDATE Customers SET End_Time='{}' WHERE Cust_ID={}".format(end, cust_id))
                                cursor.execute(
                                    "UPDATE Customers SET BILL = (TIME_TO_SEC(End_Time)-TIME_TO_SEC(Start_Time))/60 * {}".format(float(charge_pass[1][1])))
                                cursor.execute("SELECT * FROM CustomersLIVE WHERE Cust_ID={}".format(cust_id))
                                if not cursor.fetchone():
                                    cursor.execute("INSERT IGNORE INTO CustomersLIVE SELECT Cust_ID,Name,Cubicle_No,Date,"
                                               "Start_Time,End_Time FROM Customers WHERE Cust_ID={}".format(cust_id))
                                else:
                                    cursor.execute(("UPDATE IGNORE CustomersLIVE SET End_Time='{}' WHERE Cust_ID={}".format(end,cust_id)))
                                mycon.commit()
                                print("Customer's end time changed successfully...")
                            elif choice == "4":
                                break
                            else:
                                print("Invalid input.")
                elif choice == "6":
                    cust_id = int(input("Enter ID of the customer::"))
                    cursor.execute("SELECT * FROM Customers WHERE Cust_ID={}".format(cust_id))
                    data = cursor.fetchall()
                    if not data:
                        print("Customer ID not found...")
                    else:
                        header = ["Cust_ID", "Name", "Cubicle_No", "Date", "Start_Time", "End_Time", "BILL(in rupees)"]
                        print(tabulate(data, header, tablefmt="psql"))
                elif choice == "7":
                    break
                else:
                    print("Invalid input.")
        elif option == "2":
            while True:
                print("========================================")
                print("|| 1. View computer records           ||")
                print("|| 2. Add a computer record           ||")
                print("|| 3. Remove a computer record        ||")
                print("|| 4. Edit a computer record          ||")
                print("|| 5. Search a computer record        ||")
                print("|| 6. Return to the main menu         ||")
                print("========================================")
                choice = input("Enter your choice(1-6)::")
                if choice == "1":
                    cursor.execute("SELECT * FROM Computers")
                    data = cursor.fetchall()
                    if not data:
                        print("No records available.")
                    else:
                        header = ["Cubicle No", "Service Tag", "Model Name", "SPECS", "Installation Date", "Status"]
                        print(tabulate(data,header,tablefmt = "psql"))
                elif choice == "2":
                    try:
                        cubicle = int(input("Enter the allocated cubicle number::"))
                        cursor.execute("select Cubicle_No from Computers")
                        data = cursor.fetchall()
                        while (cubicle,) in data:
                            cubicle = int(input("This cubicle is already occupied...Please choose another one::"))
                        service = input("Enter service tag::")
                        model = input("Enter name of the model::")
                        date = input("Enter installation date(YYYY-MM-DD)::")
                        specs = input("Enter specifications of the computer(CPU/RAM/Storage)::")
                        cursor.execute("INSERT INTO Computers VALUES({},'{}','{}','{}','{}','{}')".format(cubicle, service, model, specs, date, "Working"))
                        mycon.commit()
                        print("Record added successfully...")
                    except:
                        print("Incorrect input..")
                elif choice == "3":
                    cursor.execute("SELECT * FROM Computers")
                    data = cursor.fetchall()
                    if not data:
                        print("No records available to remove.")
                    else:
                        remove_comp = int(input("Enter the cubicle number from where the computer is to be removed::"))
                        cursor.execute("SELECT Cubicle_No from Computers")
                        data = cursor.fetchall()
                        while (remove_comp,) not in data:
                            remove_comp = int(input("Cubicle number not found...Please try again::"))
                        cursor.execute("DELETE FROM Computers WHERE Cubicle_No ={}".format(remove_comp,))
                        mycon.commit()
                        print("Record removed successfully...")
                elif choice == "4":
                    cursor.execute("SELECT * FROM Computers")
                    data = cursor.fetchall()
                    if not data:
                        print("No computer records available to edit...")
                    else:
                        cubicle_ = int(input("Enter cubicle number of the computer to be edited::"))
                        cursor.execute("select Cubicle_No from Computers")
                        data = cursor.fetchall()
                        while (cubicle_,) not in data:
                            cubicle_ = int(input("Cubicle number not found...Please try again::"))
                        while True:
                            print("============================================")
                            print("|1. Edit computer's cubicle number         |")
                            print("|2. Edit computer's service tag            |")
                            print("|3. Edit computer's model name             |")
                            print("|4. Edit computer's specification          |")
                            print("|5. Edit computer's installation date      |")
                            print("|6. Edit computer's status                 |")
                            print("|7. Return to the computers menu           |")
                            print("============================================")
                            choice = input("Enter your choice(1-7)::")
                            if choice == "1":
                                cubicle = int(input("Enter the new cubicle number::"))
                                while (cubicle,) in data:
                                    cubicle = int(input("This cubicle is not vacant...Please choose a different one::"))
                                cursor.execute("UPDATE Computers SET Cubicle_No = {} WHERE Cubicle_No={}".format(cubicle,cubicle_))
                                mycon.commit()
                                cubicle_ = cubicle
                                cursor.execute("select Cubicle_No from Computers")
                                data = cursor.fetchall()
                            elif choice == "2":
                                service = input("Enter the service tag::")
                                cursor.execute("UPDATE Computers SET Service_Tag ='{}' WHERE Cubicle_No={}".format(service,cubicle_))
                                mycon.commit()
                            elif choice == "3":
                                model = input("Enter the model name::")
                                cursor.execute("UPDATE Computers SET Model_name ='{}' WHERE Cubicle_No={}".format(model,cubicle_))
                                mycon.commit()
                            elif choice == "4":
                                specs = input("Enter the computer's new specifications::")
                                cursor.execute("UPDATE Computers SET SPECS ='{}' WHERE Cubicle_No={}".format(specs,cubicle_))
                                mycon.commit()
                            elif choice == "5":
                                date = input("Enter the date of installation(YYYY-MM-DD)::")
                                cursor.execute("UPDATE Computers SET Installation_Date='{}' WHERE Cubicle_No={}".format(date,cubicle_))
                                mycon.commit()
                            elif choice == "6":
                                status = input("Enter status of the computer::")
                                cursor.execute("UPDATE Computers SET Status='{}' WHERE Cubicle_No={}".format(status, cubicle_))
                                mycon.commit()
                            elif choice == "7":
                                break
                            else:
                                print("Invalid input.")
                elif choice == "5":
                    cubicle = int(input("Enter the computer's cubicle number::"))
                    cursor.execute("SELECT * from Computers WHERE Cubicle_No={}".format(cubicle))
                    data = cursor.fetchall()
                    if not data:
                        print("No computer with this cubicle number is found.")
                    else:
                        header = ["Cubicle No.","Service Tag","Model Name","SPECS","Installation Date","Status"]
                        print(tabulate(data,header,tablefmt="psql"))
                elif choice == "6":
                    break
                else:
                    print("Invalid input.")
        elif option == "3":
            cursor.execute("SELECT * FROM ChargePass WHERE key1='Rate'")
            for a in cursor.fetchall():
                print("The charge per minute is Rs.", a[1]," .Do you want to change it?(y/n)::",sep="")
                charge = input()
                if charge == "y":
                    r = input("Enter the new charge per minute::")
                    cursor.execute("UPDATE ChargePass SET value1='{}' WHERE value1='{}'".format(r, a[1]))
                    mycon.commit()
                    print("Charge changed successfully...")
                    break
                else:
                    break
        elif option == "4":
            old = input("Enter the old password::")
            if old == password:
                new = input("Enter the new password::")
                cursor.execute("UPDATE ChargePass SET value1 = '{}' WHERE value1='{}'".format(new, old))
                mycon.commit()
                print("Password changed successfully...")
            else:
                print("Wrong password entered.")
        elif option == "5":
            print("*------------------------------------SUCCESSFULLY LOGGED "
                  "OUT------------------------------------------*")
            break
        else:
            print("Invalid input...")


mycon = sqltor.connect(host="localhost", username="root", passwd="Kusum2005!")
if mycon.is_connected():
    print("Successfully connected to MYSQL...")
cursor = mycon.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS cyber_cafe")
cursor.execute("USE cyber_cafe")
cursor.execute("CREATE TABLE IF NOT EXISTS Computers(Cubicle_No int(4) NOT NULL PRIMARY KEY,Service_Tag varchar(30) NOT"
               " NULL , Model_name varchar(50),SPECS varchar(100), Installation_Date DATE, Status varchar(10))")
cursor.execute("CREATE TABLE IF NOT EXISTS Customers(Cust_ID int NOT NULL PRIMARY KEY,Name varchar(30) ,Cubicle_No int("
               "4) NOT NULL , Date DATE, Start_Time TIME, End_Time TIME, BILL DECIMAL)")
cursor.execute("CREATE TABLE IF NOT EXISTS CustomersLIVE(Cust_ID int NOT NULL PRIMARY KEY,Name varchar(30) ,"
               "Cubicle_No BIGINT NOT NULL , Date DATE , Start_Time TIME, End_Time TIME)")
cursor.execute("CREATE TABLE IF NOT EXISTS ChargePass(key1 varchar(10), value1 varchar(30))")
cursor.execute("SELECT * FROM ChargePass")
charge_pass = cursor.fetchall()

while True:
    if not charge_pass:
        password = input("Create password::")
        cursor.execute("INSERT INTO ChargePass VALUES('{}','{}')".format("Password", password))
        charge_ = input("Set the charge per minute(in rupees)::")
        cursor.execute("INSERT INTO ChargePass VALUES('{}','{}')".format("Rate",charge_))
        mycon.commit()
        system()
        break
    else:
        password = input("Enter password::")
        if password == charge_pass[0][1]:
            system()
            break
        else:
            z = input("Wrong password entered...Enter t to try again or e to exit...")
            if z.lower() == "e":
                break
