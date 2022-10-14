cuadrado = 2
contador = 1
while cuadrado < 1000:
    contador = contador + 1
    strCont = str(contador)
    cuadrado = cuadrado * 2
    cadena = str(cuadrado)
    if cuadrado < 1000:
        print("potencia #" + strCont + " = " + cadena)
    else:
        print("El bucle termina aquí y la")
        print("siguiente salida sería " + cadena)
