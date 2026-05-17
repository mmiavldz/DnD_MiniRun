"""
================================================================================
MINIGAME: D&D SIMULATOR 
================================================================================
This is a short, text-based conversational role-playing game. The player creates 
a character by choosing their name, race, and class. After generating random 
attributes, an AI (GPT) generates a customized campaign introduction to set the 
mood. The main goal is to survive a turn-based combat against a randomly 
generated enemy using actions like Attack, Trick, or Surrender.

--------------------------------------------------------------------------------
WHAT IS D&D? (Dungeons & Dragons)
--------------------------------------------------------------------------------
For those unfamiliar with the original game, D&D is the world's most famous 
tabletop role-playing game. Players create fictional characters and embark on 
adventures guided by a storyteller called the Dungeon Master (DM).

Key basic concepts reflected in this code:
1. Attributes (Stats): Core characteristics like Strength, Intelligence, and 
   Charism that define how skilled the character is at certain actions.
   For example, high charisma means more chances to trick enemies while high strength 
   is better for direct attacks.

2. Classes and Races: Race (Human, Elf, Dwarf) grants physical advantages, while 
   Class (Mage, Warrior, Healer) defines the combat style and Health Points (HP).
   For example, Healers have higher HP than other classes and Dwarfs are the strongest race.

3. The d20 Dice: Most outcomes in D&D are decided by rolling a 20-sided dice.
   - A "Natural 20" is a Critical Hit (the best possible outcome, doubles damage).
   - A "Natural 1" is a Critical Fumble (the worst possible outcome, misses entirely).

4. Modifiers: The attribute score is added to the dice roll. For example, a 
   Warrior adds their Strength modifier to the d20 roll to calculate total damage.
================================================================================
"""

import random
# Checks if you´re in CIP to use ai library
try:
    from ai import call_gpt
    HAS_AI = True
except ImportError:
    HAS_AI = False

def main():
    print("Welcome traveler to Dungeon and Dragons! (kind of)")
    tutorial=str(input("Do you know how to play? (yes/no)"))
    if tutorial=="yes":
        print("Great! Let's start then.")
    else:
        print("No worries! I'll explain the basics. You will create a character and then face an enemy in a turn-based battle. You can choose to attack, try to trick the enemy, or surrender. Your goal is to defeat the enemy before they defeat you. Let's get started!")
    name = str(input("How should I call you?: "))
    print(" ")
    print(f"Well, nice to meet you {name}!")
    race = str(input("What kind of creature are you? (Human, Elf, Dwarf): "))
    print(" ")
    print("I see.. It was kind of obvious.")
    class1 = str(input("Finally, what is your class? (Mage, Warrior, Healer): "))
    print(" ")
    print("Fantastic! Now i am going to use my powers to see your attributes.. Is that ok?")
    
    player = Character(name, race, class1)
    player.mc_stats()
    
    print("Great! Now lets start this journey. First let me explain the situation..")
    print(" ")
    
    # For CIP creates a unique campaign
    if HAS_AI:
        campaign = call_gpt(f"Please write a dnd like campaign introduction to set the mood. The story must place a solo MC called {name}, dont specify gender. Their race amd class are {race} and {class1} This character has a little story and needs to figth an enemy. Nothing too long, its for a minigame. Do not include a tittle nor ai comments.") 
    # For Github has a default story
    else:
        campaign = f"Deep within the Whispering Dungeons, {name} the {race} {class1} steps into a torch-lit chamber. The heavy stone door slams shut behind you. From the shadows, a menacing growl echoes... A foe appears!"
    
    print("")
    print(campaign)
    print("")
    print("The battle begins!")
    
    enemy = Enemy()
    enemy.enemy_stats()

    while enemy.enemy_hp > 0 and player.hp > 0:
        action = input(f"{player.name}'s turn. What will you do? (Attack, Trick, Surrender): \n")
        
        if action == "Attack":
            damage = player.attack()
            enemy.enemy_hp -= damage
            print(f"{enemy.enemy_name} HP is now {enemy.enemy_hp}\n")
            
        elif action == "Trick":
            trick_roll = random.randint(1, 20)
            print(f"You roll a d20, are you able to trick {enemy.enemy_name}?:\n")
            print(f"Your roll is: {trick_roll}\n")
            if trick_roll > 10 or player.charism > 7:
                print("Enemy is successfully tricked! +5 damage\n")
                enemy.enemy_hp -= 5
                print(f"{enemy.enemy_name} HP is now {enemy.enemy_hp}\n")
            else:
                counterattack = random.randint(5, 15)
                print(f"You failed! {enemy.enemy_name} laughs at you. -{counterattack}\n")
                player.hp -= counterattack
                print(f"Your HP is now {player.hp}")
                if player.hp <= 0:
                    print("You died with honor...\n")
                    print("Game Over!")
                    break

        elif action == "Surrender":
            print(f"{player.name} throws their weapon and runs!\n")
            print("You coward! Come back here!\n")
            print("Game Over!")
            break

        if enemy.enemy_hp <= 0:
            print(f"You did it {player.name}! You defeated {enemy.enemy_name}")
            break

        print(f"{enemy.enemy_name}'s turn\n")
        player.hp -= enemy.enemy_attack()
        print(f"Your new HP is {player.hp}\n")
        
        if player.hp <= 0:
            print("You died with honor...\n")
            print("Game Over!")
            break


