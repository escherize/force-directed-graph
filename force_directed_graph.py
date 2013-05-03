##Bryan Maass
"""
Keybindings:

v       - adds a (v)ertex
V       - adds 10 (V)ertices

clicking a vertex adds a new vertex off of that node

e       - adds an (e)dge
E       - adds 10 (E)dges

Z or z  - clear screen

s or S  - will shake the vertices, in the case of a non-optimized layout

click on the background to pan!
left ctrl lets you pan or drag faster!

"""
import pygame
from pygame.locals import *
import random
import math

(width, height) = (1280, 700)

"""shows lines denoting the force vectors on vertices!"""
debug = False

"""this is how smushy the animations happen (use between .01 and .001)"""
dampen = 0.01

"""the rate at which the dampening increases after
    adding an edge or a node, or calling 0 means none"""
dampen_decrease = .00

"""pad_scaler: 4 is big, 2.5 is cozy"""
pad_scaler = 2.5

"""can increase the visual size of nodes and edges"""
view_size_scaler = 1

"""can fill in the number of v,e to begin with.
    This is for randomized graph view"""
number_of_vertices = 0
number_of_edges = 0
edge_rate = .01

"""reduce if there's lots of vibrations"""
force_max = 30

"""controls panning speed"""
mouse_sens = .4


#color declarations
monokai_bg = pygame.Color(34, 34, 34)
monokai_orange = pygame.Color(255, 151, 60)
monokai_purple = pygame.Color(145, 84, 188)
monokai_white = pygame.Color(235, 249, 243)
monokai_green = pygame.Color(152, 224, 35)
monokai_blue = pygame.Color(71, 192, 230)
color_red = pygame.Color(255, 0, 0)
color_green = pygame.Color(0, 255, 0)
color_blue = pygame.Color(0, 0, 255)
color_white = pygame.Color(255, 255, 255)
color_black = pygame.Color(0, 0, 0)

#color assignments
background_color = monokai_bg
vertex_color = monokai_purple
vertex_boarder_color = monokai_blue
word_color = monokai_white
edge_color = monokai_blue
selected_color = monokai_orange
debug_color = monokai_green


