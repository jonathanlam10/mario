import pygame

class Timer:
    def __init__(self, frames, wait=100, frameindex=0, looponce=False):    # imagerect frames
        self.frames = frames
        self.wait = wait
        self.frameindex = frameindex
        self.looponce = looponce

        self.finished = False
        self.lastframe = len(frames) - 1
        self.last = None

    def frame_index(self):
        now = pygame.time.get_ticks()
        if self.last is None:
            self.last = now
            self.frameindex = 0
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.frameindex += 1
            if self.looponce and self.frameindex == self.lastframe:
                self.finished = True
            else:
                self.frameindex %= len(self.frames)
            self.last = now
        return self.frameindex

    def reset(self):
        self.last = None
        self.finished = False

    def __str__(self): return 'Timer(frames=' + self.frames +\
                              ', wait=' + str(self.wait) + ', index=' + str(self.frameindex) + ')'

    def imagerect(self):
        return self.frames[self.frame_index()]

