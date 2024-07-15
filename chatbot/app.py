from tkinter import *
import speech_recognition as sr
from chat import get_response, bot_name, load_model, load_data, load_products_from_csv

BG_PINK = "#ff6a80"
BG_COLOR = "#ffffff"
TEXT_COLOR = "#000000"

FONT = ("Times New Roman", 10)
FONT_BOLD = ("Times New Roman", 10, "bold")

class ChatApp:
    def __init__(self, model, all_words, tags, intents, products):
        self.window = Tk()
        self.model = model
        self.all_words = all_words
        self.tags = tags
        self.intents = intents
        self.products = products
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("ChatBot")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=550, bg=BG_COLOR)

        # Head label
        head_label = Label(self.window, bg=BG_PINK, fg=TEXT_COLOR, text="Welcome", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # Tiny divider
        line = Label(self.window, width=450, bg=BG_PINK)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # Scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # Bottom label
        bottom_label = Label(self.window, bg=BG_PINK, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # Message entry box
        self.msg_entry = Entry(bottom_label, bg="#ffffff", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.62, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # Send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_PINK,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.64, rely=0.008, relheight=0.06, relwidth=0.15)

        # Speak button
        speak_button = Button(bottom_label, text="Speak", font=FONT_BOLD, width=20, bg=BG_PINK,
                              command=self._on_speak_pressed)
        speak_button.place(relx=0.80, rely=0.008, relheight=0.06, relwidth=0.19)

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")

    def _insert_message(self, msg, sender):
        if not msg.strip():
            return

        self.msg_entry.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)

        response = get_response(msg, self.model, self.all_words, self.tags, self.intents, self.products)
        if response and response != "I do not understand...":
            msg2 = f"{bot_name}: {response}\n\n"
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, msg2)
            self.text_widget.configure(state=DISABLED)

        self.text_widget.see(END)

    def _on_speak_pressed(self):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()

        try:
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            msg = recognizer.recognize_google(audio)
            self.msg_entry.delete(0, END)
            self.msg_entry.insert(END, msg)

        except sr.UnknownValueError:
            self._insert_message("Sorry, I did not understand the voice information. You may try to speak again or type the message in the input box.", "System")
        except sr.RequestError:
            self._insert_message("Could not request results; check your network connection.", "System")

def main():
    intents_file_path = 'C:/Users/manya/OneDrive/Desktop/chatbot/intents.json'
    model_file_path = 'C:/Users/manya/OneDrive/Desktop/chatbot/data.pth'
    products_file_path = 'C:/Users/manya/OneDrive/Desktop/chatbot/products.csv'

    intents = load_data(intents_file_path)
    model, all_words, tags = load_model(model_file_path)
    products = load_products_from_csv(products_file_path)

    if model is None:
        print('Cannot load the model. Exiting...')
        exit()

    app = ChatApp(model, all_words, tags, intents, products)
    app.run()

if __name__ == "__main__":
    main()
