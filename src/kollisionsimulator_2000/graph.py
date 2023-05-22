try:
    import matplotlib.pyplot as plt
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()

names = {
    "t in s": 't',
    "Kollisionen (k)": 'coll',
    "v in m/s": 'v',
    "x in m": 'x',
    "Kollisionsfrequenz in k/s": 'kps',
    "delta t in s": 'dt'
}


def open_graph(data, kugeln, label_x, label_y, cb_1, cb_2):
    x = data.get(names.get(label_x))
    y = data.get(names.get(label_y))
    if x is None or y is None:
        return

    def is_multiple(*args):
        for i in args:
            if not isinstance(i, list) or not isinstance(i[0], list):
                return False
        return True

    def modify(a, **kwargs):
        b = a[:]
        if "multiply" in kwargs.keys():
            n = 0
            for i in range(len(b)):
                for j in range(kwargs['multiply']-1):
                    b.insert(n, b[n])
                n += kwargs['multiply']
        if "start_times" in kwargs.keys():
            for i in range(kwargs['start_times']-1):
                b.insert(0, b[0])
            b = b[:-(kwargs['start_times']-1)]

        valid = False
        for k in kwargs.keys():
            if k == "multiply" or k == "start_times":
                valid = True
        if not valid:
            print("ERROR: unknown keyword or keyword missing")
            return None
        else:
            return b

    title = "%s(%s)" % (label_y.replace(" (k)", ",").replace(" in ", ",").split(",")[0],
                        label_x.replace(" (k)", ",").replace(" in ", ",").split(",")[0])
    plt.figure(num=title)

    if is_multiple(x, y):
        for i in range(len(x[0])):
            if cb_2:
                if names.get(label_x) == names.get(label_y):
                    plt.plot([k[i] for k in x], [k[i] for k in y], color=kugeln[i][3])
                elif names.get(label_y) == 'v':
                    y_temp = modify([k[i] for k in y], start_times=2, multiply=2)
                    x_temp = modify([k[i] for k in x], multiply=2)
                    plt.plot(x_temp, y_temp, color=kugeln[i][3])
                elif names.get(label_x) == 'v':
                    x_temp = modify([k[i] for k in x], start_times=2, multiply=2)
                    y_temp = modify([k[i] for k in y], multiply=2)
                    plt.plot(x_temp, y_temp, color=kugeln[i][3])
            if cb_1:
                plt.scatter([k[i] for k in x][1:], [k[i] for k in y][1:], s=5, label="Kollision", color=kugeln[i][3])

    elif is_multiple(y):
        for i in range(len(y[0])):
            if cb_2:
                if names.get(label_y) == 'v':
                    y_temp = modify([k[i] for k in y], start_times=2, multiply=2)
                    x_temp = modify(x, multiply=2)
                    plt.plot(x_temp, y_temp, color=kugeln[i][3])
                elif names.get(label_y) == 'x':
                    plt.plot(x, [k[i] for k in y], color=kugeln[i][3])
            if cb_1:
                plt.scatter(x[1:], [k[i] for k in y][1:], s=5, label="Kollision", color=kugeln[i][3])

    elif is_multiple(x):
        for i in range(len(x[0])):
            if cb_2:
                if names.get(label_x) == 'v':
                    x_temp = modify([k[i] for k in x], start_times=2, multiply=2)
                    y_temp = modify(y, multiply=2)
                    plt.plot(x_temp, y_temp, color=kugeln[i][3])
                elif names.get(label_x) == 'x':
                    plt.plot([k[i] for k in x], y, color=kugeln[i][3])
            if cb_1:
                plt.scatter([k[i] for k in x][1:], y[1:], s=5, label="Kollision", color=kugeln[i][3])
    else:
        if cb_2:
            plt.plot(x, y)
        if cb_1:
            plt.scatter(x[1:], y[1:], s=5, label="Kollision")

    # if cb_1:
        # plt.legend()
    plt.grid(True)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.show()
