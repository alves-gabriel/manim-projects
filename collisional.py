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

'''
SCENES
'''

class Scene_1(Scene):

    # Constructs the scene
    def construct(self):

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

        self.wait(1)

        ######################################################

        # Draws the equipment
        detector = ImageMobject("detector_img").scale(0.25)
        detector_line = Line(detector.get_center(), detector.get_center()-0.01*RIGHT + 0.35*UP).set_color(RED)
        self.add(detector)
        tools().mob_pos(detector, x = -3, y = -.5)

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
        outcome = tools().label(text = r'$0$', x = -3, y = .5, color = BLACK).scale(1)
        self.play(FadeIn(outcome))
        self.wait(1)

        # Writes the detection record vector and erturns the needle to the middle
        d_record = tools().label(text = r'$D = ($', x = -6, y = 2, color = BLACK).scale(1)
        self.play(Write(d_record))
        self.play(outcome.animate.align_to(d_record, UP).align_to(d_record, RIGHT).shift(0.25 * RIGHT, -0.05 * UP))
        self.play(detector_line.animate.rotate(angle = -PI/4, about_point = detector.get_center() - 0.01*RIGHT))

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
            outcome_new = tools().label(text = r'$%d$' %detection_record[i+1], x = -3, y = .5, color = BLACK).scale(1)
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
            "P(H|E)={ P(H|E)P(E) \\over P(H)}",
            color = BLACK,
            tex_to_color_map={r"E": crimson, r"H": royal_blue}
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
            "P(T|D)={"," P(D|T)","P(T)"," \\over"," P(D)}",
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
        framebox1 = SurroundingRectangle(bayes4[10:13], buff = .05).set_color(crimson)
        framebox1_label = Tex('Prior', color = crimson).scale(0.7)
        framebox1_label.next_to(framebox1, UP)
        self.play(ShowCreation(framebox1), Write(framebox1_label))
        self.wait(1)

        bayes_explanation5 = Tex(r'The prior represents our initial state-of-knowledge about the temperature', color = BLACK).scale(0.75)
        bayes_explanation5.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation4), Write(bayes_explanation5))
        self.wait(4)

        # Highlights - Likelihood
        framebox2 = SurroundingRectangle(bayes4[5:10], buff = .05).set_color(crimson)
        framebox2_label = Tex('Likelihood', color = crimson).scale(0.7)
        framebox2_label.next_to(framebox2, UP)
        self.play(ReplacementTransform(framebox1, framebox2), Write(framebox2_label), FadeOut(framebox1_label))
        self.wait(1)

        bayes_explanation6 = Tex(r'How likely we are of observing D at a certain temperature T', color = BLACK).scale(0.75)
        bayes_explanation6.move_to(-3 * UP)
        self.play(FadeOut(bayes_explanation5), Write(bayes_explanation6))
        self.wait(4)

        # Highlights - Normalization
        framebox3 = SurroundingRectangle(bayes4[14:17], buff = .05).set_color(crimson)
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

class Scene_5(Scene):

    # Fermi dirac distribution: 1-f and f
    def fermi_dirac0(self, t):

        return np.array((t, (1-2*1/(1+np.exp(1/t))), 0))

    def fermi_dirac1(self, t):

        return np.array((t, 2*1/(1+np.exp(1/t)), 0))

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

        self.play(Write(explanation))
        self.wait(2)

        # Bayes Theorem
        bayes = MathTex(
            "P(T|X_1)={"," P(X_1|T)","P(T)"," \\over"," \mathcal{N}}",
            color = BLACK
        ).scale(0.7)
        bayes.align_to(thermal_state, DOWN).shift(2 * RIGHT)
        self.play(FadeIn(bayes))

        # Likelihood and prior highlight
        framebox1 = SurroundingRectangle(bayes[1], buff = .1).set_color(crimson)
        framebox2 = SurroundingRectangle(bayes[2], buff = .1).set_color(crimson)

        self.play(ShowCreation(framebox1))

        # Explanation 1
        explanation1 = Tex('Likelihood: how likely we are to measure the qubit in the ','ground',' or in the ','excited', ' state').set_color(BLACK).scale(0.7)
        explanation1.move_to(-3.5 * UP)
        explanation1[1].set_color(ORANGE)
        explanation1[3].set_color(royal_blue)

        self.play(FadeOut(explanation), Write(explanation1))


        ######################################################

        ######################################################

        self.wait(5)
