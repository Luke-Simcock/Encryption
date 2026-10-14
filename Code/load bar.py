import sys
import time
import threading




def loader_animation():
    global running
    width = 25
    block_size = 5 
    position = 0
    direction = 1 
    running = True
    
    while running:
        track = ['='] * width
        for i in range(block_size):
            if 0 <= position + i < width:
                track[position + i] = '#'
        sys.stdout.write(f"\r[{''.join(track)}]")
        sys.stdout.flush()
        
        position += direction
        if position == (width - 3) or position == -2:
            direction *= -1
        time.sleep(0.05) 

animation_thread = threading.Thread(target=loader_animation)
animation_thread.start()
