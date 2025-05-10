import keyboard
import pyautogui
import time
import math
from ctypes import windll

# Настройки (можно менять перед запуском)
MOVE_SPEED = 50         # Скорость движения (пикселей за шаг)
MAX_RADIUS = 200        # Максимальный радиус от центра (пиксели)
ATTACK_KEY = "f"        # Клавиша атаки
CENTER_DELAY = 0.3      # Плавный возврат в центр (сек)

user32 = windll.user32

def send_left_click():
    user32.mouse_event(2, 0, 0, 0, 0)  # ЛКМ вниз
    time.sleep(0.02)
    user32.mouse_event(4, 0, 0, 0, 0)  # ЛКМ вверх

def wasd_mouse_control():
    print("WASD - движение от центра + ЛКМ, F - атака. Закрой консоль для выхода.")
    print(f"Текущие настройки: Скорость = {MOVE_SPEED}, Радиус = {MAX_RADIUS}")
    
    center_x, center_y = pyautogui.size()[0]//2, pyautogui.size()[1]//2
    pyautogui.moveTo(center_x, center_y)
    
    wasd_active = False
    last_mouse_pos = center_x, center_y
    
    while True:
        current_wasd = any(keyboard.is_pressed(k) for k in ['w','a','s','d'])
        
        if current_wasd:
            wasd_active = True
            x, y = 0, 0
            moved = False
            
            if keyboard.is_pressed('w'):
                y -= MOVE_SPEED
                moved = True
            if keyboard.is_pressed('a'):
                x -= MOVE_SPEED
                moved = True
            if keyboard.is_pressed('s'):
                y += MOVE_SPEED
                moved = True
            if keyboard.is_pressed('d'):
                x += MOVE_SPEED
                moved = True

            if moved:
                new_x, new_y = pyautogui.position()[0] + x, pyautogui.position()[1] + y
                
                # Проверка радиуса
                dx = new_x - center_x
                dy = new_y - center_y
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance > MAX_RADIUS:
                    # Корректируем позицию, чтобы оставаться в пределах круга
                    angle = math.atan2(dy, dx)
                    new_x = center_x + MAX_RADIUS * math.cos(angle)
                    new_y = center_y + MAX_RADIUS * math.sin(angle)
                
                pyautogui.moveTo(new_x, new_y, duration=0)
                last_mouse_pos = new_x, new_y
                send_left_click()  # Клик при движении
        elif wasd_active:
            wasd_active = False
            pyautogui.moveTo(center_x, center_y, CENTER_DELAY)
            last_mouse_pos = center_x, center_y
        
        # Клавиша атаки (F)
        if keyboard.is_pressed(ATTACK_KEY):
            send_left_click()
            time.sleep(0.1)
        
        time.sleep(0.01)

if __name__ == "__main__":
    wasd_mouse_control()