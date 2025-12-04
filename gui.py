import customtkinter as ctk
import tkinter as tk
from serial.tools import list_ports as tools
import myclassport

port=None


def button_connect():
    global port
    if condition.get() == 'Connect':
        condition.set('Disconnect')
        port = myclassport.ComPortProcessor(combo_vars[1][1].get(), combo_vars[2][1].get(), combo_vars[3][1].get(),
                                            combo_vars[4][1].get(), combo_vars[5][1].get())
        port.start_thread()
    else:
        condition.set('Connect')
        port.close_port()

labels_parametrs = {1:'Port:', 2:'Speed:', 3:'Bits:', 4:'Stop bits:', 5:'Parity:'}
combo_values={1:[info.device for info in tools.comports()],
              2:['9600', '1200', '2400', '4800', '14400', '19200', '28800', '38400'],
              3:['8', '7'],
              4:['1', '2'],
              5:['None', 'Even', 'Odd', 'Mark', 'Space']}
combo_vars = {}


def set_window_location(win, win_width, win_height):
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width / 2) - (win_width / 2)
    y = (screen_height / 2) - (win_height / 2)
    win.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

def open_setfil():
    win_setfil = ctk.CTkToplevel(app)
    win_setfil.title('SETFIL')
    win_setfil.resizable(False, False)
    set_window_location(win_setfil, 300, 170)
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
app.title('KF1')
app.resizable(False, False)
set_window_location(app, 698, 680)

for (key, value) in combo_values.items():
    combo_vars[key] = [value, tk.StringVar(value = value[0])]
condition = tk.StringVar(value = 'Connect')

frame_config = ctk.CTkFrame(master=app)
frame_config.grid(row=0, column=0, padx=[5,0], pady=[5,0], sticky='n')
frame_parametrs = ctk.CTkFrame(master=frame_config)
frame_parametrs.grid(row=0, column=0)
ctk.CTkLabel(master=frame_parametrs, text = 'Parametrs').grid(row=0, column=0, columnspan=2)
for (key, value) in labels_parametrs.items():
    ctk.CTkLabel(master=frame_parametrs, text = value).grid(row=key, column=0, padx=5, sticky='w')
for (key, value) in combo_vars.items():
    ctk.CTkComboBox(master=frame_parametrs, values=value[0], variable=value[1], height=25, width=100,
                    justify='center', state='readonly').grid(row=key, column=1, padx=5)
connect = ctk.CTkButton(master=frame_parametrs, textvariable = condition, command=button_connect)
connect.grid(row=6, column=0, columnspan=2, pady=5)

frame_commands = ctk.CTkFrame(master=frame_config)
frame_commands.grid(row=1, column=0, pady=[5,0])
ctk.CTkLabel(master=frame_commands, text='Commands').grid(row=0, column=0,)
mcal = ctk.CTkButton(master=frame_commands, text='MCAL')
mcal.grid(row=1, column=0, padx=16, pady=[0,5])
setfil = ctk.CTkButton(master=frame_commands, text='SETFIL', command=open_setfil)
setfil.grid(row=2, column=0, pady=[0,5])


frame_answers = ctk.CTkFrame(master=app)
frame_answers.grid(row=0, column=1, padx=5, pady=5)
ctk.CTkLabel(master=frame_answers, text = 'Answers').grid(row=0, column=0)
all_ans = ctk.CTkTextbox(master=frame_answers, activate_scrollbars=True, width=500, height=300,)
all_ans.grid(row=1, column=0, padx=5, pady=[0,10])
ctk.CTkLabel(master=frame_answers, text = 'Responses to commands').grid(row=2, column=0)
responses = ctk.CTkTextbox(master=frame_answers, activate_scrollbars=True, width=500, height=300,)
responses.grid(row=3, column=0, padx=5, pady=[0,5])


def update_textbox():
    while not port.queue.empty():
        all_ans.insert(0.0, ''.join(hex(ch) for ch in port.queue.get(timeout=1)) + '\n')
def timer_textbox():
    if port is not None:
        update_textbox()
    app.after(1000, timer_textbox)
timer_textbox()


def window_exit():
    if port is not None:
        port.close_port()
    app.destroy()
app.protocol("WM_DELETE_WINDOW", window_exit)


app.mainloop()


