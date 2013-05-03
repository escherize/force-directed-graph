class Vertex():
    def __init__(self):
        self.x = random.choice(range(width))
        self.y = random.choice(range(height))
        self.dx = int(random.random() * 100)
        self.dy = int(random.random() * 100)
        self.color = vertex_color
        self.border_color = vertex_boarder_color
        self.thickness = 0
        self.degree = 0
        self.size = 30
        self.name = str(self.size)
        if self.name is None:
            self.name = str(random.choice([v for v in range(100)]))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def display(self, screen):
        #fill
        pygame.draw.circle(screen, self.border_color, (
            int(self.x), int(self.y)), self.size * view_size_scaler + 3)
        #outline
        pygame.draw.circle(screen, self.color, (
            int(self.x), int(self.y)), self.size * view_size_scaler, self.thickness)
        fontObj = pygame.font.Font(None, max(self.size, 12))
        label = fontObj.render(self.name, False, word_color)
        screen.blit(label, (self.x-label.get_width()/2,
                            self.y-label.get_height() / 2))

    def move(self):
        self.x -= self.dx
        self.y -= self.dy
