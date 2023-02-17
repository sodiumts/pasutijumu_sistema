import PySimpleGUI as sg
from layouts import admin_create_layout, login_layout, admin_panel_layout,order_layout,user_layout,update_order_layout,view_layout
import random
class GUIBuilder:
    def __init__(self,admin,db):
        sg.theme('DarkAmber')
        self.adminCreateLayout = admin_create_layout.adminCreateLayout.copy()
        self.loginLayout = login_layout.loginLayout.copy()
        self.userLayout = user_layout.generateUserLayout()
        self.orderLayout = order_layout.generateOrderLayout()
        self.updateOrderLayout = update_order_layout.generateOrderUpdateLayout()
        self.viewLayout = view_layout.generateviewLayout()
        self.db = db
        self.currentUser = None
        self.lastSelected = None
        self.fields = ["Name_Surname","Person_code","Username","Password","ACCESS_LEVEL"]
        # self.run_admin_panel()
        if not admin:
            self.run_admin_create()
        else:
            self.run_login()

    def run_login(self):
        window = sg.Window('Login', self.loginLayout)
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            if event == 'Submit':
                if(self.db.select("USERS", "Username", f"Username='{values[0]}' AND Password='{values[1]}'")):
                    acc = self.db.select("USERS","ACCESS_LEVEL",f"Username='{values[0]}'")
                    self.currentUser = values[0]
                    if acc[0][0] == 1:
                        if sg.popup_yes_no("Would You Like To Login Into Admin Panel?") == "Yes":
                            window.close()
                            self.run_admin_panel()
                            break
                        else:
                            window.close()
                            self.run_user_layout()
                            break
                    else:
                        window.close()
                        self.run_user_layout()
                    break
                else:
                    sg.popup("Login failed")
    

    def run_user_layout(self):
        window = sg.Window("User window",self.userLayout)
        once = True
        while True:
            if once:
                window.finalize()
                window["-USERNAME-"].update(value=f"Current User: {self.currentUser}")
                vals = self.db.cursor.execute("SELECT * FROM ORDERS").fetchall()


                window["-ORDERLIST-"].update(values=vals)
                window.refresh()
                once = False
            event, values = window.read()

            if event in (None,'Cancel'):
                break
            if event == "-ADDORDER-":
                self.run_order_layout()
                window["-USERNAME-"].update(value=f"Current User: {self.currentUser}")
                vals = self.db.cursor.execute("SELECT * FROM ORDERS").fetchall()

                window["-ORDERLIST-"].update(values=vals)
                window["-DELETE-"].update(disabled=True)
                window["-EDITORDER-"].update(disabled=True)
                window["-VIEW-"].update(disabled=True)
                self.orderLayout = order_layout.generateOrderLayout()


            if event == "-VIEW-":
                select = values["-ORDERLIST-"][0]
                listvals = window["-ORDERLIST-"].get()
                passInto = self.db.cursor.execute(f"SELECT * FROM ORDERS WHERE Order_ID='{listvals[select][0]}'").fetchall()
                passInto1 = self.db.cursor.execute(f"SELECT * FROM ORDER_DETAIL WHERE Order_ID='{listvals[select][0]}'").fetchall()
                self.run_view_layout(passInto[0],passInto1[0])
                self.viewLayout = view_layout.generateviewLayout()
            if event == "-SEARCH-":
                currentValue = str(values["-SEARCH-"]).lower()
                newTable = []
                if not currentValue == "":
                    for each in vals:
                        for i in each:
                            if currentValue in str(i).lower():
                                if not each in newTable:
                                    newTable.append(each)
                else:
                    newTable = vals
                window["-ORDERLIST-"].update(values=newTable)

            if event == "-EDITORDER-":
                select = values["-ORDERLIST-"][0]
                listvals = window["-ORDERLIST-"].get()
                passInto = self.db.cursor.execute(f"SELECT * FROM ORDERS WHERE Order_ID='{listvals[select][0]}'").fetchall()
                passInto1 = self.db.cursor.execute(f"SELECT * FROM ORDER_DETAIL WHERE Order_ID='{listvals[select][0]}'").fetchall()
                self.run_update_order(passInto[0],passInto1[0])
                vals = self.db.cursor.execute("SELECT * FROM ORDERS").fetchall()

                window["-ORDERLIST-"].update(values=vals)
                window["-DELETE-"].update(disabled=True)
                window["-EDITORDER-"].update(disabled=True)
                window["-VIEW-"].update(disabled=True)
                self.updateOrderLayout = update_order_layout.generateOrderUpdateLayout()


            if event == "-ORDERLIST-":
                if values["-ORDERLIST-"]:
                    window["-DELETE-"].update(disabled=False)
                    window["-EDITORDER-"].update(disabled=False)
                    window["-VIEW-"].update(disabled=False)

            if event == "-DELETE-":
                select = values["-ORDERLIST-"][0]
                listvals = window["-ORDERLIST-"].get()

                ans = sg.PopupYesNo("Are you sure you want to delete this order?")
                if ans == "Yes":
                    self.db.delete("ORDERS",f"Order_ID={listvals[select][0]}")
                    vals = self.db.cursor.execute("SELECT * FROM ORDERS").fetchall()
                    window["-ORDERLIST-"].update(values=vals)
                    window["-EDITORDER-"].update(disabled=True)
                    window["-DELETE-"].update(disabled=True)
                    window["-VIEW-"].update(disabled=True)



    def run_order_layout(self):
        window = sg.Window("Order Management",self.orderLayout)
        while True:

            
            event,values = window.read()


            if event in (None,"Cancel"):
                window.close()
                break
            if event == "-CREATE-":
                self.db.insert("ORDERS","Organizacija,Datums,Apmaksats,Order_Received,Apm_Datums,User_ID",f"'{values[0]}','{values[2]}','{values[1]}','{values[7]}','{values[3]}','{self.currentUser}'")
                a = self.db.cursor.execute(f"Select Order_ID from ORDERS where Organizacija = '{values[0]}' and Datums = '{values[2]}'").fetchall()[0][0]
                self.db.insert("ORDER_DETAIL","Order_ID,Order_Detail,Payment_Status,Order_Address",f"'{a}','{values[6]}','{values[6]}','{values[5]}'")
                # self.db.cursor.execute(f"INSERT INTO ORDER_DETAIL (Order_ID,Order_Detail,Payment_Status,Order_Address) VALUES ('{a}','{values[8]}','{values[6]}','{values[7]}')")
                sg.popup("Order Created")
                window.close()
                break

    def run_update_order(self,valuesForUpdating1,valuesForUpdating2):
        window = sg.Window("Edit Order",self.updateOrderLayout)
        while True:
            window.finalize()

            window["-ORG-"].update(value=valuesForUpdating1[1])
            window["-PASL-"].update(value=valuesForUpdating1[2])
            window["-APM-"].update(value=valuesForUpdating1[3])
            window["-ORDSTAT-"].update(value=valuesForUpdating1[4])
            window["-APMDAT-"].update(value=valuesForUpdating1[5])

            window["-ADR-"].update(value=valuesForUpdating2[2])
            window["-EDIENI-"].update(value=valuesForUpdating2[3])
            window["-PAYMSTAT-"].update(value=valuesForUpdating2[4])

            # window["-EDIENI-"].update(value=valuesForUpdating[7])
            # window["-PAYMSTAT-"].update(value=valuesForUpdating[8])

            window.refresh()

            event,values = window.read()
            if event in (None,"Cancel"):
                window.close()
                break
            if event == "-UPDATE-":

                vals = [values["-ORG-"],values["-PASL-"],values["-APM-"],values["-ORDSTAT-"],values["-APMDAT-"],values["-ADR-"],values["-EDIENI-"],values["-PAYMSTAT-"]]
                #             0                1               2                  3                  4                5                6                    7

                self.db.update("ORDERS",f"Organizacija='{vals[0]}',Datums='{vals[1]}',Apmaksats='{vals[2]}',Order_Received='{vals[3]}',Apm_Datums='{vals[4]}',User_ID='{self.currentUser}'",f"Order_ID={valuesForUpdating1[0]}")
                self.db.update("ORDER_DETAIL",f"Order_Detail='{vals[6]}',Payment_Status='{vals[7]}',Order_Address='{vals[5]}'",f"Order_ID='{valuesForUpdating1[0]}'")
                sg.popup("Order Updated")
                window.close()
                break
    def run_view_layout(self,valuesForUpdating1,valuesForUpdating2):
        window = sg.Window("Edit Order",self.viewLayout)
        while True:
            window.finalize()

            window["-ORG-"].update(value=valuesForUpdating1[1])
            window["-PASL-"].update(value=valuesForUpdating1[2])
            window["-APM-"].update(value=valuesForUpdating1[3])
            window["-ORDSTAT-"].update(value=valuesForUpdating1[4])
            window["-APMDAT-"].update(value=valuesForUpdating1[5])

            window["-ADR-"].update(value=valuesForUpdating2[2])
            window["-EDIENI-"].update(value=valuesForUpdating2[3])
            window["-PAYMSTAT-"].update(value=valuesForUpdating2[4])
            window.refresh()

            event,values = window.read()
            if event in (None,"-BACK-"):
                window.close()
                break



    def run_admin_create(self):
        window = sg.Window('Create Admin Account', self.adminCreateLayout)
        while True:
            event, values = window.read()
            if event in (None, 'Cancel'):
                break
            if event == 'Submit':                
                self.db.insert("USERS", "Name_Surname,Person_code,Username,Password,ACCESS_LEVEL", f"'{values[0]}','{values[1]}','{values[2]}','{values[3]}',1")
                sg.popup("Admin Account Created, Please Log In")
                window.close()
                self.run_login()
                break
            
    def run_admin_panel(self):
        window = sg.Window('Admin Panel', admin_panel_layout.admin_panel_layout)
        once = True
        while True:
            if once:
                window.finalize()
                window["-USERTEXT-"].update(value=f"Current User: {self.currentUser}")
                window["-DELETE-"].update(disabled=True)
                window["-CREATE-"].update(disabled=True)
                window["-UPDATE-"].update(disabled=True)
                vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM USERS")]

                userList = []
                userList.append("Create New User")
                for i in vals:
                    userList.append(self.db.select("USERS","Username",f"User_ID is {i}")[0][0])
                window["-USERLIST-"].update(values=userList)

                
                window.refresh()
                once = False
                
            event, values = window.read()
            
            
            if event in (None, 'Cancel'):
                break


            if event == "-CREATE-":

                if values["_LevelBox_"] == "Admin":
                    access_level = 1
                else:
                    access_level = 0
                
                vals = [values["_NameBox_"],values["_PersonalBox_"]
                ,values["_UsernameBox_"],values["_PasswordBox_"],access_level]
                if(self.db.select("USERS","Username",f"Username='{vals[2]}'")):
                    sg.Popup("Username Already Exists In The Database")
                else:
                    self.db.insert(f"USERS", "Name_Surname,Person_code,Username,Password,ACCESS_LEVEL", f"'{vals[0]}','{vals[1]}','{vals[2]}','{vals[3]}',{access_level}")
                    sg.Popup("User Added!")

                vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM USERS")]

                userList = []
                userList.append("Create New User")
                for i in vals:
                    userList.append(self.db.select("USERS","Username",f"User_ID is {i}")[0][0])
                
                window["-USERLIST-"].update(values=userList)
                window["-CREATE-"].update(disabled=True)
                window["-UPDATE-"].update(disabled=True)


            if event == '-USERLIST-':
                if(values["-USERLIST-"][0]== "Create New User"):
                    window["-DELETE-"].update(disabled=True)
                    window["-CREATE-"].update(disabled=False)
                    window["-UPDATE-"].update(disabled=True)
                elif values["-USERLIST-"][0] == self.currentUser:
                    window["-DELETE-"].update(disabled=True)
                    window["-UPDATE-"].update(disabled=False)
                    vals = self.db.select("USERS","*",f"Username='{values['-USERLIST-'][0]}'")[0]
                    self.lastSelected = vals[0]
                    window["_NameBox_"].update(value=vals[1])
                    window["_PersonalBox_"].update(value=vals[2])
                    window["_UsernameBox_"].update(value=vals[3])
                    window["_PasswordBox_"].update(value=vals[4])
                    if(vals[5] == 1):
                        window["_LevelBox_"].update(value='Admin')
                    else:
                        window["_LevelBox_"].update(value='User')

                else:
                    
                    window["-DELETE-"].update(disabled=False)
                    window["-CREATE-"].update(disabled=True)
                    window["-UPDATE-"].update(disabled=False)
                    vals = self.db.select("USERS","*",f"Username='{values['-USERLIST-'][0]}'")[0]
                    self.lastSelected = vals[0]
                    window["_NameBox_"].update(value=vals[1])
                    window["_PersonalBox_"].update(value=vals[2])
                    window["_UsernameBox_"].update(value=vals[3])
                    window["_PasswordBox_"].update(value=vals[4])
                    if(vals[5] == 1):
                        window["_LevelBox_"].update(value='Admin')
                    else:
                        window["_LevelBox_"].update(value='User')
                

            if event == "-DELETE-":

                delUser = values["-USERLIST-"][0]


                res = sg.PopupYesNo(f"ARE YOU SURE YOU WANT TO DELETE USER: {delUser} ?")

                if delUser !=None:
                    if res == "Yes":
                        self.db.delete("USERS",f"Username='{delUser}'")
                        sg.Popup(f"{delUser} Was Deleted.")
                        vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM USERS")]
                        userList = []
                        userList.append("Create New User")
                        for i in vals:
                            userList.append(self.db.select("USERS","Username",f"User_ID is {i}")[0][0])

                        window["-USERLIST-"].update(values=userList)
                        delUser = None
                        window["-UPDATE-"].update(disabled=True)
                        window["-DELETE-"].update(disabled=True)
                        # values["-USERLIST-"] = []
            if event == "-UPDATE-":

                if values["_LevelBox_"] == "Admin":
                    access_level = 1
                else:
                    access_level = 0

                vals = [values["_NameBox_"],values["_PersonalBox_"]
                ,values["_UsernameBox_"],values["_PasswordBox_"],access_level]

                self.db.update("USERS",f"Name_Surname='{vals[0]}',Person_code='{vals[1]}',Username='{vals[2]}',Password='{vals[3]}',ACCESS_LEVEL='{vals[4]}'",f"User_ID='{self.lastSelected}'")
                if(self.currentUser == values['-USERLIST-'][0]):
                    self.currentUser = vals[2]
                vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM USERS")]

                userList = []
                userList.append("Create New User")
                for i in vals:
                    userList.append(self.db.select("USERS","Username",f"User_ID is {i}")[0][0])
                
                window["-USERLIST-"].update(values=userList)
                window["-CREATE-"].update(disabled=True)
                window["-UPDATE-"].update(disabled=True)
                window["-DELETE-"].update(disabled=True)
                window["-USERTEXT-"].update(value=f"Current User: {self.currentUser}")
        window.close()