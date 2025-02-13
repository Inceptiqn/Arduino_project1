import serial as sr
import threading
import queue
import dearpygui.dearpygui as dpg
import time

nsamples = 100  # Number of samples to display


def serial_task(q: queue.Queue):
    serial_conn = sr.Serial("COM7", 9600)
    while True:
        data = serial_conn.readline().decode("utf-8").strip()
        try:
            temp, hum = map(float, data.split(","))
            q.put((time.time(), temp, hum))
        except ValueError:
            print("Error: Invalid data format")


def graphics_task(q: queue.Queue):
    dpg.create_context()

    time_data = []  # Time stamps
    temp_data = []  # Temperature values
    hum_data = []  # Humidity values

    def update_series():
        if not q.empty():
            timestamp, temp, hum = q.get()
            time_data.append(timestamp)
            temp_data.append(temp)
            hum_data.append(hum)

            # Keep only the latest nsamples data points
            if len(time_data) > nsamples:
                time_data.pop(0)
                temp_data.pop(0)
                hum_data.pop(0)

            dpg.set_value('temp_series', [time_data, temp_data])
            dpg.set_value('hum_series', [time_data, hum_data])

    with dpg.window(label="Sensor Data", tag="win"):
        dpg.add_button(label="Update Series", callback=update_series)
        with dpg.plot(label="Sensor Readings", height=400, width=600):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)")
            dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")
            dpg.add_line_series([], [], label="Temperature (°C)", parent="y_axis", tag="temp_series")
            dpg.add_line_series([], [], label="Humidity (%)", parent="y_axis", tag="hum_series")

    dpg.create_viewport(title='Real-Time Sensor Data', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()


def main():
    q = queue.Queue()
    serial_thread = threading.Thread(target=serial_task, args=(q,), daemon=True)
    serial_thread.start()
    graphics_task(q)


if __name__ == "__main__":
    main()
