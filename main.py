import random
from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

# Create Black Magic
fire = Spell('Fire', 10, 100, 'black')
thunder = Spell('Thunder', 10, 100, 'black')
blizzard = Spell('Blizzard', 10, 100, 'black')
meteor = Spell('Meteor', 20, 200, 'black')
quake = Spell('Quake', 12, 120, 'black')

# Create White Magic
cure = Spell('Cure', 12, 120, 'white')
cura = Spell('Cura', 18, 200, 'white')

# Create some Items
potion = Item('Potion', 'potion', 'Heals 50 HP', 50)
hipotion = Item('Hi-Potion', 'potion', 'Heals 100 HP', 100)
superpotion = Item('Super Potion', 'potion', 'Heals 500 HP', 500)
elixer = Item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 9999)
hielixer = Item('MegaElixer', 'elixer', 'Fully restores party\'s HP/MP', 9999)

grenade = Item('Grenade', 'attack', 'Deals 500 damage', 500)

player_spell = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{'item':potion, 'quantity': 5}, {'item':hipotion, 'quantity': 5},
                {'item':superpotion, 'quantity': 5}, {'item':elixer, 'quantity': 5},
                {'item':hielixer, 'quantity': 2}, {'item':grenade, 'quantity': 5}]

player1 = Person('Mandy', 460, 65, 60, 34, player_spell, player_items)
player2 = Person('Nick', 460, 65, 60, 34, player_spell, player_items)
player3 = Person('Oscar', 460, 65, 60, 34, player_spell, player_items)

enemy1 = Person('Bat',1200,65, 45, 25, [], [])
enemy2 = Person('enemy',6000,65, 45, 25, [], [])
enemy3 = Person('Bat',1200,65, 45, 25, [], [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True

print(bcolors.FAIL + bcolors.BOLD + 'AN ENEMY ATTACKS!' + bcolors.ENDC)

while running:

    player1.get_stat_text()
    for player in players:
        player.get_stat()

    print('\n')

    enemy1.get_stat_text()
    for enemy in enemies:
        enemy.get_stat()

    # decide if battle end
    number_of_player = len(players)
    for player in players:
        dead_player_number = 0;
        if player.get_hp() <= 0:
            dead_player_number += 1
        if dead_player_number == number_of_player:
            running = False
            break
    if enemy.get_hp() <= 0:
        print(bcolors.OKGREEN + 'You win!' + bcolors.ENDC)
        running = False
        break

    print('============================')
    for player in players:
        player.choose_action()
        choice = input('Choose action:')
        index = int(choice) - 1
        print(player.name, 'choose ' + choice)

        # choose attack
        if index == 0:
            damage = player.generate_damage()

            # choose target
            choice = player.choose_target(enemies)
            target = enemies[choice]
            target.take_damage(damage)
            print(player.name, 'attack for ' + str(damage) + ' points of damage. ' + target.name + ' HP:' + str(target.get_hp()))

            # remove died enemy
            if target.get_hp() == 0:
                del enemies[choice]
                print(target.name + 'has died.')

        # choose magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('Choose magic:')) - 1

            # back to menu
            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_damage = spell.generate_damage()

            current_mp = player.get_mp()

            #not enough mp, so choose action again
            if current_mp <= spell.cost:
                print(bcolors.FAIL + '\n Not enough Mp. \n', bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                # choose target
                choice = player.choose_target(players)
                target = players[choice]
                target.heal(magic_damage)

                print(bcolors.OKBLUE + spell.name + ' heals ' + target.name + ' for', str(magic_damage) + ' HP', bcolors.ENDC)
            elif spell.type == 'black':

                # choose target
                choice = player.choose_target(enemies)
                target = enemies[choice]
                target.take_damage(magic_damage)
                print(bcolors.OKGREEN + spell.name + 'deals ' + str(magic_damage) + ' points of damage. ' + target.name + ' HP:' + str(target.get_hp()), bcolors.ENDC)

                # remove died enemy
                if target.get_hp() == 0:
                    del enemies[choice]
                    print(target.name + 'has died.')
        # choose item
        elif index == 2:
            player.choose_item()
            item_choice = int(input('Choose item:')) - 1

            #back to menu
            if item_choice == -1:
                continue

            item = player.items[item_choice]['item']
            if player.items[item_choice]['quantity'] > 0:
                player.items[item_choice]['quantity'] -= 1
            else:
                print(bcolors.FAIL, player.name,  'don\'t have enough item!', bcolors.ENDC)
                continue

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + ' heals for', str(item.prop), 'HP' + bcolors.ENDC)
            elif item.type == 'elixer':
                if item.name == 'MegaElixer':
                    for i in players:
                        i.hp = player.max_hp
                else:
                    player.mp = player.max_mp
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                
                print(bcolors.OKGREEN + '\n' + item.name + ' Fully restore HP/MP' + bcolors.ENDC)
            elif item.type == 'attack':
                # choose target
                choice = player.choose_target(enemies)
                target = enemies[choice]
                target.take_damage(item.prop)

                print(bcolors.FAIL + '\n' + item.name + ' deals', str(item.prop), 'points of damage' + bcolors.ENDC)
                
                # remove died enemy
                if target.get_hp() == 0:
                    del enemies[choice]
                    print(target.name + 'has died.')
    
    # enemy actions
    for enemy in enemies:
        enemy.choice = 1
        enemy_damage = enemy.generate_damage()
        target = players[random.randrange(0,2)]
        target.take_damage(enemy_damage)
        print(enemy.name + ' attack', bcolors.FAIL ,target.name, bcolors.ENDC, 'for', enemy_damage, 'points of damage. Player HP:', target.get_hp())

    print('============================')
    