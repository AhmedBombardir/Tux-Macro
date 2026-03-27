import gui, paths

# Field selection
field = "Clover"  # Options: Clover, Mushroom, Spider, Bamboo, Strawberry, Blue Flower, Pine Tree, Pineapple, Pumpkin, Cactus, Stump, Rose, Dandelion, Sunflower, Pepper
# Gather pattern
pattern = "CornerXSnake"  # Options: CornerXSnake, E_lol, Stationary


collect_dict = {
    # Collect settings
    # Collect
    "wealth_clock": (False, 3600),
    "mondo": (False, 2700),
    "ant_pass": (False, 7200),
    "robo_pass": (False, 79200),
    # Dispensers
    "honey_dispenser": (False, 3600),
    "treat_dispenser": (False, 3600),
    "blueberry_dispenser": (False, 14400),
    "strawberry_dispenser": (False, 14400),
    "coconut_dispenser": (False, 14400),
    "glue_dispenser": (False, 79200),
    # Beesmass
    "stockings": (False, 3600),
    "wreath": (False, 1800),
    "feast": (False, 5400),
    "robo_party": (False, 10800),
    "gingerbread": (False, 7200),
    "snow_machine": (False, 7200),
    "candles": (False, 14400),
    "honeystorm": (False, 14400),
    "samovar": (False, 21600),
    "lid_art": (False, 28800),
    "gummy_beacon": (False, 28800),
}

collect_paths = {
    "wealth_clock": paths.Cannon_wealth_clock,
    "mondo": paths.Cannon_mondo,
    "ant_pass": paths.Ant_pass,
    "robo_pass": paths.Cannon_robo_pass,
    "honey_dispenser": paths.Honey_dispenser,
    "treat_dispenser": paths.Treat_dispenser,
    "blueberry_dispenser": paths.Cannon_blueberry_dispenser,
    "strawberry_dispenser": paths.Cannon_strawberry_dispenser,
    "coconut_dispenser": paths.Coconut_dispenser,
    "glue_dispenser": paths.Glue_dispenser,
    "stockings": paths.Cannon_stockings,
    "wreath": paths.wreath,
    "feast": paths.Cannon_feast,
    "robo_party": paths.Cannon_robo_party,
    "gingerbread": paths.Cannon_gingerbread,
    "snow_machine": paths.Cannon_snow_machine,
    "candles": paths.Cannon_candles,
    "honeystorm": paths.Cannon_honeystorm,
    "samovar": paths.Cannon_samovar,
    "lid_art": paths.Cannon_lid_art,
    "gummy_beacon": paths.Cannon_gummy_beacon,
}


# Gather time (in seconds)
gatherTime = 600  # 5 minutes

# Bug Run
bug_run_enabled = False

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
