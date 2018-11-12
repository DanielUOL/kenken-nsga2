import random
import numpy as np
import matplotlib.pyplot as plt
#random.seed(5)
class Individual:
	# construcctor del tablero
	def __init__(self,tam,tablero):
		self.tablero = tablero
		self.tam = tam

	# genera una lista con numeros ordenados de posiciones
	# donde el indice es la columna en el tablero
	# y el valor es la fila del tablero
	def gentablero(self):
		indices = []
		for i in range(self.tam):
			indices.append(i)
	# se inseran los valores de la lista, removiendolas de manera aleatoria
		while (indices):
			self.tablero.append(indices.pop(random.randrange(len(indices))))


	# se hace un intercambio de posiciones en el tablero
	# se genera un indice 1
	# se genera una indice 2, validando que sea diferente del indice 1
	# se realizaa el intercambio
	def mutation(self):
		index1 = random.randrange(self.tam)
		index2 = random.randrange(self.tam)
		while(index2 == index1):
			index2 = random.randrange(self.tam)
		
		temp = self.tablero[index1]
		self.tablero[index1] = self.tablero[index2]
		self.tablero[index2] = temp 

	# se realizan n cantidad de intercambios 
	# cumpliendo las condiciones de mutation
	def mutation2(self):
		for i in range(5):
			index1 = random.randrange(self.tam)
			index2 = random.randrange(self.tam)
			while(index2 == index1):
				index2 = random.randrange(self.tam)
		
			temp = self.tablero[index1]
			self.tablero[index1] = self.tablero[index2]
			self.tablero[index2] = temp 


	# se realizan intercambios hasta que el nuevo fitness
	# sea mejor que el fitness de la configuracion inicial
	def mutation3(self):
		tablero = self.tablero
		n = self.ataques()
		while(self.ataques() >= n and self.ataques() > 0):
			
			self.tablero = tablero
			index1 = random.randrange(self.tam)
			index2 = random.randrange(self.tam)
		
			temp = self.tablero[index1]
			self.tablero[index1] = self.tablero[index2]
			self.tablero[index2] = temp

	# se realizan intercambios de posiciones de manera ordenada
	# termina cuando el nuevo fitness sea mejor que el original
	def mutation4(self):
		tablero = self.tablero
		n = self.ataques()
		if n == 0:
			return
		for i in range(self.tam - 1):
			for j in range(i + 1, self.tam - 1):
				self.tablero = tablero
				temp = self.tablero[i]
				self.tablero[i] = self.tablero[j]
				self.tablero[j] = temp

				if self.ataques() < n:
					break

	# cruce de dos individuos
	# se selecciona un punto aleatorio de cruce
	# los hijos copian los valores desde 0 hasta el punto de cruce
	# el primer hijo va copiando los valores del segundo padre excluyendo los valores que ya tiene
	# el segundo hijo va copiando los valores del primer padre excluyendo los valores que ya tiene
	def crossover(tablero1, tablero2):
		hijo1 = []
		hijo2 = []
		punto = random.randint(1,tablero1.tam - 1)
		hijo1 = tablero1.tablero[:punto]
		hijo2 = tablero2.tablero[:punto]

		for r in range(punto,tablero1.tam):
			if tablero2.tablero[r] not in hijo1:
				hijo1.append(tablero2.tablero[r])
			if tablero1.tablero[r] not in hijo2:
				hijo2.append(tablero1.tablero[r])

		for r in range(tablero1.tam):
			if tablero2.tablero[r] not in hijo1:
				hijo1.append(tablero2.tablero[r])
			if tablero1.tablero[r] not in hijo2:
				hijo2.append(tablero1.tablero[r])
		t1 = Individual(tablero1.tam,hijo1)
		t2 = Individual(tablero1.tam,hijo2)
		return t1,t2

	

	#Dos reinas estan en la misma diagonal si:
	#Mismo valor de fila - columna (diagonal descendente)
	#Mismo valor de fila + columna (diagonal ascendente)
	#reina = fila
	#self.tablero.index() = columna

	#Nota: si 3 reinas estan en la misma diagonal, contará ataque:
	# - La primera reina con la segunda
	# - La primera reina con la tercera
	# - La segunda reina con la tercera
	# y asi en casos con mas reinas

	# cuando mas alto es el numero de ataque, menos apto es el individuo
	# el individuo con ataque 0 es un individuo solucion
	def ataques(self):
		ataques = 0
		for j in self.tablero:  # j actual reina
			for i in range(j + 1,self.tam): # i siguientes reinas			
				if j - self.tablero.index(j) == i - self.tablero.index(i):
	
					ataques += 1
				if j + self.tablero.index(j) == i + self.tablero.index(i):

					ataques += 1

		return ataques

	# se verifican las diagonales siguiendo las consideraciones de la funcion ataques
	# las reinas invoucradas en ataques son agregadas a un diccionario
	def noataques(self):
		no_ataques = 0
		reinasatacadas = {}
		for j in self.tablero:  # j actual reina
			for i in range(j + 1,self.tam): # i siguientes reinas			
				if j - self.tablero.index(j) == i - self.tablero.index(i):
					reinasatacadas[self.tablero.index(j)] = j
					reinasatacadas[self.tablero.index(i)] = i

				if j + self.tablero.index(j) == i + self.tablero.index(i):
					reinasatacadas[self.tablero.index(j)] = j
					reinasatacadas[self.tablero.index(i)] = i

	# se recorre el tablero preguntando si esa reina no esta en el diccionario de ataques
	# se cuentan el numero de no ataques
		for reina in self.tablero:
			if self.tablero.index(reina) not in reinasatacadas:
				no_ataques += 1
		#print(reinasatacadas)
		return no_ataques



