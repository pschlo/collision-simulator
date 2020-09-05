try:
    from graphics import *
    from random import *
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()


class Kugel(Circle):
    liste = []
    q = 0
    end1 = False
    end2 = False

    def __init__(self, m, x, v, color, f):
        self.m = m
        self.x = x
        self.v = v
        self.f = f
        Kugel.liste.append(self)
        radius = 20
        center = Point(f.start[0] + radius, f.start[1] + radius)
        Circle.__init__(self, center, radius)
        self.setFill(color)
        self.draw(f)
        if max(i.x for i in Kugel.liste) > 0:
            Kugel.q = (f.length - 2*radius) / max(i.x for i in Kugel.liste)
        else:
            Kugel.q = f.length - 2*radius
        Kugel.sync()

    def kollision_kugel(self, kugel):
        if self.m + kugel.m != 0:
            u_self = (self.v * (self.m - kugel.m) + 2 * kugel.m * kugel.v) / (self.m + kugel.m)
            u_kugel = (kugel.v * (kugel.m - self.m) + 2 * self.m * self.v) / (self.m + kugel.m)
        else:
            u_self = 0
            u_kugel = 0
        self.v = u_self
        kugel.v = u_kugel

    def kollision_wand(self):
        self.v = -self.v

    @staticmethod
    def update_positionen(t):
        for i in Kugel.liste:
            i.x = i.v * t + i.x

    @staticmethod
    def animate(t, f):
        t_temp = 0
        while ((t_temp < t > 0.01) or (t == -1)) and not Kugel.end1 and not Kugel.end2:
            end = True
            for k in Kugel.liste:
                v = k.v * Kugel.q
                k.move(v * 0.01, 0)
                if t != -1 or (k.getCenter().getX()-k.radius < k.f.x and k.v != 0):
                    end = False
            if end: Kugel.end1 = True
            if f.isClosed(): Kugel.end2 = True
            time.sleep(0.01)
            t_temp += 0.01

    @staticmethod
    def sync():
        for k in Kugel.liste:
            x = k.x * Kugel.q
            delta = (k.f.start[0] + k.radius + x) - k.getCenter().getX()
            k.move(delta, 0)
