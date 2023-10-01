from tkinter import *
import customtkinter as ctk

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

root = ctk.CTk()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title('Hawkathon 2023 Plagiarism Detection Software')
        self.geometry(f'{1100}x{580}')

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # configure window close event
        self.protocol('WM_DELETE_WINDOW', self.on_closing)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text='Plagiarizer', font=ctk.CTkFont(size=20, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text='Appearance Mode', anchor='w')
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['Light', 'Dark', 'System'],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text='UI Scale', anchor='w')
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=['80%', '90%', '100%', '110%', '120%'],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        self.appearance_mode_optionemenu.set('Dark')
        self.scaling_optionemenu.set('100%')

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text='CTkEntry')
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky='nsew')

        self.main_button_1 = ctk.CTkButton(master=self, fg_color='transparent', border_width=2, text_color=('gray10', '#DCE4EE'))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky='nsew')

        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.textbox.insert('0.0', 'Enter suspicious text here...')

        self.set_defaults()

        self.add_funny()

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text='Type in a number:', title='CTkInputDialog')
        print('CTkInputDialog:', dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace('%', '')) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print('sidebar_button click')

    def on_closing(self):
        self.destroy()
        exit()

    def add_funny(self):
        # create tabview
        self.file_upload = ctk.CTkFrame(self)
        self.file_upload.grid(row=0, column=2, padx=(20, 20), pady=(20,0), sticky='nsew')
        self.file_upload.grid_columnconfigure(0, weight=1)
        or_label = ctk.CTkLabel(master=self.file_upload, text=f'Or...')
        or_label.grid(row=0, column=0, padx=10, pady=(20, 20))
        upload_button = ctk.CTkButton(master=self.file_upload, text='Upload File')
        upload_button.grid(row=1, column=0, padx=10, pady=(0, 20))
        supported_types = ctk.CTkLabel(master=self.file_upload, text=f'*.pdf *.txt *.docx *.doc *.csv')
        supported_types.grid(row=2, column=0, padx=10, pady=(0, 20))

        # create radiobutton frame
        self.radiobutton_frame = ctk.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky='nsew')
        self.radio_var = IntVar(value=0)
        self.label_radio_group = ctk.CTkLabel(master=self.radiobutton_frame, text='CTkRadioButton Group:')
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky='')
        self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky='n')
        self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky='n')
        self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky='n')

        # create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text='Results')
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = ctk.CTkSwitch(master=self.scrollable_frame, text=f'CTkSwitch {i}')
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky='nsew')
        self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky='n')
        self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky='n')
        self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky='n')

    def set_defaults(self):
        self.sidebar_button_3.configure(state='disabled', text='Disabled CTkButton')

if __name__ == '__main__':
    app = App()
    app.mainloop()