# -*- coding: utf8 -*-

import humanmodifier
from Render import my_render


def finished_modify():
    pass


# def modify_model(human, features_queue):
#     while not features_queue.empty():
#         feature = features_queue.get()
#         modifier = human.getModifier(feature["Modifier"])
#         action = humanmodifier.ModifierAction(modifier, 0, feature["Value"], finished_modify)
#         action.do()

# def modify_model(human, individuals_queue):
#     models_data = []
#     while not individuals_queue.empty():
#         individual = individuals_queue.get()
#         while not individual.empty():
#             feature = individual.get()
#             modifier = human.getModifier(feature["Modifier"])
#             action = humanmodifier.ModifierAction(modifier, 0, feature["Value"], finished_modify)
#             action.do()
#         models_data.append(human.mesh.__dict__["coord"].tolist())
#     return models_data

def modify_model(human, individual):
    for feature in individual:
        modifier = human.getModifier(feature["Modifier"])
        action = humanmodifier.ModifierAction(modifier, 0, feature["Value"], finished_modify)
        action.do()


def render_faces(human, individuals):
    for individual in individuals:
        modify_model(human, individual)

        image = my_render()
        yield image