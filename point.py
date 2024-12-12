import cv2
import numpy as np
import pyautogui
#
screenshot = pyautogui.screenshot()

obraz = np.array(screenshot)
obraz = cv2.cvtColor(obraz, cv2.COLOR_RGB2BGR)  # Konwersja kolorów

punkty= [(int(obraz.shape[1]*0.046875),int(obraz.shape[0]*0.38)),(int(obraz.shape[1]*0.086),int(obraz.shape[0]*0.459)),
        (int(obraz.shape[1] * 0.046875), int(obraz.shape[0] * 0.47)),(int(obraz.shape[1] * 0.086),int(obraz.shape[0] * 0.535)),
        (int(obraz.shape[1] * 0.046875), int(obraz.shape[0] * 0.55)),(int(obraz.shape[1] * 0.086), int(obraz.shape[0] * 0.615)),
        (int(obraz.shape[1] * 0.046875), int(obraz.shape[0] * 0.63)),(int(obraz.shape[1] * 0.086), int(obraz.shape[0] * 0.70))
        ]
for (x, y) in punkty:
     cv2.circle(obraz, (x, y), 5, (0, 0, 255), -1)  # Czerwony punkt

    # Wyświetlenie obrazu
cv2.imshow("Zrzut ekranu z punktami", obraz)
cv2.waitKey(0)
cv2.destroyAllWindows()
