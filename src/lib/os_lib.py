import os

def compile_form(pathToUI):
    pathToPY = os.path.splitext(pathToUI)[0] + ".py"
    qtCompilePrefStr = 'pyuic5 ' + pathToUI + ' -o ' + pathToPY
    print("Compiling QT GUI file", qtCompilePrefStr)
    os.system(qtCompilePrefStr)
