from manim import *
import numpy as np

class DrawParabola(Scene):

    # Defines a parabola from an array
    def parabola(self, t):

        return np.array((t, 2 * t ** 2, 0))

    def label(self, text, x, y, color = WHITE):

            text_label = Tex(text, color = color).scale(1)
            self.add(text_label)
            text_label.move_to(RIGHT * x)
            text_label.move_to(UP * y)

            return text_label

    # Constructs the parabola
    def construct(self):

        # Colors
        # https://www.w3schools.com/colors/colors_picker.asp
        mediumseagreen = '#3CB371'
        royal_blue = '#4169E1'
        crimson = '#DC143C'

        # Draws the environment
        env = ParametricFunction(self.parabola, t_min = -1/2, t_max = 1/2, color = mediumseagreen, fill_opacity=0)
        self.add(env.scale(2))
        env.move_to(UP * 2)
        self.play(FadeIn(env))

        env_label = self.label(text = r'E', x = 0, y = 2, color = mediumseagreen)
        self.play(FadeIn(env_label))

        # Draws the system
        system = Circle(color = royal_blue).scale(0.5)
        self.add(system)
        system.move_to(UP * 0)
        self.play(FadeIn(system))

        system_label = self.label(text = r'S', x = 0, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        # Draws the ancilla
        ancilla = Square(color = crimson).scale(0.5)
        self.add(ancilla)
        ancilla.move_to(UP * -2)
        self.play(FadeIn(ancilla))

        ancilla_label = self.label(text = r'$A_1$', x = 0, y = -2, color = crimson)
        self.play(FadeIn(ancilla_label))

        self.wait(5)
