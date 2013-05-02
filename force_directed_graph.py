#bryan maass
import pygame
from pygame.locals import *
import random
import math
# import os.path

background_colour = (50, 50, 50)
(width, height) = (1280, 700)
dampen = 0.01
dampen_decrease = 0
"""  This is a doc """
name_list = ["Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit", "Integer", "nec", "odio", "Praesent"]

frame_count = 0
current_time = None
sorted_event_index = None
edge_rate = .01
number_of_vertices = 0
number_of_edges = 0
force_max = 300
mouse_sens = .4

monokai_bg = pygame.Color(
    int(256 * 0.1333), int(256 * 0.1333), int(256 * 0.1333))
monokai_orange = pygame.Color(
    int(255 * 1.0000), int(256 * 0.5882), int(256 * 0.2353))
monokai_purple = pygame.Color(
    int(256 * 0.5647), int(256 * 0.3294), int(256 * 0.7333))
monokai_white = pygame.Color(
    int(256 * 0.9176), int(256 * 0.9725), int(256 * 0.9490))
red_color = pygame.Color(255, 0, 0)
green_color = pygame.Color(0, 255, 0)
blue_color = pygame.Color(0, 0, 255)
white_color = pygame.Color(255, 255, 255)
black_color = pygame.Color(0, 0, 0)
lightRed_color = pygame.Color(200, 50, 50)
background_color = monokai_bg
edge_color = monokai_orange
vertex_color = monokai_purple
word_color = monokai_orange

class TagInfo():
    def __init__(self):
        self.post_count = 0
        self.score = 0
        self.answer_count = 0
        self.favorite_count = 0





# h5file = tb.openFile('overflow.h5', 'r')

#input: time
#output: 

# events = []
# event_table = h5file.getNode("/", "events")


class TagGraph():
    def __init__(self):
        self.tags = {}
        self.edges = {}
        self.vertices = {}
        self.posts = set()



    def _add_post_tag(self, tag, post):
        if not tag in self.vertices:
            tg = TagInfo()
            tg.post_count = 1
            tg.score = 0
            self.vertices[tag] = tg
        else:
            self.vertices[tag].post_count += 1

    def _remove_post_tag(self, tag, post):
        self.vertices[tag].post_count -= 1
        if self.vertices[tag].post_count == 0:
            del self.vertices[tag]

    def _add_answer_tag(self, tag, answer):
        if not tag in self.vertices:
            return
        self.vertices[tag].answer_count += 1

    def _remove_answer_tag(self, tag, answer):
        if not tag in self.vertices:
            return
        self.vertices[tag].answer_count -= 1

    def add_answer(self, answer, post):
        for tag in post['tags']:
            self._add_answer_tag(tag, answer)

    def remove_answer(self, answer, post):
        for tag in post['tags']:
            self._remove_answer_tag(tag, answer)

    def add_question(self, post):
        if post['id'] in self.posts:
            return
        self.posts.add(post['id'])
        taglist = []
        for tag in post['tags']:
            taglist.append(tag)
            self._add_post_tag(tag, post)
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                if e in self.edges:
                    self.edges[e] += w
                # Add new vertex
                else:
                    self.edges[e] = w

    def remove_question(self, post):
        if not post['id'] in self.posts:
            return
        self.posts.remove(post['id'])
        taglist = []
        for tag in post['tags']:
            taglist.append(tag)
            self._remove_post_tag(tag, post)
        for i, source in enumerate(taglist):
            for target in taglist[i + 1:]:
                e = (source, target)
                if e[0] > e[1]:
                    e = (target, source)
                w = 1.0 / len(taglist)
                # Remove vertex
                if self.edges[e] == w:
                    del self.edges[e]
                else:
                    self.edges[e] -= w

    def add_vote(self, vote, post):
        vote_type = vote['vote_type_id']
        # Up Mod
        if vote_type == 2:
            for tag in post['tags']:
                self.vertices[tag].score += 1
        elif vote_type == 3:
            for tag in post['tags']:
                self.vertices[tag].score -= 1
        elif vote_type == 5:
            for tag in post['tags']:
                self.vertices[tag].favorite_count += 1

    def remove_vote(self, vote, post):
        vote_type = vote['vote_type_id']
        # Up Mod
        if vote_type == 2:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].score -= 1
        # Down mod
        elif vote_type == 3:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].score += 1
        # Favorite
        elif vote_type == 5:
            for tag in post['tags']:
                if not tag in self.vertices:
                    continue
                self.vertices[tag].favorite_count -= 1


