from .world import KillerWorld
import os


def killer_world():
    world = KillerWorld()
    print(world)

    while True:
        os.system("clear")
        print(world)
        world.step()
        # sleep((1 / 30) * 2)  # 30 fps, frame on 2s
