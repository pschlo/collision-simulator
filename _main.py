# -*- coding: utf-8 -*-
try:
    from tkinter import *
    import os
    import datetime
    from animation import *
    from no_animation import no_animation
    import graphics as gr
    from random import *
    from graph import *
    from tkinter import ttk
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()

# bg_color = "grey"
font_size = 9
font = ("TkDefaultFont", font_size)
color_list = ["red", "green", "blue", "yellow", "gray", "cyan"]

root = Tk()
gr.initgraphics(root)

root.title("Kollisions-Simulator 2000")
bg_color = root.cget("bg")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry("%sx%s+15+15" % (screen_width - 50, screen_width // 2))
# root.configure(bg="#ff4da6")
kugeln = []
data = {}


def color(n):
    if n < len(color_list):
        return color_list[n]
    else:
        return "#%02x%02x%02x" % (randrange(255), randrange(255), randrange(255))


def button_add(m, x, v):
    try:
        m = float(m.replace(",", "."))
        x = float(x.replace(",", "."))
        v = float(v.replace(",", "."))
        kugeln.append([m, x, v, None])
        for i in (
                button_graph, button_export, axis_y, axis_x, label_y, label_x, cb_graph_1, cb_graph_2, label_t1,
                label_t2,
                label_kps, label_coll, label_energy, label_momentum):
            i.config(state=DISABLED)
        for i in text_coll, text_t_sim, text_t2, text_kps, text_energy, text_momentum:
            i.config(state=NORMAL)
            i.delete(0, END)
            i.config(state=DISABLED)
        list_update()
        for i in (input_1, input_2, input_3):
            i.delete(0, END)
        input_1.insert(0, 1)
        input_2.insert(0, 1)
        input_3.insert(0, 0)

        counter["text"] = "Körper: " + str(len(kugeln))
    except ValueError:
        return


def button_rem():
    if listbox_output.curselection():
        for sel in listbox_output.curselection()[::-1]:
            del (kugeln[sel])
    elif kugeln:
        kugeln.pop()
    list_update()
    counter["text"] = "Körper: " + str(len(kugeln))
    for i in (button_graph, button_export, axis_y, axis_x, label_y, label_x, cb_graph_1, cb_graph_2, label_t1, label_t2,
              label_kps, label_coll, label_energy, label_momentum):
        i.config(state=DISABLED)
    for i in text_coll, text_t_sim, text_t2, text_kps, text_energy, text_momentum:
        i.config(state=NORMAL)
        i.delete(0, END)
        i.config(state=DISABLED)


def list_update():
    listbox_output.delete(0, END)
    listbox_color.delete(0, END)
    for n in range(len(kugeln)):
        kugeln[n][3] = color(n)
        listbox_output.insert(n, "m: %s, x: %s, v: %s" % (kugeln[n][0], kugeln[n][1], kugeln[n][2]))
        listbox_color.insert(n, " " * 20)
        listbox_color.itemconfig(n, {'bg': kugeln[n][3]})


def fill_random():
    for i in (input_1, input_2, input_3):
        i.delete(0, END)
    input_1.insert(END, str(randint(1, 100)))
    input_2.insert(END, str(randint(1, 100)))
    input_3.insert(END, str(randint(-50, 50)))


def start():
    global data

    if mode.get() == 1 and kugeln:
        data = animation(kugeln)
    elif mode.get() == 0 and kugeln:
        data = no_animation(kugeln)
    else:
        return

    for i in (cb_graph_1, cb_graph_2, label_x, label_y, button_export, button_graph, label_coll, label_kps, label_t1,
              label_t2, label_energy, label_momentum):
        i.config(state=NORMAL)
    for i in (input_1, input_2, input_3, text_coll, text_t_sim, text_t2, text_kps, text_energy, text_momentum):
        i.config(state=NORMAL)
        i.delete(0, END)
    text_t_sim.insert(0, data['t_sim'])
    text_coll.insert(0, data['coll'][-1])
    text_t2.insert(0, data['t_calc'])
    text_kps.insert(0, max(data['kps']))
    text_energy.insert(0, data['E'])
    text_momentum.insert(0, data['p_ges'][-1])
    for i in (text_coll, text_t_sim, text_t2, text_kps, text_energy, text_momentum, axis_x, axis_y):
        i.config(state="readonly")


win_help = None


def open_help():
    global win_help
    if win_help is not None and win_help.winfo_exists():
        win_help.deiconify()
        return
    win_help = Toplevel(root)
    win_help.focus_set()
    win_help.title("Hilfe  -  Kollisions-Simulator 2000")
    win_help.geometry("%sx%s+%s+%s" % (screen_width - 200, screen_height - 200, 50, 50))
    help_text = open("help.txt", "r", encoding='utf-8')
    textbox = Text(win_help, font=font, wrap=WORD)
    n = 0
    indent = 0
    for line in help_text.readlines():
        n += 1
        if line[:2] == "__":
            line = line[2:]
            textbox.insert(END, line)
            textbox.tag_add("%d" % n, "%d.0" % n, "%d.%d" % (n, len(line)))
            textbox.tag_config("%d" % n, font="TkDefaultFont 12 italic", spacing1=5, spacing3=5, lmargin1=20,
                               lmargin2=20)
            indent = 40
        elif line[0] == "_":
            line = line[1:]
            textbox.insert(END, line)
            textbox.tag_add("%d" % n, "%d.0" % n, "%d.%d" % (n, len(line)))
            textbox.tag_config("%d" % n, underline=0, font="TkDefaultFont 18 bold", spacing3=0)
            indent = 20
        elif line[0] == "-" or line[0] == "•":
            textbox.insert(END, line)
            textbox.tag_add("%d" % n, "%d.0" % n, "%d.%d" % (n, len(line)))
            textbox.tag_config("%d" % n, lmargin1=indent + 20, lmargin2=indent + 27)
        else:
            textbox.insert(END, line)
            if indent > 0:
                textbox.tag_add("%d" % n, "%d.0" % n, "%d.%d" % (n, len(line)))
                textbox.tag_config("%d" % n, lmargin1=indent, lmargin2=indent)

    # textbox.place(relx=0, rely=0, width=1, height=1)
    textbox.pack(fill=BOTH, expand=1, side=LEFT)
    textbox.config(state=DISABLED)
    scroll_help = Scrollbar(win_help, command=textbox.yview, orient=VERTICAL)
    scroll_help.pack(side=RIGHT, fill="y")
    textbox.config(yscrollcommand=scroll_help.set)


def export():
    path = "Datenexport %s" % datetime.datetime.now().strftime('%d.%m.%Y_%H-%M-%S')
    if not os.path.exists(path):
        os.makedirs(path)

    file = open(os.path.join(path, "__Körper.txt"), 'w')
    for i in range(len(kugeln)):
        file.write("Körper %s: m=%s, x=%s, v=%s\n" % (i, kugeln[i][0], kugeln[i][1], kugeln[i][2]))
    file.close()
    file = open(os.path.join(path, "_Einzeldaten.txt"), 'w')
    file.write("Kollisionen: %s\n" % data['coll'][-1])
    file.write("Zeit in der Simulation: %s\n" % data['t_sim'])
    file.write("Zeit zur Berechnung: %s\n" % data['t_calc'])
    file.write("Maximale Kollisionsfrequenz: %s\n" % max(data['kps']))
    file.write("Kinetische Energie: %s\n" % data['E'])
    file.write("Anfangsimpuls: %s" % data['p_ges'][-1])
    file.close()
    for key, value in names.items():
        file = open(os.path.join(path, key.replace("/", "p") + ".txt"), 'w')
        for line in data[value]:
            file.write(str(line) + "\n")
        file.close()


def set_entry(x, i, s):
    try:
        if i.get() == "" or s.cget("from") <= int(i.get()) <= s.cget("to"):
            i.delete(0, END)
            i.insert(END, str(x))
        elif int(i.get()) < s.cget("from"):
            s.set(s.cget("from"))
        elif int(i.get()) > s.cget("to"):
            s.set(s.cget("to"))
    except ValueError:
        s.set(0)


def update_scale(x, s):
    try:
        s.set(int(x.get()))
    except ValueError:
        s.set(0)


frame_left = Frame(root, bd=15, bg=bg_color)
frame_left.place(relx=0, rely=0, relwidth=0.75, relheight=1)
title = Label(frame_left, text="Kollisions-Simulator 2000", font="TkDefaultFont 25 bold italic", anchor="w")
title.place(relx=0, rely=0, relwidth=1, relheight=0.1)
frame_input = LabelFrame(frame_left, bg=bg_color, bd=2, pady=5, padx=20, text="Körperdaten", font=font)
frame_input.place(relx=0, rely=0.15, relwidth=1, relheight=0.26)

label_1 = Label(frame_input, text="Masse in kg", font=font, anchor="nw")
label_1.place(relx=0, rely=0, relwidth=0.3, relheight=0.15)
sv_1 = StringVar()
sv_2 = StringVar()
sv_3 = StringVar()
sv_1.trace_add("write", lambda name, index, _mode, sv=sv_1: update_scale(sv, scale_1))
sv_2.trace_add("write", lambda name, index, _mode, sv=sv_2: update_scale(sv, scale_2))
sv_3.trace_add("write", lambda name, index, _mode, sv=sv_3: update_scale(sv, scale_3))
input_1 = Entry(frame_input, font=font, textvariable=sv_1)
input_1.place(relx=0, rely=0.2, relwidth=0.3, relheight=0.15)
scale_1 = Scale(frame_input, from_=1, to=100, orient=HORIZONTAL, cursor="sb_h_double_arrow", showvalue=0, width=10,
                command=lambda x: set_entry(x, input_1, scale_1))
scale_1.place(relx=0, rely=0.4, relwidth=0.3, relheight=0.15)

label_2 = Label(frame_input, text="Position in m", font=font, anchor="nw")
label_2.place(relx=0.333, rely=0, relwidth=0.3, relheight=0.15)
input_2 = Entry(frame_input, font=font, textvariable=sv_2)
input_2.place(relx=0.333, rely=0.2, relwidth=0.3, relheight=0.15)
scale_2 = Scale(frame_input, from_=1, to=100, orient=HORIZONTAL, cursor="sb_h_double_arrow", width=10, showvalue=0,
                command=lambda x: set_entry(x, input_2, scale_2))
scale_2.place(relx=0.333, rely=0.4, relwidth=0.3, relheight=0.15)

label_3 = Label(frame_input, text="Geschwindigkeit in m/s", font=font, anchor="nw")
label_3.place(relx=0.666, rely=0, relwidth=0.3, relheight=0.15)
input_3 = Entry(frame_input, font=font, textvariable=sv_3)
input_3.place(relx=0.666, rely=0.2, relwidth=0.3, relheight=0.15)
scale_3 = Scale(frame_input, from_=-50, to=50, orient=HORIZONTAL, cursor="sb_h_double_arrow", showvalue=0, width=10,
                command=lambda x: set_entry(x, input_3, scale_3))
scale_3.place(relx=0.666, rely=0.4, relwidth=0.3, relheight=0.15)

button_plus = Button(frame_input, text="+", font=("TkDefaultFont", font_size + 15),
                     command=lambda: button_add(input_1.get(), input_2.get(), input_3.get()))
button_plus.place(relx=0, rely=0.75, relwidth=0.1, relheight=0.2)
button_start = Button(frame_left, text="Start ►", font=("TkDefaultFont", 20), command=start)
button_start.place(relx=0, rely=0.5, relwidth=0.2, relheight=0.08)
button_rand = Button(frame_input, text="⟳", font=("TkDefaultFont", 15, "bold"), command=fill_random)
button_rand.place(relx=0.15, rely=0.75, relwidth=0.05, relheight=0.2)

mode = IntVar()
checkbox_mode = Checkbutton(frame_left, text="Animation", font=font, variable=mode)
checkbox_mode.place(relx=0, rely=0.45, relwidth=0.2, relheight=0.04)
checkbox_mode.select()

button_help = Button(frame_left, text="?", command=open_help, font="TkDefaultFont 30 bold")
button_help.place(relx=1 - 0.07, rely=0.45, relwidth=0.07, relheight=0.07)

frame_graphs = LabelFrame(frame_left, text="Graphen", font=font, padx=5, pady=5)
frame_graphs.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.18)

label_x = Label(frame_graphs, text="x-Achse:", font=font, state=DISABLED)
label_y = Label(frame_graphs, text="y-Achse:", font=font, state=DISABLED)
label_y.place(relx=0, rely=0, relwidth=0.2, relheight=0.3)
label_x.place(relx=0, rely=0.4, relwidth=0.2, relheight=0.3)
options = ["t in s", "Kollisionen (k)", "delta t in s", "Kollisionsfrequenz in k/s", "v in m/s", "x in m"]
axis_x = ttk.Combobox(frame_graphs, state=DISABLED, values=options, font=font)
axis_y = ttk.Combobox(frame_graphs, state=DISABLED, values=options, font=font)
axis_y.place(relx=0.2, rely=0, relwidth=0.35, relheight=0.3)
axis_x.place(relx=0.2, rely=0.4, relwidth=0.35, relheight=0.3)

cb_1_var = IntVar()
cb_2_var = IntVar()
cb_graph_1 = Checkbutton(frame_graphs, text="Punkte", font=font, variable=cb_1_var)
cb_graph_2 = Checkbutton(frame_graphs, text="Linie", font=font, variable=cb_2_var)
cb_graph_1.place(relx=0.2, rely=0.75, relwidth=0.175, relheight=0.25)
cb_graph_2.place(relx=0.375, rely=0.75, relwidth=0.175, relheight=0.25)
cb_graph_1.config(state=DISABLED)
cb_graph_2.config(state=DISABLED)
cb_graph_1.select()
cb_graph_2.select()

button_graph = Button(frame_graphs, text="Erstellen", font=font, state=DISABLED,
                      command=lambda: open_graph(data, kugeln, axis_x.get(), axis_y.get(), cb_1_var.get(),
                                                 cb_2_var.get()))
button_graph.place(relx=0.65, rely=0, relwidth=0.3, relheight=0.3)
button_export = Button(frame_graphs, text="Daten exportieren", font=font, state=DISABLED, command=export)
button_export.place(relx=0.65, rely=0.4, relwidth=0.3, relheight=0.3)

frame_data = LabelFrame(frame_left, pady=5, padx=20, bg=bg_color, text="Ergebnis", font=font)
frame_data.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

label_coll = Label(frame_data, text="Kollisionen (k):", state=DISABLED, anchor="w", font=font)
label_coll.place(relx=0, rely=0, relwidth=0.25, relheight=0.2)
text_coll = Entry(frame_data, state="readonly", font=font)
text_coll.place(relx=0.25, rely=0, relwidth=0.15, relheight=0.2)
label_t1 = Label(frame_data, text="Zeitdauer in der Simulation in s:", state=DISABLED, anchor="w", font=font)
label_t1.place(relx=0, rely=0.3, relwidth=0.25, relheight=0.2)
text_t_sim = Entry(frame_data, state="readonly", font=font)
text_t_sim.place(relx=0.25, rely=0.3, relwidth=0.15, relheight=0.2)
label_t2 = Label(frame_data, text="Zeitdauer für die Berechnung in s:", state=DISABLED, anchor="w", font=font)
label_t2.place(relx=0, rely=0.6, relwidth=0.25, relheight=0.2)
text_t2 = Entry(frame_data, state="readonly", font=font)
text_t2.place(relx=0.25, rely=0.6, relwidth=0.15, relheight=0.2)
label_kps = Label(frame_data, text="Maximale Kollisionsfrequenz in k/s:", state=DISABLED, anchor="w", font=font)
label_kps.place(relx=0.5, rely=0, relwidth=0.3, relheight=0.2)
text_kps = Entry(frame_data, state="readonly", font=font)
text_kps.place(relx=0.8, rely=0, relwidth=0.15, relheight=0.2)
label_energy = Label(frame_data, text="Kinetische Energie in J:", state=DISABLED, anchor="w", font=font)
label_energy.place(relx=0.5, rely=0.3, relwidth=0.3, relheight=0.2)
text_energy = Entry(frame_data, state="readonly", font=font)
text_energy.place(relx=0.8, rely=0.3, relwidth=0.15, relheight=0.2)
label_momentum = Label(frame_data, text="Anfangsimpuls in kg*(m/s):", state=DISABLED, anchor="w", font=font)
label_momentum.place(relx=0.5, rely=0.6, relwidth=0.3, relheight=0.2)
text_momentum = Entry(frame_data, state="readonly", font=font)
text_momentum.place(relx=0.8, rely=0.6, relwidth=0.15, relheight=0.2)

frame_right = Frame(root, bg=bg_color, bd=0, pady=22)
frame_right.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)


def view(a, b, c=None):
    listbox_color.yview(a, b, c)
    listbox_output.yview(a, b, c)


counter = Label(frame_right, text="Körper: 0", font=font, anchor="w")
counter.place(relx=0, rely=0, relwidth=0.5, relheight=0.05)
button_minus = Button(frame_right, text="−", font=("TkDefaultFont", font_size + 15), command=button_rem)
button_minus.place(relx=0.64, rely=0, relwidth=0.3, relheight=0.04)
listbox_output = Listbox(frame_right, activestyle="none", selectmode="extended")
listbox_color = Listbox(frame_right, activestyle="none")
listbox_color.bind("<<ListboxSelect>>", lambda x: listbox_color.select_clear(0, END))
listbox_color.place(relx=0, rely=0.05, relwidth=0.1, relheight=0.95)
listbox_output.place(relx=0.1, rely=0.05, relwidth=0.84, relheight=0.95)
scroll_output = Scrollbar(frame_right, command=view, orient=VERTICAL)
scroll_output.place(relx=0.94, rely=0.05, relwidth=0.06, relheight=0.95)
listbox_output.config(yscrollcommand=scroll_output.set)
listbox_color.config(yscrollcommand=scroll_output.set)

root.mainloop()
