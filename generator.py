from random import randint, choice
from settings import *
from planet import *

def genetare(game):
    result = []

    sun_radius = randint(PLANETS_SUN_MIN_RADIUS, PLANETS_SUN_MAX_RADIUS)
    sun_x = randint(sun_radius, PLANETS_SUN_SPREAD_X) * choice([1, -1])
    sun_y = randint(sun_radius, PLANETS_SUN_SPREAD_Y) * choice([1, -1])
    result.append(Planet(game, sun_x, sun_y, sun_radius, sun_radius * PLANETS_SUN_GRAVITY_RATIO, True))

    for _ in range(PLANETS_COUNT - 1):
        planet_radius = randint(PLANETS_MIN_RADIUS, PLANETS_MAX_RADIUS)
        planet_x = randint(planet_radius, PLANETS_SPREAD_X) * choice([1, -1])
        planet_y = randint(planet_radius, PLANETS_SPREAD_Y) * choice([1, -1])
        planet_speed = randint(PLANETS_MIN_SPEED * 100, PLANETS_MAX_SPEED * 100) * choice([1, -1]) / 100
        result.append(Planet(game, planet_x, planet_y, planet_radius, planet_radius * PLANETS_GRAVITY_RATIO, False, result[0], planet_speed))
    
    return result