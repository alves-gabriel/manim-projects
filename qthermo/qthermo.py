from manim import *
import numpy as np
import random
import copy

'''
Play with

manim -pqh metrology.py <scene-name>

Use the flag -s to preview the last framebox1

manim -ps metrology.py <scene-name>

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
ROYALBLUE_RGB = np.array([65, 105, 225])/255
CRIMSON = '#DC143C'
CRIMSON_RGB = np.array([220, 20, 60])/255
ROYALPURPLE = '#7851a9'
BURNTORANGE = '#cc5500'
BURNTORANGE_RGB = np.array([204, 85, 0])/255

# Convex combination in the hue to lighten the colors. Factor should be between 0 and 1
def tint(rgb, factor):
    return rgb + (1 - rgb)*factor

# Darkens the colors
def shade(rgb, factor):
    return rgb*(1 - factor)

# Draws a pretty rectangle with a slight gradient from the borders
def PrettyQubit(qradius, color):
    return VGroup(
        Circle(radius=qradius, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        Circle(radius=0.9*qradius, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1).shift(0.05*qradius*UP + 0.05*qradius*LEFT),

        Circle(radius=0.8*qradius, \
        color = rgb_to_color(tint(color, 0.2))).set_fill(rgb_to_color(tint(color, 0.3)), opacity=1).shift(0.1*qradius*UP + 0.1*qradius*LEFT)
    )

'''
############
###SCENES###
############
'''

# Metrology basic diagram
class scene_0(Scene):
    def construct(self):

        # Cold qubit
        qubit_cold=PrettyQubit(.5, ROYALBLUE_RGB)
        qubit_cold.shift(4*LEFT + 2*UP)

        # Hot qubit
        qubit_hot=PrettyQubit(.5, CRIMSON_RGB)
        qubit_hot.shift(4*LEFT + 2*DOWN)

        # Adding them
        self.play(FadeIn(qubit_cold), FadeIn(qubit_hot))
        self.wait(1)

        # Qubit label
        qubit_labelA = Tex(r'$\rho_{th, A} = \frac{e^{-\beta_A H_A}}{Z}$', color = BLACK).scale(1)
        qubit_labelB = Tex(r'$\rho_{th, B} = \frac{e^{-\beta_B H_B}}{Z}$', color = BLACK).scale(1)
        qubit_labelA.next_to(qubit_cold, UP)
        qubit_labelB.next_to(qubit_hot, DOWN)
        self.play(FadeIn(qubit_labelA), FadeIn(qubit_labelB))
        self.wait(1)
        self.play(FadeOut(qubit_labelA), FadeOut(qubit_labelB))

        qubit_label = Tex(r'$\rho_{A, B} = \rho_A \otimes \rho_B$', color = BLACK).scale(1)
        qubit_label.next_to(qubit_hot, DOWN)
        self.play(FadeIn(qubit_label))
        self.wait(1)

        # Qubit movement
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())
        self.play(qubit_cold.animate.next_to(ORIGIN, 1.5*UP),qubit_hot.animate.next_to(ORIGIN, 1.5*DOWN), run_time=2)
        self.wait(1)

        # Interaction
        int = ParametricFunction(lambda t:np.array([np.sin(25*t)/8, t, 0]), t_range = np.array([.1, .9, 0.01]), color = BLACK, fill_opacity=0)
        int.shift(0.5*DOWN)
        self.play(FadeIn(int))

        # Interaction label
        int_label = Tex(r'$H_{AB}$', color = BLACK).scale(0.75)
        int_label.next_to(int, RIGHT)
        self.play(FadeIn(int_label))
        self.wait(1)

        # Draws the qubit interaction animation
        for i in range(20):

            # Removes the interaction
            self.wait(0.1)
            self.remove(int)

            # Sine with variable phase
            def ysin(t):
                return np.array((np.sin(25*(t + i*np.pi/80))/8, t, 0))

            # Draws the sine function for the given phase
            int = ParametricFunction(ysin, t_range = np.array([.1, .9, 0.01]), color = BLACK, fill_opacity=0)
            self.add(int)
            int.shift(0.5*DOWN)

        # Copies the qubits again and creates a mobject so we can highlight it later
        dynamics_group = VGroup(qubit_cold.copy(), qubit_hot.copy(), int, int_label)
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())
        self.wait(1)

        # Qubit getting warmer and movement
        qubit_coldII=PrettyQubit(.5, BURNTORANGE_RGB).next_to(ORIGIN, 1.5*UP)
        qubit_hotII=PrettyQubit(.5, BURNTORANGE_RGB).next_to(ORIGIN, 1.5*DOWN)

        qubit_coldII.shift(4*RIGHT + UP)
        qubit_hotII.shift(4*RIGHT + DOWN)

        self.play(ReplacementTransform(qubit_cold, qubit_coldII), \
        ReplacementTransform(qubit_hot, qubit_hotII), \
        run_time=2)
        self.wait(1)

        # Qubit label II
        qubit_labelA2 = Tex(r'$\Delta Q_{A} > 0$', color = BLACK).scale(1)
        qubit_labelB2 = Tex(r'$\Delta Q_{B} < 0$', color = BLACK).scale(1)
        qubit_labelA2.next_to(qubit_coldII, DOWN)
        qubit_labelB2.next_to(qubit_hotII, UP)
        self.play(FadeIn(qubit_labelA2), FadeIn(qubit_labelB2))
        self.wait(1)

        # Surrounding rectangles
        question1 = SurroundingRectangle(qubit_label, color=BLACK)
        question1_label = Text('i) Role of the initial state?', color=BLACK).scale(0.5)
        question1_label.next_to(question1, DOWN)
        self.play(Create(question1), Write(question1_label))
        self.wait(1)

        question2 = SurroundingRectangle(dynamics_group, color=BLACK)
        question2_label = Text('ii) How to describe the dynamics?', color=BLACK).scale(0.5)
        question2_label.next_to(question2, UP)
        self.play(Create(question2), Write(question2_label))
        self.wait(1)

        final_group = VGroup(qubit_hotII, qubit_labelB2)
        question3 = SurroundingRectangle(final_group, color=BLACK)
        question3_label = Text('iii) Thermodynamical quantities?', color=BLACK).scale(0.5)
        question3_label.next_to(question3, DOWN)
        self.play(Create(question3), Write(question3_label))
        self.wait(1)
