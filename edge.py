class Edge():
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        s.degree += 1
        t.degree += 1
        self.weight = 30
        self.color = edge_color

    def __str__(self):
        return "(" + str(self.s) + ", " + str(self.t) + ")"

    def display(self, screen):
        pygame.draw.line(screen, background_color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                         int(self.weight/2)+3)
        pygame.draw.line(screen, self.color,
                        (self.s.x, self.s.y), (self.t.x, self.t.y),
                         int(self.weight/2))
