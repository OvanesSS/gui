import customtkinter as ctk
import tkinter as tk
from serial.tools import list_ports as tools

def test():
    print(combo_vars[1][1].get(), combo_vars[2][1].get(), combo_vars[3][1].get(), combo_vars[4][1].get(), combo_vars[5][1].get())

labels_parametrs = {1:'Port:', 2:'Speed:', 3:'Bits:', 4:'Stop bits:', 5:'Parity:'}
combo_values={1:[info.device for info in tools.comports()],
              2:['1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400'],
              3:['7', '8'],
              4:['1', '2'],
              5:['None', 'Even', 'Odd', 'Mark', 'Space']}
combo_vars = {}

def open_setfil():
    win_setfil = ctk.CTkToplevel(app)
    win_setfil.title('SETFIL')
    win_setfil.resizable(False, False)
    w = 300
    h = 170
    ws = app.winfo_screenwidth()
    hs = app.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    win_setfil.geometry(f'{w}x{h}+{int(x)}+{int(y)}')
    frame_setfil = ctk.CTkFrame(master=win_setfil)
    frame_setfil.pack(expand=True, fill='both',padx=5, pady=5)
    ctk.CTkLabel(master=frame_setfil, text = 'Average:').grid(row=0, column=0, sticky = 'w', padx=5)
    avrg = ctk.CTkEntry(master=frame_setfil, width=280).grid(row=1, column=0, sticky = 'nsew', padx=5)
    ctk.CTkLabel(master=frame_setfil, text='Coefficient:').grid(row=2, column=0, sticky='w', padx=5)
    coef = ctk.CTkEntry(master=frame_setfil, width=280).grid(row=3, column=0, sticky='nsew', padx=5)
    send = ctk.CTkButton(master=frame_setfil, text='Send', width=280).grid(row=4, column=0, sticky='nsew', padx=5, pady=[15,5])
    win_setfil.grab_set()
    win_setfil.focus()

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')
app = ctk.CTk()
app.title('Customtkinter')
app.resizable(False, False)
w = 650
h = 505
ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()
x = (ws/2)-(w/2)
y = (hs/2)-(h/2)
app.geometry(f'{w}x{h}+{int(x)}+{int(y)}')

for (key, value) in combo_values.items():
    combo_vars[key] = [value, tk.StringVar(value = value[0])]

frame_parametrs = ctk.CTkFrame(master=app)
frame_parametrs.grid(row=0, column = 0, pady=10, padx=10, sticky='ew')
ctk.CTkLabel(master=frame_parametrs, text = 'Parametrs').grid(row=0, column=0, columnspan = 2, ipady = 5)
for (key, value) in labels_parametrs.items():
    ctk.CTkLabel(master=frame_parametrs, text = value).grid(row=key, column=0, sticky = 'w', padx=10)

for (key, value) in combo_vars.items():
    ctk.CTkComboBox(master=frame_parametrs, values=value[0], variable=value[1], height=25, width=100,
                    justify='center', state='readonly').grid(row=key, column=1, sticky='e', padx=10)
connect = ctk.CTkButton(master=frame_parametrs, text='Connect', command=test)
connect.grid(row=6, column=0, columnspan = 2, pady=10, padx = 25)

frame_commands = ctk.CTkFrame(master=app)
frame_commands.grid(row=1, column = 0, sticky='ew', pady=10, padx=10)
ctk.CTkLabel(master=frame_commands, text = 'Commands').grid(row=0, column=0, ipady=5, sticky='ew')
mcal = ctk.CTkButton(master = frame_commands, text='MCAL')
mcal.grid(row=1, column=0,padx=25)
setfil = ctk.CTkButton(master = frame_commands, text='SETFIL', command = open_setfil)
setfil.grid(row=2, column=0,padx=25, pady=10)

frame_answers = ctk.CTkFrame(master=app)
frame_answers.grid(row=0,column = 1, rowspan=10, padx=10, pady=10, sticky = 'nsew', ipady=5)
ctk.CTkLabel(master=frame_answers, text = 'Answers').grid(row=0, column=0, sticky = 'n', pady=5)
all = ctk.CTkTextbox(master=frame_answers, height=200, width = 400, activate_scrollbars=True)
all.grid(row=1, column=0, sticky = 'n',padx=10)
ctk.CTkLabel(master=frame_answers, text = 'Responses to commands').grid(row=2, column=0, sticky = 'n', pady=5)
responses = ctk.CTkTextbox(master=frame_answers, height=200, width = 400, activate_scrollbars=True)
responses.grid(row=3, column=0, sticky = 'n',padx=10)
app.mainloop()

