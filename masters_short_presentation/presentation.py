from manim import *
import numpy as np
import random
import copy

'''
Play with

manim -pqh presentation.py <scene-name>
'''

'''
AUXILIARY FUNCTIONS
'''

# Background default color
config.background_color = WHITE

# Colors
MSEAGREEN = '#3CB371'
MSEAGREEN_RGB =  np.array([60, 179, 113])/255
ROYALBLUE = '#4169E1'
ROYALBLUE_RGB = np.array([65, 105, 225])/255
CRIMSON = '#DC143C'
CRIMSON_RGB = np.array([220, 20, 60])/255
ROYALPURPLE = '#7851a9'
BURNTORANGE = '#cc5500'
BURNTORANGE_RGB = np.array([204, 85, 0])/255
GOLDENROD = '#daa520'
DARKRED = '##990000'
DARKRED_RGB = np.array([153, 0, 0])/255
LIGHTBLUE= '#ADD8E6'
LIGHTBLUE_RGB= np.array([173, 216, 230])/255

# Convex combination in the hue to lighten the colors. Factor should be between 0 and 1
def tint(rgb, factor):
    return rgb + (1 - rgb)*factor

# Darkens the colors
def shade(rgb, factor):
    return rgb*(1 - factor)

# Draws a pretty rectangle with a slight gradient from the borders
def PrettyQubit(qradius, color):
    return VGroup(

        # Qubit (sphere) coloring
        Circle(radius=qradius, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        Circle(radius=0.9*qradius, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1)\
        .shift(0.05*qradius*UP + 0.05*qradius*LEFT),

        Circle(radius=0.8*qradius, \
        color = rgb_to_color(tint(color, 0.2))).set_fill(rgb_to_color(tint(color, 0.3)), opacity=1)\
        .shift(0.1*qradius*UP + 0.1*qradius*LEFT),

        # Atom drawing
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2),
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2).rotate(PI / 3),
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2).rotate(-PI / 3),
        Dot(point=ORIGIN, radius=0.04)
    )

