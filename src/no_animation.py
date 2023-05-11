try:
    import time
    from solid_no_animation import Kugel
    from get_next_event import *
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()


def no_animation(kugeln):
    try:
        Kugel.liste.clear()
    except: pass

    E = 0
    for k in kugeln:
        Kugel(k[0], k[1], k[2])
        E += 0.5 * k[0] * k[2] * k[2]
    t0 = time.time()
    dt = []
    v = []
    x = []
    t_ev = 0

    while True:
        dt.append(t_ev)
        v.append([k.v for k in Kugel.liste])
        x.append([k.x for k in Kugel.liste])
        events, t_ev = getNextEvent(Kugel.liste)
        if not events: break
        Kugel.update_positionen(t_ev)

        for ev in events:
            if ev["type"] == "wall":
                ev["obj"][0].kollision_wand()
                ev["obj"][0].x = 0
            elif ev["type"] == "kollision":
                ev["obj"][0].kollision_kugel(ev["obj"][1])
                ev["obj"][0].x = ev["obj"][1].x

    t = [0]
    for i in dt:
        t.append(t[len(t)-1]+i)
    del(t[0])

    p = []
    for i in v:
        p.append([i[j] * Kugel.liste[j].m for j in range(len(i))])

    return {
        "coll": list(range(len(dt))) if dt != [] else "0",
        "t_calc": time.time()-t0,
        "t_sim": t[-1] if t != [] else "0",
        "kps": [0]+[1/i for i in dt[1:]] if dt != [] else "0",
        "dt": dt,
        "t": t,
        "v": v,
        "x": x,
        "E": E,
        "p_ges": [sum(i) for i in p],
        "p": p
    }
