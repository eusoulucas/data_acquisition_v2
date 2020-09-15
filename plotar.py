import matplotlib.pyplot as plt

file = open("datafiles/Mon Sep 14.txt", "r", encoding="UTF-8")
file2 = open("datafiles/test.txt", "w", encoding="UTF-8")
y = []
x = []
aux = 0

for dados in file:
    dados = dados.split(",")
    dados[1] = dados[1].replace("[", "")
    dados[1] = dados[1].replace("]", "")
    dados[1] = dados[1].replace(" ", "")
    dados[1] = dados[1].replace("\n", "")
    file2.write(str(float(dados[0])))
    file2.write("\n")
    y.append(float(dados[1]))
    x.append(float(dados[0]))

plt.plot(x, y)
plt.show()

file.close()
file2.close()