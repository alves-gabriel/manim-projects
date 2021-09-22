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


'''
###########
###TITLE###
###########
'''

class scene_0(Scene):
    def construct(self):

        line = Line([0, 0, 0], [1, 1, 0], color=royal_blue)
        self.add(line)

        self.wait(1)
