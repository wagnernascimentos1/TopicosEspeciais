ValorPag = list()
valorPrest = float(input())
while (valorPrest != 0):
    diasAtras = int(input())
    if (diasAtras==0):
        print("O valor total da Prestação: R$ %.2f" %(valorPrest))
        ValorPag.append(valorPrest)
    else:
        juros = valorPrest+(10*0.3)+((10*0.01)*diasAtras)
        print("O valor total da Prestação: R$ %.2f" %(juros))
        td.append(juros)
    valorPrest = float(input())


calculoFinal = sum(td)

print("Total de Prestações pagas no dia de hoje: R$ %.2f" %(calculoFinal))
