import random
from .magic import Spell
from .inventory import Item

#color in terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Person:
    def __init__(self, name, hp, mp, attack, defense, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.attack_low = attack - 10
        self.attack_hight = attack + 10
        self.defense = defense
        self.magic = magic
        self.items = items
        self.action = ['Attack', 'Magic', 'Item']

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_hight)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
        return self.hp

    def heal(self, heal_point):
        self.hp += heal_point
        if self.hp >= self.max_hp:
            self.hp = self.max_hp
    
    def get_hp(self):
        return self.hp
    
    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp
    
    def reduce_mp(self, cost):
        if self.mp >= cost:
            self.mp -= cost
    
    def choose_action(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + 'Actions:' + bcolors.ENDC)
        for item in self.action:
            print('    ' + str(i) + '.', item)
            i += 1
    
    def choose_magic(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + 'Magic:' + bcolors.ENDC)
        for spell in self.magic:
            print('    ' + str(i) + '.', spell.name, '(cost:', spell.cost, ')' )
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.OKBLUE + bcolors.BOLD + 'Items:' + bcolors.ENDC)
        for item in self.items:
            print('    ' + str(i) + '.', item['item'].name, ':', item['item'].description, '(x' + str(item['quantity']) + ')')
            i += 1

    def choose_target(self, enemies):
        i = 1
        print(bcolors.FAIL + bcolors.BOLD + 'Items:' + bcolors.ENDC)
        for enemy in enemies:
            print('    '+ str(i) + '.' + enemy.name)
            i += 1
        choice = int(input('Choose action:')) - 1
        return choice

    def get_stat(self):
        # hp bar (25 spaces)
        hp_bar = ''
        hp_bar_ticks = (self.hp / self.max_hp) * 100 / 4

        while hp_bar_ticks > 0:
            hp_bar += '█'
            hp_bar_ticks -= 1

        while len(hp_bar) < 25:
            hp_bar += ' '

        # mp bar (10 spaces)
        mp_bar = ''
        mp_bar_ticks = (self.mp / self.max_mp) * 100 / 10

        while mp_bar_ticks > 0:
            mp_bar += '█'
            mp_bar_ticks -= 1

        while len(mp_bar) < 10:
            mp_bar += ' '

        # hp number and mp member (9(hp) + 9(mp) spaces)
        hp_number = str(self.hp) + '/' + str(self.max_hp)
        mp_number = str(self.mp) + '/' + str(self.max_mp)

        while len(hp_number) < 9:
            hp_number += ' '
        
        while len(mp_number) < 9:
            mp_number += ' '

        # player name (25 space)
        if len(self.name) < 25:
            name = self.name + ':'
            while len(name) < 25:
                name += ' '
        elif len(self.name) >= 25:
            name = self.name[0:23] + ':'

        print(name + hp_number +  '|' + bcolors.OKGREEN + hp_bar + bcolors.ENDC +'|    ' + mp_number +'|' + bcolors.OKBLUE + mp_bar + bcolors.ENDC +'|')

    def get_stat_text(self):
        print('Name                             HP_________________________             MP__________')