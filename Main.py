import serial as sr
import multiprocessing as mp
from pyray import *
def serial_task(queue:mp.Queue):
    serial_conn = sr.Serial("COM11", 9600)
    while True:
        data = serial_conn.readline()
        data = data.decode("utf-8")
        data = float(data)
        queue.put(data)

def app():
    q = mp.Queue()
    serial_process = mp.Process(target=serial_task,args=(q,))
    serial_process.start()
    valore = 0
    init_window(800, 450, "Hello")
    while not window_should_close():
        if not q.empty():
            valore = q.get()
        begin_drawing()
        clear_background(WHITE)
        draw_circle(400,300,50+valore,RED)
        draw_text(f"valore={valore}", 190, 200, 20, VIOLET)
        end_drawing()
    close_window()

if __name__ == "__main__":
    mp.freeze_support()
    app()