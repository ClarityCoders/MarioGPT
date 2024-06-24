from GPT import get_message
import json
import retro
from PIL import Image
import time
import json
import csv
import keyboard

PROMPT = """
Objective: 
Avoid collision with all enemies and safely reach the end of the level. 

Environment: 
Try your best use knowledge of Super Mario Brothers for SNES

JSON Format:
move: A dictionary specifying which buttons to press. Keys must include "left", "right", "jump", and "run", with boolean values (true/false).
thoughts: Provide one line explaining why you are making that move. 
Be as funny as possible like P-13 movie funny
sleep: Number of frames to sleep. Use smaller values (e.g., 20) for high-action situations and larger values (e.g., 80+) for safer situations.
"""

comments = []

def update_move(gpt_dict):
    move = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    if gpt_dict["jump"]:
        move[0] = 1
    if gpt_dict["run"]:
        move[1] = 1
    if gpt_dict["left"]:
        move[6] = 1
    if gpt_dict["right"]:
        move[7] = 1

    return move

def main():
    try:

        current_move = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        steps = 1
        env = retro.make(game='SuperMarioWorld-Snes', record='.')
        env.seed(2024)
        env.action_space.seed(2024)
        obs = env.reset()
        response = {"move": {}}
        sleep = 20
        current_image = "your_file.jpeg"
        while True:
            obs, rew, done, info = env.step(current_move) 
            env.render()
            time.sleep(.01)
            if steps % sleep == 0 and steps > 100:
                im = Image.fromarray(obs)
                previous_image = current_image
                current_image = f"./images/your_file{steps}.jpeg"
                im.save(current_image)
                last_move = PROMPT + f" Your Last move was: {json.dumps(response['move'])}"
                response = json.loads(get_message(current_image, PROMPT, last_move))

                if "move" in response.keys():
                    move = response["move"]
                    thoughts = response["thoughts"]
                    sleep = response["sleep"]
                    print(f"Move: {move}")
                    print(f"Thoughts: {thoughts}")
                    print(f"sleep: {sleep}")
                    current_move = update_move(move)
                    print("Current_Move: ", current_move)
                    comments.append([steps, thoughts])
                else:
                    print("Uh oh.")
                    current_move = [0,0,0,0,0,0,0,0,0,0,0,0,0]
                    response = {"move": {'left': False, 'right': False, 'jump': False, 'run': False}}
            
            steps += 1

            if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                with open('output.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(comments)
                break
            if done:
                break
        env.close()
    except:
        env.unwrapped.stop_record()


if __name__ == "__main__":
    main()