class GraphPlotPanel():
    def __init__(self):
        self.selected_bg = False
        self.selected_vertex = None
        self.hovered_vertex = None
        self.running = True
        self.frame_count = 0
        self.dampen = dampen
        self.dampen_decrease = 1 - dampen_decrease
        self.E = []
        self.V = []
        self.view_size_scaler = view_size_scaler
        self.mouse_sens = mouse_sens
        pygame.init()
        self.fpsClock = pygame.time.Clock()
        self.info_font = pygame.font.SysFont("monospace", 20)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Graph Visualizer')

    def shake(self):
        self.dampen = dampen
        for v in self.V:
            move_by = random.choice([1, -1])
            v.dx = move_by * len(self.V) * 500
            move_by = random.choice([1, -1])
            v.dy = move_by * len(self.V) * 500

    def spawn_edge_and_node_here(self, v):
        v2 = Vertex()
        e = Edge(v, v2, 3)
        self.V.append(v2)
        self.E.append(e)


    def add_touching_edges(self):
        # adds an edge between overlapping edges
        touching = self.findvertex(v.x, v.y)
        if touching is not None:
            e = Edge(v, touching, 20)
            self.E.append(e)

    def findvertex(self, x, y):
        for v in self.V:
            if math.hypot(v.x - x, v.y - y) <= v.size * self.view_size_scaler:
                return v
        return None

    def spring(self, edge):
        self._spring(edge.s, edge.t, edge.weight, edge=True)

    def _spring(self, v1, v2, weight, edge):
        pad = 4 * ((v1.size + v2.size) + int(.5*len(self.V)))
        x_diff = v1.x - v2.x
        y_diff = v1.y - v2.y
        angle = math.atan2(y_diff, x_diff)
        dist = math.hypot(x_diff, y_diff)
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
            self._spring(v1, v2, 300, edge=False)

    def pan(self, x, y):
        for v in self.V:
            v.x += x * self.mouse_sens
            v.y += y * self.mouse_sens

    # def buildRandomGraph(self, number_of_vertices, edge_rate):
    #     for n in range(self.):
    #         size = random.choice([k for k in range(5, 25, 5)])
    #         v = Vertex(size)
    #         self.V.append(v)

    def add_vertex(self):
        #reset dampening
        self.dampen = dampen
        v = Vertex()
        self.V.append(v)

    def add_edge(self):
        self.dampen = dampen
        if len(self.V) > 1:
            edges = random.sample(self.V, 2)
            e = Edge(edges[1], edges[0], 20)
            self.E.append(e)

    def clear_graph(self):
        self.E = []
        self.V = []

    def calculate_positions(self):
        for e in self.E:
            self.spring(e)
        for v in self.V:
            if debug:
                pygame.draw.line(self.screen, monokai_green,
                                (v.x, v.y), (v.x + v.dx * 3, v.y + v.dy * 3), 3)
            # if self.dampen > 1e-05:
            self.repel(v)
            if math.fabs(v.dx) > 1000:
                v.dx *= .7
            if math.fabs(v.dy) > 1000:
                v.dy *= .7
            v.dx = v.dx * self.dampen
            v.dy = v.dy * self.dampen
            v.move()

    def key_event_handler(self):
        for event in pygame.event.get():
                #checking pressed keys
                keys = pygame.key.get_pressed()
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_s]:
                        self.shake()
                    if keys[pygame.K_v]:
                        if event.mod & KMOD_SHIFT:
                            for x in range(10):
                                self.add_vertex()
                        else:
                            self.add_vertex()
                        # self.add_vertex()
                    if keys[pygame.K_e]:
                        if event.mod & KMOD_SHIFT:
                            for x in range(10):
                                self.add_edge()
                        else:
                            self.add_edge()
                    if keys[pygame.K_z]:
                        self.clear_graph()
                        # self.edges = []
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    self.selected_vertex = self.findvertex(mouseX, mouseY)
                    if self.selected_vertex:
                        for x in range(3):
                            self.spawn_edge_and_node_here(self.selected_vertex)
                        self.selected_vertex.border_color = selected_color
                    else:
                        self.selected_bg = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if self.selected_vertex:
                        self.selected_vertex.border_color = vertex_boarder_color
                    self.selected_vertex = None
                    self.selected_bg = False
                elif event.type == pygame.MOUSEMOTION:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    found = self.findvertex(mouseX, mouseY)
                    if found:
                        self.hovered_vertex = found
                        self.hovered_vertex.border_color = selected_color
                        self.hovered_vertex.color = selected_color
                    elif self.hovered_vertex:
                        self.hovered_vertex.border_color = vertex_boarder_color
                        self.hovered_vertex.color = vertex_color
                        self.hovered_vertex = None

    def run(self):
        while(self.running):
            self.frame_count += 1
            self.dampen *= self.dampen_decrease
            self.key_event_handler()
            self.screen.fill(background_color)
            if self.selected_vertex:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                self.selected_vertex.x = mouseX
                self.selected_vertex.y = mouseY
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LCTRL]:
                    self.pan(int(mouseX - width / 2) * -.2,
                            (int(mouseY - height / 2) * -.2))
            if self.selected_bg:
                (mouseX, mouseY) = pygame.mouse.get_pos()
                # if math.fabs(mouseX) + math.fabs(mouseY) < 500:
                self.pan(int(mouseX - width / 2) * -.2,
                        (int(mouseY - height / 2) * -.2))
            self.calculate_positions()

            for e in self.E:
                if e.s == self.selected_vertex or\
                   e.t == self.selected_vertex or\
                   e.s == self.hovered_vertex or\
                   e.t == self.hovered_vertex:
                    e.color = selected_color
                else:
                    e.color = edge_color
                e.display(self.screen)
            for v in self.V:
                v.display(self.screen)
            vertex_number_info = self.info_font.render(
                "Vertices: " + str(len(self.V)),
                1,
                debug_color)
            edge_number_info = self.info_font.render(
                "    Edges: " + str(len(self.E)),
                1,
                debug_color)
            fps_number_info = self.info_font.render(
                "      FPS: " + str(self.fpsClock.get_fps())[:5],
                1,
                debug_color)
            self.screen.blit(vertex_number_info, (10, 10))
            self.screen.blit(edge_number_info, (10, 30))
            self.screen.blit(fps_number_info, (10, 50))
            pygame.display.flip()
            self.fpsClock.tick(120)


def launch_graph_plot():
    graph_plot = GraphPlotPanel()
    # graph_plot.buildRandomGraph(number_of_vertices, edge_rate)
    for x in range(number_of_vertices):
        graph_plot.add_vertex()
    for y in range(number_of_edges):
        graph_plot.add_edge()
    graph_plot.run()

if __name__ == "__main__":
    launch_graph_plot()
