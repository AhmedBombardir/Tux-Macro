import gui

# Field selection
field = "Clover"  # Options: Clover, Mushroom, Spider, Bamboo, Strawberry, Blue Flower, Pine Tree, Pineapple, Pumpkin, Cactus, Stump, Rose, Dandelion, Sunflower, Pepper

# Gather pattern
pattern = "CornerXSnake"  # Options: CornerXSnake, E_lol, Stationary

# Gather time (in seconds)
gatherTime = 300  # 5 minutes

# Sprinkler type
sprinkler = "Basic"  # Options: Basic, Silver, Golden, Diamond, Supreme

# Hive slot (1-6)
hiveSlot = 1

# Movespeed
moveSpeed = 29

# Bug Kill Settings
gather_interrupt = False  # If True, macro will interrupt gathering to kill bugs. If False, waits until gather finishes.

# Bug respawn times (in seconds) - default values
bug_respawn_times = {
    "ladybug": 120,      # 2 minutes
    "beetle": 120,       # 2 minutes
    "werewolf": 3600,    # 1 hour
    "mantis": 1200,      # 20 minutes
    "scorpion": 1200,    # 20 minutes
    "spider": 1800,      # 30 minutes
}