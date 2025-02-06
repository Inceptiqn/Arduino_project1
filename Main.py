import serial as sr
import multiprocessing as mp
import dearpygui.dearpygui as dpg

def serial_task(queue: mp.Queue):
    serial_conn = sr.Serial("COM11", 9600)
    while True:
        data = serial_conn.readline()
        data = data.decode("utf-8").strip()
        try:
            valore = float(data)
            queue.put(valore)
        except ValueError:
            pass  # Ignora dati non validi

def app():
    q = mp.Queue()
    serial_process = mp.Process(target=serial_task, args=(q,))
    serial_process.start()

    valore = 0.0
    valori = []
    dpg.create_context()
    dpg.create_viewport(title="Serial Data Visualization", width=800, height=450)

    with dpg.window(label="Main Window", width=800, height=450):
        dpg.add_text("Valore:")
        text_id = dpg.add_text(f"{valore}")
        with dpg.plot(label="Serial Data Graph", height=200, width=700):
            dpg.add_plot_axis(dpg.mvXAxis, label="Time", tag="x_axis")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")
            series_id = dpg.add_line_series([], [], parent=y_axis)

    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        if not q.empty():
            valore = q.get()
            valori.append(valore)
            if len(valori) > 50:
                valori.pop(0)
            dpg.set_value(text_id, f"Valore: {valore}")
            dpg.set_value(series_id, [list(range(len(valori))), valori])
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    serial_process.terminate()
    serial_process.join()

if __name__ == "__main__":
    mp.freeze_support()
    app()
