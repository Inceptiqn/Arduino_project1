import serial
import threading
import dearpygui.dearpygui as dpg
import json
import time

DATA_FILE = "data_sensore.json"
DATA_LIST = []
NSAMPLES = 50


def save_to_json():
    with open(DATA_FILE, "w") as file:
        json.dump({"dati": DATA_LIST}, file, indent=4)


def read_serial():
    ser = serial.Serial("COM8", 9600, timeout=1)
    while True:
        try:
            data = ser.readline().decode().strip()
            if not data:
                continue
            temp, hum = map(float, data.split(','))
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print(f"Time: {timestamp}, Temperature: {temp} °C, Humidity: {hum} %")
            DATA_LIST.append({"time": timestamp, "temperature": temp, "humidity": hum})
            if len(DATA_LIST) > NSAMPLES:
                DATA_LIST.pop(0)
            save_to_json()
        except Exception as e:
            print("Errore lettura seriale:", e)


def update_plot():
    if DATA_LIST:
        times = list(range(len(DATA_LIST)))
        temps = [i["temperature"] for i in DATA_LIST]
        hums = [i["humidity"] for i in DATA_LIST]

        dpg.set_value("temp_series", [times, temps])
        dpg.set_value("hum_series", [times, hums])
        dpg.set_axis_limits("x_axis", min(times), max(times))
        dpg.set_axis_limits("y_axis", 0, 50)
        dpg.configure_item("temp_series", label=f"Temperatura (°C): {temps[-1]:.2f}")
        dpg.configure_item("hum_series", label=f"Umidità (%): {hums[-1]:.2f}")


def graphics_task():
    dpg.create_context()
    dpg.create_viewport(title='Grafico sensore', width=800, height=600)
    with dpg.window(label="Grafico sensore", tag="fullscreen"):
        with dpg.plot(height=1000, width=1200):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Indice valori", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Valori", tag="y_axis")
            dpg.add_line_series([], [], label="Temperatura (°C)", parent="y_axis", tag="temp_series")
            dpg.add_line_series([], [], label="Umidità (%)", parent="y_axis", tag="hum_series")
    dpg.setup_dearpygui()
    dpg.set_primary_window("fullscreen", True)
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        update_plot()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()


def main():
    threading.Thread(target=read_serial, daemon=True).start()
    graphics_task()


if __name__ == "__main__":
    main()