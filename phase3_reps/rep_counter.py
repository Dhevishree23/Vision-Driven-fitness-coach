class RepCounter:

    def __init__(self, down=90, up=160):
        self.count = 0
        self.stage = "up"
        self.down = down
        self.up = up

    def update(self, angle):
        if angle < self.down and self.stage == "up":
            self.stage = "down"

        if angle > self.up and self.stage == "down":
            self.stage = "up"
            self.count += 1

        return self.count