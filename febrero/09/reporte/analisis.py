import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

def pingFormatFile(filename):
    filename_parts = filename.split(".")
    if filename_parts[0] == '':
        del(filename_parts[0])    
    filename_csv = filename_parts[0] + "." + "csv"
    fileout_csv = open("." + filename_csv, 'w')
    lines = open(filename).readlines()
    fileout_csv.writelines("icmp_seq;ttl;time [ms]\n")
    for l in lines[1:len(lines) - 4]:
        s = l.split()
        fileout_csv.write(s[0] + ";" + s[4].split("=")[1] + ";" + s[6].split("=")[1] + "\n")
    fileout_csv.close()
    line = lines[-2]
    s = line.split(', ')
    p_tx = int(int(s[0].split()[0]))
    p_rx = int(s[1].split()[0])
    p_loss = float(s[2].split()[0].replace('%', ''))
    time = float(s[3].split()[1].replace('ms', ''))
    rtt = lines[-1].split()[-2]
    return [p_tx, p_rx, p_loss, time, rtt]  # Devuelve informacion resumen asociada al ping

def iperfFormatFile(filename):
    filename_parts = filename.split(".")
    if filename_parts[0] == '':
        del(filename_parts[0])   
    filename_csv = filename_parts[0] + "." + "csv"
    fileout_csv = open("." + filename_csv,'w')
    lines = open(filename).readlines()
    fileout_csv.writelines("Interval [sec];Transfer [GBytes];Bandwidth [Mbits/sec]\n")
    i = 6
    for l in lines[6:len(lines)]:
        s = l.split()
        s[:2] = []
        if len(s) == 7:
            lw = s[0] + s[1] + ";" + s[3] + ";" + s[5] + "\n"
        else:
            lw = s[0] + ";" + s[2] + ";" + s[4] + "\n"
        # Lineas ...
        if i < len(lines) - 1:
            fileout_csv.write(lw)
        else:
            if len(s) == 7:
                [interval,transfer,BW] = [s[0] + s[1] , s[3] , s[5]]
            else:
                [interval, transfer, BW] = [s[0] , s[2] , s[4]]
        i += 1
    fileout_csv.close()
    return [interval, transfer, BW]


"""
Clase que permite obtener el reporte
"""

class Reporte(object):
    def __init__(self, metricas_ping = pd.DataFrame(columns=['p_tx','p_rx', 'p_loss', 'time', 'rtt_min','rtt_avg','rtt_max','rtt_mdev']),
                 metricas_iperf = pd.DataFrame(columns=['interval', 'transfer', 'BW'])):
        self.metricas_iperf = metricas_iperf # Dataframe - cada fila es una replica
        self.metricas_iperf.columns.name = 'metricas'
        self.metricas_iperf.index.name = 'replica'
        self.metricas_ping = metricas_ping  # Dataframe - cada fila es una replica
        self.metricas_iperf.columns.name = 'metricas'
        self.metricas_iperf.index.name = 'replica'

    def agregarSalidaIperf(self,bw_list):
        bw_list[1] = int(bw_list[1])
        bw_list[2] = float(bw_list[2])
        self.metricas_iperf = self.metricas_iperf.append(pd.Series(bw_list, index=['interval', 'transfer', 'BW']),ignore_index=True)

    def agregarSalidaPing(self,ping_list):
        ping_list[-1] = ping_list[-1].split('/')
        ping_list = ping_list[:-1] + ping_list[-1]
        for i in range(len(ping_list)):
            if i < 2:
                ping_list[i] = int(ping_list[i])
            else:
                ping_list[i] = float(ping_list[i])
        self.metricas_ping = self.metricas_ping.append(pd.Series(ping_list, index=['p_tx','p_rx', 'p_loss', 'time', 'rtt_min','rtt_avg','rtt_max','rtt_mdev']), ignore_index=True)

    def mostrarEstadisticasIperf(self):
        print(self.metricas_iperf.describe())

    def mostrarEstadisticasPing(self):
        print(self.metricas_ping.describe())

    def imprimirResumenIperf(self):
        print self.metricas_iperf

    def imprimirResumenPing(self):
        print self.metricas_ping
    
    def obtenerAnchoBandaPromedio(self):
        return self.metricas_iperf['BW'].mean()
    
    def obtenerRTTPromedio(self):
        return self.metricas_ping['rtt_avg'].mean()
    



if __name__ == "__main__":
    dir_root_results = "salidas"
    files_out = []
    summaryPing = []
    summaryIperf = []
    files = [ 
       os.path.join(parent, name)
       for (parent, subdirs, files) in os.walk(".")
       for name in files + subdirs
       ]

    for f in files:
        if ".out" in f:
            files_out.append(f)

    
    for f in files_out:
        # print f
        if "iperf" in f:
            summaryIperf.append({'file':f,'iperf_s':iperfFormatFile(f)})

        else:
            summaryPing.append({'file':f,'ping_s':pingFormatFile(f)})
    
    # Diccionario con los resumentes del experimento
    data_sum_iperf = {'10kpps':[],'8kpps':[],'6kpps':[],'4kpps':[],'2kpps':[],'normal':[]}
    data_sum_ping = {'10kpps':[],'8kpps':[],'6kpps':[],'4kpps':[],'2kpps':[],'normal':[]}
    for e in summaryIperf:
        name = e['file'].strip('.out').split('/')[-1]
        for k in data_sum_iperf:
            if k in name:
                data_sum_iperf[k].append(e['iperf_s'])
      
    for e in summaryPing:
        name = e['file'].strip('.out').split('/')[-1]
        for k in data_sum_ping:
            if k in name:
                data_sum_ping[k].append(e['ping_s'])

    reportes = {'10kpps':Reporte(),
                '8kpps':Reporte(),
                '6kpps':Reporte(),
                '4kpps':Reporte(),
                '2kpps':Reporte(),
                'normal':Reporte()}
    
    # Agregando los dataframes para iperf
    for k in reportes:
        for v in data_sum_iperf[k]:            
            reportes[k].agregarSalidaIperf(v)

    # Agregando los dataframes para ping    
   
    for k in reportes:
        for v in data_sum_ping[k]:
            reportes[k].agregarSalidaPing(v)
    
    """
    for k in reportes:
        print k
        print "Iperf",k
        reportes[k].imprimirResumenIperf()
        print "Ping",k
        reportes[k].imprimirResumenPing()
        print '\n'        

    """
    # Obteniendo estadisticas para las graficas
    BW_avg = []
    rtt_avg = []

    for k in reportes:
        BW_avg.append(reportes[k].obtenerAnchoBandaPromedio())
        rtt_avg.append(reportes[k].obtenerRTTPromedio())

    #print BW_avg
    #print rtt_avg
    
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html   
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.bar.html
    # https://www.tutorialspoint.com/python_pandas/python_pandas_series.htm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.plot.bar.html
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.plot.html
    
    datosGraficas = pd.DataFrame({'BW': BW_avg,'RTT': rtt_avg}, index=reportes.keys())
    axes = datosGraficas.plot.bar(rot=0, subplots=True)
    axes[1].legend(loc=2)  # doctest: +SKIP
    plt.show()

    """
    BW_avg_s = pd.Series(BW_avg, index=reportes.keys())
    rtt_avg_s = pd.Series(rtt_avg, index=reportes.keys())
    print BW_avg_s
    print rtt_avg_s
    
    plt.figure()
    BW_avg_s.plot.bar(x='rata', y='mbps', rot=0)
    plt.show()
    plt.figure()
    rtt_avg_s.plot.bar(x='rata', y='mbps', rot=0)
    plt.show()
    """









    
    








        

