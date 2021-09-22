
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

        # About the two approaches
        subtitle3 = tools().label(text = 'Bayesian x Frequentist', color = royal_blue).scale(.9).next_to(lines[1], DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(subtitle3))

        # Scients column
        scientists = Group(*[ImageMobject("scientist.png").scale(0.075) for i in range (4)])

        for i in range(len(scientists)):
            tools().mob_pos(scientists[i], x = -5, y = -i)
            self.play(FadeIn(scientists[i]))
        self.wait(2)

        # Arrows and detectors
        arrows = VGroup(*[Arrow(ORIGIN, RIGHT, color = BLACK).next_to(scientists[i], RIGHT) for i in range (4)])
        detectors =  Group(*[ImageMobject("detector_img.png").scale(0.15).next_to(arrows[i], RIGHT)  for i in range (4)])
        detector_lines = VGroup(*[Line(detectors[i].get_center(), detectors[i].get_center() + 0.2*UP).set_color(RED)  for i in range (4)])

        for i in range(len(scientists)):
            self.play(FadeIn(arrows[i]), FadeIn(detectors[i]), FadeIn(detector_lines[i]), run_time = 0.5)

        # Braces and arrow for the detectors
        cases = MathTex("\left]", color = BLACK).scale(5).next_to(detectors, LEFT).align_to(detectors, LEFT).shift(RIGHT)
        histogram_arrow = Arrow(ORIGIN, RIGHT, color = BLACK).scale(5).next_to(cases, RIGHT).shift(-0.25 * RIGHT)
        self.play(FadeIn(cases), FadeIn(histogram_arrow))
        self.wait(2)

        # Histogram axis
        axis = show_axis(x0 = 1.5-1, y0 = -2.25, x_start = -0.1, y_start = -0.1, x_end = 3.25, y_end = 2.5)
        self.play(ShowCreation(axis[0]), ShowCreation(axis[1]))
        xlabel = tools().label(text = '$\hat{T}$', x = 5-1, y = -2.25, color = BLACK).scale(0.6)
        ylabel = tools().label(text = 'Counts', x = 1.5-1, y = 0.5, color = BLACK).scale(0.6)
        self.play(FadeIn(xlabel), FadeIn(ylabel))

        # Histogram
        histogram_img = ImageMobject("histogram.png").scale(1)
        histogram_img.move_to(3 * RIGHT - 1.425 * UP - RIGHT)
        self.play(FadeIn(histogram_img))
        self.wait(4)

        # Integration
        frequentist_integration = Tex("$\displaystyle{= \\int... P(\\boldsymbol{X})d\\boldsymbol{X}}$", color=BLACK).scale(.6).next_to(histogram_img, RIGHT).shift(0.75*RIGHT)
        self.play(FadeIn(frequentist_integration))
        self.wait(4)

        # Variance indication
        var_arrow = VGroup(
                    Arrow(ORIGIN, 3*RIGHT, color = BLACK).move_to(histogram_img.get_center(), histogram_img.get_center()).shift(UP + 1.4 * RIGHT),
                    Arrow(3*RIGHT, ORIGIN, color = BLACK).move_to(histogram_img.get_center(), histogram_img.get_center()).shift(UP + 1.1 * RIGHT)
                    )
        var_text = MathTex("\displaystyle{\\text{var}(\hat{T})}", color = BLACK).scale(0.6).next_to(var_arrow, UP)
        self.play(FadeIn(var_arrow.scale(0.5)),FadeIn(var_text))

        # Variance explanation
        var_explanation1 =  tools().label(text = r'We build a histogram with the estimation $\hat{T}$ made by each scientist', y = -3.75, color = BLACK).scale(0.6)
        self.play(FadeIn(var_explanation1))
        self.wait(3)
        self.play(FadeOut(var_explanation1))

        var_explanation2 =  tools().label(text = r'This histogram will have variance $\text{var}(\hat{T})$', y = -3.75, color = BLACK).scale(0.6)
        self.play(FadeIn(var_explanation2))
        self.wait(3)
        self.play(FadeOut(var_explanation2))

        var_explanation3 =  tools().label(text = r'The CR-bround tells us how well their results agree', y = -3.75, color = BLACK).scale(0.6)
        self.play(FadeIn(var_explanation3))
        self.wait(1)
        self.play(FadeOut(var_explanation3))

        ######################################################

        #  About the two approaches - Frequentist Deletion
        self.play(FadeOut(subtitle3), FadeOut(scientists), FadeOut(arrows), FadeOut(detectors), FadeOut(detector_lines),
                  FadeOut(cases), FadeOut(histogram_arrow), FadeOut(axis[0]), FadeOut(axis[1]), FadeOut(histogram_img),
                  FadeOut(xlabel), FadeOut(ylabel), FadeOut(var_arrow), FadeOut(var_text), FadeOut(frequentist_integration))

        ######################################################

        # Scientist and detector
        scientist = ImageMobject("scientist.png").scale(0.075)
        tools().mob_pos(scientist, x = -4, y = -0.5
        arrow = Arrow(ORIGIN, RIGHT, color = BLACK).next_to(scientist, RIGHT)
        detector = ImageMobject("detector_img.png").scale(0.15).next_to(arrow, RIGHT)
        detector_line = Line(detector.get_center(), detector.get_center() + 0.2*UP).set_color(RED)
        arrow2 = CurvedArrow(detector.get_center()-0.5*UP, scientist.get_center()-0.5*UP,angle = -np.pi).set_color(BLACK).scale(0.6)
        arrow3 = Arrow(ORIGIN, RIGHT, color = BLACK).next_to(detector, RIGHT)
        scientist_group = Group(scientist, arrow, detector, detector_line, arrow2, arrow3)

        ######################################################

        #  About the two approaches - Full Bayesian Deletion
        self.play(FadeOut(scientist_group))

        ######################################################

        # Bayesian Full Picture

        # Scientist and detector group
        scientist_group = Group(
                                copy.copy(scientist),
                                copy.copy(scientist).shift(1.2 * UP),
                                copy.copy(scientist).shift(1.2 * DOWN)
        )
        tools().mob_pos(scientist_group, x = -4, y = -0.5)

        # Arrows group
        arrow_group = VGroup(
                            copy.deepcopy(arrow),
                            copy.deepcopy(arrow).shift(1.2 * UP),
                            copy.deepcopy(arrow).shift(1.2 * DOWN)
        )

        self.play(FadeIn(scientist_group),FadeIn(arrow_group))

        # Detector group
        detector_group = Group(
                            copy.copy(detector),
                            copy.copy(detector).shift(1.2 * UP),
                            copy.copy(detector).shift(1.2 * DOWN)
        )

        # Detector needle group
        detector_line = Line(detector.get_center(), detector.get_center() + 0.2*UP).set_color(RED)
        detector_line_group = VGroup(
                                copy.copy(detector_line),
                                copy.copy(detector_line).shift(1.2 * UP),
                                copy.copy(detector_line).shift(1.2 * DOWN)
        )

        # Detector arrow group
        self.play(FadeIn(detector_group), FadeIn(detector_line_group))
        self.wait(1)

        arrow3_group = VGroup(
                            copy.deepcopy(arrow3),
                            copy.deepcopy(arrow3).shift(1.2 * UP),
                            copy.deepcopy(arrow3).shift(1.2 * DOWN)
        )

        # Axis group
        axis = show_axis(x0 = -1, y0 = -1, x_start = -0.1, y_start = -0.1, x_end = 2.0, y_end = 1.0)
        axis_group = Group(
                            copy.deepcopy(axis[0]),
                            copy.deepcopy(axis[0]).shift(1.2 * UP),
                            copy.deepcopy(axis[0]).shift(1.2 *DOWN),
                            copy.deepcopy(axis[1]),
                            copy.deepcopy(axis[1]).shift(1.2 * UP),
                            copy.deepcopy(axis[1]).shift(1.2 *DOWN),

        )

        # Posterior Group
        posterior_plot = ParametricFunction(tools().gaussian, t_min = 0.5, t_max = 3.5, color = crimson, fill_opacity=0).scale(0.5)
        tools().mob_pos(posterior_plot.scale(1), x = 2.25, y = -3.25)
        posterior_plot.align_to(axis[1], LEFT).align_to(axis[0], DOWN).shift(0.2 * UP + 0.2 * RIGHT)

        posterior_plot_group = Group(
                                    copy.deepcopy(posterior_plot),
                                    copy.deepcopy(posterior_plot).shift(1.2 * UP),
                                    copy.deepcopy(posterior_plot).shift(1.2 *DOWN),
        )

        self.play(FadeIn(arrow3_group), FadeIn(axis_group), FadeIn(posterior_plot_group))
        self.wait(1)

        # Full Bayesian Integration
        bayesian_integration = Tex("$\displaystyle{= \\int \\int... P(\\theta, \\boldsymbol{X})d\\theta d\\boldsymbol{X}}$", color=BLACK).scale(.7).next_to(posterior_plot_group, RIGHT).shift(.25*RIGHT)
        bayes_explanation4 =  Tex(r'We can also average over \emph{both} random variables $\theta$ and $\boldsymbol{X}$', color = BLACK).scale(0.6).next_to(posterior_plot_group, DOWN)

        self.play(FadeIn(bayesian_integration), FadeIn(bayes_explanation4))
        self.wait(4)
        self.play(FadeOut(bayes_explanation4))

        ######################################################

        #  About the two approaches - Full Bayesian Deletion
        self.play(FadeOut(scientist_group), FadeOut(arrow_group), FadeOut(detector_group), FadeOut(detector_line_group), FadeOut(arrow3_group),
                  FadeOut(axis_group), FadeOut(posterior_plot_group), FadeOut(bayesian_integration))

        ######################################################

        # About the bayesian approach
        subtitle4 = tools().label(text = 'Bayesian Approach', color = royal_blue).scale(.9).next_to(lines[1], DOWN).align_to(subtitle, LEFT)
        self.play(FadeIn(subtitle4))
        lines = []

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

        ######################################################

        # Highlight box
        bayes_highlight = Rectangle(width = 12, height = 1, color = BLACK).to_edge(0.5*DOWN)
        bayes_highlight = bayes_highlight.set_fill(royal_blue, opacity = 0.4)
        self.play(ShowCreation(bayes_highlight))

        bayes_highlight_explanation=tools().label(text=r"\textbf{Message:} we want a thermometer which is good for a wide range of temperatures $\rightarrow$ the Bayesian MSE is appropriate", color = BLACK).scale(0.6).move_to(bayes_highlight.get_center())
        self.play(FadeIn(bayes_highlight_explanation))

        self.wait(5)

