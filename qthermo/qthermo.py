from manim import *
import numpy as np
import random
import copy

'''
Play with

manim -pqh qthermo.py <scene-name>

Use the flag -s to preview the last framebox1

manim -ps qthermo.py <scene-name>

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
        Circle(radius=qradius, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        Circle(radius=0.9*qradius, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1).shift(0.05*qradius*UP + 0.05*qradius*LEFT),

        Circle(radius=0.8*qradius, \
        color = rgb_to_color(tint(color, 0.2))).set_fill(rgb_to_color(tint(color, 0.3)), opacity=1).shift(0.1*qradius*UP + 0.1*qradius*LEFT)
    )

# Draws a cassini oval, with background and dashed contour
def cassini_oval(b2, scale_size):

        # Parameters
        a2=2.0

        # Background
        corr2_back = ParametricFunction(lambda t:\
        np.sqrt(a2**2*np.cos(2*t)+np.sqrt((b2**4-a2**4)+a2**4*np.cos(2*t)**2))*\
        np.array([np.sin(t), np.cos(t), 0]),\
        t_range = np.array([0, 2*np.pi, 0.01]), color = WHITE)
        corr2_back=corr2_back.set_fill(color=GOLDENROD, opacity=.25)
        corr2_back.scale(scale_size)

        # Dashed contour
        corr2 = copy.deepcopy(corr2_back).set_color(color=GOLDENROD)
        corr2 = DashedVMobject(corr2).scale(1.01)

        return VGroup(corr2, corr2_back)

'''
############
###SCENES###
############
'''

# Qubits interacting
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
        int_label = Tex(r'$V$', color = BLACK).scale(0.75)
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
        qubit_labelA2 = Tex(r'$\Delta E_{A} > 0$', color = BLACK).scale(1)
        qubit_labelB2 = Tex(r'$\Delta E_{B} < 0$', color = BLACK).scale(1)
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
        question3_label = Text('iii) Thermodynamic quantities?', color=BLACK).scale(0.5)
        question3_label.next_to(question3, DOWN)
        self.play(Create(question3), Write(question3_label))
        self.wait(1)

# Thermal operation
class scene_1(Scene):
    def construct(self):

        # Parabolas
        osc1 = ParametricFunction(lambda t:np.array([t, t**2, 0]), t_range = np.array([-1.5, 1.5, 0.02]), color = BLACK, fill_opacity=0)
        osc2 = ParametricFunction(lambda t:np.array([t, t**2, 0]), t_range = np.array([1.5, -1.5, 0.02]), color = BLACK, fill_opacity=0)
        osc1.shift(4*LEFT)
        osc2.shift(4*RIGHT)

        # Energy levels
        osc_center1, osc_center2=osc1.get_center(), osc2.get_center()
        energy_levels = VGroup(\
         DashedLine(osc_center1 - 0.4*UP - 2*LEFT, osc_center1 - 0.4*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center1 + 0.0*UP - 2*LEFT, osc_center1 + 0.0*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center1 + 0.4*UP - 2*LEFT, osc_center1 + 0.4*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center1 + 0.8*UP - 2*LEFT, osc_center1 + 0.8*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center2 - 0.4*UP - 2*LEFT, osc_center2 - 0.4*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center2 + 0.0*UP - 2*LEFT, osc_center2 + 0.0*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center2 + 0.4*UP - 2*LEFT, osc_center2 + 0.4*UP + 2*LEFT, color = GRAY),\
         DashedLine(osc_center2 + 0.8*UP - 2*LEFT, osc_center2 + 0.8*UP + 2*LEFT, color = GRAY),\
        )

        # Creates
        self.play(Create(energy_levels))
        self.play(Create(osc1), Create(osc2))

        # First boson group
        bosonA_swap=Circle(radius=.5, color = BLACK).scale(0.5).set_fill(MSEAGREEN, opacity=0.9).move_to(osc_center1+0.55*UP+0.5*RIGHT)
        bosonAgroup=VGroup(\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(CRIMSON, opacity=0.9).move_to(osc_center1-0.5*UP),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(CRIMSON, opacity=0.9).move_to(osc_center1-0.1*UP+0.3*LEFT),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(CRIMSON, opacity=0.9).move_to(osc_center1+0.2*UP+0.1*RIGHT),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(CRIMSON, opacity=0.9).move_to(osc_center1+0.7*UP),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(CRIMSON, opacity=0.9).move_to(osc_center1+0.6*UP+0.5*LEFT),\
        )

        # Second boson group
        # bosonB_swap=Circle(radius=.5, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2+0.6*UP+0.5*LEFT)
        bosonBgroup=VGroup(\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2-0.65*UP),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2+0.1*UP+0.45*LEFT),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2+0.3*UP+0.1*RIGHT),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2-0.4*UP+0.4*LEFT),\
          Circle(radius=.45, color = BLACK).scale(0.5).set_fill(GOLDENROD, opacity=0.9).move_to(osc_center2-0.4*UP+0.5*RIGHT),\
        )

        # Hamiltonians
        HA_label = Tex(r'$H_A = n_A = \omega a^\dagger a$', color = BLACK).next_to(osc1, DOWN)
        HB_label = Tex(r'$H_B = n_B = \omega b^\dagger b$', color = BLACK).next_to(osc2, DOWN)

        self.play(ShowIncreasingSubsets(bosonAgroup), ShowIncreasingSubsets(bosonBgroup), animation_rate=2)
        self.wait(1)

        self.play(Create(bosonA_swap), Write(HA_label), Write(HB_label))
        self.wait(1)

        # Interaction
        # Draws the SWAP interaction with two arrows
        SWAP1 = CurvedArrow(LEFT, RIGHT, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP2 = CurvedArrow(RIGHT, LEFT, angle = np.pi/2).set_color(BLACK).scale(.75)
        SWAP1.shift(UP)
        SWAP2.shift(UP)

        #  SWAP label, aligned to the SE interaction label
        swap_label = Tex(r'$V = $','$a$', '$\otimes$', '$b^\dagger$', '$+ a^\dagger \otimes b$', color = BLACK)
        swap_label.next_to(SWAP2, 3*UP)
        self.play(Write(swap_label))
        self.wait(1)

        self.play(FadeIn(SWAP1), FadeIn(SWAP2))
        self.wait(1)

        # Highlights the first term by growing it
        self.play(swap_label[1].animate.scale(1.5).set_color(CRIMSON))
        self.play(swap_label[1].animate.scale(.66).set_color(BLACK))
        self.wait(.5)

        self.play(swap_label[3].animate.scale(1.5).set_color(CRIMSON))
        self.play(swap_label[3].animate.scale(.66).set_color(BLACK))
        self.wait(.5)

        # Flips the SWAP arrows
        self.play(bosonA_swap.animate.move_to(osc_center2+0.6*UP+0.5*LEFT),\
        SWAP1.animate.rotate(np.pi, axis = UP), SWAP2.animate.rotate(np.pi, axis = UP))
        self.wait(1)

        # No work!
        work_indication = Arrow(DOWN, 3*DOWN, color = BLACK)
        work_indication.next_to(SWAP2, DOWN).shift(DOWN)
        work_label = Text('No energy is stored in the interaction!', color = BLACK).scale(0.5)
        work_label.next_to(work_indication, DOWN).shift(0.2*DOWN)
        self.play(Create(work_indication))
        self.play(Write(work_label))
        self.wait(1)
        self.play(FadeOut(work_indication), FadeOut(work_label))

        # Heat flow
        heat_arrow = CurvedArrow(3*LEFT, 3*RIGHT, angle = np.pi/2).set_color(BLACK).scale(.75).shift(DOWN)
        heat_label = Tex(r'$Q_A = - Q_B$', color = BLACK)
        heat_label.next_to(heat_arrow, DOWN)
        self.play(Create(heat_arrow))
        self.play(Write(heat_label))

        self.wait(1)

# Relative entropy
class scene_2(Scene):
    def construct(self):

        # Thermal state
        thermal_dot = VGroup(Circle(radius=.2, color = CRIMSON), \
        Circle(radius=.1, color = CRIMSON).set_fill(CRIMSON,  opacity=1))
        thermal_label=Tex(r'$\rho_{th} = \frac{e^{-\beta H}}{Z}$', color=BLACK)
        thermal_label.next_to(thermal_dot, DOWN)

        # Arbitrary state
        state_dot = Circle(radius=.1, color = BLACK).set_fill(BLACK,  opacity=1)
        state_dot.move_to(LEFT + 2*UP)
        state_label=Tex(r'$\rho_\tau$', color=BLACK)
        state_label.next_to(state_dot, UP)

        # Dashed line evolution
        dashline=DashedLine(thermal_dot.get_center(), state_dot.get_center(), color=BLACK)

        # Animations
        self.play(Create(dashline), GrowFromCenter(thermal_dot))
        self.play(GrowFromCenter(state_dot))
        self.play(Write(thermal_label))
        self.play(Write(state_label))

        self.wait(2)

# Mutual information. Leminstica and Cassini ovals are used here.
# See:  https://mathworld.wolfram.com/Lemniscate.html and https://github.com/3b1b/manim/issues/1100
# and also https://www.researchgate.net/publication/329186459_A_Multi_Foci_Closed_Curve_Cassini_Oval_its_Properties_and_Applications
class scene_3(Scene):
    def construct(self):

        # Cassini Ovals
        b=2.2
        a=2.0

        # Background
        corr1_back = ParametricFunction(lambda t:\
        np.sqrt(a**2*np.cos(2*t)+np.sqrt((b**4-a**4)+a**4*np.cos(2*t)**2))*\
        np.array([np.sin(t), np.cos(t), 0]),\
        t_range = np.array([0, 2*np.pi, 0.01]), color = WHITE)
        corr1_back=corr1_back.set_fill(color=GOLDENROD, opacity=.25)
        corr1_back.shift(4*LEFT)

        # Dashed contour
        corr1 = copy.deepcopy(corr1_back).set_color(color=GOLDENROD)
        corr1 = DashedVMobject(corr1)

        # Cold qubit
        qubit_cold=PrettyQubit(.5, ROYALBLUE_RGB)
        qubit_cold.shift(4*LEFT + 2*UP)

        # Hot qubit
        qubit_hot=PrettyQubit(.5, CRIMSON_RGB)
        qubit_hot.shift(4*LEFT + 2*DOWN)

        # Animates
        self.play(FadeIn(corr1_back), Create(corr1), FadeIn(qubit_cold), FadeIn(qubit_hot))
        self.wait(1)

        # Mutual Information 1
        #info1=Tex(r'$I(A:B)$','$=S(\rho_A)+S(\rho_B)-S(\rho_{AB})$', color=BLACK)
        info1=Tex(r'$I(A:B)$', color=BLACK)
        info1.next_to(corr1, DOWN)
        self.play(Write(info1))

        # Adds second correlation drawing
        corr_old=cassini_oval(2.2, 1)

        # Saves old qubits in initial position
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())

        # Save qubits as copy of themselves so we can "send them to foreground"
        qubit_cold=qubit_cold.copy()
        qubit_hot=qubit_hot.copy()

        # Qubit movement
        self.play(FadeIn(corr_old), qubit_cold.animate.next_to(ORIGIN, 1.5*UP),qubit_hot.animate.next_to(ORIGIN, 1.5*DOWN), run_time=2)
        self.wait(1)

        # Interaction
        int = ParametricFunction(lambda t:np.array([np.sin(25*t)/8, t, 0]), t_range = np.array([.1, .9, 0.01]), color = BLACK, fill_opacity=0)
        int.shift(0.5*DOWN)
        self.play(FadeIn(int))

        # Interaction label
        int_label = Tex(r'$V$', color = BLACK).scale(0.75)
        int_label.next_to(int, RIGHT)
        self.play(FadeIn(int_label))
        self.wait(1)

        # Draws the qubit interaction animation
        for i in range(30):

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

            # Updates the correlations
            self.remove(corr_old)
            corr=cassini_oval(2.2-0.2*i/30, 1-0.2*i/30)
            self.add(corr)
            corr_old=corr

            # Sends the qubits to the foreground
            self.add(qubit_cold.copy())
            self.add(qubit_hot.copy())
            self.add(int_label)

        self.wait(1)

        # Mutual Information 2
        info2=Tex(r'$I_\tau(A:B)$', color=BLACK)
        info2.next_to(corr_old, DOWN)
        self.play(Write(info2))

        # Mutual Info change. Arrow and deltas
        info_indication = Arrow(3*LEFT, 0.75*LEFT, color = BLACK)
        self.play(Create(info_indication))

        info_change=Tex(r'$\Delta I(A:B)$', color=BLACK)
        info_change.next_to(info_indication, DOWN).scale(0.7)
        self.play(Write(info_change))

        self.wait(2)

# Normal flow
# Reversal of flow
class scene_4(Scene):
    def construct(self):

        # Cold qubit
        qubit_cold=PrettyQubit(.5, ROYALBLUE_RGB)
        qubit_cold.shift(4*LEFT + 2*UP)

        # Hot qubit
        qubit_hot=PrettyQubit(.5, CRIMSON_RGB)
        qubit_hot.shift(4*LEFT + 2*DOWN)

        # Animates
        self.play(FadeIn(qubit_cold), FadeIn(qubit_hot))

        # Mutual Information 1
        #info1=Tex(r'$I(A:B)$','$=S(\rho_A)+S(\rho_B)-S(\rho_{AB})$', color=BLACK)
        info1=Tex(r'$I(A:B) = 0$', color=BLACK)
        info1.next_to(qubit_hot, DOWN)
        self.play(Write(info1))

        # Adds second correlation drawing
        corr_old=cassini_oval(2.0, 0)

        # Saves old qubits in initial position
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())

        # Save qubits as copy of themselves so we can "send them to foreground"
        qubit_cold=qubit_cold.copy()
        qubit_hot=qubit_hot.copy()

        # Qubit movement
        self.play(FadeIn(corr_old), qubit_cold.animate.next_to(ORIGIN, 1.5*UP),qubit_hot.animate.next_to(ORIGIN, 1.5*DOWN), run_time=2)
        self.wait(1)

        # Interaction
        int = ParametricFunction(lambda t:np.array([np.sin(25*t)/8, t, 0]), t_range = np.array([.1, .9, 0.01]), color = BLACK, fill_opacity=0)
        int.shift(0.5*DOWN)

        # Interaction label
        int_label = Tex(r'$V$', color = BLACK).scale(0.75)
        int_label.next_to(int, RIGHT)
        self.play(FadeIn(int), FadeIn(int_label))
        self.wait(1)

        # Draws the qubit interaction animation
        for i in range(30):

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

            # Updates the correlations
            self.remove(corr_old)
            corr=cassini_oval(2.0+0.2*i/30, i/30)
            self.add(corr)
            corr_old=corr

            # Sends the qubits to the foreground
            self.add(qubit_cold.copy())
            self.add(qubit_hot.copy())
            self.add(int_label)

        self.wait(1)

        # Mutual Information 2
        info2=Tex(r'$I_\tau(A:B) > 0$', color=BLACK)
        info2.next_to(corr_old, DOWN)
        self.play(FadeIn(info2))

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

        self.wait(2)

# Reversal of flow
class scene_5(Scene):
    def construct(self):

        # Cassini Ovals
        b=2.2
        a=2.0

        # Background
        corr1_back = ParametricFunction(lambda t:\
        np.sqrt(a**2*np.cos(2*t)+np.sqrt((b**4-a**4)+a**4*np.cos(2*t)**2))*\
        np.array([np.sin(t), np.cos(t), 0]),\
        t_range = np.array([0, 2*np.pi, 0.01]), color = WHITE)
        corr1_back=corr1_back.set_fill(color=GOLDENROD, opacity=.25)
        corr1_back.shift(4*LEFT)

        # Dashed contour
        corr1 = copy.deepcopy(corr1_back).set_color(color=GOLDENROD)
        corr1 = DashedVMobject(corr1)

        # Cold qubit
        qubit_cold=PrettyQubit(.5, ROYALBLUE_RGB)
        qubit_cold.shift(4*LEFT + 2*UP)

        # Hot qubit
        qubit_hot=PrettyQubit(.5, CRIMSON_RGB)
        qubit_hot.shift(4*LEFT + 2*DOWN)

        # Animates
        self.play(FadeIn(corr1_back), FadeIn(corr1), FadeIn(qubit_cold), FadeIn(qubit_hot))

        # Mutual Information 1
        #info1=Tex(r'$I(A:B)$','$=S(\rho_A)+S(\rho_B)-S(\rho_{AB})$', color=BLACK)
        info1=Tex(r'$I(A:B)$', color=BLACK)
        info1.next_to(corr1, DOWN)
        self.play(Write(info1))

        # Adds second correlation drawing
        corr_old=cassini_oval(2.2, 1)

        # Saves old qubits in initial position
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())

        # Save qubits as copy of themselves so we can "send them to foreground"
        qubit_cold=qubit_cold.copy()
        qubit_hot=qubit_hot.copy()

        # Qubit movement
        self.play(FadeIn(corr_old), qubit_cold.animate.next_to(ORIGIN, 1.5*UP),qubit_hot.animate.next_to(ORIGIN, 1.5*DOWN), run_time=2)
        self.wait(1)

        # Interaction
        int = ParametricFunction(lambda t:np.array([np.sin(25*t)/8, t, 0]), t_range = np.array([.1, .9, 0.01]), color = BLACK, fill_opacity=0)
        int.shift(0.5*DOWN)

        # Interaction label
        int_label = Tex(r'$V$', color = BLACK).scale(0.75)
        int_label.next_to(int, RIGHT)
        self.play(FadeIn(int), FadeIn(int_label))
        self.wait(1)

        # Draws the qubit interaction animation
        for i in range(30):

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

            # Updates the correlations
            self.remove(corr_old)
            corr=cassini_oval(2.2-0.2*i/30, 1-0.2*i/30)
            self.add(corr)
            corr_old=corr

            # Sends the qubits to the foreground
            self.add(qubit_cold.copy())
            self.add(qubit_hot.copy())
            self.add(int_label)

        self.wait(1)

        # Mutual Information 2
        info2=Tex(r'$I_\tau(A:B) < I(A:B)$', color=BLACK)
        info2.next_to(corr_old, DOWN)
        self.play(FadeIn(info2))

        # Copies the qubits again and creates a mobject so we can highlight it later
        dynamics_group = VGroup(qubit_cold.copy(), qubit_hot.copy(), int, int_label)
        self.add(qubit_cold.copy())
        self.add(qubit_hot.copy())
        self.wait(1)

        # Qubit getting warmer and movement
        qubit_coldII=PrettyQubit(.5, LIGHTBLUE_RGB).next_to(ORIGIN, 1.5*UP)
        qubit_hotII=PrettyQubit(.5, DARKRED_RGB).next_to(ORIGIN, 1.5*DOWN)

        qubit_coldII.shift(4*RIGHT + UP)
        qubit_hotII.shift(4*RIGHT + DOWN)

        self.play(ReplacementTransform(qubit_cold, qubit_coldII), \
        ReplacementTransform(qubit_hot, qubit_hotII), \
        run_time=2)

        self.wait(2)
