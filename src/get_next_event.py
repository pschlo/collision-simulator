
def getNextEvent(kugeln):

    events = []

    k = 0
    for i in kugeln:
        k += 1
        for j in kugeln[k:]:
            if i.v != j.v:
                t = (j.x - i.x) / (i.v - j.v)
                if t > 0:
                    events.append(dict(type="kollision", time=t, obj=[i, j]))

    for i in kugeln:
        if i.v != 0:
            t = -(i.x / i.v)
            if t > 0:
                events.append(dict(type="wall", time=t, obj=[i]))

    # cleaning
    t_min = min(ev["time"] for ev in events) if events else 0
    for ev in events[:]:
        if ev["time"] > t_min:
            events.remove(ev)

    for k in kugeln:
        a = []
        for ev in events[:]:
            if k in ev["obj"]:
                a.append(ev["type"])
        if "kollision" in a and "wall" in a:
            for ev in events[:]:
                if ev["type"] == "kollision":
                    events.remove(ev)

    return events, t_min


# def form(zahl):
    # return ('%f' % zahl).rstrip('0').rstrip('.')


def get_max(a):
    _max = None
    for i in a:
        for j in i:
            if _max is None or abs(j) > _max:
                _max = abs(j)
    return _max


def get_min(a):
    _max = None
    for i in a:
        for j in i:
            if _max is None or abs(j) < _max:
                _max = abs(j)
    return _max
