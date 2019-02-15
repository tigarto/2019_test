import os
import pandas as pd
def iperfFormatFile(filename, filename_csv):
    """ 
    Genera un archivo .csv a partir de un archivo de entrada (.out)
  
    Toma un archivo de entrada cuyo contenido es la captura de trafico iperf y lo procesa para generar un archivo con informacion equivalente en formato .csv. 
  
    Parameters: 
    filename (str): Nombre del archivo de entrada.
    filename_csv (str): Nombre del archivo de salida 
  
    Returns: 
    list: Resumen con los datos del archivo de entrada analizado   
    """
    
    fileout_csv = open(filename_csv,'w')
    lines = open(filename).readlines()
    # Encabezado --> Interval [sec];Transfer [GBytes];Bandwidth [Mbits/sec]
    i = 6 # Linea inicial a partir del cual se hace el procesamiento del archivo
    fileout_csv.write('interval;transfer;BW\n')  # Escribiendo el titulo (primera linea)
    for l in lines[6:len(lines)]:
        s = l.split()
        s[:2] = []
        # Validando el numero de elementos de la linea
        if len(s) == 7:
            lw = s[0] + s[1] + ";" + s[3] + ";" + s[5] + "\n"
        else:
            lw = s[0] + ";" + s[2] + ";" + s[4] + "\n"

        # Verificacion del numero actual de la linea
        if i < len(lines) - 1:
            # Lineas del archivo excepto la ultima
            fileout_csv.write(lw)
        else:
            # Ultima lines
            if len(s) == 7:
                [interval,transfer,BW] = [s[0] + s[1] , s[3] , s[5]]
            else:
                [interval, transfer, BW] = [s[0] , s[2] , s[4]]
        i += 1
    fileout_csv.close()
    # Retorno del resumen
    return [interval, transfer, BW]
    

def generateDir(dirName):
    """ 
    Genera un directorio
  
    Genera un directorio cuyo nombre es dado en el parametro

    Parameters: 
    dirName (str): Nombre del directorio. Retorna una indicacion si este se genero o si no existe.
     
  
    Returns: 
    None
    """

    if not os.path.exists(dirName):
        if '/' in dirName:
            os.makedirs(dirName)
        else:
            os.mkdir(dirName)
        print("Directorio ", dirName, " creado ")
    else:
        print("Directorio ", dirName, " ya exite")

if __name__ == "__main__":
    # Configuracion para el analisis  de los resultados
    resumen = pd.DataFrame(columns=['tasa','interval', 'transfer', 'BW'])
    srcDir = './iperf_files/'
    dstDir = './csv_files/'     
    # generateDir(dstDir)
    files = os.listdir(srcDir)
    # Generando los archivos csv
    for f in files:
        fNamecsv = f.split('.')[0] + '.csv'
        tasa = fNamecsv.split('_')[1].replace('.csv','')
        [I,T,BW] = iperfFormatFile(srcDir + f, dstDir + fNamecsv)
        resumen = resumen.append({'tasa':tasa, 'interval': I, 'transfer': T, 'BW': BW}, ignore_index=True)
    print(resumen)
    resumen.to_csv(dstDir + 'resumen.csv', sep=';', header=['tasa','interval', 'transfer', 'BW'])





