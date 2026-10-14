import random

random.seed(42)

N_BITS = 5
P_CRUCE = 0.8
P_MUT = 0.05
GENERACIONES = 20


def decodificar(c):
    return int(c, 2)


def aptitud(c):
    return decodificar(c) ** 2


def ruleta(poblacion):
    total = sum(aptitud(c) for c in poblacion)
    r = random.uniform(0, total)
    acumulado = 0
    for c in poblacion:
        acumulado += aptitud(c)
        if acumulado >= r:
            return c
    return poblacion[-1]


def cruce(p1, p2):
    if random.random() < P_CRUCE:
        punto = random.randint(1, N_BITS - 1)
        return p1[:punto] + p2[punto:], p2[:punto] + p1[punto:]
    return p1, p2


def mutar(c):
    bits = list(c)
    for i in range(len(bits)):
        if random.random() < P_MUT:
            bits[i] = "1" if bits[i] == "0" else "0"
    return "".join(bits)


poblacion = ["00101", "01100", "10010", "11001"]
historial = []

for gen in range(1, GENERACIONES + 1):
    elite = max(poblacion, key=aptitud)          # elitismo
    nueva = [elite]
    while len(nueva) < len(poblacion):
        h1, h2 = cruce(ruleta(poblacion), ruleta(poblacion))
        nueva.append(mutar(h1))
        if len(nueva) < len(poblacion):
            nueva.append(mutar(h2))
    poblacion = nueva
    mejor = max(poblacion, key=aptitud)
    historial.append(aptitud(mejor))
    print(f"Gen {gen:2d}: {poblacion}  mejor={mejor} (x={decodificar(mejor)}, f={aptitud(mejor)})")

mejor = max(poblacion, key=aptitud)
print("\nMejor cromosoma final:", mejor)
print("x =", decodificar(mejor), " aptitud =", aptitud(mejor))
print("Historial de mejor aptitud:", historial)
print("Óptimo global posible: 11111 -> x=31, f=961")
