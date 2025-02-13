import serial as sr
import threading
import queue
import dearpygui.dearpygui as dpg
import time

dataT_list = [] # Lista per la temperatura
dataU_list = [] # Lista per l'umidità
time_list = [] # Lista per il tempo (numero di letture)
count = 0 # Contatore per le letture


def Serial():
    global count
    ser = sr.Serial("COM7", 9600)
    while True:
        data = ser.readline().decode("utf-8")
        datasplit = data.split(',')
        dataT = float(datasplit[0])
        dataU = float(datasplit[1])
        print(dataT, '°C')
        print(dataU, '%')
        dpg.set_value("Temp", f"{dataT} °C")
        dpg.set_value("Umi", f"{dataU} %")
        # Aggiorna i dati della lista
        dataT_list.append(dataT)
        dataU_list.append(dataU)
        time_list.append(count)
        count += 1
        # Mantieni solo gli ultimi 50 valori per evitare problemi di performance
        if len(time_list) > 50:
            dataT_list.pop(0)
            dataU_list.pop(0)
            time_list.pop(0)
        # Aggiorna il grafico
        dpg.set_value("temp_plot", [time_list, dataT_list])
        dpg.set_value("umi_plot", [time_list, dataU_list])


def main():
    serial_thread = threading.Thread(target=Serial())
    serial_thread.start()
    dpg.create_context()
    dpg.create_viewport(title='Real-Time Sensor Data')
    with dpg.window(label="Temperatura"):
        with dpg.group(horizontal=True):
            dpg.add_text(tag="temp")
            dpg.add_text('°C')
        with dpg.group(horizontal=True):
            dpg.add_text(tag="hum")
            dpg.add_text('%')
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()


if __name__ == "__main__":
    main()
