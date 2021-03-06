from manim import *
import numpy as np
import random
import copy

'''
Command to concatenate all the scenes together:
ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4
'''

'''
AUXILIARY FUNCTIONS
'''

# Background default color
config.background_color = WHITE

# Colors
mediumseagreen = '#3CB371'
royal_blue = '#4169E1'
crimson = '#DC143C'
royal_purple = '#7851a9'

class tools(Scene):

    # Draws a label at (x,y)
    def label(self, text, x = 0, y = 0, color = WHITE):

            text_label = Tex(text, color = color).scale(1)
            self.add(text_label)
            text_label = text_label.move_to(RIGHT * x + UP * y)
            self.add(text_label)

            return text_label

    # Positions a mobject at (x, y)
    def mob_pos(self, mobj, x = 0, y = 0):

            return mobj.move_to(RIGHT * x + UP * y)

    # Returns a parabola
    def parabola(self, t):

        return np.array((t, 2 * t ** 2, 0))

    def ysin(self, t):

        return np.array((np.sin(25*t)/8, t, 0))

    def gaussian(self, t):

        return np.array((t, np.exp(-(t - 2)**2/(2*0.25)), 0))

    def flat(self, t):

        return np.array((t, 1, 0))

'''
###########
###TITLE###
###########
'''

class Title(Scene):
    def construct(self):

        # Title
        title = Tex('Bayesian Quantum Thermometry', color = royal_blue).scale(1.5)
        title.to_edge(UP, buff=1.5).to_edge(LEFT, buff=1.5)
        self.add(title)

        # Authors
        author1 = Tex('\emph{Gabriel O. Alves}', color = BLACK).scale(0.8)
        author2 = Tex('\emph{Gabriel T. Landi}', color = BLACK).scale(0.8)
        author1.next_to(title, DOWN).align_to(title, LEFT)
        author2.next_to(author1, DOWN).align_to(title, LEFT)
        self.add(author1)
        self.add(author2)

        # Institution and Date
        institution = Tex('\\textbf{Universidade de São Paulo}', color = BLACK).scale(0.8)
        date = Tex('\\textbf{Date:} April 12th, 2021', color = BLACK).scale(0.8)

        # Positioning
        institution.to_edge(DOWN, buff=1.5).align_to(title, LEFT)
        date.next_to(institution, DOWN).align_to(title, LEFT)
        self.add(institution)
        self.add(date)

        # Group Logo
        group_logo = ImageMobject("logo.png").scale(0.75)
        group_logo.to_edge(DOWN, buff=0.5).to_edge(RIGHT, buff=1.5)
        self.add(group_logo)

        self.wait(5)

'''
###########
##SCENE 0##
###########
'''

class Scene_0(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Introduction}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.play(Write(title))
        self.wait(1)

        ######################################################

        # About thermometry
        subtitle = tools().label(text = 'How to measure temperature?', x = -3, y = 2, color = royal_blue).scale(.9)
        self.play(FadeIn(subtitle))
        self.wait(2)

        lines = []

        lines.append(tools().label(text = r'$\bullet$ Important for ultra-low temperature quantum experiments', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ The temperature is not an observable', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ It must be \emph{indirectly} inferred', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ Commonly its dependence is encoded into operators and states', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ Data processing is a challenge in itself', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))

        # Diagram Explanation
        self.play(FadeIn(lines[0]))
        self.wait(1)
        self.play(FadeIn(lines[1]), FadeIn(lines[2]))
        self.wait(3)

        # Draws the digram - model
        model_rectangle = RoundedRectangle(width = 5.5, height = 2.5, color = GRAY).scale(1)
        model_rectangle.shift(-4.0 * RIGHT).align_to(lines[4], UP).shift(-0.5*UP)
        model_rectangle_label = Tex("Model", color = GRAY).next_to(model_rectangle, UP, buff = -0.5)

        self.add(model_rectangle)
        self.play(GrowFromEdge(model_rectangle, LEFT))
        self.play(Write(model_rectangle_label))

        # Draws the digram - bath
        bath_rectangle = RoundedRectangle(width = 2, height = 1.25, color = mediumseagreen).scale(1)
        bath_rectangle.set_fill(color = mediumseagreen, opacity = 0.25).move_to(model_rectangle.get_center()).shift(1.5*LEFT)
        bath_rectangle_label = Tex("Bath", color = mediumseagreen).move_to(bath_rectangle.get_center())

        self.add(bath_rectangle)
        self.play(GrowFromEdge(bath_rectangle, LEFT))
        self.play(Write(bath_rectangle_label))

        # Draws the digram - ancilla
        ancilla_rectangle = RoundedRectangle(width = 2, height = 1.25, color = crimson).scale(1)
        ancilla_rectangle.set_fill(color = crimson, opacity = 0.25).move_to(model_rectangle.get_center()).shift(1.5*RIGHT)
        ancilla_rectangle_label = Tex("Ancilla", color = crimson).scale(0.7).next_to(ancilla_rectangle, UP, buff = -0.5)
        temperature_label = MathTex("T", color = crimson).scale(0.5).move_to(ancilla_rectangle.get_center()).shift(-0.2*UP)

        # Interaction
        interaction = ParametricFunction(lambda t:np.array((t, np.sin(25*t)/8, 0)), t_min = 0, t_max = 1, color = BLACK, fill_opacity=0)
        interaction.move_to(model_rectangle.get_center())
        self.play(ShowCreation(interaction))

        self.play(GrowFromCenter(ancilla_rectangle))
        self.play(Write(ancilla_rectangle_label),Write(temperature_label))
        self.wait(3)

        # Diagram Explanation
        self.play(FadeIn(lines[3]))
        self.wait(3)

        ######################################################

        # Draws the digram - arrow and data
        arrow1 = Arrow(ORIGIN, 2 * RIGHT, buff = 0.1).set_color(BLACK)
        arrow1.next_to(model_rectangle, RIGHT)
        arrow1_label = Tex("Protocol", color = BLACK).scale(0.75).next_to(arrow1, DOWN)
        self.play(FadeIn(arrow1), Write(arrow1_label))

        data_rectangle = RoundedRectangle(width = 1.5, height = 1, color = royal_blue).scale(1)
        data_rectangle.set_fill(color = royal_blue, opacity = 0.25).next_to(arrow1, RIGHT)
        data_rectangle_label = Tex("Data", color = royal_blue).scale(0.75).move_to(data_rectangle.get_center())
        self.play(GrowFromCenter(data_rectangle))
        self.play(Write(data_rectangle_label))
        self.wait(3)

        ######################################################

        # Draws the digram - arrow and results
        arrow2 = Arrow(ORIGIN, 2 * RIGHT, buff = 0.1).set_color(BLACK)
        arrow2.next_to(data_rectangle, RIGHT)
        arrow2_label = Tex("Processing", color = BLACK).scale(0.75).next_to(arrow2, DOWN)
        self.play(FadeIn(arrow2), Write(arrow2_label))

        estimation_rectangle = RoundedRectangle(width = 2, height = 1, color = royal_purple).scale(1)
        estimation_rectangle.set_fill(color = royal_purple, opacity = 0.25).next_to(arrow2, RIGHT)
        estimation_rectangle_label = Tex("Estimation", color = royal_purple).scale(0.75).next_to(estimation_rectangle, UP, buff = -0.5)
        temperature_estimation_label = MathTex("\hat{T}", color = royal_purple).scale(0.5).move_to(estimation_rectangle.get_center()).shift(-0.2*UP)

        self.play(GrowFromCenter(estimation_rectangle))
        self.play(Write(estimation_rectangle_label), Write(temperature_estimation_label))
        self.wait(3)

        ######################################################

        # Rectangle highlight
        diagram_highlight1 = Rectangle(width = 9.5, height = 2.8, color = crimson).scale(1)
        tools().mob_pos(diagram_highlight1, x = -2.1, y = -2.3)
        self.play(ShowCreation(diagram_highlight1))
        self.wait(2)

        # Diagram Explanation
        self.play(FadeIn(lines[4]))
        self.wait(2)

        diagram_highlight2 = Rectangle(width = 6, height = 2.0, color = crimson).scale(1)
        tools().mob_pos(diagram_highlight2, x = 3.95, y = -2.3)
        self.play(ReplacementTransform(diagram_highlight1, diagram_highlight2))

        highlight_label = Tex("Our main objective!", color = crimson).scale(0.5).next_to(diagram_highlight2, UP)
        self.play(Write(highlight_label))

        self.wait(5)

'''
###########
##SCENE 1##
###########
'''

