class VISUALIZER:
    def __init__(self, *args, **kwargs):
        pass

    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """
        print("Hello default launch!")
        pass

class DEMO_VIS(VISUALIZER):
    """
    Visualizer for the final product (including game mechanics and such)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """
        pass

class ROBOT_VIS(VISUALIZER):
    """
    Sets up a visualizer for a single robot
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """
        pass

class FAKE_VIS(VISUALIZER):
    """
    Sets up a fake visualizer that doesn't do much
    """    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def launch(self):
        """
        Launches the visualizer on a new thread and responds to external input
        """

        print("Hello fake visualizer!")
        pass