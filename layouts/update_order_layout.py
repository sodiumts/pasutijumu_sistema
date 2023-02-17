import PySimpleGUI as sg
def generateOrderUpdateLayout():
    orderUpdateLayout = [
        [sg.Text("Organizacija",size=(15,1)),sg.InputText(size=(30,1),key="-ORG-")],
        [sg.Text("Apmaksats", size=(15,1)),sg.InputText(size=(30,1),key="-APM-")],
        [sg.Text("Pasutijuma Laiks", size=(15,1)),sg.InputText(size=(30,1),key="-PASL-")],
        [sg.Text("Apmaksas Datums", size=(15,1)),sg.InputText(size=(30,1),key="-APMDAT-")],
        [sg.Text("Payment Status", size=(15,1)),sg.InputText(size=(30,1),key="-PAYMSTAT-")],
        [sg.Text("Adrese",size=(15,1)),sg.InputText(size=(30,1),key="-ADR-")],
        [sg.Text("Pasūtītie Ēdieni",size=(15,1)),sg.InputText(size=(30,1),key="-EDIENI-")],
        [sg.Text("Order Status", size=(15,1)),sg.InputText(size=(30,1),key="-ORDSTAT-")],
        [sg.Button("Update",key="-UPDATE-"),sg.Button("Cancel")]
    ]
    return orderUpdateLayout
    