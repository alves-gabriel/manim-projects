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
        color = rgb_to_color(tint(color, 0.1))).set_fill(rgb_to_color(tint(color, 0.2)), opacity=1).shift(0.05*qradius*UP + 0.05*qradius*LEFT),

        Circle(radius=0.8*qradius, \
        color = rgb_to_color(tint(color, 0.2))).set_fill(rgb_to_color(tint(color, 0.3)), opacity=1).shift(0.1*qradius*UP + 0.1*qradius*LEFT),

        # Atom drawing
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2),
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2).rotate(PI / 3),
        Ellipse(width=.8, height=.4, color=WHITE, stroke_width=2).rotate(-PI / 3),
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

    background=Circle(fill_opacity=1, radius=.98)
    background.set_color(color=[rgb_to_color(MSEAGREEN_RGB),WHITE])
    color_direction=[1,1,1]
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


'''
############
###SCENES###
############
'''

# Qubits interacting
class scene_0(Scene):
    def construct(self):

        # Qubit - System
        qubitSystem=PrettyQubit(.5, ROYALBLUE_RGB)
        qubitSystem.shift(0*LEFT + 0*UP)

        # Qubit - Ancilla
        qubitAncilla=PrettyQubit(.5, CRIMSON_RGB)
        qubitAncilla.shift(0*LEFT - 2*UP)

        # Adding them
        self.play(FadeIn(qubitSystem), FadeIn(qubitAncilla))

        qubitBath = Bath(MSEAGREEN_RGB).shift(0*LEFT + 2.5*UP)
        self.add(qubitBath)

        self.wait(10)