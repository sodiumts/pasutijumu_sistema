import PySimpleGUI as sg

loginLayout = [  
    [sg.Text('Please enter your User Name and Password')],
    [sg.Text('User Name', size=(15, 1)), sg.InputText(do_not_clear=False),],
    [sg.Text('Password', size=(15, 1)), sg.InputText(password_char='*',do_not_clear=False)],
    [sg.Submit(), sg.Cancel()] 
]
