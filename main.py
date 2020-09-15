from aquisicao import LiveGraph

titulo = "Tensão[V]xAmostras[n]" #str(input("Digite o titulo do seu gráfico: "))
intervalo = 10 #int(input("Digite o intervalo entre as plotagens: "))
canal = "Dev3/ai0" #str(input("Digite o canal de aquisição: "))
taxa_de_aquisicao = 9920.0#float(input("Digite a taxa de aquisição: "))
tempo_ct = 3.0#float(input("Tempo de C/T [s]: "))
taxa_arm = 5000.0#float(input("Taxa de armazenamento: "))

graph = LiveGraph(titulo, intervalo, canal, taxa_de_aquisicao, tempo_ct, taxa_arm)
graph.plot()