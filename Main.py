import serial as sr
import threading
import dearpygui.dearpygui as dpg
import time

time_list = []
dataT_list = []
dataU_list = []
count = 0
nsamples = 50

def Serial():
    global count
    ser = sr.Serial("COM8", 9600, timeout=1)

    while True:
        try:
            data = ser.readline().decode("utf-8").strip()
            if not data:
                continue

            datasplit = data.split(',')
            temp = float(datasplit[0])
            hum = float(datasplit[1])
            print(f"Temperature: {temp} °C, Humidity: {hum} %")

            dataT_list.append(temp)
            dataU_list.append(hum)
            time_list.append(count)
            count += 1

            if len(time_list) > nsamples:
                dataT_list.pop(0)
                dataU_list.pop(0)
                time_list.pop(0)
        except Exception as e:
            print("Error reading serial data:", e)

def update_plot():
    if time_list:
        dpg.set_value("temp_series", [time_list, dataT_list])
        dpg.set_value("hum_series", [time_list, dataU_list])

        # Set the x-axis limits to keep the graph within the desired range
        dpg.set_axis_limits("x_axis", min(time_list), max(time_list))

def graphics_task():
    dpg.create_context()
    dpg.create_viewport(title='Real-Time Sensor Data', width=800, height=600)

    with dpg.window(label="Sensor Data", tag="win"):
        with dpg.plot(label="Sensor Readings", height=400, width=600):
            dpg.add_plot_legend()
            dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="x_axis")
            dpg.add_plot_axis(dpg.mvYAxis, label="Value", tag="y_axis")

            dpg.add_line_series([], [], label="Temperature (°C)", parent="y_axis", tag="temp_series")
            dpg.add_line_series([], [], label="Humidity (%)", parent="y_axis", tag="hum_series")
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
