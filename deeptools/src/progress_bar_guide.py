import threading #esto es lo que te permite no bloquear Nuke al usar un codigo lento
import time #esto es solo para el test, no hace falta

def test():
    task = nuke.ProgressTask('Randomizing...') #esto es el mensajito a la izquierda de la barra de progreso
    curvesKnob = nuke.selectedNode()['curves'].rootLayer
    progIncr = 100.0 / len(curvesKnob) #esto se usa luego para hacer avanzar la barra, en mi caso, 100/numero de elementos en Root de la roto
    counter = 0
    for i in curvesKnob:
        if task.isCancelled(): #esto, como podras imaginar, es lo que pasa si le das a cancel
            nuke.executeInMainThread(nuke.message, args=('Canceled',))
            break
        task.setProgress(int(counter*progIncr)) # esto es lo que avanza de la barra. Usas el counter y lu multiplicas por el numero que hemos sacado antes
        task.setMessage(i.name) #Esto es lo que sale justo sobre la barra. En mi caso, al estar en un loop, coge el nombre de cada elemento en Root, pero puedes poner un mensaje fijo. A mi personalmente me gusta que cambie :-)
        time.sleep(4) # Esto no es necesario, es solo para el test. Para el codigo 4 segundos.
        counter = counter + 1

threading.Thread(target=test).start() # Esto lanza la funcion en un thread diferente al principal (en el que corre Nuke)