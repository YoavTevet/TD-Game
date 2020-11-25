

class Projectile:

    def __init__(self, x, y, xvel=10, yvel=10, radius=3, power=1):
        self.xvel = xvel
        self.yvel = yvel
        self.orx = x
        self.ory = y
        self.x = x
        self.y = y
        self.radius = radius
        self.power = power
