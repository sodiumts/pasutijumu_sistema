import PySimpleGUI as sg

font = ("Arial",20)
orderFilter = [
    [sg.Text("Filter Attributes",size=(15,1),font=font)],
    [sg.Text("Pasūtījuma Numurs",size=(15,1)),sg.InputText(size=(17,1))],
    [sg.Text("Pasutijuma ID",size=(15,1)),sg.InputText(size=(17,1))],
    [sg.Text("Klienta Adrese",size=(15,1)),sg.InputText(size=(17,1))],
    [sg.Text("Klienta Vārds",size=(15,1)),sg.InputText(size=(17,1))],
    [sg.Button("Find",size=(32,1))]
]

layoutButtons = [
    [sg.Button("Add Order",key="-ADDORDER-"),sg.Button("Edit Order"),sg.Button("Cancel")]
]
userLayout = [
    [sg.Text("Pasūtījumu ieraksts")],
    [sg.Text(key="-USERNAME-")],
    [sg.Table(size=(90,6),values=[],key="-ORDERLIST-",headings=("Order_NR","Organizācija","Datums","Apmaksats","Order Received","Apmaksas Datums","Assigned User"),enable_events=True)],
    [sg.Column(orderFilter),sg.VSeparator(),sg.Column(layoutButtons)]
]
