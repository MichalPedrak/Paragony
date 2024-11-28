import customtkinter as ctk

def button_callback():
    print("Button clicked")

app = ctk.CTk()
app.geometry("400x150")
button = ctk.CTkButton(app, text="Click me", command=button_callback)
button.pack(padx=20, pady=20)
app.mainloop()



