from classes.Sound import Sound


class SoundPlayer:
    def __init__(self):
        self.bg_sound, self.coin_sound, self.jump_sound, self.death_sound, self.grow_up_sound, self.shrink_down_sound, self.mine_sound = (
            Sound(i) for i in range(0, 7))
        self.allow_sound = True
