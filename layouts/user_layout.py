import PySimpleGUI as sg
def generateUserLayout():
    font = ("Arial",20)
    orderFilter = [
        [sg.Text("Search",size=(15,1),font=font)],
        [sg.InputText(size=(30,1),key="-SEARCH-",enable_events=True)],
    ]

    layoutButtons = [
        [sg.Button("Add Order",key="-ADDORDER-"),sg.Button("View Details",key="-VIEW-",disabled_button_color="gray",mouseover_colors="white",disabled=True),sg.Button("Edit Order",key="-EDITORDER-",disabled=True,disabled_button_color="gray",mouseover_colors="white"),sg.Button("Delete",key="-DELETE-",disabled_button_color="gray",mouseover_colors="white",disabled=True),sg.Button("Cancel")]
    ]
    userLayout = [
        [sg.Text("Pasūtījumu ieraksts")],
        [sg.Text(key="-USERNAME-")],
        [sg.Table(size=(90,6),values=[],key="-ORDERLIST-",headings=("Order_NR","Organizācija","Datums","Apmaksats","Order Received","Apmaksas Datums","Last Eddited By"),enable_events=True,justification="left")],
        [sg.Column(orderFilter),sg.VSeparator(),sg.Column(layoutButtons)]
    ]
    return userLayout