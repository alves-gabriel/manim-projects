from manim import *
import numpy as np

config.background_color = WHITE

class Collisional_Model(Scene):

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
        SEint_label = self.label(text = r'$\mathcal{L}(\rho) = i [\rho, H] + (n + 1) D[\sigma_-] + n D[\sigma_+]$', x = 3, y = 0.75, color = BLACK).scale(0.5)
        self.play(Write(SEint_label))

        # Shifts the SE interaction  label up and shows the corresponding unitary
        self.play(SEint_label.animate.shift(0.5 * UP))
        SEint_label2 = self.label(text = r'$\mathcal{E}(\rho) = e^{\mathcal{L} \tau_{SE}}(\rho)$', x = 0, y = 0.75, color = BLACK).scale(0.5)
        SEint_label2.align_to(SEint_label, LEFT)
        self.play(Write(SEint_label2))
        self.wait(2)

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
        swap_label = self.label(text = r'$V = \sigma_ + \otimes \sigma_- + \sigma_- \otimes \sigma_+$', x = 2, y = -1.2, color = BLACK).scale(0.5)
        swap_label.align_to(SEint_label, LEFT)
        self.play(Write(swap_label))
        self.wait(1)

        # Shifts the SWAP label up and shows the corresponding unitary
        self.play(swap_label.animate.shift(0.5 * UP))
        swap_label2 = self.label(text = r'$U = U_{SWAP} = \exp \left( - i V \tau_{SA} \right)$', x = 2, y = -1.2, color = BLACK).scale(0.5)
        swap_label2.align_to(swap_label, LEFT)
        self.play(Write(swap_label2))
        self.wait(1)

        ######################################################

        # Draws the ancillae trail
        n_ancillae = 4
        ancilla_trail = []
        ancilla_trail_label = []

        # Trail with 5 ancillae
        for i in range(4):
            ancilla_trail.append(RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5))
            ancilla_trail[i].set_fill(crimson, opacity=0.25)
            self.add(ancilla_trail[i])
            self.mob_pos(ancilla_trail[i], x = 3*(i+1), y = -2)
            self.play(FadeIn(ancilla_trail[i]))

            # Ancillae label
            ancilla_trail_label.append(self.label(text = r'$A_%i$' %(i+2), x = 3*(i + 1), y = -2, color = crimson))
            self.play(FadeIn(ancilla_trail_label[i]))

        # Throws one ancilla away
        self.play(ancilla.animate.shift(3 * LEFT), ancilla_label.animate.shift(3 * LEFT))

        # Moves the ancillae to the lefts
        for i in range(4):
            self.play(ancilla_trail[i].animate.shift(3 * LEFT), ancilla_trail_label[i].animate.shift(3 * LEFT))

        self.wait(1)

        ######################################################

        # Draws the equiptment
        detector = ImageMobject("detector_img").scale(0.25)
        detector_line = Line(detector.get_center(), detector.get_center()-0.01*RIGHT + 0.35*UP).set_color(RED)
        self.add(detector)
        self.mob_pos(detector, x = -3, y = -.5)

        # Creates a needle in the detector
        detector_line = Line(detector.get_center() - 0.01*RIGHT, detector.get_center() - 0.01*RIGHT + 0.35*UP).set_color(RED)
        self.add(detector_line)

        # Equipment fade in
        self.play(FadeIn(detector_line), FadeIn(detector))
        self.wait(2)

        # Rotates the needle around its edge
        self.play(detector_line.animate.rotate(angle = PI/4, about_point = detector.get_center() - 0.01*RIGHT))
        self.wait(1)

        # Performs the first measurement and stores it in the measurement record
        outcome = self.label(text = r'$0$', x = -3, y = .5, color = BLACK).scale(1)
        self.play(FadeIn(outcome))
        self.wait(1)

        # Writes the detection record vector and erturns the needle to the middle
        d_record = self.label(text = r'$D = ($', x = -6, y = 2, color = BLACK).scale(1)
        self.play(Write(d_record))
        self.play(outcome.animate.align_to(d_record, UP).align_to(d_record, RIGHT).shift(0.25 * RIGHT, -0.05 * UP))
        self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center() - 0.01*RIGHT))

        # Throws one ancilla away
        self.play(FadeOutAndShift(ancilla, 3 * LEFT), FadeOutAndShift(ancilla_label, 3 * LEFT))

        ######################################################

        detection_record = [0, 1, 0, 0, 1]

        for i in range(n_ancillae-1):

            # # Animates the SE interaction again
            # self.remove(SEint)
            # for j in range(20*(i+1) - 1, 20*(i+2)):
            #
            #     # Sine with variable phase
            #     def ysin(t):
            #
            #         return np.array((np.sin(25*(t + j*np.pi/80))/8, t, 0))
            #
            #     # Draws the sine function for the given phase
            #     SEint = ParametricFunction(ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0, a = 1)
            #     self.add(SEint.scale(1))
            #     self.mob_pos(SEint, x = 0, y = 1)
            #
            #     # Animation interval
            #     self.wait(0.1)
            #     self.remove(SEint)

            # Renders the wave one last time otherwise it disappears
            self.add(SEint.scale(1))

            # Flips the SWAP arrows
            self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT))
            self.wait(0.05)

            # Moves the ancillae to the left
            for j in range(n_ancillae - i):
                self.play(ancilla_trail[i + j].animate.shift(3 * LEFT), ancilla_trail_label[i + j].animate.shift(3 * LEFT))

            self.wait(1)

            # Rotates the needle around its edge
            if detection_record[i+1]==0:
                self.play(detector_line.animate.rotate(angle = +PI/4, about_point = detector.get_center() - 0.01*RIGHT))
            else:
                self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center() - 0.01*RIGHT))

            # Performs the first measurement and stores it in the measurement record
            outcome_new = self.label(text = r'$%d$' %detection_record[i+1], x = -3, y = .5, color = BLACK).scale(1)
            self.play(FadeIn(outcome_new))
            self.wait(1)

            # Writes into the detection record vector
            self.play(outcome_new.animate.align_to(d_record, UP).align_to(outcome, RIGHT).shift(0.55 * RIGHT, -0.05 * UP))

            # Returns the needle to the middle
            if detection_record[i+1]==0:
                self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center() - 0.01*RIGHT))
            else:
                self.play(detector_line.animate.rotate(angle = +PI/4, about_point = detector.get_center() - 0.01*RIGHT))

            # Updates the last digit in the detection record vectors
            outcome = outcome_new

            #Throws one ancilla away
            self.play(FadeOutAndShift(ancilla_trail[i], 3 * LEFT), FadeOutAndShift(ancilla_trail_label[i], 3 * LEFT))

        # Closes the detection record vector with a "...)" and erases the detector
        d_close = self.label(text = r'$...)$', x = -2.9, y = 2, color = BLACK).scale(1)
        self.play(FadeIn(d_close))
        self.play(FadeOut(detector), FadeOut(detector_line))
        self.wait(1)

        # Hightlights the Detection Record
        d_highlight = Rectangle(width = 4.5, height = 1.0, color = royal_blue)
        self.mob_pos(d_highlight, x = -4.6, y = 2)
        self.play(ShowCreation(d_highlight))

        # Highlight
        d_highlight = self.label(text = 'Detection Record', x = -4.6, y = 1, color = royal_blue).scale(1)
        self.play(Write(d_highlight))

        ######################################################

        # Thermal map and unitaries
        thermal_map = self.label(text = r'$\rho_S^n = \tr_{A_n}\{U^\dagger \mathcal{E}(\rho_S^{n-1} \otimes \rho_{A_n}) U\}$', x = 0, y = -3, color = BLACK).scale(0.5)
        self.play(Write(thermal_map))
        self.wait(1)

        # Hightlights the stroboscopic map
        d_highlight = Rectangle(width = 3.75, height = .75, color = crimson)
        self.mob_pos(d_highlight, x = 0, y = -3)
        self.play(ShowCreation(d_highlight))

        # Highlight
        d_highlight = self.label(text = 'Stroboscopic Map', x = 0, y = -3.75, color = crimson).scale(.5)
        self.play(Write(d_highlight))

        ######################################################

        self.wait(5)