def PrettySquare(len, color):
    return VGroup(

        # Qubit (sphere) coloring
        RoundedRectangle(corner_radius=0.2*len, height=len, width=len, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        RoundedRectangle(corner_radius=0.2*len, height=0.9*len, width=0.9*len, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1),

        RoundedRectangle(corner_radius=0.2*len, height=0.8*len, width=0.8*len, \
        color = rgb_to_color(tint(color, 0.2))).set_fill(rgb_to_color(tint(color, 0.3)), opacity=1),

        # Atom drawing
        Ellipse(width=.6, height=.3, color=WHITE, stroke_width=2),
        Ellipse(width=.6, height=.3, color=WHITE, stroke_width=2).rotate(PI / 3),
        Ellipse(width=.6, height=.3, color=WHITE, stroke_width=2).rotate(-PI / 3),
        Dot(point=ORIGIN, radius=0.04)
    )

def MovingParticle(qradius, color):

    conv_color=rgb_to_color(color)

    def particle(valOpacity):
        return Circle(radius=qradius).set_stroke(color=conv_color, opacity=valOpacity, width=5)\
        .set_fill(rgb_to_color(tint(color, 0.2)), opacity=valOpacity)

    return VGroup(

        # Shadows
        particle(0.33).shift(1.6*qradius*LEFT),
        particle(0.66).shift(0.8*qradius*LEFT),

        # Particle
        particle(1.0)
    )

def Bath(color):

    # Gradient background
    background=Circle(fill_opacity=.5, radius=.98)
    background.set_color(color=[rgb_to_color(MSEAGREEN_RGB),WHITE])
    color_direction=[1,1,0]
    background.set_sheen_direction(color_direction)

    return VGroup(
        background,

        # Reservoir border
        DashedVMobject(Circle(radius=1, color=BLACK), dashed_ratio=0.5),

        # Moving particle (with shadow effect)
        MovingParticle(.15, MSEAGREEN_RGB).shift(0.0*RIGHT+0.5*UP),
        MovingParticle(.15, MSEAGREEN_RGB).shift(.7*RIGHT+.25*UP).rotate(PI/4),
        MovingParticle(.15, MSEAGREEN_RGB).shift(-.5*RIGHT+.1*UP).rotate(-PI/8),
        MovingParticle(.15, MSEAGREEN_RGB).shift(.1*RIGHT-.2*UP).rotate(PI/2),
        MovingParticle(.15, MSEAGREEN_RGB).shift(-.3*RIGHT-.5*UP).rotate(-PI/6),
        MovingParticle(.15, MSEAGREEN_RGB).shift(.5*RIGHT-.5*UP).rotate(1.25*PI)
    )

def show_axis(x0 = 0, y0 = 0, x_start = -0.01, x_end =  1, y_start = -0.01, y_end = 1):

    x_axis = Arrow((x_start + x0) * RIGHT + y0 * UP, (x_end + x0) * RIGHT + y0 * UP, buff = 0).set_color(BLACK)
    y_axis = Arrow((y_start + y0) * UP + x0 * RIGHT, (y_end + y0) * UP + x0 * RIGHT, buff = 0).set_color(BLACK)

    return x_axis, y_axis

# Draws the bernoulli distribution
def likelihood_dist(norm, m, n):
    return  ParametricFunction(\
    lambda t: np.array([t,norm*(1-1/(1+np.exp(1/t)))**m * (1/(1+np.exp(1/t)))**n, 0])\
    , t_range = [0.01, 3.5], color = rgb_to_color(BURNTORANGE_RGB), fill_opacity=0)

'''
############
###SCENES###
############
'''

# Qubits interacting
class scene_0(Scene):
    def construct(self):

        # Qubit - System
        qubit_system = PrettyQubit(.5, ROYALBLUE_RGB)
        qubit_system.shift(0*LEFT + 0*UP)
        qubit_system_label = Tex(r'$S$', color = BLACK).next_to(qubit_system, RIGHT)

        # Bath
        qubit_bath = Bath(MSEAGREEN_RGB).shift(0*LEFT + 2.5*UP)
        qubit_bath_label = Tex(r'$E$', color = BLACK).next_to(qubit_bath, RIGHT)

        # Draws the ancillae trail
        n_ancillae = 4
        ancilla_trail = []
        ancilla_trail_label = []
        
        ancilla_trail.append(PrettySquare(1, CRIMSON_RGB).shift(0*LEFT - 2*UP))
        ancilla_trail_label.append(Tex(r'$A_1$', color = BLACK).next_to(ancilla_trail[0], DOWN))

        # Adding them
        self.play(FadeIn(qubit_system), FadeIn(qubit_bath), FadeIn(ancilla_trail[0]))
        self.play(Write(qubit_system_label), Write(qubit_bath_label), Write(ancilla_trail_label[0]))

        # Interaction        
        interaction = ParametricFunction(lambda t:np.array((np.sin(25*t)/8, t, 0)), \
        t_range = np.array([0,1]), color = BLACK, fill_opacity=0)
        interaction.move_to(qubit_bath.get_center() + 1.5*DOWN)

        # SE interaction label
        SEint_label = Tex(\
        r'$\mathcal{L}(\rho) = i [\rho, H] + (n + 1) D[\sigma_-] + n D[\sigma_+]$'\
        ,color = BLACK).move_to(interaction.get_center() + 3.25*RIGHT).scale(0.6)

        self.play(Create(interaction), Write(SEint_label))

        # Draws the SWAP interaction with two arrows
        SWAP1 = CurvedArrow(0, -1*UP, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP2 = CurvedArrow(-1*UP, 0, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP1.move_to(-0.2*RIGHT - UP)
        SWAP2.move_to(+0.2*RIGHT - UP)
        self.play(FadeIn(SWAP1), FadeIn(SWAP2))

        # Flips the SWAP arrows
        self.play(SWAP1.animate.rotate(np.pi, axis = RIGHT), SWAP2.animate.rotate(np.pi, axis = RIGHT))

        # SWAP label, aligned to the SE interaction label
        swap_label = Tex(r'$V = \sigma_ + \otimes \sigma_- + \sigma_- \otimes \sigma_+$'\
        ,color = BLACK).scale(0.6)
        swap_label.align_to(SEint_label, LEFT).shift(DOWN)
        self.play(Write(swap_label))

        # Maps and unitaries
        SEint_label2 = Tex(r'$\mathcal{E}(\rho) = e^{\mathcal{L} \tau_{SE}}(\rho)$'\
        ,color = BLACK).scale(0.5)
        SEint_label2.next_to(SEint_label, DOWN)

        swap_label2 = Tex(r'$U = \exp \left( - i V \tau_{SA} \right)$'\
        ,color = BLACK).scale(0.5)
        swap_label2.next_to(swap_label, UP)

        self.play(Write(SEint_label2), Write(swap_label2))

        # Highlights tSA and tSE
        frameLindblad = SurroundingRectangle(SEint_label2, CRIMSON)
        frameSWAP = SurroundingRectangle(swap_label2, CRIMSON)
        self.play(Create(frameLindblad), Create(frameSWAP))

        ######################################################

        # Draws the equipment
        detector = ImageMobject("detector_img").scale(0.25)
        detector.move_to(-3*RIGHT-0.75*UP)
        self.add(detector)

        # Creates a needle in the detector
        proble_angle=PI/2
        detector_line = Line(detector.get_center() - 0.01*RIGHT, detector.get_center() + 0.35*UP)
        detector_line.set_color(RED)
        detector_line.rotate(angle = proble_angle/2, about_point = detector.get_center())
        self.add(detector_line)
        self.play(FadeIn(detector_line), FadeIn(detector))

        # Detection record
        detection_record = [0, 1, 0, 1]
        d_record = Tex(r'$D = $', color = BLACK).next_to(detector, UP).shift(2*LEFT+0.75*UP)
        outcome = copy.deepcopy(d_record)
        self.play(Write(d_record))

        # Axes
        axis_prior = show_axis(x0 = -6, y0 = 1.5, x_start = -0.1, y_start = -0.1, x_end = 4, y_end = 2)
        self.play(Create(axis_prior[0]))
        self.play(Create(axis_prior[1]))
        xlabel = Tex(r'$T$', color = BLACK).scale(0.5)
        xlabel.move_to(-1.5*RIGHT+1.5*UP)
        ylabel = Tex(r'$P(T)$', color = BLACK).scale(0.5)
        ylabel.move_to(-6*RIGHT+3.75*UP)
        self.play(FadeIn(xlabel), FadeIn(ylabel))

        # Draws the prior
        bayes = likelihood_dist(1.0, 0, 0)
        bayes.next_to(axis_prior[0], UP).shift(0.5*UP)
        bayes.align_to(axis_prior[1], LEFT).shift(0.2* RIGHT - 0.2*UP)
        self.play(FadeIn(bayes))

        # Posteriors and their labels
        posterior_list = [likelihood_dist(1.0, 1, 0)
            ,likelihood_dist(2.0, 2, 0)\
            ,likelihood_dist(2.0, 2, 1)\
            ,likelihood_dist(100.0, 8, 2)]

        posterior_label_list = [r'$P(T | X_1)$'
            ,r'$P(T | X_2 X_1)$'\
            ,r'$P(T | X_3 X_2 X_1$)'\
            ,r'$P(T | X_4 X_3 X_2 X_1)$']

        # Trail with 5 ancillae
        for i in range(1, n_ancillae):
            ancilla_trail.append(PrettySquare(1, CRIMSON_RGB))
            self.add(ancilla_trail[i])
            ancilla_trail[i].shift(3*i*RIGHT-2*UP)
            self.play(FadeIn(ancilla_trail[i]))

            # Ancillae label
            ancilla_trail_label.append(\
            Tex(r'$A_%i$' %(i+1), color = BLACK).next_to(ancilla_trail[i], DOWN))
            self.play(FadeIn(ancilla_trail_label[i]))

        # Moves the ancillae to the left until they are all measured
        while ancilla_trail:
            for (ancilla, label) in zip(ancilla_trail, ancilla_trail_label):
                self.play(ancilla.animate.shift(3*LEFT), label.animate.shift(3*LEFT))

            # Rotates the needle around its edge back and forth
            proble_angle*=-1
            self.play(detector_line.animate.rotate(angle = proble_angle, about_point = detector.get_center()))

            # Writes into the detection record
            outcome_new = Tex(r'$%d$' %detection_record[0], color = BLACK).next_to(detector, UP)
            self.play(FadeIn(outcome_new), run_time=0.5)

            # Writes into the detection record vector
            self.play(outcome_new.animate.align_to(d_record, UP).align_to(outcome, RIGHT)\
            .shift(0.55 * RIGHT, -0.05 * UP), run_time=0.5)

            # Updates the last digit in the detection record vectors
            outcome = outcome_new

            # Updates the distribution and the axes labels
            bayes_new = posterior_list[0].move_to(bayes.get_center())
            ylabel_new = Tex(posterior_label_list[0], color=BLACK).scale(0.5)
            ylabel_new.move_to(ylabel.get_center())
            posterior_list.pop(0)
            posterior_label_list.pop(0)

            # Replaces them
            self.play(ReplacementTransform(bayes, bayes_new))
            self.play(FadeOut(ylabel), FadeIn(ylabel_new))
            bayes = bayes_new
            ylabel = ylabel_new

            # Discards the ancilla
            self.play(FadeOut(ancilla_trail[0]), FadeOut(ancilla_trail_label[0]))
            ancilla_trail.pop(0)
            ancilla_trail_label.pop(0)
            detection_record.pop(0)

        # Add ... to the detection record and deletes the detector
        self.play(FadeIn(Tex(r'$...$', color = BLACK).next_to(outcome, RIGHT)))
        self.play(FadeOut(detector), FadeOut(detector_line), FadeOut(SWAP1), FadeOut(SWAP2))

        self.wait(1)