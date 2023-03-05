import os
from time import sleep

from .agent import random_agent
from .world import FoodWorld


def food_world():
    world = FoodWorld()

    agent = random_agent(world)

    while True:
        observations = world.get_agent_observation()
        agent.infer_states(observations)
        agent.infer_policies()

        action = world.action_names[int(agent.sample_action()[0])]

        world.print()
        os.system("clear")

        if world.agent_energy <= 0:
            print("☠️ Agent Died ☠️")
            break

        world.move(action)
        sleep((1 / 30) * 2)  # 30 fps, frame on 2s
