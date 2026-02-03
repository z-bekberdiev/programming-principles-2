class Pair:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def add(self):
        return self.a + self.b

a1, b1, a2, b2 = [int(n) for n in input().split()]
pair1 = Pair(a1, a2)
pair2 = Pair(b1, b2)
print("Result:", pair1.add(), pair2.add())