class Scene_1(Scene):

    # Constructs the scene
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{The Collisional Model}', x = 0, y = 3.5, color = royal_blue).scale(1.1)
        ref = ImageMobject("assets/collisional/ref1.png").scale(1).to_edge(0.25*DOWN).to_edge(LEFT)
        Underline(title)

        self.play(Write(title), FadeIn(ref))
        self.wait(1)

        ######################################################

        # Draws the environment
        env = ParametricFunction(tools().parabola, t_min = -1/2, t_max = 1/2, color = mediumseagreen, fill_opacity=0).scale(2)
        self.add(env)
        tools().mob_pos(env, x = 0, y = 2)
        self.play(FadeIn(env))

        # Environment label
        env_label = tools().label(text = r'$E$', x = 0, y = 2, color = mediumseagreen)
        self.play(FadeIn(env_label))

        # Draws the system
        system = Circle(color = royal_blue).scale(0.5)
        system.set_fill(royal_blue, opacity=0.5)
        self.add(system)
        tools().mob_pos(system, x = 0, y = 0)
        self.play(FadeIn(system))

        # System Label
        system_label = tools().label(text = r'$S$', x = 0, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        # System Hamiltonian
        system_hamiltonian = tools().label(text = r'$H = \frac{\Omega}{2}\sigma_Z$', x = 2, y = 0, color = royal_blue)
        self.play(FadeIn(system_hamiltonian))
        self.wait(1.5)
        self.play(FadeOut(system_hamiltonian))

        # Draws the SE interaction animation
        for i in range(20):

            # Sine with variable phase
            def ysin(t):

                return np.array((np.sin(25*(t + i*np.pi/80))/8, t, 0))

            # Draws the sine function for the given phase
            SEint = ParametricFunction(ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0, a = 1)
            self.add(SEint.scale(1))
            tools().mob_pos(SEint, x = 0, y = 1)

            # Animation interval
            self.wait(0.1)
            self.remove(SEint)

        # Renders the wave one last time otherwise it disappears
        self.add(SEint.scale(1))

        # SE interaction label
        SEint_label = tools().label(text = r'$\mathcal{L}(\rho) = i [\rho, H] + (n + 1) D[\sigma_-] + n D[\sigma_+]$', x = 3, y = 0.75, color = BLACK).scale(0.5)
        self.play(Write(SEint_label))

        # Shifts the SE interaction  label up and shows the corresponding unitary
        self.play(SEint_label.animate.shift(0.5 * UP))
        SEint_label2 = tools().label(text = r'$\mathcal{E}(\rho) = e^{\mathcal{L} \tau_{SE}}(\rho)$', x = 0, y = 0.75, color = BLACK).scale(0.5)
        SEint_label2.align_to(SEint_label, LEFT)
        self.play(Write(SEint_label2))
        self.wait(2)

        ######################################################

        # Draws the ancilla
        ancilla = RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5)
        ancilla.set_fill(crimson, opacity=0.25)
        self.add(ancilla)
        tools().mob_pos(ancilla, x = 0, y = -2)
        self.play(FadeIn(ancilla))

        # Ancilla label
        ancilla_label = tools().label(text = r'$A_1$', x = 0, y = -2, color = crimson)
        self.play(FadeIn(ancilla_label))

        # Ancilla Hamiltonian
        ancilla_hamiltonian = tools().label(text = r'$H_A = \frac{\Omega}{2}\sigma_Z$', x = 2, y = -2, color = crimson)
        self.play(FadeIn(ancilla_hamiltonian))
        self.wait(1.5)
        self.play(FadeOut(ancilla_hamiltonian))

        # Draws the SWAP interaction with two arrows
        SWAP1 = CurvedArrow(0, -1*UP, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP2 = CurvedArrow(-1*UP, 0, angle = np.pi/2).set_color(BLACK).scale(.75)
        tools().mob_pos(SWAP1, x = -0.2, y = -1)
        tools().mob_pos(SWAP2, x = +0.2, y = -1)
        self.play(FadeIn(SWAP1), FadeIn(SWAP2))
        self.wait(1)

        # Flips the SWAP arrows
        self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT))
        self.wait(0.05)

        # SWAP label, aligned to the SE interaction label
        swap_label = tools().label(text = r'$V = \sigma_ + \otimes \sigma_- + \sigma_- \otimes \sigma_+$', x = 2, y = -1.2, color = BLACK).scale(0.5)
        swap_label.align_to(SEint_label, LEFT)
        self.play(Write(swap_label))
        self.wait(1)

        # Shifts the SWAP label up and shows the corresponding unitary
        self.play(swap_label.animate.shift(0.5 * UP))
        swap_label2 = tools().label(text = r'$U = U_{PSWAP} = \exp \left( - i V \tau_{SA} \right)$', x = 2, y = -1.2, color = BLACK).scale(0.5)
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
            tools().mob_pos(ancilla_trail[i], x = 3*(i+1), y = -2)
            self.play(FadeIn(ancilla_trail[i]))

            # Ancillae label
            ancilla_trail_label.append(tools().label(text = r'$A_%i$' %(i+2), x = 3*(i + 1), y = -2, color = crimson))
            self.play(FadeIn(ancilla_trail_label[i]))

        # Throws one ancilla away
        self.play(ancilla.animate.shift(3 * LEFT), ancilla_label.animate.shift(3 * LEFT))

        # Moves the ancillae to the lefts
        for i in range(4):
            self.play(ancilla_trail[i].animate.shift(3 * LEFT), ancilla_trail_label[i].animate.shift(3 * LEFT))

        ######################################################

        # Draws the equipment
        detector = ImageMobject("detector_img").scale(0.25)
        self.add(detector)
        tools().mob_pos(detector, x = -3, y = -.5)

        # Creates a needle in the detector
        detector_line = Line(detector.get_center() - 0.01*RIGHT, detector.get_center() + 0.35*UP).set_color(RED)
        self.add(detector_line)

        # Equipment fade in
        self.play(FadeIn(detector_line), FadeIn(detector))

        # Rotates the needle around its edge
        self.play(detector_line.animate.rotate(angle = PI/4, about_point = detector.get_center()))
        self.wait(1)

        # Performs the first measurement and stores it in the measurement record
        outcome = tools().label(text = r'$0$', x = -3, y = .5, color = BLACK).scale(1)
        self.play(FadeIn(outcome))
        self.wait(1)

        # Writes the detection record vector and erturns the needle to the middle
        d_record = tools().label(text = r'$D = ($', x = -6, y = 2, color = BLACK).scale(1)
        self.play(Write(d_record))
        self.play(outcome.animate.align_to(d_record, UP).align_to(d_record, RIGHT).shift(0.25 * RIGHT, -0.05 * UP))
        self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center()))

        # Throws one ancilla away
        self.play(FadeOutAndShift(ancilla, 3 * LEFT), FadeOutAndShift(ancilla_label, 3 * LEFT))

        ######################################################

        detection_record = [0, 1, 0, 0, 1]

        for i in range(n_ancillae-1):

            # Animates the SE interaction again
            self.remove(SEint)
            for j in range(20*(i+1) - 1, 20*(i+2)):

                # Sine with variable phase
                def ysin(t):

                    return np.array((np.sin(25*(t + j*np.pi/80))/8, t, 0))

                # Draws the sine function for the given phase
                SEint = ParametricFunction(ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0)
                self.add(SEint.scale(1))
                tools().mob_pos(SEint, x = 0, y = 1)

                # Animation interval
                self.wait(0.1)
                self.remove(SEint)

            # Renders the wave one last time otherwise it disappears
            self.add(SEint.scale(1))

            # Flips the SWAP arrows
            self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT), run_time=0.5)
            self.wait(0.05)

            # Moves the ancillae to the left
            for j in range(n_ancillae - i):
                self.play(ancilla_trail[i + j].animate.shift(3 * LEFT),
                          ancilla_trail_label[i + j].animate.shift(3 * LEFT),
                          run_time=0.5)

            # Rotates the needle around its edge
            if detection_record[i+1]==0:
                self.play(detector_line.animate.rotate(angle = +PI/4, about_point = detector.get_center()))
            else:
                self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center()))

            # Performs the first measurement and stores it in the measurement record
            outcome_new = tools().label(text = r'$%d$' %detection_record[i+1], x = -3, y = .5, color = BLACK).scale(1)
            self.play(FadeIn(outcome_new), run_time=0.5)

            # Writes into the detection record vector
            self.play(outcome_new.animate.align_to(d_record, UP).align_to(outcome, RIGHT).shift(0.55 * RIGHT, -0.05 * UP), run_time=0.5)

            # Returns the needle to the middle
            if detection_record[i+1]==0:
                self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center()))
            else:
                self.play(detector_line.animate.rotate(angle = +PI/4, about_point = detector.get_center()))

            # Updates the last digit in the detection record vectors
            outcome = outcome_new

            #Throws one ancilla away
            self.play(FadeOutAndShift(ancilla_trail[i], 3 * LEFT), FadeOutAndShift(ancilla_trail_label[i], 3 * LEFT))

        # Closes the detection record vector with a "...)" and erases the detector
        d_close = tools().label(text = r'$... )$', x = -2.9, y = 2, color = BLACK).scale(1)
        self.play(FadeIn(d_close))
        self.play(FadeOut(detector), FadeOut(detector_line))
        self.wait(1)

        # Hightlights the Detection Record
        d_highlight = Rectangle(width = 4.5, height = 1.0, color = royal_blue)
        tools().mob_pos(d_highlight, x = -4.6, y = 2)
        self.play(ShowCreation(d_highlight))

        # Highlight
        d_highlight_label = tools().label(text = 'Detection Record', x = -4.6, y = 1, color = royal_blue).scale(1)
        self.play(Write(d_highlight_label))

        ######################################################

        # Thermal map and unitaries
        thermal_map = tools().label(text = r'$\rho_S^n = \tr_{A_n}\{U \mathcal{E}(\rho_S^{n-1} \otimes \rho_{A_n}) U^\dagger\}$', x = 0, y = -3, color = BLACK).scale(0.5)
        self.play(Write(thermal_map))
        self.wait(1)

        # Hightlights the stroboscopic map
        map_highlight = Rectangle(width = 3.75, height = .75, color = crimson)
        tools().mob_pos(map_highlight, x = 0, y = -3)
        self.play(ShowCreation(map_highlight))

        # Highlight
        map_highlight_label = Tex('Stroboscopic Map', color = crimson).scale(.5).next_to(map_highlight, LEFT)
        self.play(Write(map_highlight_label))

        ######################################################

        self.wait(5)

'''
###########
##SCENE 2##
###########
'''

