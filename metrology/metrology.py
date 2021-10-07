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
CRIMSON = '#DC143C'
CRIMSON_RGB = np.array([220, 20, 60])/255
ROYALPURPLE = '#7851a9'

# Convex combination in the hue to lighten the colors. Factor should be between 0 and 1
def tint(rgb, factor):
    return rgb + (1 - rgb)*factor

# Darkens the colors
def shade(rgb, factor):
    return rgb*(1 - factor)

# Draws a pretty rectangle with a slight gradient from the borders
def PrettyRectangle(rec_width, rec_height, color):
    return VGroup(
        RoundedRectangle(corner_radius=0.25, width = rec_width, height = rec_height, \
        color = rgb_to_color(color)).set_fill(rgb_to_color(tint(color, 0.1)), opacity=1),

        RoundedRectangle(corner_radius=0.95*0.25, width = 0.95*rec_width, height = 0.95*rec_height, \
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1)
    )

'''
############
###SCENES###
############
'''

# Metrology basic diagram
class scene_0(Scene):
    def construct(self):

        # Initial state
        system = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/system.jpg-000001.png").scale(.45)
        system.to_edge(LEFT, buff = 0.25)
        system_label=Tex(r"State $\rho_0$", color = BLACK).scale(0.75).next_to(system, UP, buff = 0.5)
        self.play(GrowFromEdge(system, LEFT), Write(system_label))
        self.wait(1)

        arrow=[]
        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(system, RIGHT)
        self.play(Create(arrow[-1]))

        # Dynamical part
        dynamics = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/dynamics.jpg-000001.png").scale(.25)
        dynamics.next_to(arrow[-1], RIGHT)
        dynamics_label=Tex(r"Dynamics $U(\theta)$, $\mathcal{L}_\theta$, ...", color = BLACK).scale(0.75).next_to(dynamics, DOWN, buff = 0.5)
        self.play(GrowFromEdge(dynamics, LEFT), Write(dynamics_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(dynamics, RIGHT)
        self.play(Create(arrow[-1]))

        #  Final State
        systemII = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/systemII.jpg-000001.png").scale(.45)
        systemII.next_to(arrow[-1], RIGHT)
        systemII_label=Tex(r"State $\rho_\theta$", color = BLACK).scale(0.75).next_to(systemII, UP, buff = 0.5)
        self.play(GrowFromEdge(systemII, LEFT), Write(systemII_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(systemII, RIGHT)
        self.play(Create(arrow[-1]))

        # Detector
        detector = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/detector.jpg-000001.png").scale(.2)
        detector.next_to(arrow[-1], RIGHT)
        detector_label=Tex(r"Measurement $\xi$", color = BLACK).scale(0.75).next_to(detector, DOWN, buff = 0.5)
        self.play(GrowFromEdge(detector, LEFT), Write(detector_label))
        self.wait(1)

        arrow.append(Arrow(ORIGIN, 0.75*RIGHT, buff = 0.1).set_color(BLACK))
        arrow[-1].next_to(detector, RIGHT)
        self.play(Create(arrow[-1]))

        # Estimator
        computer = ImageMobject("/home/gabriel/github/manim-projects/metrology/assets/computer.jpg-000001.png").scale(.2)
        computer.next_to(arrow[-1], RIGHT)
        computer_label=Tex(r"Estimation", color = BLACK).scale(0.75).next_to(computer, UP, buff = 0.5)
        self.play(FadeIn(computer), Write(computer_label))
        self.wait(1)

        # diagram_rec_width = 2
        #
        # # Draws the dynamical process
        # dynamics_rectangle = PrettyRectangle(diagram_rec_width, 0.6*diagram_rec_width, CRIMSON_RGB)
        # dynamics_rectangle.next_to(system.get_center(), RIGHT).shift(2*RIGHT)
        #
        # self.add(dynamics_rectangle)
        # self.play(GrowFromEdge(dynamics_rectangle, LEFT))

# Vectorization
class scene_1(Scene):
    def construct(self):

        # Original matrix
        m0=Matrix([["a", "b"], ["c", "d"]], left_bracket="(", right_bracket=")")
        m0.get_entries().set_color(BLACK)
        m0.get_brackets().set_color(BLACK)
        self.play(FadeIn(m0))

        # Vec operator
        vec0=Tex("\\text{vec}", color=BLACK).next_to(m0, LEFT)
        eqsign=Tex("=", color=BLACK).next_to(m0, RIGHT)
        self.play(FadeIn(vec0), FadeIn(eqsign))
        self.wait(1)

        # First column highlight
        rec0=SurroundingRectangle(m0.get_columns()[0], color=ROYALBLUE)
        self.play(FadeIn(rec0))

        # Vectorized matrix
        m0vec=Matrix([["a"], ["c"], ["b"], ["d"]], left_bracket="(", right_bracket=")")
        m0vec.get_brackets().set_color(BLACK)
        m0vec.next_to(eqsign, RIGHT)
        self.play(FadeIn(m0vec))

        # Moves the first rectangle into the vectorized matrix
        # and makes the first two entries appear
        vecrec0=SurroundingRectangle(m0vec.get_entries()[0:2], color=ROYALBLUE)
        self.play(ReplacementTransform(rec0, vecrec0), FadeIn(m0vec.get_entries()[0:2].set_color(BLACK)))
        self.wait(1)
        self.play(FadeOut(vecrec0))

        # Second column highlight
        rec1=SurroundingRectangle(m0.get_columns()[1], color=CRIMSON)
        self.play(FadeIn(rec1))
        self.wait(1)

        # Second rectangle into vectorized matrix
        vecrec1=SurroundingRectangle(m0vec.get_entries()[2:4], color=CRIMSON)
        self.play(ReplacementTransform(rec1, vecrec1), FadeIn(m0vec.get_entries()[2:4].set_color(BLACK)))
        self.wait(1)
        self.play(FadeOut(vecrec1))

        self.wait(1)

# Vectorization Identity
class scene_2(Scene):
    def construct(self):

        # Matrix B full
        B0=Matrix([[r"B_{1,1}", r"B_{1,2}", r"\hdots"],[r"B_{2,1}", r"B_{2,2}",r"\ddots"]], left_bracket="(", right_bracket=")").scale(0.75)
        B0.add(MathTex("B=", color=BLACK).next_to(B0,LEFT))
        B0.to_edge(2*RIGHT)
        B0.get_entries().set_color(BLACK)
        B0.get_brackets().set_color(BLACK)
        self.play(Write(B0))

        # First column highlight
        rec0=SurroundingRectangle(B0.get_columns()[0], color=CRIMSON)
        rec0_label=MathTex(r"\vec{B}_1", color=CRIMSON).next_to(rec0, DOWN).scale(0.75)
        self.play(Create(rec0))
        self.play(Write(rec0_label))
        self.wait(1)
        self.play(FadeOut(rec0,rec0_label))

        # Matrix B with columns
        B1=Matrix([[r"\vec{B}_1", r"\vec{B_2}", r"\hdots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        B1_label=MathTex("B=", color=BLACK).next_to(B1,LEFT)
        B1.add(B1_label)
        B1.to_edge(2*RIGHT)
        B1.get_entries().set_color(BLACK)
        B1.get_brackets().set_color(BLACK)
        self.play(ReplacementTransform(B0, B1))
        self.wait(1)

        # Matrix A full
        A0=Matrix([[r"A_{1,1}", r"A_{1,2}", r"\hdots"],[r"A_{2,1}", r"A_{2,2}",r"\ddots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        A0_label=MathTex("A=", color=BLACK).next_to(A0,LEFT).scale(0.75)
        A0.add(A0_label)
        A0.to_edge(2*LEFT)
        A0.get_entries().set_color(BLACK)
        A0.get_brackets().set_color(BLACK)
        self.play(Write(A0))

        # First column highlight
        rec0=SurroundingRectangle(A0.get_columns()[0], color=CRIMSON)
        rec0_label=MathTex(r"\vec{A}_1", color=CRIMSON).next_to(rec0, DOWN)
        self.play(Create(rec0))
        self.play(Write(rec0_label))
        self.wait(1)

        # Transposition
        A0_dagger=Matrix([[r"A_{1,1}^*", r"A_{2,1}^*", r"\hdots"],[r"A_{1,2}^*", r"A_{2,2}^*",r"\ddots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        A0_dagger_label=MathTex("A^\dagger=", color=BLACK).next_to(A0_dagger,LEFT)
        A0_dagger.add(A0_dagger_label)
        A0_dagger.to_edge(2*LEFT)
        A0_dagger.get_entries().set_color(BLACK)
        A0_dagger.get_brackets().set_color(BLACK)

        # First row highlight
        rec1=SurroundingRectangle(A0_dagger.get_rows()[0], color=CRIMSON)
        rec1_label=MathTex(r"\vec{A}_1^\dagger", color=CRIMSON).next_to(rec1, UP).scale(0.75)

        # Transposition animation
        self.play(ReplacementTransform(A0, A0_dagger),\
        ReplacementTransform(rec0, rec1),\
        ReplacementTransform(rec0_label, rec1_label))
        self.wait(1)
        self.play(FadeOut(rec1, rec1_label))

        # Matrix B with columns
        A1=Matrix([[r"\vec{A}_1^\dagger"], [r"\vec{A}_2^\dagger"], [r"\vdots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        A1_label=MathTex("A^\dagger=", color=BLACK).next_to(A1,LEFT).scale(0.75)
        A1.add(A1_label)
        A1.to_edge(2*LEFT)
        A1.get_entries().set_color(BLACK)
        A1.get_brackets().set_color(BLACK)
        self.play(ReplacementTransform(A0_dagger, A1))
        self.wait(1)

        # Removes the "A=" and the "B="
        self.play(FadeOut(B1_label),FadeOut(A1_label))
        B1.remove(B1_label)
        A1.remove(A1_label)

        # AB product
        AB_prod_label=MathTex("A^\dagger B=", color=BLACK).to_edge(3*LEFT).scale(0.75)
        self.play(A1.animate.next_to(AB_prod_label, RIGHT))
        self.play(B1.animate.next_to(A1, RIGHT))
        self.play(Write(AB_prod_label))

        # Product Matrix
        AB_equal_sign=MathTex("=", color=BLACK).next_to(B1, RIGHT).scale(0.75)
        AB=Matrix([
            [r"\vec{A}_1^\dagger \vec{B}_1", r"\vec{A}_1^\dagger \vec{B}_2", r"\hdots"],\
            [r"\vec{A}_2^\dagger \vec{B}_1", r"\vec{A}_2^\dagger \vec{B}_2", "."],\
            [r"\vdots", r".",r"\ddots"]],\
            left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        AB.next_to(AB_equal_sign, RIGHT)
        AB.get_brackets().set_color(BLACK)
        self.play(Write(AB_equal_sign), Write(AB))

        # Multiplication - elements are highlighted using Indicete(...)
        AB_elem=AB.get_entries()
        A_elem=A1.get_entries()
        B_elem=B1.get_entries()

        # AB11
        self.play(Indicate(A_elem[0], color=CRIMSON), Indicate(B_elem[0], color=CRIMSON))
        self.play(AB_elem[0].animate.set_color(BLACK))

        # AB12
        self.play(Indicate(A_elem[0], color=CRIMSON), Indicate(B_elem[1], color=CRIMSON))
        self.play(AB_elem[1].animate.set_color(BLACK))

        # AB21
        self.play(Indicate(A_elem[1], color=CRIMSON), Indicate(B_elem[0], color=CRIMSON))
        self.play(AB_elem[3].animate.set_color(BLACK))

        # AB22
        self.play(Indicate(A_elem[1], color=CRIMSON), Indicate(B_elem[1], color=CRIMSON))
        self.play(AB_elem[4].animate.set_color(BLACK))

        # All of them
        el_group=VGroup()
        for el in AB_elem:
            #Phantom is not working so I want to keep some elements white -> If
            if el!=AB_elem[5] and el!=AB_elem[7]:
                 el_group.add(el)

        self.play(el_group.animate.set_color(BLACK))

        # Trace
        AB_Tr=MathTex(r"\text{tr}(A^\dagger B)=", color=BLACK).scale(0.75)
        AB_Tr.to_edge(2*DOWN).to_edge(LEFT)
        self.play(Write(AB_Tr))

        # Summation
        AB_Tr_sum=MathTex(r"\vec{A}_1^\dagger \vec{B}_1+\vec{A}_2^\dagger \vec{B}_2+...=", color=BLACK).scale(0.75)
        AB_Tr_sum.next_to(AB_Tr, RIGHT)
        self.play(Write(AB_Tr_sum))
        self.wait(1)

        # Vector form of sum
        AB_inner0=Matrix([[r"\vec{A}_1^\dagger", r"\vec{A}_2^\dagger", r"\hdots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        AB_inner0.next_to(AB_Tr_sum, RIGHT)
        AB_inner1=Matrix([[r"\vec{B}_1"], [r"\vec{B}_2"], [r"\vdots"]], left_bracket="(", right_bracket=")", element_alignment_corner=np.array([ 0., 0., 0.])).scale(0.75)
        AB_inner1.next_to(AB_inner0, RIGHT)

        AB_inner0.get_entries().set_color(BLACK)
        AB_inner0.get_brackets().set_color(BLACK)
        AB_inner1.get_entries().set_color(BLACK)
        AB_inner1.get_brackets().set_color(BLACK)

        self.play(Write(AB_inner0), Write(AB_inner1))
        self.wait(1)

        # Vec procuct
        AB_vec_prod=MathTex(r"=\text{vec}(A)^\dagger \text{vec}(B)", color=BLACK).scale(0.75)
        AB_vec_prod.next_to(AB_inner1)
        self.play(Write(AB_vec_prod))

        self.wait(1)

# Vectorization Identity
class scene_3(Scene):
    def construct(self):
        pass
