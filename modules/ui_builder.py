import PySimpleGUI as sg
from layouts import admin_create_layout, login_layout, admin_panel_layout,user_layout,order_layout

class GUIBuilder:
    def __init__(self,admin,db):
        sg.theme('DarkAmber')
        self.adminCreateLayout = admin_create_layout.adminCreateLayout
        self.loginLayout = login_layout.loginLayout
        self.userLayout = user_layout.userLayout
        self.orderLayout = order_layout.orderLayout
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
                    #if user is admin
                    # print(acc[0][0])
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
                    # self.run_admin_panel()
                    break
                else:
                    sg.popup("Login failed")
    

    def run_user_layout(self):
        window = sg.Window("User window",self.userLayout)
        once = True
        while True:
            if once:
                window.finalize()
                print(self.currentUser)
                window["-USERNAME-"].update(value=f"Current User: {self.currentUser}")
                vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM ORDERS")]
                print(vals)
                window.refresh()
                once = False
            event, values = window.read()

            if event in (None,'Cancel'):
                break
            if event == "-ADDORDER-":
                self.run_order_layout()
            



    def run_order_layout(self):
        window = sg.Window("Order Management",self.orderLayout)
        while True:

            
            event,values = window.read()


            if event in (None,"Cancel"):
                break
            if event == "-CREATE-":
                print(values)
                orderNR = 19
                pasutijuma_laiks = 2
                self.db.insert("ORDERS","Order_NR,Organizacija,Datums,Apmaksats,Order_Received,Apm_Datums,User_ID",f"'{orderNR}','{values[0]}','{values[2]}','{values[3]}','{values[4]}','{values[5]}','{self.currentUser}'")
                self.db.insert("ORDER_DETAIL","Order_ID,Order_Detail,Payment_Status,Order_Address",f"'{orderNR}','{values[8]}','{values[9]}','{values[7]}'")



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
                print(vals)
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
                print(values)
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
                print(vals)
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
                print(values)
                if values["_LevelBox_"] == "Admin":
                    access_level = 1
                else:
                    access_level = 0

                vals = [values["_NameBox_"],values["_PersonalBox_"]
                ,values["_UsernameBox_"],values["_PasswordBox_"],access_level]
                print(vals)
                self.db.update("USERS",f"Name_Surname='{vals[0]}',Person_code='{vals[1]}',Username='{vals[2]}',Password='{vals[3]}',ACCESS_LEVEL='{vals[4]}'",f"User_ID='{self.lastSelected}'")
                if(self.currentUser == values['-USERLIST-'][0]):
                    self.currentUser = vals[2]
                vals = [i[0] for i in self.db.cursor.execute("SELECT * FROM USERS")]
                print(vals)
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