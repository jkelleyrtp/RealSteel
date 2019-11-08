class DEVICE:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)





class ROBOT_DEVICE(DEVICE):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class FAKE_DEVICE(DEVICE):
    # Builds a fake device instead of a real device to mimic and verify commands

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)