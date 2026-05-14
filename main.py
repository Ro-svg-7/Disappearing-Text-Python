from tkinter import *
from tkinter import messagebox

timer = None
progress = 0
bar_width = 0

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

def update_bar():
    global bar_width

    if bar_width < 900 :
        bar_width += 9
        timer_canvas.coords(progress_bar, 0, 0, bar_width, 8)

        window.after(50, update_bar)

def delete_text():
    text_area.delete("1.0", END)
    messagebox.showinfo("Time's Up!", "Your time is up! All your progress has been lost.")

def start_timer(event):
    global timer
    if timer is not None:
        window.after_cancel(timer)

    print("Timer Reset!")
    global bar_width
    bar_width = 0
    timer_canvas.coords(progress_bar, 0,0,0,8)
    update_bar()
    timer = window.after(5000, delete_text)

#-----------------------------TIMER-----------------------------#
timer_canvas = Canvas(window, 
                      width=900, 
                      height=8,
                      bg="#222222",
                      highlightthickness=0)
timer_canvas.place(relx=0.5, rely=0.08, anchor="center")

progress_bar = timer_canvas.create_rectangle(
    0, 0, 0, 8, fill="red", width=0 
)
text_area.bind("<KeyPress>", start_timer)

window.mainloop()