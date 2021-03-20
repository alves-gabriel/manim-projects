from manim import *
import numpy as np

# ffmpeg -f concat -safe 0 -i files.txt -c copy output.mp4

config.background_color = WHITE

'''
AUXILIARY FUNCTIONS
'''

# Colors
# https://www.w3schools.com/colors/colors_picker.asp
mediumseagreen = '#3CB371'
royal_blue = '#4169E1'
crimson = '#DC143C'

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
##SCENE 1##
###########
'''

class Scene_1(Scene):

    # Constructs the scene
    def construct(self):

        # Title
        title = tools().label(text = '\\underline{The model}', x = 0, y = 3, color = royal_blue).scale(2)
        Underline(title)

        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

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
        swap_label2 = tools().label(text = r'$U = U_{SWAP} = \exp \left( - i V \tau_{SA} \right)$', x = 2, y = -1.2, color = BLACK).scale(0.5)
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
        d_highlight = tools().label(text = 'Detection Record', x = -4.6, y = 1, color = royal_blue).scale(1)
        self.play(Write(d_highlight))

        ######################################################

        # Thermal map and unitaries
        thermal_map = tools().label(text = r'$\rho_S^n = \tr_{A_n}\{U^\dagger \mathcal{E}(\rho_S^{n-1} \otimes \rho_{A_n}) U\}$', x = 0, y = -3, color = BLACK).scale(0.5)
        self.play(Write(thermal_map))
        self.wait(1)

        # Hightlights the stroboscopic map
        d_highlight = Rectangle(width = 3.75, height = .75, color = crimson)
        tools().mob_pos(d_highlight, x = 0, y = -3)
        self.play(ShowCreation(d_highlight))

        # Highlight
        d_highlight = tools().label(text = 'Stroboscopic Map', x = 0, y = -3.75, color = crimson).scale(.5)
        self.play(Write(d_highlight))

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
        title = tools().label(text = 'The Receipt', x = 0, y = 3, color = royal_blue).scale(2)
        title = Underline(title)
        subtitle = tools().label(text = 'The Model', x = -5, y = 2, color = royal_blue).scale(1)

        # Text lines
        lines = []

        self.play(Write(title))
        self.play(Write(subtitle))

        ######################################################

        # Text
        lines.append(tools().label(text = r' $\bullet$ SE map + SA unitary ' + r'$\rightarrow$ Stroboscopic Map', color = BLACK).scale(0.7).next_to(subtitle, DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[0]))

        lines.append(tools().label(text = r'$\rho_S^n = \Phi(\rho) := \tr_{A_n}\{U^\dagger \mathcal{E}(\rho_S^{n-1} \otimes \rho_{A_n}) U\}$' , color = BLACK).scale(0.7).next_to(lines[0], DOWN).align_to(subtitle, LEFT))
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
        lines.append(tools().label(text = r'$\bullet$ Ancilla measurements after the', color = BLACK).scale(0.7).next_to(lines[1], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'system reaches the \emph{steady state}:', color = BLACK).scale(0.7).next_to(lines[2], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[2]), FadeIn(lines[3]))

        lines.append(tools().label(text = r'$\rho_{S}^* = \Phi(\rho_{S}^*)$', color = BLACK).scale(0.7).next_to(lines[3], DOWN).align_to(subtitle, LEFT))
        lines[4].shift(0.25*RIGHT)
        self.play(FadeIn(lines[4]))

        self.play(FadeOut(system_label))
        system_label = tools().label(text = r'$\rho_{S}^*$', x = 4, y = 0, color = royal_blue)
        self.play(FadeIn(system_label))

        ######################################################

        # Text
        lines.append(tools().label(text = r'$\bullet$ Local or joint measurements', color = BLACK).scale(0.7).next_to(lines[4], DOWN).align_to(subtitle, LEFT))
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

        self.play(ShowCreation(local_measurement))
        self.play(FadeOut(local_measurement))

        self.play(ShowCreation(global_measurement))

        self.wait(1)

        ######################################################

        # Text
        lines.append(tools().label(text = r'$\bullet$ Probability distribution associated with', color = BLACK).scale(0.7).next_to(lines[5], DOWN).align_to(subtitle, LEFT))
        lines.append(tools().label(text = r'the measurements in the SS:', color = BLACK).scale(0.7).next_to(lines[6], DOWN).align_to(subtitle, LEFT))
        self.play(FadeIn(lines[6]), FadeIn(lines[7]))

        lines.append(tools().label(text = r'$p(X_i|T) = \tr\{M_i \rho_{A_1...A_n}^* M_i^\dagger\}$', color = BLACK).scale(0.7).next_to(lines[7], DOWN).align_to(subtitle, LEFT))
        lines[8].shift(0.25*RIGHT)
        self.play(FadeIn(lines[8]))

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
        title = tools().label(text = '\\underline{Thermometry}', x = 0, y = 3, color = royal_blue).scale(2)
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
        title = tools().label(text = '\\underline{Bayes Theorem}', x = 0, y = 3, color = royal_blue).scale(2)
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

        ######################################################

        #Bayes Theorem proof
        bayes = MathTex(
            "P(x_1,x_2)=P(x_1|x_2)P(x_2)=P(x_2|x_1)P(x_1)",
            color = BLACK,
            tex_to_color_map={r"x_1": crimson, r"x_2": royal_blue}
        )

        self.play(Write(bayes))

        # Bayes Theorem
        bayes2 = MathTex(
            "P(x_1|x_2)={ P(x_2|x_1)P(x_1) \\over P(x_2)}",
            color = BLACK,
            tex_to_color_map={r"x_1": crimson, r"x_2": royal_blue}
        )
        bayes2.align_to(bayes, DOWN).shift(2 * DOWN)
        self.play(Write(bayes2))
        self.play(FadeOut(bayes))

        # Explanation 1
        bayes_explanation = Tex(r'We usually speak in terms of ', r'hypothesis', ' and ', r'evidence', x = 0, y = 1, color = BLACK).scale(0.75)
        bayes_explanation[1].set_color(crimson)
        bayes_explanation[3].set_color(royal_blue)
        self.play(Write(bayes_explanation))

        # Bayes Theorem
        bayes3 = MathTex(
            "P(H|E)={ P(E|H)P(H) \\over P(H)}",
            color = BLACK,
            tex_to_color_map={r"H": crimson, r"E": royal_blue}
        )
        bayes3.align_to(bayes, DOWN).shift(2 * DOWN)
        self.play(FadeOut(bayes2), FadeIn(bayes3))

        # Explanation 2
        bayes_explanation2 = Tex(r'i.e. what are the odds of confirming the ', r'hypothesis', ' given the ', r'evidence','?', color = BLACK).scale(0.75)
        bayes_explanation2.move_to(-3 * UP)
        bayes_explanation2[1].set_color(crimson)
        bayes_explanation2[3].set_color(royal_blue)
        self.play(Write(bayes_explanation2))
        self.wait(1)

        # Explanation 3
        bayes_explanation3 = Tex(r'Here, we consider the parameter, the ', r'temperature', ' and the observed ', r'data', x = 0, y = 1, color = BLACK).scale(0.75)
        bayes_explanation3[1].set_color(crimson)
        bayes_explanation3[3].set_color(royal_blue)
        self.play(FadeOut(bayes_explanation), Write(bayes_explanation3))

        # Bayes Theorem
        bayes4 = MathTex(
            "P(T|D)","={"," P(D|T)","P(T)"," \\over"," P(D)}",
            color = BLACK,
            tex_to_color_map={r"T": crimson, r"D": royal_blue}
        )
        bayes4.align_to(bayes, DOWN).shift(2 * DOWN)
        self.play(FadeOut(bayes3), FadeIn(bayes4))

        # Explanation 4
        bayes_explanation4 = Tex(r'What are the odds of measuring a certain ', r'temperature', ' given the ', r'data/measurement record','?', color = BLACK).scale(0.75)
        bayes_explanation4.move_to(-3 * UP)
        bayes_explanation4[1].set_color(crimson)
        bayes_explanation4[3].set_color(royal_blue)
        self.play(FadeOut(bayes_explanation2), Write(bayes_explanation4))
        self.wait(4)

        # Highlights - Prior
        framebox1 = SurroundingRectangle(bayes4[11:14], buff = .05).set_color(crimson)
        framebox1_label = Tex('Prior', color = crimson).scale(0.7)
        framebox1_label.next_to(framebox1, UP)
        self.play(ShowCreation(framebox1), Write(framebox1_label))
        self.wait(1)

        bayes_explanation5 = Tex(r'The prior represents our initial state-of-knowledge about the temperature', color = BLACK).scale(0.75)
        bayes_explanation5.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation4), Write(bayes_explanation5))
        self.wait(4)

        # Highlights - Likelihood
        framebox2 = SurroundingRectangle(bayes4[6:11], buff = .05).set_color(crimson)
        framebox2_label = Tex('Likelihood', color = crimson).scale(0.7)
        framebox2_label.next_to(framebox2, UP)
        self.play(ReplacementTransform(framebox1, framebox2), Write(framebox2_label), FadeOut(framebox1_label))
        self.wait(1)

        bayes_explanation6 = Tex(r'How likely we are of observing D at a certain temperature T', color = BLACK).scale(0.75)
        bayes_explanation6.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation5), Write(bayes_explanation6))
        self.wait(4)

        # Highlights - Normalization
        framebox3 = SurroundingRectangle(bayes4[15:18], buff = .05).set_color(crimson)
        framebox3_label = Tex('Normalization', color = crimson).scale(0.7)
        framebox3_label.next_to(framebox3, RIGHT)
        self.play(ReplacementTransform(framebox2, framebox3), Write(framebox3_label), FadeOut(framebox2_label))
        self.wait(1)

        bayes_explanation7 = Tex(r'How likely we are of observing D, but \emph{irrespective} of T: a marginal distribution', color = BLACK).scale(0.75)
        bayes_explanation7.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation6), Write(bayes_explanation7))
        self.wait(4)

        # Highlights - Normalization
        framebox4 = SurroundingRectangle(bayes4[0:5], buff = .05).set_color(crimson)
        framebox4_label = Tex('Posterior', color = crimson).scale(0.7)
        framebox4_label.next_to(framebox4, UP)
        self.play(ReplacementTransform(framebox3, framebox4), Write(framebox4_label), FadeOut(framebox3_label))
        self.wait(1)

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
        title = tools().label(text = '\\underline{An example}', x = 0, y = 3, color = royal_blue).scale(2)
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
        d_record.append(MathTex("X_1 = 0", color = royal_blue).scale(0.7))
        d_record[0].align_to(distribution_text, DOWN)
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
        posterior1 = ParametricFunction(self.fermi_dirac0, t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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
        self.add(estimator_triangle,decimal, estimator_line)
        self.play(FadeIn(estimator_triangle),FadeIn(estimator_line),FadeIn(decimal))

        ######################################################

        # Updating explanation
        explanation6 = Tex(r"How to further update our knowledge after performing more measurements?", color = BLACK).scale(0.7)
        explanation6.move_to(-3.5 * UP)
        self.play(FadeOut(explanation5), Write(explanation6))

        # Second outcome
        d_record.append(MathTex("X_2 = 0", color = royal_blue).scale(0.7))
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
        posterior2 = ParametricFunction(lambda t: np.array([t,(1-2*1/(1+np.exp(1/t)))**2,0]), t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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
        posterior3 = ParametricFunction(lambda t: np.array([t,3*(1-1/(1+np.exp(1/t)))**2 * (1/(1+np.exp(1/t)))**1,0]), t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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
        d_record.append(MathTex("X_4 = 0", color = royal_blue).scale(0.7))
        d_record[3].next_to(d_record[2], RIGHT)
        self.play(FadeIn(d_record[3]))
        self.wait(2)

        # Draws the 4th posterior
        posterior4 = ParametricFunction(lambda t: np.array([t,5*(1-1/(1+np.exp(1/t)))**3 * (1/(1+np.exp(1/t)))**1,0]), t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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
        posterior5 = ParametricFunction(lambda t: np.array([t,500000000000*(1-1/(1+np.exp(1/t)))**36 * (1/(1+np.exp(1/t)))**12,0]), t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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
        posterior_gaussian = ParametricFunction(lambda t: np.array([t,2*np.exp(-(t-0.91)**2/(2*0.0025)),0]), t_min = 0.01, t_max = 2.5, color = crimson, fill_opacity=0).scale(1)
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

def Scene_6(Scene):
    def construct(self):
        pass
