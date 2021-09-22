from manim import *
import numpy as np
import random
import copy

'''
Play with

manim -pqh github/manim-projects/metrology/metrology.py <scene-name>

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
###########
###TITLE###
###########
'''

class scene_0(Scene):
    def construct(self):

        system = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/system.jpg-000001.png").scale(.5)
        system.to_edge(LEFT, buff = 1)
        self.play(GrowFromEdge(system, LEFT))
        self.wait(1)

        dynamics = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/dynamics.jpg-000001.png").scale(.25)
        dynamics.next_to(dynamics.get_center(), RIGHT).shift(RIGHT)
        self.play(GrowFromEdge(dynamics, LEFT))
        self.wait(1)

        # diagram_rec_width = 2
        #
        # # Draws the dynamical process
        # dynamics_rectangle = PrettyRectangle(diagram_rec_width, 0.6*diagram_rec_width, CRIMSON_RGB)
        # dynamics_rectangle.next_to(system.get_center(), RIGHT).shift(2*RIGHT)
        #
        # self.add(dynamics_rectangle)
        # self.play(GrowFromEdge(dynamics_rectangle, LEFT))

        systemII = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/systemII.jpg-000001.png").scale(.5)
        systemII.next_to(dynamics.get_center(), RIGHT).shift(2*RIGHT)
        self.play(GrowFromEdge(systemII, LEFT))
        self.wait(1)

        self.wait(2)

        # # Draws the digram - ancilla
        # ancilla_rectangle = RoundedRectangle(width = 2, height = 1.25, color = CRIMSON).scale(1)
        # ancilla_rectangle.set_fill(color = CRIMSON, opacity = 0.25).move_to(model_rectangle.get_center()).shift(1.5*RIGHT)
        # ancilla_rectangle_label = Tex("Ancilla", color = CRIMSON).scale(0.7).next_to(ancilla_rectangle, UP, buff = -0.5)
        # temperature_label = MathTex("T", color = CRIMSON).scale(0.5).move_to(ancilla_rectangle.get_center()).shift(-0.2*UP)
        #
        # # Interaction
        # interaction = ParametricFunction(lambda t:np.array((t, np.sin(25*t)/8, 0)), t_range = np.array([0, 1]), color = BLACK, fill_opacity=0)
        # interaction.move_to(model_rectangle.get_center())
        # self.play(Create(interaction))
        #
        # self.play(GrowFromCenter(ancilla_rectangle))
        # self.play(Write(ancilla_rectangle_label),Write(temperature_label))
        # self.wait(3)
        #
        # ######################################################
        #
        # # Draws the digram - arrow and data
        # arrow1 = Arrow(ORIGIN, 2 * RIGHT, buff = 0.1).set_color(BLACK)
        # arrow1.next_to(model_rectangle, RIGHT)
        # arrow1_label = Tex("Protocol", color = BLACK).scale(0.75).next_to(arrow1, DOWN)
        # self.play(FadeIn(arrow1), Write(arrow1_label))
        #
        # data_rectangle = RoundedRectangle(width = 1.5, height = 1, color = ROYALBLUE).scale(1)
        # data_rectangle.set_fill(color = ROYALBLUE, opacity = 0.25).next_to(arrow1, RIGHT)
        # data_rectangle_label = Tex("Data", color = ROYALBLUE).scale(0.75).move_to(data_rectangle.get_center())
        # self.play(GrowFromCenter(data_rectangle))
        # self.play(Write(data_rectangle_label))
        # self.wait(3)
        #
        # ######################################################
        #
        # # Draws the digram - arrow and results
        # arrow2 = Arrow(ORIGIN, 2 * RIGHT, buff = 0.1).set_color(BLACK)
        # arrow2.next_to(data_rectangle, RIGHT)
        # arrow2_label = Tex("Processing", color = BLACK).scale(0.75).next_to(arrow2, DOWN)
        # self.play(FadeIn(arrow2), Write(arrow2_label))
        #
        # estimation_rectangle = RoundedRectangle(width = 2, height = 1, color = ROYALPURPLE).scale(1)
        # estimation_rectangle.set_fill(color = ROYALPURPLE, opacity = 0.25).next_to(arrow2, RIGHT)
        # estimation_rectangle_label = Tex("Estimation", color = ROYALPURPLE).scale(0.75).next_to(estimation_rectangle, UP, buff = -0.5)
        # temperature_estimation_label = MathTex("\hat{T}", color = ROYALPURPLE).scale(0.5).move_to(estimation_rectangle.get_center()).shift(-0.2*UP)
        #
        # self.play(GrowFromCenter(estimation_rectangle))
        # self.play(Write(estimation_rectangle_label), Write(temperature_estimation_label))
        # self.wait(3)
