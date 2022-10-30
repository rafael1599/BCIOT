def exect():
    for contador in range(1, 1001):
        if contador % 2 != 0:
            continue
        print(contador)


if __name__ == "__main__":
    exect()

# contador = 1
# for contador in range(1, 501):
#     par = contador * 2
#     print("Posicion #", contador, ", NUM =", par)


# cuadrado = 2
# contador = 1
# while cuadrado < 1000000:
#     contador = contador + 1
#     strCont = str(contador)
#     cuadrado = cuadrado * 2
#     cadena = str(cuadrado)
#     if cuadrado < 1000000:
#         print("potencia #" + strCont + " = " + cadena)
#     else:
#         print("El bucle termina aquí y la")
#         print("siguiente salida sería " + cadena)
