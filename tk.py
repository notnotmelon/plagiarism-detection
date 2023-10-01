from tkinter import *
import customtkinter as ctk
from tkinter import filedialog
import fileparse
import threading
import webbrowser

import google_search
import plagiarism_checker
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

root = ctk.CTk()

def is_internal_string(text):
    text = text.replace('\n', '')
    return text == '' or text == 'Enter suspicious text here...' or text == 'Could not parse file!' or text == 'Please enter text to check for plagiarism!'

# add newlines every 80 characters after spaces
def make_readable(text):
    result = ''
    i = 0
    while i < len(text):
        result += text[i:i+80] + '\n'
        i += 80
    return result

class ResultsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x300")

    def process_results(self, plagiarisized_substrings, unsearchable_urls):
        for substring, url in plagiarisized_substrings:
            print(f'"{substring}" was plagiarized from {url}')
            switch = ctk.CTkLabel(self, text=f'{make_readable(substring)}\n\nwas plagiarized from')
            switch.pack(padx=20, pady=20)
            switch = ctk.CTkButton(self, text=url, command=lambda url=url: webbrowser.open(url), fg_color='transparent', border_width=0, text_color='blue')
            switch.pack(padx=20, pady=0)
        for url in unsearchable_urls:
            print('Could not search ' + url)
            switch = ctk.CTkLabel(self, text='Could not search ' + url)
            switch.pack(padx=20, pady=20)
        return self

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Hawkathon 2023 Plagiarism Detection Software')
        self.geometry(f'{1100}x{580}')
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
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
        self.entry.grid(row=3, column=1, columnspan=1, padx=(20, 0), pady=(20, 20), sticky='nsew')
        self.progressbar = ctk.CTkProgressBar(self)
        self.progressbar.grid(row=3, column=1, padx=(20, 00), pady=(20, 20), sticky='nsew')
        self.progressbar.set(1)

        self.main_button = ctk.CTkButton(master=self, fg_color='transparent', border_width=2, text_color=('gray10', '#DCE4EE'), text='Check Plagiarism', command=self.check_plagiarism)
        self.main_button.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky='nsew')

        # create textbox
        self.textbox = ctk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, rowspan=2, padx=(20, 0), pady=(20, 0), sticky='nsew')
        self.textbox.insert('0.0', 'Enter suspicious text here...')

        # create tabview
        self.file_upload = ctk.CTkFrame(self)
        self.file_upload.grid(row=0, column=2, padx=(20, 20), pady=(20,0), sticky='nsew')
        self.file_upload.grid_columnconfigure(0, weight=1)
        or_label = ctk.CTkLabel(master=self.file_upload, text=f'Or...')
        or_label.grid(row=0, column=0, padx=10, pady=(20, 20))
        upload_button = ctk.CTkButton(master=self.file_upload, text='Upload File', command=self.upload_action)
        upload_button.grid(row=1, column=0, padx=10, pady=(0, 20))
        supported_types = ctk.CTkLabel(master=self.file_upload, text=f'*.pdf *.txt *.docx *.doc *.csv\nand more')
        supported_types.grid(row=2, column=0, padx=10, pady=(0, 20))

        # create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text='Results')
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 20), pady=(20, 0), sticky='nsew')
        self.scrollable_frame.grid_columnconfigure(0, weight=1)

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

    def upload_action(self):
        filename = filedialog.askopenfilename()
        result = fileparse.get_text(filename)
        if result is None:
            result = 'Could not parse file!'
        self.textbox.delete('0.0', END)
        self.textbox.insert('0.0', result)

    def check_plagiarism(self):
        if plagiarism_checker.is_busy():
            return
        text = self.textbox.get('0.0', END).replace('\n', '')
        if is_internal_string(text):
            self.textbox.delete('0.0', END)
            self.textbox.insert('0.0', 'Please enter text to check for plagiarism!')
            return
        self.progressbar.configure(mode='indeterminnate')
        self.progressbar.start()
        top_urls = google_search.search(text, 10)
        for url in top_urls:
            print(url)
        if len(top_urls) == 0:
            print('No results found')
            self.finish_check_plagiarism(None)
        else:
            event = threading.Event()
            threading.Thread(target=lambda: plagiarism_checker.find_plagiarism(text, top_urls, event)).start()
            threading.Thread(target=lambda: self.finish_check_plagiarism(event)).start()

    
    action_queue = []
    def duqueue(self):
        while len(self.action_queue) != 0:
            self.action_queue[0]()
            del self.action_queue[0]

    def finish_check_plagiarism(self, event):
        if event is not None:
            event.wait()
        print('Finished checking plagiarism')
        self.progressbar.configure(mode='determinnate')
        self.progressbar.set(1)
        self.progressbar.stop()
        plagiarisized_substrings, unsearchable_urls = plagiarism_checker.results()
        self.action_queue.append(lambda: ResultsWindow(self).process_results(plagiarisized_substrings, unsearchable_urls).focus())
        self.after(1, self.duqueue)

if __name__ == '__main__':
    app = App()
    app.mainloop()