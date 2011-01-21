# Special user actions class.
class ActOfNature:

    # def __init__ (self, start_phrase='', end_phrase=''): {{{2
    def __init__ (self, start_phrase='', end_phrase=''):
        self.start_phrase = start_phrase
        self.end_phrase = end_phrase
        self.on = False
        self.cycles = 0
        self.x = 0
        self.y = 0

    # def set_pos (self, (x,y)): {{{2
    def set_pos (self, (x,y)):
        self.x = int(x)
        self.y = int(y)
    # }}}2

    # def end (self): {{{2
    def end (self):
        self.on = False
        self.cycles = 0
        self.x = 0
        self.y = 0
        if not self.end_phrase == '':
            print self.end_phrase
    # def start (self, pos=(0,0)): {{{2
    def start (self, pos=(0,0)):
        self.on = True
        self.x, self.y = pos
        if not self.start_phrase == '':
            print self.start_phrase
    # def toggle (self, pos=(0,0)): {{{2
    def toggle (self, pos=(0,0)):
        if self.on:
            self.end()
        else:
            self.start(pos)
    # }}}2
    
    # def update (self, rate): {{{2
    def update (self, rate):
        if self.on:
            self.cycles += 1
            if self.cycles % rate == 0:
                return True
        return False
    #}}}2
