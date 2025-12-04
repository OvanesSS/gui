import customtkinter as ctk
import tkinter as tk
from serial.tools import list_ports as tools
import myclassport


class _SingletonWrapper:
    def __init__(self, cls):
        self.__wrapped__ = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.__wrapped__(*args, **kwargs)
        return self._instance

def singleton(cls):
    return _SingletonWrapper(cls)

@singleton
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.labels_parametrs = {1: 'Port:', 2: 'Speed:', 3: 'Bits:', 4: 'Stop bits:', 5: 'Parity:'}
        self.combo_values = {1: [info.device for info in tools.comports()],
                             2: ['9600', '1200', '2400', '4800', '14400', '19200', '28800', '38400'],
                             3: ['8', '7'],
                             4: ['1', '2'],
                             5: ['None', 'Even', 'Odd', 'Mark', 'Space']}
        self.combo_vars = {}
        self.port = None

        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.title('KF1')
        self.resizable(False, False)
        self.set_window_location(698, 680)
        self.protocol("WM_DELETE_WINDOW", self.window_exit)

        for (key, value) in self.combo_values.items():
            self.combo_vars[key] = [value, tk.StringVar(value=value[0])]
        self.condition = tk.StringVar(value='Connect')
        self._init_config_menu()
        self._init_answ_win()
        self.timer_textbox()
        self.timer_textbox()

    def set_window_location(self, win_width, win_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (win_width / 2)
        y = (screen_height / 2) - (win_height / 2)
        self.geometry(f'{win_width}x{win_height}+{int(x)}+{int(y)}')

    def _init_config_menu(self):
        self.frame_config = ctk.CTkFrame(master=self)
        self.frame_config.grid(row=0, column=0, padx=[5, 0], pady=[5, 0], sticky='n')
        self.frame_parametrs = ctk.CTkFrame(master=self.frame_config)
        self.frame_parametrs.grid(row=0, column=0)
        ctk.CTkLabel(master=self.frame_parametrs, text='Parametrs').grid(row=0, column=0, columnspan=2)
        for (key, value) in self.labels_parametrs.items():
            ctk.CTkLabel(master=self.frame_parametrs, text=value).grid(row=key, column=0, padx=5, sticky='w')
        for (key, value) in self.combo_vars.items():
            ctk.CTkComboBox(master=self.frame_parametrs, values=value[0], variable=value[1], height=25, width=100,
                            justify='center', state='readonly').grid(row=key, column=1, padx=5)
        self.connect = ctk.CTkButton(master=self.frame_parametrs, textvariable=self.condition, command=self.button_connect)
        self.connect.grid(row=6, column=0, columnspan=2, pady=5)

        self.frame_commands = ctk.CTkFrame(master=self.frame_config)
        self.frame_commands.grid(row=1, column=0, pady=[5, 0])
        ctk.CTkLabel(master=self.frame_commands, text='Commands').grid(row=0, column=0, )
        self.mcal = ctk.CTkButton(master=self.frame_commands, text='MCAL')
        self.mcal.grid(row=1, column=0, padx=16, pady=[0, 5])
        self.setfil = ctk.CTkButton(master=self.frame_commands, text='SETFIL', command=self.open_setfil)
        self.setfil.grid(row=2, column=0, pady=[0, 5])


    def _init_answ_win(self):
        self.frame_answers = ctk.CTkFrame(master=self)
        self.frame_answers.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(master=self.frame_answers, text='Answers').grid(row=0, column=0)
        self.all_ans = ctk.CTkTextbox(master=self.frame_answers, activate_scrollbars=True, width=500, height=300, )
        self.all_ans.grid(row=1, column=0, padx=5, pady=[0, 10])
        ctk.CTkLabel(master=self.frame_answers, text='Responses to commands').grid(row=2, column=0)
        self.responses = ctk.CTkTextbox(master=self.frame_answers, activate_scrollbars=True, width=500, height=300, )
        self.responses.grid(row=3, column=0, padx=5, pady=[0, 5])


    def button_connect(self):
        if self.condition.get() == 'Connect':
            self.condition.set('Disconnect')
            self.port = myclassport.ComPortProcessor(self.combo_vars[1][1].get(), self.combo_vars[2][1].get(),
                                                     self.combo_vars[3][1].get(), self.combo_vars[4][1].get(),
                                                     self.combo_vars[5][1].get())
            self.port.start_thread()
        else:
            self.condition.set('Connect')
            self.port.close_port()

    def open_setfil(self): pass


    def update_textbox(self):
        while not self.port.queue.empty():
            self.all_ans.insert(0.0, ''.join(hex(ch) for ch in self.port.queue.get(timeout=1)) + '\n')

    def timer_textbox(self):
        if self.port is not None:
            self.update_textbox()
        self.after(500, self.timer_textbox)

    def window_exit(self):
        if self.port is not None:
            self.port.close_port()
        self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()