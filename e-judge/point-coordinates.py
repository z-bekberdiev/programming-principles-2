class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def show(self, x, y):
        print(f"({x}, {y})")

    def move(self, new_x, new_y):
        self.new_x = new_x
        self.new_y = new_y

    def dist(self):
        print(f"{(((self.new_x - self.x) ** 2 + (self.new_y - self.y) ** 2) ** (1/2)):.2f}")
    
a, b = [int(c) for c in input().split()]
x, y = [int(z) for z in input().split()]
new_x, new_y = [int(new_z) for new_z in input().split()]
point = Point(x, y)
point.show(a, b)
point.show(x, y)
point.move(new_x, new_y)
point.dist()