class Scene_2(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{The Recipe}', x = 0, y = 3.5, color = royal_blue).scale(1.1)
        Underline(title)

        subtitle = tools().label(text = 'The Model', x = -5, y = 2.25, color = royal_blue).scale(1)

        # Text lines
        lines = []

        self.play(Write(title))
        self.play(Write(subtitle))

        ######################################################

        # Text
        lines.append(tools().label(text = r' $\bullet$ SE map + SA unitary ' + r'$\rightarrow$ Stroboscopic Map', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[0]))

        lines.append(tools().label(text = r'$\rho_S^n = \Phi(\rho) := \tr_{A_n}\{U \mathcal{E}(\rho_S^{n-1} \otimes \rho_{A_n}) U^\dagger\}$' , color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle, LEFT))
        lines[1].shift(0.25*RIGHT)
        self.play(FadeIn(lines[1]))

        # Draws the environment
        env = ParametricFunction(tools().parabola, t_min = -1/2, t_max = 1/2, color = mediumseagreen, fill_opacity=0).scale(2)
        tools().mob_pos(env, x = 4, y = 2)

        # Environment label
        env_label = tools().label(text = r'$E$', x = 4, y = 2, color = mediumseagreen)

        # Draws the system
        system = Circle(color = royal_blue).scale(0.5)
        system.set_fill(royal_blue, opacity=0.5)
        tools().mob_pos(system, x = 4, y = 0)

        # System Label
        system_label = tools().label(text = r'$S$', x = 4, y = 0, color = royal_blue)

        # Draws the sine function for the given phase
        SEint = ParametricFunction(tools().ysin, t_min = -1/2, t_max = 1/2, color = BLACK, fill_opacity=0)
        tools().mob_pos(SEint, x = 4, y = 1)

        # Draws the ancillae
        ancilla1 = RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5)
        ancilla2 = RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5)
        ancilla3 = RoundedRectangle(width = 2, height = 2, color = crimson).scale(0.5)

        ancilla1.set_fill(crimson, opacity=0.25)
        ancilla2.set_fill(crimson, opacity=0.25)
        ancilla3.set_fill(crimson, opacity=0.25)

        tools().mob_pos(ancilla1, x = 2.5, y = -2)
        tools().mob_pos(ancilla2, x = 4, y = -2)
        tools().mob_pos(ancilla3, x = 5.5, y = -2)

        # Ancilla label
        ancilla_label1 = tools().label(text = r'$A_{\small n-1}$', x = 2.5, y = -2, color = crimson).scale(.6)
        ancilla_label2 = tools().label(text = r'$A_{\small n}$', x = 4, y = -2, color = crimson).scale(.6)
        ancilla_label3 = tools().label(text = r'$A_{\small n+1}$', x = 5.5, y = -2, color = crimson).scale(.6)

        # Draws the SWAP interaction with two arrows
        SWAP1 = CurvedArrow(0, -1*UP, angle = np.pi/2).set_color(BLACK).scale(.7)
        SWAP2 = CurvedArrow(-1*UP, 0, angle = np.pi/2).set_color(BLACK).scale(.7)
        tools().mob_pos(SWAP1, x = 4 - 0.2, y = -1)
        tools().mob_pos(SWAP2, x = 4 + 0.2, y = -1)
        self.wait(1)

        self.play(FadeIn(env), FadeIn(env_label), FadeIn(system), FadeIn(system_label), FadeIn(SEint), FadeIn(ancilla1), FadeIn(ancilla2), \
                  FadeIn(ancilla3), FadeIn(ancilla_label1), FadeIn(ancilla_label2), FadeIn(ancilla_label3), FadeIn(SWAP1), FadeIn(SWAP2))

        ######################################################

        # Text
        lines.append(tools().label(text = r'$\bullet$ Ancilla measurements after the', color = BLACK).scale(0.6).next_to(lines[1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'system reaches the \emph{steady state}:', color = BLACK).scale(0.6).next_to(lines[2], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[2]), FadeIn(lines[3]))

        lines.append(tools().label(text = r'$\rho_{S}^* = \Phi(\rho_{S}^*)$', color = BLACK).scale(0.6).next_to(lines[3], DOWN).align_to(subtitle, LEFT))
        lines[4].shift(0.25*RIGHT)
        self.play(FadeIn(lines[4]))

        self.play(FadeOut(system_label))
        system_label = tools().label(text = r'$\rho_{S}^*$', x = 4, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        ######################################################

        # Text
        lines.append(tools().label(text = r'$\bullet$ Both joint and local measurements are possible', color = BLACK).scale(0.6).next_to(lines[4], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[5]))

        # Draws the equipment
        detector = ImageMobject("detector_img").scale(0.2)
        detector_line = Line(detector.get_center(), detector.get_center()-0.01*RIGHT + 0.35*UP).set_color(RED)
        self.add(detector)
        tools().mob_pos(detector, x = 4, y = -3.1)

        # Creates a needle in the detector
        detector_line = Line(detector.get_center() - 0.01*RIGHT, detector.get_center() - 0.01*RIGHT + 0.35*UP).set_color(RED)
        self.add(detector_line)

        # Equipment fade in
        self.play(FadeIn(detector_line), FadeIn(detector))
        self.wait(2)

        # Kraus Operators
        Kraus = tools().label(text = 'Kraus Operators: ' + r'$M_0, ... , M_N$', x = 4, y = -3.75, color = BLACK).scale(.6)
        self.play(FadeIn(Kraus))
        self.wait(2)

        # Measurement Highlight
        local_measurement = Rectangle(width = 1.25, height = 1.15, color = crimson)
        global_measurement = Rectangle(width = 4.25, height = 1.15, color = crimson)
        tools().mob_pos(local_measurement, x = 4, y = -2)
        tools().mob_pos(global_measurement, x = 4, y = -2)

        self.play(ShowCreation(global_measurement))
        self.play(FadeOut(global_measurement))

        self.play(ShowCreation(local_measurement))

        self.wait(1)

        ######################################################

        # Text
        lines.append(tools().label(text = r'$\bullet$ We approximate single-ancilla i.i.d. measurements', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ Probability distribution associated with', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r' the measurements in the SS:', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[6]), FadeIn(lines[7]), FadeIn(lines[8]))

        lines.append(tools().label(text = r'$p(X_i|T) = \tr\{M_i \rho_{A_1...A_n}^* M_i^\dagger\}$', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines[9].shift(0.25*RIGHT)
        self.play(FadeIn(lines[9]))

        ######################################################

        self.wait(5)

'''
###########
##SCENE 3##
###########
'''

class Scene_3(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Thermometry}', x = 0, y = 3.0, color = royal_blue).scale(1.1)
        Underline(title)
        subtitle = tools().label(text = 'The Model', x = -5, y = 2, color = royal_blue).scale(1)
        subtitle2 = tools().label(text = 'Parameter Estimation', x = -5, y = -2, color = royal_blue).scale(1)

        # Text lines
        lines = []

        self.play(Write(title))
        self.play(Write(subtitle))

        ######################################################

        # About the model
        lines.append(tools().label(text = r' $\bullet$ What are the optimal parameter $\tau_{SA}$ and $\tau_{SE}$?', color = BLACK).scale(0.7).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r' $\bullet$ What are the optimal POVMs?', color = BLACK).scale(0.7).next_to(lines[0], DOWN).align_to(subtitle, LEFT))

        self.play(FadeIn(lines[0]),FadeIn(lines[1]))

        # Paper screenshot
        paper = ImageMobject("landi_paper").scale(.8)
        self.add(paper)
        tools().mob_pos(paper, x = 0, y = -2)

        # Paper fade out
        self.play(FadeIn(paper))
        self.wait(2)
        self.play(FadeOut(paper))

        ######################################################

        # About the inference
        subtitle2.next_to(lines[1], DOWN).align_to(subtitle, LEFT)
        self.play(Write(subtitle2))

        lines.append(tools().label(text = r'How to effectively process the data?', color = BLACK).scale(0.7).next_to(subtitle2, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ How to define and construct estimators?', color = BLACK).scale(0.7).next_to(lines[2], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ What are the relevant figures of merit?', color = BLACK).scale(0.7).next_to(lines[3], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ What are the suitable bounds for the problem?', color = BLACK).scale(0.7).next_to(lines[4], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[2]), FadeIn(lines[3]), FadeIn(lines[4]), FadeIn(lines[5]))

        self.wait(1)

        # Hightlights the text above
        hightlight = Rectangle(width = 8, height = 3, color = royal_blue)
        tools().mob_pos(hightlight, x = -2.5, y = -0.875)
        self.play(ShowCreation(hightlight))

        self.play(FadeIn(tools().label(text = r'We can use Bayesian Inference!', x = -3, y = -3, color = royal_blue).scale(0.7)))

        self.wait(5)

'''
###########
##SCENE 4##
###########
'''

class Scene_4(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Bayes Theorem}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)
        subtitle = tools().label(text = 'The Question', x = -5, y = 2, color = royal_blue).scale(1)

        self.play(Write(title))
        self.play(Write(subtitle))

        # Question
        question=Tex(r' How to \emph{infer} the ', r'parameter', ' from the ', r'data',r'?', color = BLACK)
        question.scale(0.7).next_to(subtitle, DOWN).align_to(subtitle, LEFT)
        question[1].set_color(crimson)
        question[3].set_color(royal_blue)

        self.play(Write(question))
        self.wait(2)

        ######################################################

        #Bayes Theorem proof
        bayes = MathTex(
            "P(T, D)=P(T|D)P(D)=P(D|T)P(T)",
            color = BLACK,
            tex_to_color_map={r"T": crimson, r"D": royal_blue}
        )

        self.play(Write(bayes))
        self.wait(2)

        # Bayes Theorem
        bayes2 = MathTex(
            "P(T|D)","={"," P(D|T)","P(T)"," \\over"," P(D)}",
            color = BLACK,
            tex_to_color_map={r"T": crimson, r"D": royal_blue}
        )
        bayes2.align_to(bayes, DOWN).shift(2 * DOWN)
        self.play(Write(bayes2))
        self.wait(2)

        # Explanation
        bayes_explanation = Tex(r'Here, we consider the parameter - the ', r'temperature', ' - and the observed ', r'data', x = 0, y = 1, color = BLACK).scale(0.75)
        bayes_explanation[1].set_color(crimson)
        bayes_explanation[3].set_color(royal_blue)
        self.play(FadeOut(bayes), Write(bayes_explanation))

        # Explanation 4
        bayes_explanation4 = Tex(r'What are the odds of measuring a certain ', r'temperature', ' given the ', r'data/measurement record','?', color = BLACK).scale(0.75)
        bayes_explanation4.move_to(-3 * UP)
        bayes_explanation4[1].set_color(crimson)
        bayes_explanation4[3].set_color(royal_blue)
        self.play(Write(bayes_explanation4))
        self.wait(4)

        # Highlights - Prior
        framebox1 = SurroundingRectangle(bayes2[11:14], buff = .05).set_color(crimson)
        framebox1_label = Tex('Prior', color = crimson).scale(0.7)
        framebox1_label.next_to(framebox1, UP)
        self.play(ShowCreation(framebox1), Write(framebox1_label))
        self.wait(1)

        bayes_explanation5 = Tex(r'The prior represents our initial state-of-knowledge about the temperature', color = BLACK).scale(0.75)
        bayes_explanation5.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation4), Write(bayes_explanation5))
        self.wait(4)

        # Highlights - Likelihood
        framebox2 = SurroundingRectangle(bayes2[6:11], buff = .05).set_color(crimson)
        framebox2_label = Tex('Likelihood', color = crimson).scale(0.7)
        framebox2_label.next_to(framebox2, UP)
        self.play(ReplacementTransform(framebox1, framebox2), Write(framebox2_label), FadeOut(framebox1_label))
        self.wait(2)

        bayes_explanation6 = Tex(r'How likely we are of observing D at a certain temperature T', color = BLACK).scale(0.75)
        bayes_explanation6.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation5), Write(bayes_explanation6))
        self.wait(4)

        # Highlights - Normalization
        framebox3 = SurroundingRectangle(bayes2[15:18], buff = .05).set_color(crimson)
        framebox3_label = Tex('Normalization', color = crimson).scale(0.7)
        framebox3_label.next_to(framebox3, RIGHT)
        self.play(ReplacementTransform(framebox2, framebox3), Write(framebox3_label), FadeOut(framebox2_label))
        self.wait(2)

        bayes_explanation7 = Tex(r'How likely we are of observing D, but \emph{irrespective} of T: a marginal distribution', color = BLACK).scale(0.75)
        bayes_explanation7.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation6), Write(bayes_explanation7))
        self.wait(4)

        # Highlights - Normalization
        framebox4 = SurroundingRectangle(bayes2[0:5], buff = .05).set_color(crimson)
        framebox4_label = Tex('Posterior', color = crimson).scale(0.7)
        framebox4_label.next_to(framebox4, UP)
        self.play(ReplacementTransform(framebox3, framebox4), Write(framebox4_label), FadeOut(framebox3_label))
        self.wait(2)

        bayes_explanation8 = Tex(r'Our updated state-of-knowledge of the system, after acquiring data. If we got D,\
                                 what are the chances that the temperature is T?', color = BLACK).scale(0.75)
        bayes_explanation8.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation7), Write(bayes_explanation8))
        self.wait(4)

        self.wait(5)

'''
###########
##SCENE 5##
###########
'''

