class AddUpdater1(Scene):
    def construct(self):
        dot = Dot().set_color(BLACK)
        text = Tex("Label")\
               .next_to(dot,RIGHT,buff=SMALL_BUFF).set_color(BLACK)

        self.add(dot,text)
        # Add update function to the objects
        text.add_updater(lambda m: m.next_to(dot,RIGHT,buff=SMALL_BUFF))

        # Add the object again
        self.add(text)

        self.play(dot.animate.shift(UP*2))

        # Remove update function
        text.clear_updaters()

        self.wait(2)