class TimeFilter():
    def __init__(self, event_array, sorted_event_index):
        self.event_array = event_array
        self.sorted_event_index = sorted_event_index
        self.oldindex = 0
        self.newindex = 0
        self.isReverse = None

    def setTime(self, time):
        #binary search to find the latest index
        #that is lte this time
        self.oldindex = 0
        self.newindex = self._bisect_left(time)
        if self.newindex > self.oldindex:
            self.isReverse = False
        else:
            self.isReverse = True

    def event_seq_gen(self):
        i = self.oldindex
        if not self.isReverse:
            while i < self.newindex:
                yield self.event_array[self.sorted_event_index[i]]
                i += 1
        elif self.isReverse:
            while i > self.newindex:
                yield self.event_array[self.sorted_event_index[i]]
                i -= 1

    def _bisect_left(self, x, lo=0, hi=None):
        max = self.event_array[0]['timestamp']
        i = 1
        while x > max and i < len(self.event_array):
            max = self.event_array[i]['timestamp']
            i += 1
        return i



# Vert(name, total_rep, ...)
# Edge(w,(v1,v2))


class GraphPlotPanel():
    def __init__(self):
        self.selected_bg = False
        self.selected_vertex = None
        self.running = True
        self.frame_count = 0
        self.frame_rate = 0
        self.dampen = dampen
        self.dampen_decrease = 1-dampen_decrease
        self.mouse_sens = mouse_sens
        self.E = []
        self.V = []
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        # pygame.mixer.init(buffer=256)
        # pygame.mixer.music.load('blip.wav')
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Graph Viewer')

    def drawStats(self):
        fontObj = pygame.font.Font(None, 20)
        s = str(self.frame_rate)
        print ("%.2f", self.frame_rate)
        label = fontObj.render(s, False, word_color)
        self.screen.blit(label, (width - 50, height - 25))

    def shake(self):
        self.dampen = dampen
        for v in self.V:
            touching = self.findvertex(v.x, v.y)
            if touching is not None:
                e = Edge(v, touching, 20)
                self.E.append(e)
        for v in self.V:
            m = random.choice([1, -1])
            v.dx = m * len(self.V) * 5000
            m = random.choice([1, -1])
            v.dy = m * len(self.V) * 5000

    def findvertex(self, x, y):
        for v in self.V:
            if math.hypot(v.x - x, v.y - y) <= v.size:
                return v
        return None

    def spring(self, edge):
        self._spring(edge.s, edge.t, edge.weight, edge=True)

    def _spring(self, v1, v2, weight, edge):
        pad = 2.5 * ((v1.size + v2.size) + len(self.V))
        x_diff = v1.x - v2.x
        y_diff = v1.y - v2.y
        angle = math.atan2(y_diff, x_diff)
        dist = math.hypot(x_diff, y_diff)
        if dist < width/3 or edge:
            force = 10 * (dist - pad)
            if force > force_max:
                force = force_max
            if edge:
                force = 20 * (dist - pad / 2)
            x_force = math.cos(angle) * force
            y_force = math.sin(angle) * force
            v1.dx += x_force
            v2.dx -= x_force
            v1.dy += y_force
            v2.dy -= y_force

    def repel(self, v1):
        for v2 in self.V:
            if v2 == v1:
                return
            self._spring(v1, v2, 30, edge=False)

    def pan(self, x, y):
        for v in self.V:
            v.x += x * self.mouse_sens
            v.y += y * self.mouse_sens

    # def buildRandomGraph(self, number_of_vertices, edge_rate):
    #     for n in range(self.):
    #         size = random.choice([k for k in range(5, 25, 5)])
    #         v = Vertex(size)
    #         self.V.append(v)

    def add_node(self):
        self.dampen = dampen
        size = random.choice([k for k in range(10, 50, 5)])
        v = Vertex(size, str(size))
        self.V.append(v)

    def add_edge(self):
        self.dampen = dampen
        if len(self.V) > 1:
            edges = random.sample(self.V, 2)
            e = Edge(edges[1], edges[0], 20)
            self.E.append(e)

    def run(self):
        while(self.running):
            self.frame_count += 1
            self.dampen *= self.dampen_decrease
            for event in pygame.event.get():
                #checking pressed keys
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_s or pygame.K_S]:
                        self.shake()
                    if keys[pygame.K_v or pygame.K_V]:
                        self.add_node()
                    if keys[pygame.K_t or pygame.K_T]:
                        for x in range(10):
                            self.add_node()
                    if keys[pygame.K_e or pygame.K_E]:
                        self.add_edge()
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    found = self.findvertex(mouseX, mouseY)
                    if found:
                        self.selected_vertex = found
                    else:
                        self.selected_bg = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.selected_vertex = None
                    self.selected_bg = False
            self.screen.fill(background_color)
            if self.selected_vertex:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.selected_vertex.x = mouseX
                self.selected_vertex.y = mouseY
            if self.selected_bg:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # if math.fabs(mouseX) + math.fabs(mouseY) < 500:
                self.pan(int(mouseX - width / 2) * -.2,
                        (int(mouseY - height / 2)* -.2))
            if self.dampen > .00001:
                for e in self.E:
                    self.spring(e)
                for v in self.V:
                    # pygame.draw.line(screen, (0, 0, 0),
                    #      (v.x, v.y), (v.x+v.dx*10, v.y+v.dy*10), 2
                    # if self.dampen > 1e-05:
                    self.repel(v)
                    if math.fabs(v.dx) > 1000:
                        v.dx *= .7
                    if math.fabs(v.dy) > 1000:
                        v.dy *= .7
                    v.dx = v.dx * self.dampen
                    v.dy = v.dy * self.dampen
                    v.move()

            for e in self.E:
                e.display(self.screen)
            for v in self.V:
                v.display(self.screen)
            self.frame_rate = self.fpsClock.get_fps()
            self.fpsClock.tick(60)
            self.drawStats()
            pygame.display.flip()


