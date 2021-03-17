from manim import *
import numpy as np

config.background_color = WHITE

class Colisional_Model(Scene):

    '''
    AUXILIARY FUNCTIONS
    '''

    # Returns a parabola
    def parabola(self, t):

        return np.array((t, 2 * t ** 2, 0))

    # Draws a label at (x,y)
    def label(self, text, x, y, color = WHITE):

            text_label = Tex(text, color = color).scale(1)
            self.add(text_label)
            text_label = text_label.move_to(RIGHT * x + UP * y)
            self.add(text_label)

            return text_label

    # Positions a mobject at (x, y)
    def mob_pos(self, mobj, x, y):

            return mobj.move_to(RIGHT * x + UP * y)


    '''
    SCENE
    '''

    # Constructs the scene
    def construct(self):

        # Colors
        # https://www.w3schools.com/colors/colors_picker.asp
        mediumseagreen = '#3CB371'
        royal_blue = '#4169E1'
        crimson = '#DC143C'

        ######################################################

        # Draws the environment
        env = ParametricFunction(self.parabola, t_min = -1/2, t_max = 1/2, color = mediumseagreen, fill_opacity=0)
        self.add(env.scale(2))
        self.mob_pos(env, x = 0, y = 2)
        self.play(FadeIn(env))

        # Environment label
        env_label = self.label(text = r'$E$', x = 0, y = 2, color = mediumseagreen)
        self.play(FadeIn(env_label))

        # Draws the system
        system = Circle(color = royal_blue).scale(0.5)
        system.set_fill(royal_blue, opacity=0.5)
        self.add(system)
        self.mob_pos(system, x = 0, y = 0)
        self.play(FadeIn(system))

        # System Label
        system_label = self.label(text = r'$S$', x = 0, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        # Draws the SE interaction animation
        for i in range(20):

            # Sine with variable phase
            def ysin(t):

                return np.array((np.sin(25*(t + i*np.pi/80))/8, t, 0))

            # Draws the sine function for the given phase
            SEint = ParametricFunction(ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0, a = 1)
            self.add(SEint.scale(1))
            self.mob_pos(SEint, x = 0, y = 1)

            # Animation interval
            self.wait(0.1)
            self.remove(SEint)

        # Renders the wave one last time otherwise it disappears
        self.add(SEint.scale(1))

        # SE interaction label
        SEint_label = self.label(text = r'$\mathcal{L}(\rho) = i [\rho, H] + (n + 1) D[\sigma_-] + n D[\sigma_+]$', x = 3, y = 1, color = BLACK).scale(0.5)
        self.play(Write(SEint_label))

        ######################################################

        # Draws the ancilla
        ancilla = RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5)
        ancilla.set_fill(crimson, opacity=0.25)
        self.add(ancilla)
        self.mob_pos(ancilla, x = 0, y = -2)
        self.play(FadeIn(ancilla))

        # Ancilla label
        ancilla_label = self.label(text = r'$A_1$', x = 0, y = -2, color = crimson)
        self.play(FadeIn(ancilla_label))

        # Draws the SWAP interaction with two arrows
        SWAP1 = CurvedArrow(0, -1*UP, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP2 = CurvedArrow(-1*UP, 0, angle = np.pi/2).set_color(BLACK).scale(.75)
        self.mob_pos(SWAP1, x = -0.2, y = -1)
        self.mob_pos(SWAP2, x = +0.2, y = -1)
        self.play(FadeIn(SWAP1), FadeIn(SWAP2))
        self.wait(1)

        # Flips the SWAP arrows
        self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT))
        self.wait(0.05)

        # SWAP label, aligned to the SE interaction label
        swap_label = self.label(text = r'$V = \sigma_ + \otimes \sigma_- + \sigma_- \otimes \sigma_+$', x = 2, y = -1, color = BLACK).scale(0.5)
        swap_label.align_to(SEint_label, LEFT)
        self.play(Write(swap_label))
        self.wait(1)

        # Shifts the SWAP label up and shows the corresponding unitary
        self.play(swap_label.animate.shift(0.5 * UP))
        swap_label2 = self.label(text = r'$U = U_{SWAP} = \exp \left( - i V \tau_{SA} \right)$', x = 2, y = -1, color = BLACK).scale(0.5)
        swap_label2.align_to(swap_label, LEFT)
        self.play(Write(swap_label2))
        self.wait(5)

        ######################################################

        # Throws one ancilla away
        self.play(FadeOutAndShift(ancilla, 2 * LEFT), FadeOutAndShift(ancilla_label, 2 * LEFT))
