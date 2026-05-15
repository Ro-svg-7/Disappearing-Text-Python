from tkinter import *
import random

timer = None
progress = 0
bar_width = 0
start_delay = None
bar_after_id = None
corruption_after_id = None
idle_time = 0

#-----------------------------WINDOW CREATION-----------------------------#
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

#-----------------------------CORRUPTION PHASE-----------------------------#
def lerp_color(start_rgb, end_rgb, t):
    r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0])*t)
    g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1])*t)
    b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2])*t)
    return f"#{r:02x}{g:02x}{b:02x}"

def reset_corruption():
    global corruption_after_id
    if corruption_after_id is not None:
        window.after_cancel(corruption_after_id)
        corruption_after_id = None
    text_area.configure(bg="grey")

    x =  window.winfo_x()
    y = window.winfo_y()
    window.geometry(f"+{x}+{y}")

def run_corruption():
    global corruption_after_id, idle_time

    if timer is None:
        return

    idle_time += 50

    t = min(idle_time / 5000, 1.0)

    #-------------Phase 1-------------#
    if t < 0.4:
        phase_t = t/0.4
        color = lerp_color((128,128,128), (122, 64,64), phase_t)
        text_area.configure(bg=color)
    
    #-------------Phase 2-------------#
    elif t < 0.8:
        phase_t = (t-0.4)/0.4
        color = lerp_color((122,64,64),(107,0,0),phase_t)
        text_area.configure(bg=color)

    #-------------Phase 3-------------#
    else:
        phase_t = (t-0.8)/0.2
        if int(idle_time/150)%2 == 0:
            color = lerp_color((107,0,0),(180,0,0),phase_t)
        else:
            color = lerp_color((180,0,0),(60,0,0),phase_t)
        text_area.configure(bg=color)

        shake_x = random.randint(-6,6)
        shake_y = random.randint(-4,4)
        x = window.winfo_x() + shake_x
        y = window.winfo_y() + shake_y
        window.geometry(f"+{x}+{y}")
    
    corruption_after_id = window.after(50, run_corruption)

#-----------------------------UPDATES BAR PROGRESS-----------------------------#

def update_bar():
    global bar_width, bar_after_id

    if bar_width < 900 :
        bar_width += 9
        timer_canvas.coords(progress_bar, 0, 0, bar_width, 8)

        bar_after_id = window.after(50, update_bar)
    
#-----------------------------STOPS BAR PROGRESS-----------------------------#

def stop_bar():
    global bar_after_id, bar_width
    if bar_after_id is not None:
        window.after_cancel(bar_after_id)
        bar_after_id = None
    bar_width = 0
    timer_canvas.coords(progress_bar, 0,0,0,8)

#-----------------------------DRAMATIC MESSAGE-----------------------------#

def type_death_message():
    message = "Your words have been devoured by the RoMonster!"
    text_area.configure(state=NORMAL, fg="#ff2222")

    def fade_message(step=0):
        reds=["#ff2222", "#dd1111", "#bb0000", "#990000",
            "#770000", "#550000", "#330000", "#110000"]

        if step < len(reds):
            text_area.configure(fg=reds[step])
            text_area.after(120, lambda: fade_message( step + 1))
        else:
            text_area.configure(fg="#110000")
    #-------------TYPES MESSAGE WORD-BY-WORD-------------#    
    def type_char(i):
        if i < len(message):
            text_area.insert(END, message[i])
            text_area.after(80, lambda: type_char( i + 1))
        else:
            fade_message()
            
    type_char(0)

#-----------------------------DELETES TEXT ON WINDOW-----------------------------#

def delete_text():
    global timer
    stop_bar()
    reset_corruption()
    timer=None

    text_area.configure(bg="#111111", fg="#ff2222", state=NORMAL)
    text_area.delete("1.0", END)

    text_area.after(400, type_death_message)

    def on_restart(event):
        text_area.configure(bg="gray", fg="white", state=NORMAL)
        text_area.delete("1.0", END)
        text_area.bind("<KeyPress>", on_key_press)

    text_area.bind("<KeyPress>", on_restart)

#-----------------------------MANAGES TIME NOT SPEND WRITING-----------------------------#

def idle_tick():
    global idle_time, corruption_after_id
    idle_time += 50

#-----------------------------STARTS COUNTDOWN FOR TIMER-----------------------------#

def start_countdown():
    global timer, idle_time
    idle_time = 0
    stop_bar()
    update_bar()
    run_corruption()
    timer = window.after(5000, delete_text)

#-----------------------------MANAGES EVENTS WHEN USER TYPES-----------------------------#

def on_key_press(event):
    global timer, start_delay, idle_time

    #Cancel 5sec delete timer
    if timer is not None:
        window.after_cancel(timer)
        timer = None
    
    #Cancel pending 300ms countdown timer
    if start_delay is not None:
        window.after_cancel(start_delay)
        start_delay = None

    idle_time = 0
    stop_bar()
    reset_corruption()

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