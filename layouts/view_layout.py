import PySimpleGUI as sg
def generateviewLayout():
    viewLayout = [
        [sg.Text("Organizacija",size=(15,1)),sg.InputText(size=(30,1),key="-ORG-",disabled=True)],
        [sg.Text("Apmaksats", size=(15,1)),sg.InputText(size=(30,1),key="-APM-",disabled=True)],
        [sg.Text("Pasutijuma Laiks", size=(15,1)),sg.InputText(size=(30,1),key="-PASL-",disabled=True)],
        [sg.Text("Apmaksas Datums", size=(15,1)),sg.InputText(size=(30,1),key="-APMDAT-",disabled=True)],
        [sg.Text("Payment Status", size=(15,1)),sg.InputText(size=(30,1),key="-PAYMSTAT-",disabled=True)],
        [sg.Text("Adrese",size=(15,1)),sg.InputText(size=(30,1),key="-ADR-",disabled=True)],
        [sg.Text("Pasūtītie Ēdieni",size=(15,1)),sg.InputText(size=(30,1),key="-EDIENI-",disabled=True)],
        [sg.Text("Order Status", size=(15,1)),sg.InputText(size=(30,1),key="-ORDSTAT-",disabled=True)],
        [sg.Button("Back",key="-BACK-")]
    ]
    return viewLayout
    