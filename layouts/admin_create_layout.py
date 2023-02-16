import PySimpleGUI as sg

adminCreateLayout = [  [sg.Text('Please enter the credentials for the admin account')],
            [sg.Text('Full Name', size=(15, 1)), sg.InputText()],
            [sg.Text('Personal Code', size=(15, 1)), sg.InputText()],
            [sg.Text('Username', size=(15, 1)), sg.InputText()],
            [sg.Text('Password', size=(15, 1)), sg.InputText(password_char='*')],
            [sg.Submit(), sg.Cancel()] ]