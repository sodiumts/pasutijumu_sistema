import PySimpleGUI as sg

orderLayout = [
    [sg.Text("Organizacija",size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Vārds Uzvārds",size=(15,1),),sg.InputText(size=(30,1))],
    [sg.Text("Pasūtījuma Laiks", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Apmaksats", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Saņemts", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Apmaksas Datums", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Payment Status", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Adrese",size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Pasūtītie Ēdieni",size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Text("Order Status", size=(15,1)),sg.InputText(size=(30,1))],
    [sg.Button("Create",key="-CREATE-"),sg.Button("Update"),sg.Button("Delete"),sg.Button("Cancel")]
]