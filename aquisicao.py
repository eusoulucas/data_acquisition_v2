import nidaqmx
import nidaqmx.system
import nidaqmx.constants
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import time
import numpy as np
import sys #encerrar o programa

class LiveGraph:
    def __init__(self, titulo, intervalo, canal, taxa_aq, tempo_ct, taxa_arm):
        self.x_data, self.y_data = [], []
        self.canal = canal
        self.taxa_aq = float(taxa_aq)
        self.tempo_ct = tempo_ct
        self.taxa_de_armazenamento = taxa_arm

        '''self.figure = plt.figure()
        self.title = plt.title(titulo)
        self.xlabel = plt.xlabel("Amostras (n)")
        self.ylabel = plt.ylabel("Tensão (V)")
        self.line, = plt.plot(self.x_data, self.y_data)

        self.animation = FuncAnimation(self.figure, self.update, interval=intervalo)'''
        self.inicio = time.time()
        self.th = Thread(target = self.thread_f, daemon=True)
        self.th.start()
        self.th.join()

    def plot(self):
        #plt.show()
        pass

    '''def update(self, frame):
        self.line.set_data(self.x_data, self.y_data)
        self.figure.gca().relim()
        self.figure.gca().autoscale_view()
        return self.line,
'''
    def salvar(self):
        datafile = open("C:/Users/lucad/PycharmProjects/NI_Python/datafiles/" + time.ctime()[:10] + ".txt", "a", encoding="UTF-8")

        media = round(np.mean(self.y_data),4)
        for i in range(0, len(self.y_data)):
            datafile.write(str(self.x_data[i]) + "," + str(self.y_data[i]) + "\n")
        datafile.close()
        self.y_data = []
        self.x_data = []

    def thread_f(self):
        tarefa = nidaqmx.Task()
        tarefa.ai_channels.add_ai_voltage_chan(self.canal)  # ("Dev1/ai0")

        n_amostras = self.tempo_ct * self.taxa_aq
        tarefa.timing.cfg_samp_clk_timing(rate = self.taxa_aq,
                                          active_edge = nidaqmx.constants.Edge.RISING, #RISING
                                          sample_mode = nidaqmx.constants.AcquisitionType.CONTINUOUS, #CONTINUOS
                                          samps_per_chan = int(n_amostras))
        tarefa.start()
        '''caso não houvesse essa função no codigo a 
            operação iria iniciar e para diversas vezes
            no laço causando uma perda de performance'''
        aux = 0
        while True:
            # retorna as amostras requisitadas em forma escalar, lista, ou uma lista de listas.
            try:
                data = tarefa.read(number_of_samples_per_channel= 1, timeout = 10)
            except Exception as e:
                print(e)

            self.y_data.append(data)
            self.x_data.append(time.perf_counter_ns())

            if len(self.y_data) == self.taxa_de_armazenamento:
                th_salvar = Thread(target = self.salvar)
                th_salvar.start()

        tarefa.close()
