import serial as sr
import threading
import dearpygui.dearpygui as dpg
import json
import time

data_list = []
nsamples = 50
json_file = "data_sensore.json"

def save_to_json():
    data = {"dati": data_list}
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

def Serial():
    ser = sr.Serial("COM8", 9600, timeout=1)
    while True:
        try:
            data = ser.readline().decode("utf-8").strip()
            if not data:
                continue
            datasplit = data.split(',')
            temp = float(datasplit[0])
            hum = float(datasplit[1])
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(f"Time: {timestamp}, Temperature: {temp} °C, Humidity: {hum} %")
            data_list.append({"time": timestamp, "temperature": temp, "humidity": hum})
            if len(data_list) > nsamples:
                data_list.pop(0)
            save_to_json()
        except Exception as e:
            print("Errore lettura seriale:", e)


def update_plot():
    if data_list:
        time_stamps = list(range(len(data_list)))
        dpg.set_value("temp_series", [time_stamps, [d["temperature"] for d in data_list]])
        dpg.set_value("hum_series", [time_stamps, [d["humidity"] for d in data_list]])
        dpg.set_axis_limits("x_axis", min(time_stamps), max(time_stamps))


def graphics_task():
    dpg.create_context()
    dpg.create_viewport(title='Grafico sensore', width=800, height=600)
    with dpg.window(label="Grafico sensore", tag="win"):
        with dpg.plot(label="Grafico sensore", height=400, width=600):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Indice valori", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Valori", tag="y_axis")
            dpg.add_line_series([], [], label="Temperatura (°C)", parent="y_axis", tag="temp_series")
            dpg.add_line_series([], [], label="Umidita (%)", parent="y_axis", tag="hum_series")
    dpg.setup_dearpygui()
    dpg.show_viewport()
    while dpg.is_dearpygui_running():
        update_plot()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()

def main():
    serial_thread = threading.Thread(target=Serial, daemon=True)
    serial_thread.start()
    graphics_task()

if __name__ == "__main__":
    main()