class Scene_5(Scene):

    # Fermi dirac distribution: 1-f and f
    def fermi_dirac0(self, t):

        return np.array((t, (1-2*1/(1+np.exp(1/t))), 0))

    def fermi_dirac1(self, t):

        return np.array((t, 2*1/(1+np.exp(1/t)), 0))

    ######################################################

    def construct(self):

        # Title
        title = tools().label(text = '\\underline{An example}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)
        subtitle = tools().label(text = 'Qubit Thermal State', x = -4.55, y = 2, color = royal_blue).scale(1)

        self.play(Write(title))
        self.play(Write(subtitle))

        ######################################################

        # Definitions
        thermal_state = tools().label(
                       text = r'$\rho_{th} = \frac{e^{-\frac{H}{T}}}{Z} =\begin{matrix}\begin{pmatrix} f & 0 \\ 0& 1 - f\end{pmatrix}\end{matrix}$, \
                                with $f \equiv \frac{1}{1 + e^{\Omega/T}}$', x = -5, y = 2, color = BLACK).scale(0.75)
        thermal_state.scale(0.7).next_to(subtitle, DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(thermal_state))

        # Prob. Distribution
        distribution_text = tools().label(
                       text = r'$X_i \in \{0,1\}$ and $P(X_i|T) = f^{X_i}(1-f)^{1-X_i}$' , x = -5, y = 2, color = BLACK).scale(0.75)
        distribution_text.scale(0.7).next_to(thermal_state, DOWN).align_to(thermal_state, LEFT)
        self.play(FadeIn(distribution_text))

        # Axis definition
        def show_axis(x0 = 0, y0 = 0, x_start = -0.01, x_end =  1, y_start = -0.01, y_end = 1):

            x_axis = Arrow((x_start + x0) * RIGHT + y0 * UP, (x_end + x0) * RIGHT + y0 * UP, buff = 0).set_color(BLACK)
            y_axis = Arrow((y_start + y0) * UP + x0 * RIGHT, (y_end + y0) * UP + x0 * RIGHT, buff = 0).set_color(BLACK)

            return x_axis, y_axis

        #Draws the axis
        axis = show_axis(x0 = -5, y0 = -2.75, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2.5)
        self.play(ShowCreation(axis[0]))
        self.play(ShowCreation(axis[1]))
        xlabel = tools().label(text = '$T$', x = -0.8, y = -2.75, color = BLACK).scale(0.5)
        ylabel = tools().label(text = '$P(X | T)$', x = -5, y = 0, color = BLACK).scale(0.5)
        self.play(FadeIn(xlabel), FadeIn(ylabel))

        # Draws the curves
        fermi_dirac_plot = ParametricFunction(self.fermi_dirac0, t_min = 0.01, t_max = 4, color = ORANGE, fill_opacity=0).scale(1)
        fermi_dirac_plot2 = ParametricFunction(self.fermi_dirac1, t_min = 0.01, t_max = 4, color = royal_blue, fill_opacity=0).scale(1)
        tools().mob_pos(fermi_dirac_plot.scale(1), x = -5, y = -2.5)
        tools().mob_pos(fermi_dirac_plot2.scale(1), x = -5, y = -2.5)
        fermi_dirac_plot.align_to(axis[1], LEFT).shift(1.2 * UP + 0.2 * RIGHT)
        fermi_dirac_plot2.align_to(axis[1], LEFT).shift(0.2 * UP + 0.2 * RIGHT)
        self.play(ShowCreation(fermi_dirac_plot),ShowCreation(fermi_dirac_plot2))
        X0label = tools().label(text = '$P(X = 0| T)$', x = -1, y = -1.25, color = ORANGE).scale(0.5)
        X1label = tools().label(text = '$P(X = 1| T)$', x = -1, y = -2.25, color = royal_blue).scale(0.5)
        self.play(FadeIn(X0label), FadeIn(X1label))

        # Explanation 1
        explanation = Tex('How can we apply the Bayes theorem here?').set_color(BLACK).scale(0.7)
        explanation.move_to(-3.5 * UP)

        self.play(Write(explanation), FadeOut(distribution_text))
        self.wait(2)

        ######################################################

        # Bayes Theorem
        bayes = MathTex(
            "P(T|X_1)","={"," P(X_1|T)","P(T)"," \\over"," \mathcal{N}}",
            color = BLACK
        ).scale(0.7)
        bayes.align_to(thermal_state, DOWN).shift(2 * RIGHT)
        self.play(FadeIn(bayes))

        # Likelihood hightlight
        framebox1 = SurroundingRectangle(bayes[2], buff = .1).set_color(crimson)
        likelihood_frame = Rectangle(width = 6, height = 3.5, color = crimson).set_color(crimson)
        tools().mob_pos(likelihood_frame, x = -2.75, y = -1.5)
        self.play(ShowCreation(framebox1), ShowCreation(likelihood_frame))
        self.wait(1)

        # Likelihood explanation
        explanation1 = Tex('Likelihood: how likely we are to measure the qubit in the ','ground',' or in the ','excited', ' state').set_color(BLACK).scale(0.7)
        explanation1.move_to(-3.5 * UP)
        explanation1[1].set_color(ORANGE)
        explanation1[3].set_color(royal_blue)
        self.play(FadeOut(explanation), FadeOut(framebox1), FadeOut(likelihood_frame), Write(explanation1))

        # Prior highlight
        framebox2 = SurroundingRectangle(bayes[3], buff = .1).set_color(crimson)
        self.play(ShowCreation(framebox2))
        self.wait(1)

        # Prior explanation
        explanation2 = Tex('There\'s always a certai subjectivity when choosing a prior').set_color(BLACK).scale(0.7)
        explanation2.move_to(-3.5 * UP)
        self.play(FadeOut(explanation1), FadeOut(framebox2), Write(explanation2))
        self.wait(2)

        explanation3 = Tex('For example, they can be a Gaussian...').set_color(BLACK).scale(0.7)
        explanation3.move_to(-3.5 * UP)
        self.play(FadeOut(explanation2), Write(explanation3))

        # Draws the axis
        axis_prior = show_axis(x0 = 1, y0 = -2.75, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2.5)
        self.play(ShowCreation(axis_prior[0]))
        self.play(ShowCreation(axis_prior[1]))
        xlabel_prior = tools().label(text = '$T$', x = 5.25, y = -2.75, color = BLACK).scale(0.5)
        ylabel_prior = tools().label(text = '$P(T)$', x = 1, y = 0, color = BLACK).scale(0.5)
        self.play(FadeIn(xlabel_prior), FadeIn(ylabel_prior))

        # Draws the curves - Gaussian
        prior_plot = ParametricFunction(tools().gaussian, t_min = 0.01, t_max = 4, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(prior_plot.scale(1), x = 1, y = -2.5)
        prior_plot.align_to(axis_prior[1], LEFT).shift(0.3 * UP + 0.2 * RIGHT)
        self.play(ShowCreation(prior_plot))
        self.wait(2)

        # Prior explanation - flat
        explanation4 = Tex('Or simply flat - a state of ignorance...').set_color(BLACK).scale(0.7)
        explanation4.move_to(-3.5 * UP)
        self.play(FadeOut(explanation3), Write(explanation4))

        # Draws the curves - flat
        prior_plot2 = ParametricFunction(tools().flat, t_min = 0.01, t_max = 4, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(prior_plot2.scale(1), x = 1, y = -2.5)
        prior_plot2.align_to(axis_prior[1], LEFT).shift(0.25 * UP + 0.2 * RIGHT)
        self.play(FadeOut(prior_plot), ShowCreation(prior_plot2))
        self.wait(2)

        # Erases the prior
        self.play(FadeOut(prior_plot2), FadeOut(axis_prior[0]), FadeOut(axis_prior[1]), FadeOut(xlabel_prior), FadeOut(ylabel_prior))

        ######################################################

        # First outcome
        d_record = []
        d_record.append(MathTex("X_1 = 0", color = ORANGE).scale(0.7))
        d_record[0].align_to(distribution_text, DOWN).align_to(distribution_text, LEFT)
        self.play(FadeIn(d_record[0]))

        # Updating explanation
        explanation5 = Tex(r"Suppose we measure $X_1 = 0$. We multiply the prior and the likelihood to get the posterior, updating our state-of-knowledge", color = BLACK).scale(0.7)
        explanation5.move_to(-3.5 * UP)
        self.play(FadeOut(explanation4), Write(explanation5))

        # Writes the posterior
        posterior = MathTex("P(T|X_1)=", color = BLACK).scale(0.7)
        prob_times = MathTex("\\times", color = BLACK).scale(0.7)
        posterior.move_to(1 * RIGHT - 1.5 * UP)
        prob_times.move_to(4.25 * RIGHT - 1.5 * UP)
        self.play(FadeIn(posterior), FadeIn(prob_times))

        #Draws the axis
        axis1 = show_axis(x0 = 2, y0 = -2, x_start = -0.1, y_start = -0.1, x_end = 2, y_end = 1.1)
        self.play(FadeIn(axis1[0]), FadeIn(axis1[1]))

        axis2 = show_axis(x0 = 4.75, y0 = -2, x_start = -0.1, y_start = -0.1, x_end = 2, y_end = 1.1)
        self.play(FadeIn(axis2[0]), FadeIn(axis2[1]))

        # Draws the curves
        likelihood_plot1 = ParametricFunction(self.fermi_dirac0, t_min = 0.01, t_max = 3, color = ORANGE, fill_opacity=0).scale(0.5)
        prior_plot1 = ParametricFunction(tools().flat, t_min = 0.01, t_max = 3, color = crimson, fill_opacity=0).scale(0.5)
        tools().mob_pos(likelihood_plot1, x = 2.75, y = -1.5)
        tools().mob_pos(prior_plot1, x = 5.5, y = -1.5)
        self.play(FadeIn(likelihood_plot1), FadeIn(prior_plot1))
        self.wait(2)

        # Erases the visual Bayes
        self.play(FadeOut(posterior),FadeOut(prob_times),FadeOut(axis1[0]),FadeOut(axis1[1]),FadeOut(axis2[0]),FadeOut(axis2[1]),
                  FadeOut(likelihood_plot1),FadeOut(prior_plot1))

        # Draws the posterior axis
        axis_posterior = show_axis(x0 = 1, y0 = -2.75, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2.5)
        self.play(ShowCreation(axis_posterior[0]))
        self.play(ShowCreation(axis_posterior[1]))
        xlabel_posterior = tools().label(text = '$T$', x = -0.8 + 6, y = -2.75, color = BLACK).scale(0.5)
        ylabel_posterior = tools().label(text = '$P(T | X_1)$', x = -5 + 6, y = 0, color = BLACK).scale(0.5)
        self.play(FadeIn(xlabel_posterior), FadeIn(ylabel_posterior))

        # Draws the 1st posterior
        posterior1 = ParametricFunction(self.fermi_dirac0, t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior1.scale(1), x = -5 + 6, y = -2.5)
        posterior1.align_to(axis_posterior[1], LEFT).shift(1.2 * UP + 0.2 * RIGHT)
        self.play(ShowCreation(posterior1))

        ######################################################

        # A triangle to highlight the MAP, a dashed line and the decimal number
        estimator_triangle = RegularPolygon(3, start_angle=PI/2).scale(0.15)\
                            .move_to(1 * RIGHT - 3 * UP).set_color(BLACK)
        estimator_line = DashedLine(estimator_triangle.get_center() + 0.25 * UP, estimator_triangle.get_center()+ 2 * UP, color = BLACK)
        decimal = DecimalNumber(0, num_decimal_places = 3, unit=None).set_color(BLACK).scale(0.4)

        # Updaters for the decimal value, position and for the line position
        decimal.add_updater(lambda d: d.next_to(estimator_triangle, DOWN*0.2))
        decimal.add_updater(lambda d: d.set_value(estimator_triangle.get_center()[0] - 1))
        estimator_line.add_updater(lambda m: m.move_to(estimator_triangle.get_center() + 0.25 * UP, estimator_triangle.get_center() + 2 * UP))

        # Initialization of the objects
        estimator_triangle.move_to(1 * RIGHT -3 * UP),
        self.add(estimator_triangle, estimator_line)
        self.play(FadeIn(estimator_triangle),FadeIn(estimator_line))
        # self.play(FadeIn(FadeIn(decimal))), I'm commenting the decimal out for aesthetics reasons

        ######################################################

        # Updating explanation
        explanation6 = Tex(r"How to further update our knowledge after performing more measurements?", color = BLACK).scale(0.7)
        explanation6.move_to(-3.5 * UP)
        self.play(FadeOut(explanation5), Write(explanation6))

        # Second outcome
        d_record.append(MathTex("X_2 = 0", color = ORANGE).scale(0.7))
        d_record[1].next_to(d_record[0], RIGHT)
        self.play(FadeIn(d_record[1]))
        self.wait(5)

        # Posterior becomes Prior
        substitution_line1 = Line(1.5 * UP + 0.75 * RIGHT , 2.25 * UP + 0.75 * RIGHT, color = crimson)
        substitution_line2 = Line(2.25 * UP + 0.75 * RIGHT , 2.25 * UP + 3.5 * RIGHT , color = crimson)
        substitution_line3 = Arrow(2.25 * UP + 3.5 * RIGHT  , 1.8 * UP + 3.5 * RIGHT , color = crimson)
        substitution_framebox1 = SurroundingRectangle(bayes[0], buff = .1).set_color(crimson)
        substitution_framebox2 = SurroundingRectangle(bayes[3], buff = .1).set_color(crimson)

        # Substitution indication
        self.play(ShowCreation(substitution_framebox1), ShowCreation(substitution_framebox2),
                  ShowCreation(substitution_line1), ShowCreation(substitution_line2), ShowCreation(substitution_line3))

        # Updating explanation
        explanation7 = Tex(r"Sequential updating: the posterior becomes the new prior", color = BLACK).scale(0.7)
        explanation7.move_to(-3.5 * UP)
        self.play(FadeOut(explanation6), Write(explanation7))

        # Substitution deletion
        self.play(FadeOut(substitution_framebox1), FadeOut(substitution_framebox2),
                  FadeOut(substitution_line1), FadeOut(substitution_line2), FadeOut(substitution_line3))

        # Bayes Update
        bayes_update = MathTex(
            "P(T|X_2 X_1)","={"," P(X_2|T)","P(T | X_1)"," \\over"," \mathcal{N}}",
            color = BLACK
        ).scale(0.7)
        bayes_update.align_to(thermal_state, DOWN).shift(2 * RIGHT)
        self.play(ReplacementTransform(bayes, bayes_update))

        # Updating explanation
        explanation8 = Tex(r"And the posterior is further updated", color = BLACK).scale(0.7)
        explanation8.move_to(-3.5 * UP)
        self.play(FadeOut(explanation7), Write(explanation8))

        # Draws the 2nd posterior
        posterior2 = ParametricFunction(lambda t: np.array([t,(1-2*1/(1+np.exp(1/t)))**2,0]), t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior2.scale(1), x = -5 + 6, y = -2.5)
        posterior2.align_to(axis_posterior[1], LEFT).shift(1.2 * UP + 0.2 * RIGHT)
        ylabel_posterior2 = tools().label(text = '$P(T | X_2 X_1)$', x = -5 + 6, y = 0, color = BLACK).scale(0.5)
        self.play(ReplacementTransform(ylabel_posterior, ylabel_posterior2))

        self.play(ReplacementTransform(posterior1, posterior2))

        self.wait(2)

        ######################################################

        # Third outcome
        d_record.append(MathTex("X_3 = 1", color = royal_blue).scale(0.7))
        d_record[2].next_to(d_record[1], RIGHT)
        self.play(FadeIn(d_record[2]))
        self.wait(2)

        # Substitution indication
        substitution_framebox1 = SurroundingRectangle(bayes_update[0], buff = .1).set_color(crimson)
        substitution_framebox2 = SurroundingRectangle(bayes_update[3], buff = .1).set_color(crimson)

        self.play(ShowCreation(substitution_framebox1), ShowCreation(substitution_framebox2),
                  ShowCreation(substitution_line1), ShowCreation(substitution_line2), ShowCreation(substitution_line3))
        self.wait(1)

        # Substitution deletion
        self.play(FadeOut(substitution_framebox1), FadeOut(substitution_framebox2),
                  FadeOut(substitution_line1), FadeOut(substitution_line2), FadeOut(substitution_line3))

        # Bayes Update
        bayes_update2 = MathTex(
            "P(T|X_2 X_ 3 X_1)","={"," P(X_3|T)","P(T| X_2 X_1)"," \\over"," \mathcal{N}}",
            color = BLACK
        ).scale(0.7)
        bayes_update2.align_to(thermal_state, DOWN).shift(2 * RIGHT)
        self.play(ReplacementTransform(bayes_update, bayes_update2))

        # Draws the 3rd posterior
        posterior3 = ParametricFunction(lambda t: np.array([t,3*(1-1/(1+np.exp(1/t)))**2 * (1/(1+np.exp(1/t)))**1,0]), t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior3.scale(1), x = -5 + 6, y = -2.5)
        posterior3.align_to(axis_posterior[1], LEFT).shift(0.7 * UP + 0.2 * RIGHT)
        self.play(ReplacementTransform(posterior2, posterior3))
        ylabel_posterior3 = tools().label(text = '$P(T | X_3 X_2 X_1)$', x = -5 + 6, y = 0, color = BLACK).scale(0.5)
        self.play(ReplacementTransform(ylabel_posterior2, ylabel_posterior3))

        # Moves towards the maximum at 1.443
        self.play(
                estimator_triangle.animate.move_to((-5 + 6 + 1.443) * RIGHT -3 * UP),
                run_time=5
            )

        self.wait(2)

        ######################################################

        # Bayes Update
        bayes_update3 = MathTex(
            "P(T|X_n ... X_1)","={"," P(X_n|T)","P(T | X_1...X_{n-1})"," \\over"," \mathcal{N}}",
            color = BLACK
        ).scale(0.7)
        bayes_update3.align_to(thermal_state, DOWN).shift(2 * RIGHT)
        self.play(ReplacementTransform(bayes_update2, bayes_update3))

        self.wait(2)

        # Third outcome
        d_record.append(MathTex("X_4 = 0", color = ORANGE).scale(0.7))
        d_record[3].next_to(d_record[2], RIGHT)
        self.play(FadeIn(d_record[3]))
        self.wait(2)

        # Draws the 4th posterior
        posterior4 = ParametricFunction(lambda t: np.array([t,5*(1-1/(1+np.exp(1/t)))**3 * (1/(1+np.exp(1/t)))**1,0]), t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior4.scale(1), x = -5 + 6, y = -2.5)
        posterior4.align_to(axis_posterior[1], LEFT).shift(0.5 * UP + 0.2 * RIGHT)
        self.play(ReplacementTransform(posterior3, posterior4))
        ylabel_posterior4 = tools().label(text = '$P(T | X_N ... X_1)$', x = -5 + 6, y = 0, color = BLACK).scale(0.5)
        self.play(ReplacementTransform(ylabel_posterior3, ylabel_posterior4))

        # Moves towards the maximum at 0.910
        self.play(
                estimator_triangle.animate.move_to((-5 + 6 + 0.910) * RIGHT -3 * UP),
                run_time=1
            )

        # Last outcome
        d_record.append(MathTex("...", color = royal_blue).scale(0.7))
        d_record[4].next_to(d_record[3], RIGHT)
        self.play(FadeIn(d_record[4]))
        self.wait(2)

        # Draws the 5th posterior
        posterior5 = ParametricFunction(lambda t: np.array([t,500000000000*(1-1/(1+np.exp(1/t)))**36 * (1/(1+np.exp(1/t)))**12,0]), t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior5.scale(1), x = -5 + 6, y = -2.5)
        posterior5.align_to(axis_posterior[1], LEFT).shift(0.25 * UP + 0.2 * RIGHT)
        self.play(ReplacementTransform(posterior4, posterior5))

        self.wait(2)

        # Updating explanation
        explanation9 = Tex(r"The posterior starts to peak around a value", color = BLACK).scale(0.7)
        explanation9.move_to(-3.5 * UP)
        self.play(FadeOut(explanation8), Write(explanation9))
        self.wait(2)

        # Draws the final posterior
        posterior_gaussian = ParametricFunction(lambda t: np.array([t,2*np.exp(-(t-0.91)**2/(2*0.0025)),0]), t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior_gaussian.scale(1), x = -5 + 6, y = -2.5)
        posterior_gaussian.align_to(axis_posterior[1], LEFT).shift(0.75 * UP + 0.2 * RIGHT)
        self.play(ReplacementTransform(posterior5, posterior_gaussian))

        # Updating explanation
        explanation10 = Tex(r"And eventually it becomes a Gaussian in the asymptotic limit", color = BLACK).scale(0.7)
        explanation10.move_to(-3.5 * UP)
        self.play(FadeOut(explanation9), Write(explanation10))
        self.wait(2)

        # Updating explanation
        explanation11 = Tex(r"Choosing the peak of the posterior is an estimator in itself: MAP", color = BLACK).scale(0.65)
        explanation11.move_to(-3.5 * UP)
        self.play(FadeOut(explanation10), Write(explanation11))
        self.wait(2)

        # Updating explanation
        explanation12 = Tex(r"How do we formally define estimators? How can we construct them?", color = BLACK).scale(0.7)
        explanation12.move_to(-3.5 * UP)
        self.play(FadeOut(explanation11), Write(explanation12))

        self.wait(5)

'''
###########
##SCENE 6##
###########
'''

class Scene_6(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Results I}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.play(Write(title))
        self.wait(1)

        ######################################################

        # About the experiments
        subtitle = Tex('Posterior Density',color = royal_blue).scale(.9)
        subtitle.next_to(title, DOWN).to_edge(LEFT)
        self.play(FadeIn(subtitle))
        lines = []

        lines.append(tools().label(text = r'$\bullet$ "Flat" prior', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ $\tau_{SE} = 0.2$ ', color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ Full SWAP: $\tau_{SA} = \frac{\pi}{2}$ ', color = BLACK).scale(0.6).next_to(lines[1], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[0]), FadeIn(lines[1]), FadeIn(lines[2]))

        # Prior
        prior_plot = ImageMobject("assets/collisional/PriorPDF.png").scale(1)
        prior_plot.next_to(lines[1], RIGHT).shift(2*RIGHT)
        self.play(FadeIn(prior_plot))

        #PDF grid
        PDFGrid = ImageMobject("assets/collisional/PDFGrid.png").scale(1)
        PDFGrid.next_to(lines[2], DOWN).align_to(subtitle, LEFT).shift(DOWN)
        self.play(FadeIn(PDFGrid))

        # Arrow
        PDFGridArrow = Arrow(ORIGIN, 7*RIGHT).set_color(crimson)
        PDFGridArrow.next_to(PDFGrid, DOWN)
        PDFGridArrow_Label = Tex("Number of measured ancillas", color=crimson)
        PDFGridArrow_Label.scale(0.5).next_to(PDFGridArrow, DOWN)

        self.play(ShowCreation(PDFGridArrow), Write(PDFGridArrow_Label))
        self.wait(2)
        self.play(FadeOut(PDFGridArrow), FadeOut(PDFGridArrow_Label))

        # Fist slice
        highlight1 = Rectangle(width = 0.1, height = 2, color = crimson)
        tools().mob_pos(highlight1, x = -5.85, y = -1.6)
        self.play(GrowFromEdge(highlight1, LEFT))

        PDFPlot1 = ImageMobject("assets/collisional/PDFPlot1.png").scale(0.75)
        PDFPlot1.next_to(highlight1, DOWN)
        self.play(FadeIn(PDFPlot1))
        self.wait(2)
        self.play(FadeOut(PDFPlot1))

        # Second slice
        highlight2 = Rectangle(width = 0.1, height = 2, color = crimson)
        tools().mob_pos(highlight2, x = -5.45, y = -1.6)
        self.play(ReplacementTransform(highlight1, highlight2))

        PDFPlot2 = ImageMobject("assets/collisional/PDFPlot2.png").scale(0.75)
        PDFPlot2.next_to(highlight2, DOWN)
        self.play(FadeIn(PDFPlot2))
        self.wait(2)
        self.play(FadeOut(PDFPlot2))

        # Third slice
        highlight3 = Rectangle(width = 0.1, height = 2, color = crimson)
        tools().mob_pos(highlight3, x = -4.9, y = -1.6)
        self.play(ReplacementTransform(highlight2, highlight3))

        PDFPlot3 = ImageMobject("assets/collisional/PDFPlot3.png").scale(0.75)
        PDFPlot3.next_to(highlight3, DOWN)
        self.play(FadeIn(PDFPlot3))
        self.wait(2)
        self.play(FadeOut(PDFPlot3))

        # Fourth slice
        highlight4 = Rectangle(width = 0.1, height = 2, color = crimson)
        tools().mob_pos(highlight4, x = -3.9, y = -1.6)
        self.play(ReplacementTransform(highlight3, highlight4))

        PDFPlot4 = ImageMobject("assets/collisional/PDFPlot4.png").scale(0.75)
        PDFPlot4.next_to(highlight4, DOWN)
        self.play(FadeIn(PDFPlot4))
        self.wait(2)
        self.play(FadeOut(PDFPlot4), FadeOut(highlight4))

        # PDF Animation
        nPDF = 20
        loops = 4
        PDF_List = Group(*[ImageMobject('assets/collisional/PDFList'+str(i+1)+'.png').scale(1) for i in range(nPDF)])
        PDF_List.next_to(PDFGrid, RIGHT).shift(0.5*RIGHT)

        self.play(FadeIn(PDF_List[0]))
        for i in range(loops*nPDF - 1):
            self.wait(0.25)
            self.remove(PDF_List[i%nPDF])
            self.add(PDF_List[(i+1)%nPDF])

        # Erase Lines
        self.play(FadeOut(lines[0]), FadeOut(lines[1]), FadeOut(lines[2]), FadeOut(prior_plot))

        # Explanation on asymptotic limit
        lines=[]
        lines.append(tools().label(text = r'$\bullet$ The posterior becomes assymptotically Gaussian', color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle, LEFT))

        self.play(FadeIn(lines[0]))

        self.wait(5)

'''
###########
##SCENE 7##
###########
'''

class Scene_7(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Estimators}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.play(Write(title))
        self.wait(1)

        ######################################################

        # About estimators
        subtitle = tools().label(text = 'Definition', x = -5, y = 2.5, color = royal_blue).scale(.9)
        self.play(FadeIn(subtitle))
        lines = []

        lines.append(tools().label(text = r'$\bullet$ An estimator is an arbitrary function of the outcomes $X_1, ..., X_n$', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\hat{T} = f(X_1, ..., X_N)$', color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r"$\bullet$ It's a random variable itself", color = BLACK).scale(0.6).next_to(lines[1], DOWN).align_to(subtitle, LEFT))

        self.play(FadeIn(lines[0]),FadeIn(lines[1]),FadeIn(lines[2]))

        # About Bayesian Estimators
        subtitle2 = tools().label(text = 'Bayesian Estimators', x = -5, y = 2, color = royal_blue).scale(.9).next_to(lines[2], DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(subtitle2))

        # Bayesian estimator definition
        lines.append(Tex('A \emph{bayesian} estimator minimizes an ','error or risk function', color = BLACK).scale(0.6).next_to(subtitle2, DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[3]))

        # Error function definition
        error_func = MathTex("\epsilon =","{\displaystyle \int} dT P(T)","{\displaystyle \int}","C(\hat{T}, T)","P(X | T) dX",
                     color = BLACK).scale(0.6)
        error_func.move_to(-1 * UP)
        self.play(FadeIn(error_func))
        self.wait(1)

        # Error function explanation  - cost function
        explanation1 = Tex("It depends on a", " cost function", color = BLACK).scale(0.6)
        explanation1.move_to(-2 * UP)
        explanation1[1].set_color(crimson)
        self.play(FadeIn(explanation1), FadeToColor(error_func[3], crimson))
        self.wait(2)
        self.play(FadeOut(explanation1), FadeToColor(error_func[3], BLACK))

        # Error function explanation  - integrals
        explanation2 = Tex("It's integrated over the", " parameters", " and", " the data", color = BLACK).scale(0.6)
        explanation2.move_to(-2 * UP)
        explanation2[1].set_color(crimson)
        explanation2[3].set_color(royal_blue)
        self.play(FadeIn(explanation2), FadeToColor(error_func[1], crimson), FadeToColor(error_func[2], royal_blue), FadeToColor(error_func[4], royal_blue))
        self.wait(3)
        self.play(FadeOut(explanation2), FadeToColor(error_func[1], BLACK), FadeToColor(error_func[2], BLACK), FadeToColor(error_func[4], BLACK))

        # Error function explanation  - cost function
        explanation3 = Tex("Different estimators will minimize different cost functions/errors", color = BLACK).scale(0.6)
        explanation3.move_to(-2 * UP)
        self.play(FadeIn(explanation3))
        self.wait(2)
        self.play(FadeOut(explanation3))

        ######################################################

        # Estimators examples
        # MAP - moves the equation to the right
        self.play(error_func.animate.align_to(subtitle, LEFT))

        # Axis definition
        def show_axis(x0 = 0, y0 = 0, x_start = -0.01, x_end =  1, y_start = -0.01, y_end = 1):

            x_axis = Arrow((x_start + x0) * RIGHT + y0 * UP, (x_end + x0) * RIGHT + y0 * UP, buff = 0).set_color(BLACK)
            y_axis = Arrow((y_start + y0) * UP + x0 * RIGHT, (y_end + y0) * UP + x0 * RIGHT, buff = 0).set_color(BLACK)

            return x_axis, y_axis

        # Draws the axis
        axis_prior = show_axis(x0 = 1.25, y0 = -3.25, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2.5)
        self.play(ShowCreation(axis_prior[0]), ShowCreation(axis_prior[1]))
        xlabel_prior = tools().label(text = '$T$', x = 5.5, y = -3.25, color = BLACK).scale(0.5)
        ylabel_prior = tools().label(text = '$P(T)$', x = 1.75, y = -0.75, color = BLACK).scale(0.5)
        self.play(FadeIn(xlabel_prior), FadeIn(ylabel_prior))

        # Prior plot
        prior_plot = ParametricFunction(tools().flat, t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(prior_plot.scale(1), x = 2.25, y = -3.25)
        prior_plot.align_to(axis_prior[1], LEFT).shift(0.3 * UP + 0.2 * RIGHT)
        self.play(ShowCreation(prior_plot))
        self.wait(2)

        # Posterior plot
        sigma = 0.75
        mu = 0.5
        log_normal = lambda t: np.array([t, 3*1/(t*sigma*np.sqrt(2*np.pi))*np.exp(-(np.log(t) - mu)**2/(2*sigma**2)), 0])
        posterior_plot = ParametricFunction(log_normal, t_min = 0.01, t_max = 3.9, color = crimson, fill_opacity=0).scale(1)
        tools().mob_pos(posterior_plot.scale(1), x = 2.25, y = -2.9)
        posterior_plot.align_to(axis_prior[1], LEFT).shift(0.3 * UP + 0.2 * RIGHT)
        ylabel_posterior = tools().label(text = '$P(T | X)$', x = 1.8, y = -0.75, color = BLACK).scale(0.5)

        self.play(ReplacementTransform(ylabel_prior, ylabel_posterior))
        self.play(ReplacementTransform(prior_plot, posterior_plot))
        self.wait(2)

        # Estimator triangle
        estimator_triangle = RegularPolygon(3, start_angle=PI/2).scale(0.15)\
                            .move_to((1.25 + 0.93) * RIGHT - 3.5 * UP).set_color(BLACK) #The origin is at x = 1.25, I add the mode of the log normal
        MAP_line = DashedLine(estimator_triangle.get_center() + 0.25 * UP, estimator_triangle.get_center()+ 2 * UP, color = BLACK)

        # Initialization of the objects and MAP indicator
        MAP_indicator=MathTex("{\displaystyle\hat{T}_{MAP}}", color = BLACK).scale(0.45).next_to(MAP_line, 1 * UP)
        self.add(estimator_triangle, MAP_line)

        self.play(FadeIn(estimator_triangle),FadeIn(MAP_line))
        self.play(FadeIn(MAP_indicator))

        # MAP explanation
        MAP_explanation=tools().label(text=r"The mode minimizes the uniform cost", color = BLACK).scale(0.6).next_to(error_func, DOWN).align_to(error_func,LEFT)
        self.play(FadeIn(MAP_explanation))
        self.wait(2)

        ######################################################

        # Median indicator
        MED_line = DashedLine(estimator_triangle.get_center() + 0.25 * UP, estimator_triangle.get_center()+ 2 * UP, color = BLACK)
        self.play(estimator_triangle.animate.move_to((1.25 + 1.65) * RIGHT - 3.5 * UP),
                  MED_line.animate.shift((1.65 - 0.93) * RIGHT))
        MED_indicator=MathTex("{\displaystyle\hat{T}_{BM}}", color = BLACK).scale(0.45).next_to(MED_line, 1 * UP)

        self.add(MED_line)
        self.wait(1)
        self.play(FadeIn(MED_indicator))

        # Median explanation
        MED_explanation=tools().label(text=r"The median minimizes the absolute cost", color = BLACK).scale(0.6).next_to(error_func, DOWN).align_to(error_func,LEFT)
        self.play(FadeOut(MAP_explanation), FadeIn(MED_explanation))

        MED_cost = MathTex("C(\hat{T},T) = |\hat{T} - T|",
                     color = BLACK).scale(0.6).next_to(MED_explanation, DOWN).align_to(MED_explanation,LEFT)
        self.play(FadeIn(MED_cost))
        self.wait(1)

        ######################################################

        # Average indicator
        AVG_line = DashedLine(estimator_triangle.get_center() + 0.25 * UP, estimator_triangle.get_center()+ 2 * UP, color = BLACK)
        self.play(estimator_triangle.animate.move_to((1.25 + 2.18) * RIGHT - 3.5 * UP),
                  AVG_line.animate.shift((2.18 - 1.65) * RIGHT))
        AVG_indicator=MathTex("{\displaystyle\hat{T}_{BA}}", color = BLACK).scale(0.45).next_to(AVG_line, 1 * UP)

        self.add(AVG_line)
        self.wait(1)
        self.play(FadeIn(AVG_indicator))

        # Average explanation
        self.play(FadeOut(MED_explanation), FadeOut(MED_cost))

        # Highlight box
        result_hightlight = Rectangle(width = 7, height = 2.25, color = BLACK).next_to(error_func, DOWN).align_to(error_func,LEFT)
        result_hightlight = result_hightlight.set_fill(royal_blue, opacity = 0.4)
        self.play(ShowCreation(result_hightlight))

        AVG_explanation=tools().label(text=r"The posterior average minimizes the squared error", color = BLACK).scale(0.6).align_to(error_func, DOWN).align_to(error_func,LEFT).shift(.1 * RIGHT - .75 * UP)
        self.play(FadeIn(AVG_explanation))

        # Bayesian mean formulae
        AVG_cost = MathTex("C(\hat{T},T) = (\hat{T} - T)^2\\text{, and the estimator is}",
                     color = BLACK).scale(0.6).next_to(AVG_explanation, DOWN).align_to(AVG_explanation,LEFT)

        AVG_estimator = MathTex("\displaystyle{\hat{T}_{BA} = \int T P(T|X)dT}",
                     color = BLACK).scale(0.6).next_to(AVG_cost, DOWN).align_to(AVG_cost,LEFT).shift(7/4 * RIGHT)

        self.play(FadeIn(AVG_cost), FadeIn(AVG_estimator))
        self.wait(2)

        # Deletes the plot with a white rectangle above
        self.play(FadeIn(Rectangle(width = 4.5, height = 4.0, color = WHITE).to_edge(RIGHT).to_edge(DOWN).shift(LEFT + DOWN).set_fill(WHITE, opacity = 1.0)))

        ######################################################

        # Estimators
        Estimators = ImageMobject("assets/collisional/Estimators_presentation.png").scale(0.95)
        Estimators.to_edge(RIGHT).to_edge(DOWN).shift(LEFT + 0.5*DOWN)
        Estimators_label =Tex("Estimated Temperature", color = royal_blue).scale(0.6)
        Estimators_label.next_to(Estimators, UP)

        self.play(FadeIn(Estimators), Write(Estimators_label))

        self.wait(2)

        ######################################################

        # Rearranges the slide

        self.play(FadeOut(subtitle), FadeOut(lines[0]), FadeOut(lines[1]), FadeOut(lines[2]))
        result_group = VGroup(result_hightlight, AVG_explanation, AVG_cost, AVG_estimator)
        self.play(subtitle2.animate.align_to(subtitle, LEFT).align_to(subtitle, UP), run_time=0.5)
        self.play(error_func.animate.next_to(subtitle2, DOWN).align_to(subtitle2, LEFT), run_time=0.5)
        self.play(lines[3][0].animate.next_to(error_func, DOWN).align_to(error_func, LEFT), run_time=0.5)
        self.play(lines[3][1].animate.next_to(lines[3][0], DOWN).align_to(lines[3][0], LEFT), run_time=0.5)
        self.play(result_group.animate.next_to(error_func, RIGHT).shift(0.5*DOWN), run_time=0.5)

        ######################################################

        # Conditional error
        stochastic_mse_plot = ImageMobject("assets/collisional/StochasticMSE1c.png").scale(0.875)
        stochastic_mse_plot.to_edge(LEFT).to_edge(DOWN).shift(RIGHT + 0.5*DOWN)
        stochastic_mse_plot_label =Tex("$\\epsilon$ conditioned on $T_0 = 1.5\Omega$", color = royal_blue).scale(0.6)
        stochastic_mse_plot_label.next_to(stochastic_mse_plot, UP)

        self.play(FadeIn(stochastic_mse_plot), Write(stochastic_mse_plot_label))

        self.wait(2)

        self.play(FadeOut(stochastic_mse_plot), FadeOut(stochastic_mse_plot_label))
        self.play(FadeOut(Estimators), FadeOut(Estimators_label))

        ######################################################

        lines.append(Tex("The frequentist error (integrated on $\\boldsymbol{X}$) will depend on T", color = BLACK).scale(0.6).shift(0.5*DOWN))

        contidional_mse_plot = ImageMobject("assets/collisional/mseBA1b.png").scale(.75)
        contidional_mse_plot.next_to(lines[-1], DOWN)

        self.play(FadeIn(lines[-1]), FadeIn(contidional_mse_plot))

        self.wait(2)

        ######################################################

        self.play(contidional_mse_plot.animate.shift(4*LEFT))
        integration_arrow = Arrow(ORIGIN, 2 * RIGHT, buff = 0.1).set_color(BLACK)
        integration_arrow.next_to(contidional_mse_plot, RIGHT).shift(0.6*RIGHT)
        mse_integration = MathTex('\\displaystyle{\int...P(T)dT}', color=BLACK).next_to(integration_arrow, DOWN).scale(0.5).shift(0.5*UP)
        self.play(ShowCreation(integration_arrow), Write(mse_integration))

        lines.append(Tex("We can then integrate these curves on T to find the Bayesian error", color = BLACK).scale(0.6).shift(0.5*DOWN))
        self.play(ReplacementTransform(lines[-2],lines[-1]))

        mse_plot = ImageMobject("assets/collisional/VanTreesPlot1b.png").scale(1)
        mse_plot.move_to(contidional_mse_plot.get_center()).shift(8*RIGHT)
        self.play(FadeIn(mse_plot))

        ######################################################

        self.wait(5)

'''
###########
##SCENE 8##
###########
'''

class Scene_8(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{The Van-Trees inequality}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.play(Write(title))
        self.wait(1)

        ######################################################

        # About bayesian framework
        subtitle = tools().label(text = 'Bounds', x = -5, y = 2.5, color = royal_blue).scale(.9)
        self.play(FadeIn(subtitle))
        lines = []

        lines.append(tools().label(text = r'$\bullet$ How to evaluate performance?', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ How does this framework changes non-bayesian bounds?', color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle, LEFT))

        self.play(FadeIn(lines[0]),FadeIn(lines[1]))

        ######################################################

        # About frequentist approach
        subtitle2 = tools().label(text = 'Non-Bayesian Approach', color = royal_blue).scale(.9).next_to(lines[1], DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(subtitle2))

        lines.append(tools().label(text = 'Cramer-Rao bound', color = BLACK).scale(0.6).next_to(subtitle2, DOWN).align_to(subtitle2, LEFT))
        self.play(FadeIn(lines[2]))

        lines.append(tools().label(text = r'$\bullet$ A bound for the \emph{variance} of the estimator', color = BLACK).scale(0.6).next_to(lines[2], DOWN).align_to(subtitle2, LEFT))
        self.play(FadeIn(lines[3]))

        # Cramer Rao Bound
        CR_Bound = MathTex("\displaystyle{\\text{var} (\hat{\\theta}) \geqslant \\frac{1}{I(\\theta)}}",
                     color = BLACK).scale(0.6).align_to(lines[3], UP).shift(-.5*UP)

        self.play(Write(CR_Bound))
        self.wait(1)
        self.play(CR_Bound.animate.next_to(lines[3], DOWN))

        ######################################################

        # Axis definition
        def show_axis(x0 = 0, y0 = 0, x_start = -0.01, x_end =  1, y_start = -0.01, y_end = 1):

            x_axis = Arrow((x_start + x0) * RIGHT + y0 * UP, (x_end + x0) * RIGHT + y0 * UP, buff = 0).set_color(BLACK)
            y_axis = Arrow((y_start + y0) * UP + x0 * RIGHT, (y_end + y0) * UP + x0 * RIGHT, buff = 0).set_color(BLACK)

            return x_axis, y_axis

        # Draws the axis
        axis = show_axis(x0 = 1.25, y0 = -3.25, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2.5)
        self.play(ShowCreation(axis[0]), ShowCreation(axis[1]))
        xlabel = tools().label(text = '$n$', x = 5.5, y = -3.25, color = BLACK).scale(0.6)
        ylabel = tools().label(text = '$\sigma^2$', x = 1.25, y = -0.5, color = BLACK).scale(0.6)
        self.play(FadeIn(xlabel), FadeIn(ylabel))

        # Bound Plot w/ Dashed Line
        fisher_scaling = lambda t: np.array([t, 1.5 - t/4,0])
        CR_plot = DashedVMobject(ParametricFunction(fisher_scaling, t_min = 0.01, t_max = 3.5, color = BLACK, fill_opacity=0).scale(1))
        tools().mob_pos(CR_plot.scale(1), x = 2.25, y = -3.25)
        CR_plot.align_to(axis[1], LEFT).shift(0.5 * UP + 0.2 * RIGHT)
        self.play(ShowCreation(CR_plot))
        self.wait(2)

        # Variance example
        variance_scaling_ex = lambda t: np.array([t, 3 - np.log((t+1)/4),0])
        Var_plot = VGroup(ParametricFunction(variance_scaling_ex, t_min = 0.01, t_max = 3.5, color = crimson, fill_opacity=0).scale(1),
                          ParametricFunction(variance_scaling_ex, t_min = 0.01, t_max = 3.5, color = mediumseagreen, fill_opacity=0).scale(1).shift(0.25*UP),
                          ParametricFunction(variance_scaling_ex, t_min = 0.1, t_max = 3.5, color = ORANGE, fill_opacity=0).scale(1).shift(0.5*UP)
        )

        tools().mob_pos(Var_plot.scale(1), x = 2.25, y = -3)
        Var_plot.align_to(axis[1], LEFT).shift(UP + 0.2 * RIGHT)

        Var_plot_label = VGroup(Tex("$T_0$", color = crimson).next_to(Var_plot[0], RIGHT).scale(0.3),
                                Tex("$T_1$", color = mediumseagreen).next_to(Var_plot[1], RIGHT).scale(0.3),
                                Tex("$T_2$", color = ORANGE).next_to(Var_plot[2], RIGHT).scale(0.3)
        ).shift(0.75*DOWN + 0.2*LEFT)

        # Draws the variance curves
        self.play(ShowCreation(Var_plot[0]), FadeIn(Var_plot_label[0]))
        self.wait(2)

        # Variance explanation
        lines.append(tools().label(text = r'$\bullet$ $\sigma$ is parameter-dependent (in this framework)', color = BLACK).scale(0.6).next_to(CR_Bound, DOWN).align_to(subtitle2, LEFT))
        self.play(FadeIn(lines[4]))

        self.play(ShowCreation(Var_plot[1]), FadeIn(Var_plot_label[1]))
        self.play(ShowCreation(Var_plot[2]), FadeIn(Var_plot_label[2]))
        self.wait(2)

        lines.append(tools().label(text = r'$\bullet$ Assumes unbiased estimators - it is restrictive', color = BLACK).scale(0.6).next_to(lines[4], DOWN).align_to(subtitle2, LEFT))
        lines.append(tools().label(text = r'$\bullet$ What role does the prior plays here?', color = BLACK).scale(0.6).next_to(lines[5], DOWN).align_to(subtitle2, LEFT))

        self.play(FadeIn(lines[5]))
        self.play(FadeIn(lines[6]))
        self.wait(3)

        ######################################################

        # Frequentist Approach Deletion
        wrong_line1 = Line(-5*RIGHT - 2.5 * UP, +5*RIGHT + UP).set_color(crimson)
        wrong_line2 = Line(-5*RIGHT + UP, +5*RIGHT - 2.5 * UP).set_color(crimson)

        self.play(ShowCreation(wrong_line1))
        self.play(ShowCreation(wrong_line2))
        self.wait(1)

        self.play(FadeOut(subtitle2), FadeOut(lines[2]), FadeOut(lines[3]), FadeOut(lines[4]), FadeOut(lines[5]), FadeOut(lines[6]),
                  FadeOut(CR_Bound), FadeOut(wrong_line1), FadeOut(wrong_line2))

        self.play(FadeOut(axis[0]),FadeOut(axis[1]),FadeOut(CR_plot),FadeOut(Var_plot), FadeOut(Var_plot_label),
                  FadeOut(xlabel), FadeOut(ylabel))

        ######################################################

        # About the bayesian approach
        subtitle4 = tools().label(text = 'Bayesian Approach', color = royal_blue).scale(.9).next_to(lines[1], DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(subtitle4))
        lines = []

        ref = Tex('{\\footnotesize Harry L. Van. Trees and Kristine L. Bell. \emph{Detection Estimation and Modulation Theory,}', color = BLACK).scale(0.4).to_edge(LEFT).to_edge(DOWN).shift(0.4*DOWN)
        ref2 = Tex('{\\footnotesize2nd Edition, Part I. John Wiley \& Sons, 2013.}', color = BLACK).scale(0.4).next_to(ref).shift(0.1*LEFT)
        self.play(FadeIn(ref), FadeIn(ref2))

        lines.append(tools().label(text = r'$\bullet$ MSE $\rightarrow$ new figure of merit (average over $\boldsymbol{X}$ \emph{and} $\theta$)', color = BLACK).scale(0.6).next_to(subtitle4, DOWN).align_to(subtitle4, LEFT))
        lines.append(tools().label(text = r'$\bullet$ We can incorporate information from the Prior', color = BLACK).scale(0.6).next_to(lines[0], DOWN).align_to(subtitle4, LEFT))
        self.play(FadeIn(lines[0]))
        self.play(FadeIn(lines[1]))

        # Bayesian Cramer Rao Bound
        Van_trees = MathTex("\displaystyle{\\epsilon_{MSE} (\hat{\\theta}) \geqslant \\frac{1}{",
                            "\mathbb{E}_\lambda[I(\\theta)]"," +",
                            "I(\\lambda)}}",
                            color = BLACK).scale(0.6).align_to(lines[1], UP).shift(-.5*UP)

        self.play(Write(Van_trees))
        self.wait(1)

        # Van trees explanation
        prior_fisher = MathTex("I(\lambda) \equiv \int \\left(\\frac{\partial \\ln \lambda(\\theta)}{\partial \\theta}\\right)^2 \lambda(\\theta)d\\theta ",
                            color = crimson).scale(0.6).align_to(Van_trees, UP).shift(-UP - 3 * RIGHT)

        Van_trees_explanation1 = Tex("The bound takes into account the initial information from the", " prior", color = BLACK).scale(0.6).shift(-3 * UP)
        Van_trees_explanation1[1].set_color(crimson)
        self.play(Write(prior_fisher), Write(Van_trees_explanation1), FadeToColor(Van_trees[3],crimson))
        self.wait(2)

        fisher = MathTex("\mathbb{E}_\lambda[I(\\theta)] \equiv \int \lambda(\\theta)d\\theta \int \\left(\\frac{\partial \\ln P(\\theta|x)}{\partial \\theta}\\right)^2 P(\\theta|x)dx ",
                            color = crimson).scale(0.6).align_to(Van_trees, UP).shift(-UP + 2.5 * RIGHT)
        Van_trees_explanation2 = Tex("And the Fisher information averaged over the", " parameter", color = BLACK).scale(0.6).shift(-3 * UP)
        Van_trees_explanation2[1].set_color(crimson)
        self.play(FadeOut(Van_trees_explanation1),
                  Write(fisher), Write(Van_trees_explanation2),
                  FadeToColor(Van_trees[3], BLACK),  FadeToColor(prior_fisher, BLACK), FadeToColor(Van_trees[1],crimson))
        self.wait(2)

        self.play(FadeOut(Van_trees_explanation2),
                  FadeToColor(fisher, BLACK),  FadeToColor(Van_trees[1],BLACK))
        self.wait(2)

        self.play(FadeOut(ref), FadeOut(ref2))

        ######################################################

        # Highlight box
        bayes_highlight = Rectangle(width = 12, height = 1, color = BLACK).to_edge(0.5*DOWN)
        bayes_highlight = bayes_highlight.set_fill(royal_blue, opacity = 0.4)
        self.play(ShowCreation(bayes_highlight))

        bayes_highlight_explanation=tools().label(text=r"\textbf{Message:} we want a thermometer which is good for a wide range of temperatures $\rightarrow$ the Bayesian MSE is appropriate", color = BLACK).scale(0.6).move_to(bayes_highlight.get_center())
        self.play(FadeIn(bayes_highlight_explanation))

        self.wait(5)

'''
###########
##SCENE 9##
###########
'''

class Scene_9(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Results II}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.add(title)
        self.wait(1)

        ######################################################

        # About the experiments
        subtitle = Tex('Plotting the error',color = royal_blue).scale(.9)
        subtitle.next_to(title, DOWN).to_edge(LEFT)
        self.play(FadeIn(subtitle))
        lines = []

        lines.append(tools().label(text = r'$\bullet$ The asymptotic limit may be different from the asymptotic Van Trees', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[-1]))

        ######################################################

        MSEPlot1 = ImageMobject("assets/collisional/VanTreesPlot1b.png").scale(1).next_to(lines[-1], DOWN)
        self.play(FadeIn(MSEPlot1))

        self.wait(1)

        MSEPlot1_bound = ImageMobject("assets/collisional/VanTreesPlot1d.png").scale(1).next_to(lines[-1], DOWN)
        self.play(FadeOut(MSEPlot1), FadeIn(MSEPlot1_bound))

        self.wait(2)

        self.play(FadeOut(MSEPlot1_bound))

        ######################################################

        lines.append(tools().label(text = r'$\bullet$ We fix the temperature for some tests $T_0 = 1.5 \Omega$', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[-1]))

        MSEPlot2 = ImageMobject("assets/collisional/tSAPlot1.png").scale(1).next_to(lines[-1], DOWN).align_to(subtitle,LEFT)
        self.play(FadeIn(MSEPlot2))

        MSEPlot3 = ImageMobject("assets/collisional/tSAPlot2.png").scale(1).next_to(MSEPlot2, RIGHT)
        self.play(FadeIn(MSEPlot3))

        ######################################################

        self.wait(5)

'''
##############
##CONCLUSION##
##############
'''

class Conclusion(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Conclusion}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.add(title)
        self.wait(1)

        ######################################################

        subtitle = Tex('---',color = WHITE).scale(.9)
        subtitle.next_to(title, DOWN).to_edge(LEFT)
        self.play(FadeIn(subtitle))
        lines = []

        lines.append(tools().label(text = r'$\bullet$ Collisional Models are a natural platform to perform thermometry', color = BLACK).scale(0.6).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ We can use Bayesian inference to explicitly construct estimators', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ The bayesian framework provides a concise and practical formalism', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'to evaluate their performance', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'$\bullet$ We can construct bayesian analogues to frequentist bounds', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'(e.g. Cramer Rao $\rightarrow$ Van Trees)', color = BLACK).scale(0.6).next_to(lines[-1], DOWN).align_to(subtitle, LEFT))

        self.play(FadeIn(lines[0]), FadeIn(lines[1]), FadeIn(lines[2]), FadeIn(lines[3]), FadeIn(lines[4]), FadeIn(lines[5]))

        self.wait(5)

'''
##############
##REFERENCES##
##############
'''

class References(Scene):
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{Thank you!}', x = 0, y = 3, color = royal_blue).scale(1.1)
        Underline(title)

        self.add(title)

        ######################################################

        # About the experiments
        subtitle = Tex('References',color = royal_blue).scale(.9)
        subtitle.next_to(title, DOWN).to_edge(LEFT)
        self.add(subtitle)

        #references_img = ImageMobject("assets/collisional/references.png").scale(2).next_to(subtitle, DOWN).align_to(subtitle, LEFT)
        #self.add(references_img)

        lines=[]
        lines.append(Text('Edwin  T.  Jaynes  and  G.  Larry  Bretthorst.Probability  theory:   the  logic  ofscience.  Cambridge Univ. Press, 2019', color = BLACK).scale(0.3).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        lines.append(Text('Stella  Seah,  Stefan  Nimmrichter,  Daniel  Grimmer,  Jader  P.  Santos,  ValerioScarani, and Gabriel T. Landi. Collisional quantum thermometry.Phys. Rev.Lett., 123:180602, Oct 2019', color = BLACK).scale(0.3).next_to(lines[-1], DOWN).align_to(lines[-1], LEFT))
        lines.append(Text('MP Shutzenberger.  A generalization of the fr ́echet-cram ́er inequality to thecase of bayes estimation.Bull. Amer. Math. Soc, 63(142), 1957.', color = BLACK).scale(0.3).next_to(lines[-1], DOWN).align_to(lines[-1], LEFT))
        lines.append(Text('Harry L. Van. Trees and Kristine L. Bell.Detection Estimation and Modula-tion Theory, 2nd Edition, Part I.  John Wiley & Sons, 2013.', color = BLACK).scale(0.3).next_to(lines[-1], DOWN).align_to(lines[-1], LEFT))

        self.add(lines[0], lines[1], lines[2], lines[3])

        ######################################################

        # Group Logo
        group_logo = ImageMobject("logo.png").scale(0.75)
        group_logo.to_edge(RIGHT, buff=1.5)
        self.add(group_logo)

        self.wait(5)
