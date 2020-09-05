try:
    from random import *
except ImportError as e:
    print(repr(e))
    print("\nZum Beenden Taste drücken...")
    input()
    exit()


class Kugel():
    liste = []
    end = False

    def __init__(self, m, x, v):
        self.m = m
        self.x = x
        self.v = v
        Kugel.liste.append(self)

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
