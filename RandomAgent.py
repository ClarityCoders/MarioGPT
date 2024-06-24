import base64
import retro


def main():
    #Airstriker-Genesis
    #SuperMarioWorld-Snes
    env = retro.make(game='Airstriker-Genesis')
    print(env.action_space)
    obs = env.reset()
    while True:
        obs, rew, done, info = env.step(env.action_space.sample())
        img = obs.tobytes()
        # print( base64.b64encode(img).decode("utf-8"))
        env.render()
        if done:
            obs = env.reset()
    env.close()


if __name__ == "__main__":
    main()