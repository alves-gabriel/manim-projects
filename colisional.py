from manim import *
import numpy as np

config.background_color = WHITE

class Colisional_Model(Scene):

    # Defines a parabola from an array
    def parabola(self, t):

        return np.array((t, 2 * t ** 2, 0))

    # Defines a parabola from an array
    def ysin(self, t):

        return np.array((np.sin(25*t)/8, t, 0))

    def label(self, text, x, y, color = WHITE):

            text_label = Tex(text, color = color).scale(1)
            self.add(text_label)
            text_label = text_label.move_to(RIGHT * x + UP * y)
            self.add(text_label)

            return text_label

    def mob_pos(self, mobj, x, y):

            return mobj.move_to(RIGHT * x + UP * y)

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
        self.mob_pos(env, x = 0, y = 2)
        self.play(FadeIn(env))

        env_label = self.label(text = r'$E$', x = 0, y = 2, color = mediumseagreen)
        self.play(FadeIn(env_label))

        # Draws the system
        system = Circle(color = royal_blue).scale(0.5)
        system.set_fill(royal_blue, opacity=0.5)
        self.add(system)
        self.mob_pos(system, x = 0, y = 0)
        self.play(FadeIn(system))

        system_label = self.label(text = r'$S$', x = 0, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        # Draws the interaction
        SEint = ParametricFunction(self.ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0)
        self.add(SEint.scale(1))
        self.mob_pos(SEint, x = 0, y = 1)
        self.play(FadeIn(SEint))

        SEint_label = self.label(text = r'$\mathcal{L}(\rho) = i [\rho, H] + (n + 1) D[\sigma_-] + n D[\sigma_+]$', x = 3, y = 1, color = BLACK).scale(0.5)
        self.play(ShowCreation(SEint_label))

        # Draws the ancilla
        ancilla = Square(color = crimson).scale(0.5)
        ancilla.set_fill(crimson, opacity=0.25)
        self.add(ancilla)
        self.mob_pos(ancilla, x = 0, y = -2)
        self.play(FadeIn(ancilla))

        ancilla_label = self.label(text = r'$A_1$', x = 0, y = -2, color = crimson)
        self.play(FadeIn(ancilla_label))

        # Draws the SWAP
        SWAP1 = CurvedArrow(0, -1*UP, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP2 = CurvedArrow(-1*UP, 0, angle = np.pi/2).set_color(BLACK).scale(.75)
        self.mob_pos(SWAP1, x = -0.2, y = -1)
        self.mob_pos(SWAP2, x = +0.2, y = -1)
        self.play(FadeIn(SWAP1), FadeIn(SWAP2))
        self.wait(1)

        self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT))
        self.wait(5)

        swap_label = self.label(text = r'$U = \sigma_ + \otimes \sigma_- + \sigma_- \otimes \sigma_+$', x = 2, y = -1, color = BLACK).scale(0.5)
        self.play(FadeIn(swap_label))

        self.wait(1)