N = 100  # tamaño de la poblacion
R = 100  # numero de reinas
pM = .9  # probabilidad de mutacion
i = 0  # contador de generaciones
G = 120  # Numero de generaciones
t = int(N//2.5)
ganador = []
stats = {'max':[],'min':[],'avg':[]}
#Inicializar Poblacion
population = [Individual(R,[]) for i in range (N)]
for tablero in population:
	tablero.gentablero()

print("Generacion | Maximo | Minimo | Promedio")
#Iterar por Generaciones
while (i < G):
	fitness_values = [x.ataques() for x in population]
	stats['max'].append(max(fitness_values))
	stats['min'].append(min(fitness_values))
	stats['avg'].append(sum(fitness_values)/N)
	print("  |  ",i,"   |   ",max(fitness_values),"   |   ",min(fitness_values)," | ",round(sum(fitness_values)/N,2))
	
	offspring = []
	for _ in range(N//4):
		torneo = []
		#  Seleccion por torneo
		#1. Se escogen 6 tableros aleatorios
		#2. Se ordenan por fitness
		#3. Se cruzan los primeros 2(mas aptos)
		for t in range(6):
			torneo.append(population[random.randint(0,N - 1)])
		torneo.sort(key=lambda x: x.ataques())

		#Cruze
		H1,H2 = Individual.crossover(torneo[0],torneo[1])

		#Mutacion
		if random.random() <= pM:
			H1.mutation()
		if random.random() <= pM:
			H2.mutation()

		offspring.append(H1)
		offspring.append(H2)

	# seleccion de sobrevivientes
	#1. se ordena la poblacion por menos aptos
	#2. la nueva poblacion sustituye a los menos aptos
	"""
	population.sort(key=lambda x: -x.ataques())

	for j in range(4):
		for k in range(N):
			if offspring[j].ataques() < population[k].ataques():
				population[k] = offspring[j]
			pass

	i += 1
	"""
	plebada = population + offspring
	plebada.sort(key=lambda x: x.ataques())
	population = plebada[:N]
	i += 1


print(sum(stats['avg'])/G)

plt.close('all')
plt.plot(stats['max'],'g',label='max')
plt.plot(stats['min'],'r',label='min')
plt.plot(stats['avg'],'b',label='avg')
plt.legend()
plt.show()