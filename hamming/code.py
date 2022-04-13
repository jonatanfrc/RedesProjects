def calculateRedundantBits(m):
	# Utilizar a formula 2 ^ r >= m + r + 1 para calcular o número de bits redundantes.
	# Iterar entre 0 .. m e retornar o valor que satisfaça a equação.
	for i in range(m):
		if(2**i >= m + i + 1):
			return i

def positionRedundantBits(data, redundant):
    # Bits de redundancia são alocados nas posições que correspondam à potência de 2.
	j = 0
	k = 1
	m = len(data)
	result = ''
	# Se a posição é uma potencia de 2, então se insere 0.
	for i in range(1, m + redundant +1):
		if(i == 2**j):
			result = result + '0'
			j += 1
		else:
			result = result + data[-1 * k]
			k += 1
	# As posições do resultado são invertidas.
	return result[::-1]

def calculateParityBits(arr, redundant):
	n = len(arr)
	# Para encontrar o bit de paridade, terá que iterar de 0 a r-1.
	for i in range(redundant):
		value = 0
		for j in range(1, n + 1):
			if(j & (2**i) == (2**i)):
				value = value ^ int(arr[-1 * j])
				# -1 * j é dado já que o array é invertido
		# Concatenação
		# (0 .. n - 2^r) + bit de paridade + (n - 2^r + 1 .. n)
		arr = arr[:n-(2**i)] + str(value) + arr[n-(2**i)+1:]
	return arr

def findError(arr, nr):
	n = len(arr)
	res = 0
	# Calcula novamente os bits de paridade
	for i in range(nr):
		value = 0
		for j in range(1, n + 1):
			if(j & (2**i) == (2**i)):
				value = value ^ int(arr[-1 * j])
        # Cria um número binário agrupando as paridades
		res = res + value*(10**i)
	# Converte binário para decimal
	return int(str(res), 2)

# Dados a serem transmitidos
data = '1011001'

# Calcula o número de bits redundantes necessários
size = len(data)
redundant = calculateRedundantBits(size)

# Determina a posição dos bits redundantes
arr = positionRedundantBits(data, redundant)

# Determina os bits de paridade
arr = calculateParityBits(arr, redundant)

# Dados a serem tranferidos
print("Dados transferidos são: " + arr)

# Estimula o erro em transmissão mudando um valor de bit
# 10101001110 -> 11101001110, erro na décima posição.
arr = '11101001110'
print("Erro nos dados. Dado transmitido: " + arr)

correction = findError(arr, redundant)
print("O erro se encontra na posição: " + str(correction))
