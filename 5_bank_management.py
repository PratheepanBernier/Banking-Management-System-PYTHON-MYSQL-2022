import mysql.connector
from datetime import datetime,date

class manager:
    def login(self,type,id,password):
        self.type,self.id,self.password = type,id,password
        try:
            d=0
            if self.type=="manager" or self.type=="clerk":
                mydb = mysql.connector.connect(
                host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
                mycursor = mydb.cursor()
                mycursor.execute("SELECT employee_id, designation, password FROM employee_details")
                myresult = mycursor.fetchall()
                for x in myresult:
                    if x[0]==self.id and x[1]==self.type and x[2]==self.password:
                        d=1
            else:
                mydb = mysql.connector.connect(
                host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
                mycursor = mydb.cursor()
                mycursor.execute("SELECT cif_id, password FROM user_details")
                myresult = mycursor.fetchall()
                for x in myresult:
                    if x[0]==self.id and x[1]==self.password:
                        d=1
        except:
            print("\nInvalid credentials ! \n***")
            return 0
        if d==1:
            return 1
        else:
            print("\nInvalid credentials ! \n***")
            return 0

    def view_transaction_details(self,type):
        self.type = type
        d=0
        if self.type=="clerk":
            emplo_id=int(input("Enter Employee ID of the Clerk: "))
            mydb=mysql.connector.connect(
            host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql="SELECT emp.employee_id , emp.name, emp.email_id, tr.cif_id, tr.account_no,tr.transaction_id, tr.debit,tr.credit,tr.date_and_time,tr.balance FROM employee_details emp JOIN transaction_details tr ON emp.employee_id=tr.employee_id WHERE tr.employee_id=%s  ORDER BY date_and_time DESC"
            val=(emplo_id,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            for x in myresult:
                if d==0:
                    print("Employee ID:",x[0],"\nName:",x[1],"\nEmail ID:",x[2])
                dt_time=x[8].strftime("%m/%d/%Y, %H:%M:%S")
                print("\nTransaction ID:",x[5],"Transaction Date,Time:",dt_time,"User CIF ID:",x[3],"User Account no.:",x[4],"Debit:Rs.",x[6],"Credit:Rs.",x[7],"\nBalance:Rs.",x[9],"\n***")
                d=1

        if self.type=="date":
            start_date=input("Enter Start Date(mm/dd/yyyy): ")
            end_date=input("Enter End Date(mm/dd/yyyy): ")
            start_=datetime.strptime(start_date,'%m/%d/%Y')
            end_=datetime.strptime(end_date,'%m/%d/%Y')
            mydb=mysql.connector.connect(
            host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql="SELECT employee_id , remarks, cif_id, account_no,transaction_id, debit,credit,date_and_time,balance FROM transaction_details WHERE date BETWEEN %s AND %s ORDER BY date_and_time DESC"
            val=(start_.date(),end_.date(),)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            if myresult!=[]:
                for x in myresult:
                    dt_time=x[7].strftime("%m/%d/%Y, %H:%M:%S")
                    print("\nEmployee ID/User ID:",x[0],"\nTransaction ID:",x[4],"Transaction Date,Time:",dt_time,"User CIF ID:",x[3],"User Account no.:",x[3],"Debit:Rs.",x[5],"Credit:Rs.",x[6],"\nBalance:Rs.",x[8],"\nTransaction Done",x[1],"\n***")
                    d=1
            else:
                print("No Transactions done on those days! \n***")
                return False

        if d==1:
            return 1
        else:
            print("Invalid Input!!! \n***")
            return 0

    def view_account_statement(self,cif_id):
        self.cif_id = cif_id
        d=0
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        sql='SELECT transaction_id,date_and_time,debit,credit,remarks,balance FROM transaction_details WHERE cif_id=%s '
        cif_ = (self.cif_id,)
        mycursor.execute (sql,cif_)
        myresult = mycursor.fetchall()
        for x in range(len(myresult)-1,-1,-1):
            dt_time=myresult[x][1].strftime("%m/%d/%Y, %H:%M:%S")
            print("Transaction ID:",myresult[x][0],"\tDate/Time:",dt_time,"\tCredit:",myresult[x][2],"\tDebit:",myresult[x][3],"\nTransaction done",myresult[x][4],"\tBalance:",myresult[x][5])
            d=1
        if d==1:
            return 1
        else:
            print("Invalid Input! \n***")
            return 0

    def view_account_details(self,cif_id):
        self.cid_id = cif_id
        d=0
        mydb = mysql.connector.connect(
        host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        sql="SELECT us.account_no, us.name, us.email_id,tr.date_and_time,tr.balance,tr.remarks FROM user_details us JOIN transaction_details tr ON tr.cif_id=us.cif_id WHERE us.cif_id=%s  ORDER BY date_and_time DESC;"
        val=(self.cid_id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        for x in myresult:
            dt_time=x[3].strftime("%m/%d/%Y, %H:%M:%S")
            print("Account number:",x[0],"\nName:",x[1],"\nEmail ID:",x[2],"\nLast Transaction Date,Time:",dt_time,"\nCurrent Balance:Rs.",x[4],"\nLast Transaction Done",x[5],"\n***")
            d=1
            break
        if d==1:
            return 1
        else:
            print("Invalid Input! \n***")
            return 0
        

    def add_new_clerk(self,designation,email_id,password):
        self.designation,self.email_id,self.password = designation,email_id,password
        d=0
        try:
            mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql = "INSERT INTO employee_details (designation, email_id, password) VALUES (%s, %s, %s)"
            val = (self.designation,self.email_id,self.password)
            mycursor.execute(sql, val)
            mydb.commit()
            d=1
        except:
            print("\nInvalid Credentials! \n***")
            return 0
        if d==1:
            return 1
        else:
            print("Invalid Credentials!!! \n***")
            return 0
    

    def remove_existing_clerk(self,employee_id):
        self.employee_id = employee_id
        d=0
        try:
            mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql = "DELETE FROM employee_details WHERE employee_id=%s"
            val = (self.employee_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            d=1
        except:
            d=0
        if d==1:
            return 1
        else:
            print("\nInvalid Credential! \n***")
            return 0

    def update_my_details(self,type,employee_id,to_update,detail):
        self.type,self.employee_id,self.to_update,self.detail = type,employee_id,to_update,detail
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        d=0
        if self.to_update=="name":
            if self.type=="manager" or self.type=="clerk":
                try:
                    sql = "UPDATE employee_details SET name=%s WHERE employee_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
            else:
                try:
                    sql = "UPDATE user_details SET name=%s WHERE cif_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
        
        elif self.to_update=="email_id":
            if self.type=="manager" or self.type=="clerk":
                try:
                    sql = "UPDATE employee_details SET email_id=%s WHERE employee_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
            else:
                try:
                    sql = "UPDATE user_details SET email_id=%s WHERE cif_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
                
        else:
            if self.type=="manager" or self.type=="clerk":
                try:
                    sql = "UPDATE employee_details SET password=%s WHERE employee_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
            else:
                try:
                    sql = "UPDATE user_details SET password=%s WHERE cif_id=%s"
                    val = (self.detail,self.employee_id)
                    mycursor.execute(sql, val)
                    mydb.commit()
                    d=1
                except:
                    d=0
                    print("\nInvalid Credentials! \n***")
        if d==1:
            return 1
        else:
            return 0

    def update_my_password(self,type,employee_id,old_password,new_password):
        self.type,self.employee_id,self.old_password,self.new_password = type,employee_id,old_password,new_password
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        d=0
        if self.type=="manager" or self.type=="clerk":
            try:
                sql = "UPDATE employee_details SET password=%s WHERE employee_id=%s and password=%s"
                val = (self.new_password,self.employee_id,self.old_password)
                mycursor.execute(sql, val)
                mydb.commit()
                d=1
            except:
                d=0
                print("\nInvalid Credentials! \n***")
        else:
            try:
                sql = "UPDATE user_details SET password=%s WHERE cif_id=%s and password=%s"
                val = (self.new_password,self.employee_id,self.old_password)
                mycursor.execute(sql, val)
                mydb.commit()
                d=1
            except:
                d=0
                print("\nInvalid Credentials! \n***")
        if d==1:
            return 1
        else:
            return 0

class clerk(manager):
    def banking(self,emp_id,cif_id,account_no,type,amount):
        self.type,self.emp_id,self.cif_id,self.account_no,self.amount = type,emp_id,cif_id,account_no,amount
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        sql='SELECT balance FROM transaction_details WHERE cif_id=%s'
        cif_ = (self.cif_id,)
        mycursor.execute (sql,cif_)
        myresult = mycursor.fetchall()
        for x in myresult:
            temp=x[0]
        d=0
        if self.type=="debit":
            try:
                temp2=temp-self.amount
                if not temp2>=0:
                    print("Transaction declined due to insufficient balance! \n***")
                    return False
                sql = "INSERT INTO transaction_details (employee_id,cif_id,account_no,date,date_and_time,debit,credit,remarks,balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (self.emp_id,self.cif_id,self.account_no,date.today(),datetime.now(),self.amount,0,"by clerk",temp2)
                mycursor.execute(sql, val)
                mydb.commit()
                d=1
            except:
                d=0
                print("\nInvalid Credentials! \n***")
            
        else:
            try:
                sql = "INSERT INTO transaction_details (employee_id,cif_id,account_no,date,date_and_time,debit,credit,remarks,balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val = (self.emp_id,self.cif_id,self.account_no,date.today(),datetime.now(),0,self.amount,"by clerk",self.amount+temp)
                mycursor.execute(sql, val)
                mydb.commit()
                d=1
            except :
                d=0
                print("\nInvalid Credentials! \n***")
        if d==1:
            return 1
        else:
            return 0 

    def add_new_user(self,emp_id,account_no,name,email_id,password):
        self.emp_id,self.account_no,self.name,self.email_id,self.password = emp_id,account_no,name,email_id,password
        d=0
        try:
            mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql = "INSERT INTO user_details (account_no, name, email_id, password) VALUES (%s, %s, %s, %s)"
            val = (self.account_no,self.name,self.email_id,self.password)
            mycursor.execute(sql, val)
            mydb.commit()
            d=1
        except:
            d=0
            print("\nInvalid Credentials! \n***")
        if d==1:
            mydb = mysql.connector.connect(
            host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql= "SELECT cif_id FROM user_details WHERE account_no=%s"
            val=(self.account_no,)
            mycursor.execute(sql,val)
            myresult = mycursor.fetchall()
            cif_id=myresult[0][0]
            mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql = "INSERT INTO transaction_details (employee_id, cif_id, account_no, date, date_and_time,debit,credit,remarks,balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.emp_id,cif_id,self.account_no,date.today(),datetime.now(),0,500,"by clerk",500)
            mycursor.execute(sql, val)
            mydb.commit()
            print("Get Rs.500 from user as an initial deposit!!! \n***")
            return 1
        else:
            return 0

    def remove_existing_user(self,cif_id):
        self.cif_id = cif_id
        d=0
        try:
            mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
            mycursor = mydb.cursor()
            sql = "DELETE FROM user_details WHERE cif_id=%s"
            val = (self.cif_id,)
            mycursor.execute(sql, val)
            mydb.commit()
            d=1
        except:
            d=0
            print("\nInvalid Credentials! \n***")
        if d==1:
            return 1
        else:
            return 0

class user(clerk):
    def view_mini_statement(self,cif_id):
        self.cif_id = cif_id
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        sql='SELECT transaction_id,date_and_time,debit,credit,remarks,balance FROM transaction_details WHERE cif_id=%s LIMIT 5'
        cif_ = (self.cif_id,)
        mycursor.execute (sql,cif_)
        myresult = mycursor.fetchall()
        for x in range(len(myresult)-1,-1,-1):
            dt_time=myresult[x][1].strftime("%m/%d/%Y, %H:%M:%S")
            print("Transaction ID:",myresult[x][0],"\tDate/Time:",dt_time,"\tCredit:",myresult[x][2],"\tDebit:",myresult[x][3],"\nRemark:",myresult[x][4],"\tBalance:",myresult[x][5])
        return 1

    def view_balance(self,cif_id):
        self.cif_id=cif_id
        d=0
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        sql='SELECT balance FROM transaction_details WHERE cif_id=%s'
        cif_ = (self.cif_id,)
        mycursor.execute (sql,cif_)
        myresult = mycursor.fetchall()
        for x in myresult:
            temp=x[0]
            d=1
        if d==1:
            print("Your Balance is Rs.",temp)
            return 1
        else:
            return 0 

    def amount_transfer(self,cust_id_1,account_no_1,cust_id_2,account_no_2,amount):
        self.cust_id_1,self.account_no_1,self.cust_id_2,self.account_no_2,self.amount=cust_id_1,account_no_1,cust_id_2,account_no_2,amount
        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT cif_id,account_no FROM user_details")
        myresults=mycursor.fetchall()
        temp_0=0
        for x in myresults:
            if x[0]==self.cust_id_2 and x[1]==self.account_no_2:
                temp_0=1
        mycursor.execute("SELECT account_no FROM user_details")
        myresults=mycursor.fetchall()
        temp_1=0
        for x in myresults:
            if x[0]==self.account_no_1:
                temp_1=1
        if temp_0!=1 and temp_1!=1:
            print("Invalid Credentials")
            return False
        sql='SELECT balance FROM transaction_details WHERE cif_id=%s'
        cust_ = (self.cust_id_1,)
        mycursor.execute (sql,cust_)
        myresult = mycursor.fetchall()
        for x in myresult:
            temp=x[0]
        d=0
        try:
            temp2=temp-self.amount
            if not temp2>=0:
                print("Transaction declined due to insufficient balance! \n***")
                return False
            sql = "INSERT INTO transaction_details (employee_id,cif_id,account_no,date,date_and_time,debit,credit,remarks,balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.cust_id_1,self.cust_id_1,self.account_no_1,date.today(),datetime.now(),self.amount,0,"by self",temp2)
            mycursor.execute(sql, val)
            mydb.commit()
            d=1
            sql='SELECT balance FROM transaction_details WHERE cif_id=%s'
            cust_ = (self.cust_id_2,)
            mycursor.execute (sql,cust_)
            myresult = mycursor.fetchall()
            for x in myresult:
                temp=x[0]
            sql = "INSERT INTO transaction_details (employee_id,cif_id,account_no,date,date_and_time,debit,credit,remarks,balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (self.cust_id_1,self.cust_id_2,self.account_no_2,date.today(),datetime.now(),0,self.amount,"by fund transfer",self.amount+temp)
            mycursor.execute(sql, val)
            mydb.commit()
        except :
                d=0
                print("\nInvalid Credentials! \n***")
        if d==1:
            return 1
        else:
            return 0

c=clerk()
m=manager()
u=user()
print("Bank Management System !!!")
loop_1=True
while loop_1==True:
    print("1.Manager \n2.Clerk/Cashier \n3.User \n4.Exit")
    loop_2 = input("Enter your choice : ")
    if loop_2=="1":
        print("***\nManager Login!!!")
        type="manager"
        emp_id=int(input("Enter Employee ID: "))
        password=input("Enter Password: ")
        if m.login(type,emp_id,password)==True:
            print("***\nWelcome Manager!!!")
            manager_loop=True
            while manager_loop==True:
                choice1=input("1.View Transaction Details \n2.View Account Statement \n3.View Account details \n4.Add New Clerk \n5.Remove Existing Clerk \n6.Update My Details \n7.Update My Password \n8.Logout \nEnter your choice: ")
                if choice1=="1":
                    type=""
                    choice_trans=input("1.View transactions based on Clerk \n2.View transactions based on date \nEnter your choice: ")
                    if choice_trans=="1":
                        type="clerk"
                    if choice_trans=="2":
                        type="date"
                    if m.view_transaction_details(type)==True:
                        print("Transaction viewed Successfully!!! \n***")
                    
                elif choice1=="2":
                    cif_id=int(input("Enter CIF ID of the User:"))
                    if m.view_account_statement(cif_id)==True:
                        print("Account Statement viewed Successfully!!! \n***")

                elif choice1=="3":
                    cif_id=int(input("Enter CIF ID of the user you wish to see details: "))
                    if m.view_account_details(cif_id)==True:
                        print("Details viewed Successfully!!! \n***")  

                elif choice1=="4":
                    designation="clerk"
                    print("***\nAdding new clerk...")
                    email_id=input("Enter email ID: ")
                    password=input("Enter Password:")
                    if m.add_new_clerk(designation,email_id,password)==True:
                        mydb = mysql.connector.connect(host="localhost",user="yourusername",password="yourpassword",database="bank_management_system")
                        mycursor = mydb.cursor()
                        sql='SELECT employee_id, password FROM employee_details WHERE email_id=%s'
                        email_ = (email_id,)
                        mycursor.execute (sql,email_)
                        myresult = mycursor.fetchall()
                        for x in myresult:
                            print("\nEmployee ID :",x[0],"\nPassword: ",x[1])
                            print("New Clerk Added Successfully!!! \n***")  

                elif choice1=="5":
                    emp_id=int(input("Enter Employee ID of the Clerk you want to remove: "))
                    if m.remove_existing_clerk(emp_id)==True:
                        print("Clerk Removed successfully")

                elif choice1=="6":
                    type="manager"
                    update_choice=input("1.Name \n2.Email ID \nEnter your choice: ")
                    if update_choice=="1":
                        to_update="name"
                        detail=input("Enter new name: ")
                        if m.update_my_details(type,emp_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    elif update_choice=="2":
                        to_update="email_id"
                        detail=input("Enter new Email ID: ")
                        if m.update_my_details(type,emp_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    else:
                        print("Invalid input! \n***")

                elif choice1=="7":
                    type="manager"
                    old_password=input("Enter your current password: ")
                    new_password=input("Enter your new password: ")
                    if m.update_my_password(type,emp_id,old_password,new_password)==True:
                        print("Updated Successfully!!! \n***")

                elif choice1=="8":
                    print("Logged Out Successfully!!! \n***")
                    manager_loop=False

                else:
                    print("Invalid Input!!! \n***")

        loop_1=True
    elif loop_2=="2":
        print("***\nClerk Login!!!")
        type="clerk"
        emp_id=int(input("Enter Employee ID: "))
        password=input("Enter Password: ")
        if c.login(type,emp_id,password)==True:
            print("***\nWelcome Clerk!!!")
            clerk_loop=True
            while clerk_loop==True:
                choice2=input("1.Banking(Deposit and Withdrawl) \n2.View Transaction Details \n3.View Account Statement \n4.View Account details \n5.Add New User \n6.Remove Existing User \n7.Update User Details \n8.Update My Details \n9.Update My Password \n10.Logout \nEnter your choice: ")
                if choice2=="1":
                    cif_id=int(input("Enter CIF ID of the user: "))
                    account_no=int(input("Enter Account number of the user: "))
                    type_choice=input("1.Withdrawl \n2.Deposit \nEnter your choice: ")
                    if type_choice=="1":
                        type="debit"
                    elif type_choice=="2":
                        type="deposit"
                    else:
                        print("Invalid type value! \n***")
                        break
                    amount=float(input("Enter the amount: "))
                    if c.banking(emp_id,cif_id,account_no,type,amount)==True:
                        print("Transaction Successfull!!! \n***")

                elif choice2=="2":
                    type="date"
                    if c.view_transaction_details(type)==True:
                        print("Transaction details viewed Successfully!!! \n***")

                elif choice2=="3":
                    cif_id=int(input("Enter CIF ID of the user:"))
                    if c.view_account_statement(cif_id)==True:
                        print("Account Statement viewed Successfully!!! \n***")

                elif choice2=="4":
                    cif_id=int(input("Enter CIF ID of the User:"))
                    if c.view_account_details(cif_id)==True:
                        print("Account Details viewed Successfully!!! \n***")

                elif choice2=="5":
                    account_no=int(input("Enter Account number: "))
                    name=input("Enter Name: ")
                    email_id=input("Enter Email ID: ")
                    password=input("Enter Password: ")
                    if c.add_new_user(emp_id,account_no,name,email_id,password)== True:
                        print("New User Added Successfully!!! \n***")
                elif choice2=="6":
                    cif_id=int(input("Enter CIF ID of the user you want to remove: "))
                    if c.remove_existing_user(cif_id)==True:
                        print("User Removed Successfully!!! \n***")
                elif choice2=="7":
                    cif_id=int(input("Enter CIF ID of the User you want to Update details: "))
                    type="user"
                    update_choice=input("1.Name \n2.Email ID \n3.Password \nEnter your choice: ")
                    if update_choice=="1":
                        to_update="name"
                        detail=input("Enter new name: ")
                        if c.update_my_details(type,cif_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    elif update_choice=="2":
                        to_update="email_id"
                        detail=input("Enter new Email ID: ")
                        if c.update_my_details(type,cif_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    elif update_choice=="3":
                        to_update="password"
                        detail=input("Enter new Password: ")
                        if c.update_my_details(type,cif_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    else:
                        print("Invalid input! \n***")
                
                elif choice2=="8":
                    type="clerk"
                    update_choice=input("1.Name \n2.Email ID \nEnter your choice: ")
                    if update_choice=="1":
                        to_update="name"
                        detail=input("Enter new name: ")
                        if c.update_my_details(type,emp_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    elif update_choice=="2":
                        to_update="email_id"
                        detail=input("Enter new Email ID: ")
                        if c.update_my_details(type,emp_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    else:
                        print("Invalid input! \n***")
                
                elif choice2=="9":
                    type="clerk"
                    old_password=input("Enter your current password: ")
                    new_password=input("Enter your new password: ")
                    if c.update_my_password(type,emp_id,old_password,new_password)==True:
                        print("Updated Successfully!!! \n***")
            
                elif choice2=="10":
                    print("Logged Out Successfully!!! \n***")
                    clerk_loop=False

                else:
                    print("Invalid Input!!! \n***")

        loop_1=True

    elif loop_2=="3":
        print("***\nUser Login!!!")
        type="User"
        cust_id=int(input("Enter Customer ID: "))
        password=input("Enter Password: ")
        if u.login(type,cust_id,password)==True:
            print("***\nWelcome User!!!")
            user_loop=True
            while user_loop==True:
                choice3=input("1.View Account Statement \n2.View Mini Statement \n3.View Balance \n4.Transfer of amount to other account \n5.View Account details \n6.Update My Details \n7.Update My Password \n8.Logout \nEnter your choice: ")
                if choice3=="1":
                    if m.view_account_statement(cust_id)==True:
                        print("Account Statement viewed Successfully!!! \n***")

                elif choice3=="2":
                    if u.view_mini_statement(cust_id)==True:
                        print("Mini Statement viewed Successfully!!! \n***")

                elif choice3=="3":
                    if u.view_balance(cust_id)==True:
                        print("Balance viewed Successfully!!! \n***")

                elif choice3=="4":
                    account_no_1=int(input("Enter your Account no.: "))
                    cust_id_2=int(input("Enter CIF ID of the benificiery: "))
                    account_no_2=int(input("Enter Account number of the benificiery: "))
                    amount=float(input("Enter the amount: "))
                    if u.amount_transfer(cust_id,account_no_1,cust_id_2,account_no_2,amount)==True:                       
                        print("Amount Transfered Successfully!!! \n***")

                elif choice3=="5":
                    if u.view_account_details(cust_id)==True:
                        print("Account Details Viewed Successfully!!! \n***")

                elif choice3=="6":
                    type="user"
                    update_choice=input("1.Name \n2.Email ID \nEnter your choice: ")
                    if update_choice=="1":
                        to_update="name"
                        detail=input("Enter new name: ")
                        if u.update_my_details(type,cust_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    elif update_choice=="2":
                        to_update="email_id"
                        detail=input("Enter new Email ID: ")
                        if u.update_my_details(type,cust_id,to_update,detail)==True:
                            print("Updated Successfully!!! \n***")
                    else:
                        print("Invalid input! \n***")
                
                elif choice3=="7":
                    type="user"
                    old_password=input("Enter your current password: ")
                    new_password=input("Enter your new password: ")
                    if c.update_my_password(type,cust_id,old_password,new_password)==True:
                        print("Updated Successfully!!! \n***")
            
                elif choice3=="8":
                    print("Logged Out Successfully!!! \n***")
                    user_loop=False

                else:
                    print("Invalid Input!!! \n***")

        loop_1=True

    elif loop_2=="4":
        print("Exited Successfully!!! \n***")
        loop_1=False
        exit()
    else:
        print("Invalid Input ! Enter numbers only from 1 to 4 ! \n***")
        loop_1=True