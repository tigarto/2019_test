import os
import shutil

class Extraer(object):
    def __init__(self, dirSource, dirDest): 
        self.dirSource = dirSource
        self.dirDest = dirDest

    def listFilesCsv(self):
        csv_files = []
        for dirpath, dirs, files in os.walk(self.dirSource):
            if files != []:
                for f in files:
                    if ".csv" in f:
                        csv_files.append(dirpath + "/"+ f)
        return csv_files 

    def getNameFile(self, completeName):
        return completeName.split('/')[-1]

    def copyFilesToDest(self):
        origen_cvs_files = self.listFilesCsv()
        for f in origen_cvs_files:
            print self.getNameFile(f)
            shutil.copyfile(f, self.dirDest + self.getNameFile(f))

    def createDestDir(self, dirName = None):
        if dirName != None:
            self.dirDest = dirName
        if not os.path.exists(self.dirDest):
            if '/' in self.dirDest:
                os.makedirs(self.dirDest)
            else:
                os.mkdir(self.dirDest)
            print("Directory ", self.dirDest, " Created ")
        else:
            print("Directory ", self.dirDest, " already exists")



        #shutil.copyfile(src_file, dest_file, *, follow_symlinks=True)

    

if __name__ == "__main__":
    extra = Extraer('./experimento2/salidas_50_1/','./csv_50_1/')
    extra.listFilesCsv()
    extra.createDestDir()
    extra.copyFilesToDest()
    #print(extra.listFilesCsv())

    

    

