from tkinter import *
from tkinter import messagebox

timer = None
progress = 0
bar_width = 0
start_delay = None
bar_after_id = None

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
    global bar_width, bar_after_id

    if bar_width < 900 :
        bar_width += 9
        timer_canvas.coords(progress_bar, 0, 0, bar_width, 8)

        bar_after_id = window.after(50, update_bar)

def stop_bar():
    global bar_after_id, bar_width
    if bar_after_id is not None:
        window.after_cancel(bar_after_id)
        bar_after_id = None
    bar_width = 0
    timer_canvas.coords(progress_bar, 0,0,0,8)

def delete_text():
    stop_bar()
    text_area.delete("1.0", END)
    messagebox.showinfo("Time's Up!", "Your time is up! All your progress has been lost.")

def start_countdown():
    global timer
    stop_bar()
    update_bar()
    timer = window.after(5000, delete_text)

def on_key_press(event):
    global timer, start_delay

    #Cancel 5sec delete timer
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    
    #Cancel pendign 300ms countdown timer
    if start_delay is not None:
        window.after_cancel(start_delay)
        start_delay = None

    stop_bar()

    start_delay = window.after(300, start_countdown)
    
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
text_area.bind("<KeyPress>", on_key_press)

window.mainloop()