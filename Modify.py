# -*- coding: utf8 -*-

import time
import humanmodifier
from Render import my_render


def finished_modify():
    pass


def modify_model(human, individual):
    for feature in individual:
        modifier = human.getModifier(feature["Modifier"])
        action = humanmodifier.ModifierAction(modifier, 0, feature["Value"], finished_modify)
        action.do()
        # time.sleep(0.05)


def render_faces(human, individuals):
    for individual in individuals:
        modify_model(human, individual)

        image = my_render()
        yield image