def launch_graph_plot():
    graph_plot = GraphPlotPanel()
    # graph_plot.buildRandomGraph(number_of_vertices, edge_rate)
    for x in range(number_of_vertices):
        graph_plot.add_node()
    for y in range(number_of_edges):
        graph_plot.add_edge()
    graph_plot.run()


class Edge():
    def __init__(self, s, t, weight):
        self.s = s
        self.t = t
        s.degree += 1
        t.degree += 1
        self.weight = min(random.choice([x for x in range(5, 15)]), s.size, t.size)
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


class Vertex():
    def __init__(self, size, name=None):
        self.x = random.choice(range(size, width-size))
        self.y = random.choice(range(size, height-size))
        self.dx = int(random.random() * 100)
        self.dy = int(random.random() * 100)
        self.mass = size
        self.color = vertex_color
        self.border = background_color
        self.thickness = 0
        self.degree = 0
        self.size = size
        self.name = name
        if self.name is None:
            self.name = str(random.choice([v for v in range(100)]))

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def display(self, screen):
        pygame.draw.circle(screen, self.border, (
            int(self.x), int(self.y)), self.size+3)
        pygame.draw.circle(screen, self.color, (
            int(self.x), int(self.y)), self.size, self.thickness)
        fontObj = pygame.font.Font(None, max(self.size, 12))
        label = fontObj.render(self.name, False, word_color)
        screen.blit(label, (self.x-label.get_width()/2,
                            self.y-label.get_height() / 2))

        

    def move(self):
        self.x -= self.dx
        self.y -= self.dy

if __name__ == "__main__":
    launch_graph_plot()
