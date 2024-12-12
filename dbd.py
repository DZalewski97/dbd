import cv2
import numpy as np
import pyautogui
import os
import tkinter as tk
from threading import Thread
import time
import keyboard


script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir,"hook.png")

counter_surv_1 = 0
counter_surv_2 = 0
counter_surv_3 = 0
counter_surv_4 = 0

template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

template_height,template_width = template.shape[:2]

previous_states = [False, False, False, False]

def find_template():
    global counter_surv_1,counter_surv_2,counter_surv_3,counter_surv_4,previous_states

    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    screen_rgb = cv2.cvtColor(screen_np, cv2.COLOR_BGR2RGB)
    screen_gray = cv2.cvtColor(screen_rgb, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)


    result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    #loc = np.where(result >= threshold)

    regions = [[int(screen_rgb.shape[1]*0.046875),int(screen_rgb.shape[0]*0.38),int(screen_rgb.shape[1]*0.086),int(screen_rgb.shape[0]*0.459)],
               [int(screen_rgb.shape[1] * 0.046875), int(screen_rgb.shape[0] * 0.47), int(screen_rgb.shape[1] * 0.086), int(screen_rgb.shape[0] * 0.535)],
               [int(screen_rgb.shape[1] * 0.046875), int(screen_rgb.shape[0] * 0.55), int(screen_rgb.shape[1] * 0.086), int(screen_rgb.shape[0] * 0.615)],
               [int(screen_rgb.shape[1] * 0.046875), int(screen_rgb.shape[0] * 0.63), int(screen_rgb.shape[1] * 0.086), int(screen_rgb.shape[0] * 0.70)]
               ]
    # print(regions)
    current_states = [False] * len(regions)

    for i, (x1, y1, x2, y2) in enumerate(regions):
        region_result = result[y1:y2, x1:x2]
        loc_in_region = np.where(region_result >= threshold)

        if len(loc_in_region[0]) > 0:
            current_states[i] = True

            if not previous_states[i]:
                print(f"Obrazek znaleziony w regionie {i + 1}!")
                if i == 0 and counter_surv_1 < 3:
                    counter_surv_1 += 1
                elif i == 1 and counter_surv_2 < 3:
                    counter_surv_2 += 1
                elif i == 2 and counter_surv_3 < 3:
                    counter_surv_3 += 1
                elif i == 3 and counter_surv_4 < 3:
                    counter_surv_4 += 1

    previous_states = current_states

    if keyboard.is_pressed("1") and counter_surv_1 < 3 and not keyboard.is_pressed("ctrl"):
        counter_surv_1 += 1
    elif keyboard.is_pressed("1") and counter_surv_1 > 0 and keyboard.is_pressed("ctrl"):
        counter_surv_1 -= 1

    if keyboard.is_pressed("2") and counter_surv_2 < 3 and not keyboard.is_pressed("ctrl"):
        counter_surv_2 += 1
    elif keyboard.is_pressed("2") and counter_surv_2 > 0 and keyboard.is_pressed("ctrl"):
        counter_surv_2 -= 1


    if keyboard.is_pressed("3") and counter_surv_3 < 3 and not keyboard.is_pressed("ctrl"):
        counter_surv_3 += 1
    elif keyboard.is_pressed("3") and counter_surv_3 > 0 and keyboard.is_pressed("ctrl"):
        counter_surv_3 -= 1


    if keyboard.is_pressed("4") and counter_surv_4 < 3 and not keyboard.is_pressed("ctrl"):
        counter_surv_4 += 1
    elif keyboard.is_pressed("4") and counter_surv_4 > 0 and keyboard.is_pressed("ctrl"):
        counter_surv_4 -= 1



def show_overlay():

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.7)
    root.wait_visibility(root)
    root.configure(bg='black')
    root.geometry('100x120+50+50')
    root.overrideredirect(True)


    label1 = tk.Label(root, text=f"Region 1: {counter_surv_1}", fg="white", bg="black", font=("Arial", 16))
    label2 = tk.Label(root, text=f"Region 2: {counter_surv_2}", fg="white", bg="black", font=("Arial", 16))
    label3 = tk.Label(root, text=f"Region 3: {counter_surv_3}", fg="white", bg="black", font=("Arial", 16))
    label4 = tk.Label(root, text=f"Region 4: {counter_surv_4}", fg="white", bg="black", font=("Arial", 16))

    label1.pack()
    label2.pack()
    label3.pack()
    label4.pack()


    def update_labels():
        while True:
            label1.config(text=f"{counter_surv_1}")
            label2.config(text=f"{counter_surv_2}")
            label3.config(text=f"{counter_surv_3}")
            label4.config(text=f"{counter_surv_4}")
            time.sleep(0.1)


    Thread(target=update_labels, daemon=True).start()


    root.mainloop()

def main():

    Thread(target=lambda: [find_template() for _ in iter(int, 1)], daemon=True).start()


    show_overlay()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)