class Character:
    def __init__(self, name, race, class1):
        self.name = name
        self.race = race
        self.class1 = class1
        strength_range = {"Dwarf": [10, 18], "Human": [8, 15], "Elf": [5, 12]}
        min_s, max_s = strength_range.get(race, (5, 18))
        self.strength = random.randint(min_s, max_s)
        self.intelligence = random.randint(1, 15)
        self.charism = random.randint(1, 15)
        if class1 == "Mage":
            self.hp = 100
        elif class1 == "Warrior":
            self.hp = 80
        elif class1 == "Healer":
            self.hp = 120
        else:
            self.hp = 50

    def mc_stats(self):
        print(" ")
        print(f"==== {self.name}'s stats ====")
        print(f"Your Strength is: {self.strength}")
        print(f"Your Intelligence is: {self.intelligence}")
        print(f"Your Charism is: {self.charism}")
        print(f"Your HP is: {self.hp}")
        print("=======================")
        print(" ")

    def attack(self):
        dice_roll = random.randint(1, 20)
        if self.class1 == "Warrior":
            modifier = self.strength
        elif self.class1 == "Mage":
            modifier = self.intelligence
        else:
            modifier = self.charism
        
        total_attack = dice_roll + modifier
        print(f"{self.name} rolls a d20: {dice_roll}\n")
        
        if dice_roll == 20:
            buffed_attack = total_attack * 2
            print(f"Critic! You doubled the damage: {buffed_attack}\n")
        elif dice_roll == 1:
            buffed_attack = 0
            print(f"You tripped and missed! No damage for the oponent.\n")
        else:
            buffed_attack = total_attack
            print(f"Your attack damage is {buffed_attack}. No buff applied.\n")
            
        return buffed_attack


class Enemy:
    def __init__(self):
        # For CIP uses ai library to create the enemy
        if HAS_AI:
            self.enemy_name = call_gpt("Create JUST ONE random enemy dnd like name. Do not explain nor comment.")
            self.enemy_race = call_gpt("Choose JUST ONE random enemy race from dnd. Do not explain nor comment.")
        # For github uses pre-created enemies
        else:
            self.enemy_name = random.choice(["Gorgoroth", "Xanathar", "Malakor", "Skraan"])
            self.enemy_race = random.choice(["Orc", "Goblin", "Beholder", "Dark Elf"])
            
        self.enemy_hp = random.randint(80, 200)
        self.enemy_strength = random.randint(5, 20)

    def enemy_stats(self):
        print(" ")
        print(f"==== {self.enemy_name} ====")
        print(f"Enemy race: {self.enemy_race}")
        print(f"Enemy HP: {self.enemy_hp}")
        print(f"Enemy strength: {self.enemy_strength}")
        print("====================")
        print(" ")

    def enemy_attack(self):
        dmg = random.randint(1, 10) + self.enemy_strength
        print(f"{self.enemy_name} counterattacks with {dmg} damage!\n")
        return dmg


if __name__ == "__main__":
    main()
