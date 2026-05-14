from tkinter import *
from tkinter import messagebox

window = Tk()
window.title("Dangerous Writing App")

window.geometry("1200x800")
window.configure(bg="black")

writing_frame = Frame(window, bg="black",
                      width=900, height=600)

writing_frame.place(relx=0.5, rely=0.5, anchor="center")

writing_frame.pack_propagate(False)

text_area = Text(writing_frame, bg="grey", fg="white",
                 insertbackground="red", font=("Georgia", 18),
                  wrap=WORD, bd=0, padx=30, pady=30)

text_area.pack(fill="both", expand=True)

window.mainloop()