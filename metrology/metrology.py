from manim import *
import numpy as np
import random
import copy

'''
Play with

manim -pqh github/manim-projects/metrology/metrology.py <scene-name>

Use the flag -s to preview the last framebox1

manim -ps github/manim-projects/metrology/metrology.py <scene-name>

Command to concatenate all the scenes together:
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4

Convert PDF to JPG/PNG:

pdftoppm  github/manim-projects/metrology/assets/file.pdf github/manim-projects/metrology/assets/file.jpg -jpeg -rx 300 -ry 300

or

pdftopng -alpha -r 300  github/manim-projects/metrology/assets/system.pdf github/manim-projects/metrology/assets/system.jpg

for transparency
'''

'''
AUXILIARY FUNCTIONS
'''

# Background default color
config.background_color = WHITE

# Colors
MSEAGREEN = '#3CB371'
ROYALBLUE = '#4169E1'
CRIMSON = '#DC143C'
CRIMSON_RGB = np.array([220, 20, 60])/255
ROYALPURPLE = '#7851a9'

# Convex combination in the hue to lighten the colors. Factor should be between 0 and 1
def tint(rgb, factor):
    return rgb + (1 - rgb)*factor

# Darkens the colors
def shade(rgb, factor):
    return rgb*(1 - factor)

# Draws a pretty rectangle with a slight gradient from the borders
def PrettyRectangle(rec_width, rec_height, color):
    return VGroup(
        RoundedRectangle(corner_radius=0.25, width = rec_width, height = rec_height, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        RoundedRectangle(corner_radius=0.95*0.25, width = 0.95*rec_width, height = 0.95*rec_height, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1)
    )

'''
############
###SCENES###
############
'''

# Metrology basic diagram
class scene_0(Scene):
    def construct(self):

        # Initial state
        system = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/system.jpg-000001.png").scale(.45)
        system.to_edge(LEFT, buff = 0.25)
        system_label=Tex(r"State $\rho_0$", color = BLACK).scale(0.75).next_to(system, UP, buff = 0.5)
        self.play(GrowFromEdge(system, LEFT), Write(system_label))
        self.wait(1)

        arrow=[]
        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(system, RIGHT)
        self.play(Create(arrow[-1]))

        # Dynamical part
        dynamics = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/dynamics.jpg-000001.png").scale(.25)
        dynamics.next_to(arrow[-1], RIGHT)
        dynamics_label=Tex(r"Dynamics $U(\theta)$, $\mathcal{L}_\theta$, ...", color = BLACK).scale(0.75).next_to(dynamics, DOWN, buff = 0.5)
        self.play(GrowFromEdge(dynamics, LEFT), Write(dynamics_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(dynamics, RIGHT)
        self.play(Create(arrow[-1]))

        #  Final State
        systemII = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/systemII.jpg-000001.png").scale(.45)
        systemII.next_to(arrow[-1], RIGHT)
        systemII_label=Tex(r"State $\rho_\theta$", color = BLACK).scale(0.75).next_to(systemII, UP, buff = 0.5)
        self.play(GrowFromEdge(systemII, LEFT), Write(systemII_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(systemII, RIGHT)
        self.play(Create(arrow[-1]))

        # Detector
        detector = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/detector.jpg-000001.png").scale(.2)
        detector.next_to(arrow[-1], RIGHT)
        detector_label=Tex(r"Measurement $\xi$", color = BLACK).scale(0.75).next_to(detector, DOWN, buff = 0.5)
        self.play(GrowFromEdge(detector, LEFT), Write(detector_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(detector, RIGHT)
        self.play(Create(arrow[-1]))

        # Estimator
        computer = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/computer.jpg-000001.png").scale(.2)
        computer.next_to(arrow[-1], RIGHT)
        computer_label=Tex(r"Estimation", color = BLACK).scale(0.75).next_to(computer, UP, buff = 0.5)
        self.play(FadeIn(computer), Write(computer_label))
        self.wait(1)

        # diagram_rec_width = 2
        #
        # # Draws the dynamical process
        # dynamics_rectangle = PrettyRectangle(diagram_rec_width, 0.6*diagram_rec_width, CRIMSON_RGB)
        # dynamics_rectangle.next_to(system.get_center(), RIGHT).shift(2*RIGHT)
        #
        # self.add(dynamics_rectangle)
        # self.play(GrowFromEdge(dynamics_rectangle, LEFT))
