class CountdownTimer:
    def __init__(self, seconds):
        self.seconds = seconds

    def tick(self):
        if self.seconds > 0:
            self.seconds -= 1

    def is_finished(self):
        return self.seconds <= 0 
    