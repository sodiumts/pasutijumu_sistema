import PySimpleGUI as sg

user_list_column = [
    [sg.Text('User List')],
    [sg.Listbox(values=["Create New User"], size=(30, 6),enable_events=True, key='-USERLIST-')]]

user_atribute_column = [[sg.Text('User Atributes'),sg.Text(key="-USERTEXT-")],
                        [sg.Text('Name Surname', size=(15, 1)), sg.InputText(default_text="",do_not_clear=False,key="_NameBox_",),],
                        [sg.Text('Personal Code', size=(15, 1)), sg.InputText(do_not_clear=False,key="_PersonalBox_"),],
                        [sg.Text('Username', size=(15, 1)), sg.InputText(do_not_clear=False,key="_UsernameBox_"),],
                        [sg.Text('Password', size=(15, 1)), sg.InputText(do_not_clear=False,key="_PasswordBox_")],
                        [sg.Text("Access Level", size=(15, 1)), sg.Combo(["Admin", "User"], default_value="User", size=(10, 1),key="_LevelBox_")],
                        [sg.Button('Create',key="-CREATE-",disabled_button_color="gray",mouseover_colors="white"), sg.Button('Update',key="-UPDATE-",disabled_button_color="gray",mouseover_colors="white"), sg.Button('Delete',key="-DELETE-",disabled=True,disabled_button_color="gray",mouseover_colors="white"),sg.Cancel()]]
                         
admin_panel_layout = [[sg.Column(user_list_column), sg.VSeperator(), sg.Column(user_atribute_column)]]
