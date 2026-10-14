<img width="1465" height="627" alt="image" src="https://github.com/user-attachments/assets/2bd8554a-7b78-4244-a427-fc6db2a61911" />


# Punto 1 — Algoritmos evolutivos y algoritmos genéticos
## ¿De qué trata?

Se quiere **maximizar** la función

```
f(x) = x²,   x ∈ {0, 1, ..., 31}
```

El máximo es evidente (x = 31, f = 961), pero el objetivo es que un **algoritmo genético**
lo encuentre por sí solo, imitando la evolución natural:

- Cada número se representa como un **cromosoma binario de 5 bits** (por ejemplo, 25 = `11001`).
- Se parte de una población de 4 cromosomas: `P = {00101, 01100, 10010, 11001}`.
- En cada generación, los individuos con mayor aptitud tienen más probabilidad de
  reproducirse (**selección**), sus bits se mezclan (**cruce**) y a veces cambian al azar
  (**mutación**).
  
---

## A. Componente matemático y conceptual

### 1. Decodificación y aptitud

Cada bit vale una potencia de 2: `16 8 4 2 1`. Por ejemplo,
`01100` = 0·16 + 1·8 + 1·4 + 0·2 + 0·1 = 12.

| Cromosoma | x (decimal) | f(x) = x² |
|-----------|-------------|-----------|
| 00101     | 5           | 25        |
| 01100     | 12          | 144       |
| 10010     | 18          | 324       |
| 11001     | 25          | 625       |
| **Suma**  |             | **1118**  |

### 2. Probabilidad de selección por ruleta

```
pᵢ = f(xᵢ) / Σ f(xⱼ),   con Σ f(xⱼ) = 1118
```

| Cromosoma | Cálculo    | pᵢ     | Porcentaje |
|-----------|------------|--------|------------|
| 00101     | 25 / 1118  | 0,0224 | 2,24 %     |
| 01100     | 144 / 1118 | 0,1288 | 12,88 %    |
| 10010     | 324 / 1118 | 0,2898 | 28,98 %    |
| 11001     | 625 / 1118 | 0,5590 | 55,90 %    |

Es como una ruleta donde cada individuo ocupa una porción proporcional a su aptitud:
`11001` ocupa más de la mitad, por eso es el que más se reproduce.

### 3. Cruce de un punto después del segundo bit

```
Padre 1: 01 | 100
Padre 2: 11 | 001
---------------------
Hijo 1:  01 | 001  ->  01001  (x = 9,  f = 81)
Hijo 2:  11 | 100  ->  11100  (x = 28, f = 784)
```

Cada hijo toma los dos primeros bits de un padre y los tres últimos del otro.

### 4. Mutación del último bit del primer descendiente

```
01001  ->  01000
```

Nuevo valor: **x = 8**, aptitud **f(8) = 64** (antes era 81, es decir, empeoró).

### 5. Preguntas

**¿Qué relación existe entre un algoritmo evolutivo y un algoritmo genético?**
Un algoritmo genético es un **tipo particular** de algoritmo evolutivo. Los algoritmos
evolutivos son la familia general, inspirada en la evolución natural: trabajan con una
población de soluciones que se seleccionan y modifican generación tras generación. El
algoritmo genético se caracteriza por representar las soluciones como cromosomas
(normalmente cadenas binarias) y por usar cruce y mutación como operadores principales.

**¿Qué función cumplen selección, cruce y mutación?**
- **Selección:** elige a los padres dando más oportunidad a los de mejor aptitud.
  Dirige la búsqueda hacia buenas soluciones (**explotación**).
- **Cruce:** combina partes de dos padres para formar hijos, buscando reunir las
  mejores características de ambos.
- **Mutación:** cambia bits al azar con baja probabilidad. Introduce variedad nueva y
  evita que la población se vuelva idéntica (**exploración**).

**¿Por qué una mutación puede ser útil aunque empeore la aptitud inmediata?**
Porque mantiene la diversidad y puede crear combinaciones que ningún individuo tenía.
Si todos los cromosomas tienen un bit en 0, el cruce nunca podrá ponerlo en 1: solo la
mutación puede hacerlo. Un hijo peor hoy puede aportar el material genético necesario
para llegar al óptimo después, y evita que el algoritmo se estanque en un óptimo local.
Esto se ve en la ejecución de este punto (ver la explicación más abajo).

---

## B. Implementación 

### Parámetros

| Parámetro           | Valor                             |
|---------------------|-----------------------------------|
| Población inicial   | 00101, 01100, 10010, 11001        |
| Selección           | Ruleta                            |
| Cruce               | Un punto, probabilidad 0,8        |
| Mutación            | Independiente por bit, prob. 0,05 |
| Elitismo            | Se conserva el mejor individuo    |
| Tamaño de población | 4                     |
| Generaciones        | 20                                |
| Semilla             | 42                                |

### Funcion del codigo

| Función / bloque      | Qué hace |
|-----------------------|----------|
| `decodificar(c)`      | Convierte el cromosoma binario a decimal con `int(c, 2)`. |
| `aptitud(c)`          | Calcula f(x) = x². |
| `ruleta(poblacion)`   | Lanza un número aleatorio entre 0 y la suma de aptitudes y recorre la población acumulando aptitudes hasta superarlo. |
| `cruce(p1, p2)`       | Con probabilidad 0,8 elige un punto de corte al azar (1 a 4) e intercambia las colas; si no, devuelve los padres sin cambios. |
| `mutar(c)`            | Recorre cada bit y lo invierte con probabilidad 0,05. |
| Ciclo principal       | Guarda al mejor, llena la población hasta 4 con hijos, y registra la mejor aptitud de cada generación. |

`random.seed(42)` hace que los números aleatorios sean siempre los mismos, por lo que
cualquier persona que ejecute el código obtiene exactamente el mismo resultado.

### Ejecutar

Se ejecuta localmente 

```bash
python punto1_genetico.py
```

En Windows también funciona `py punto1_genetico.py`.

---

### Salida

Cada línea `Gen N` muestra:
- la **población completa** de esa generación (los 4 cromosomas), y
- el **mejor individuo**, con su valor de `x` y su aptitud `f`.

Al final se imprimen el mejor cromosoma, su valor, su aptitud y el historial de la
mejor aptitud de cada generación.

### Análisis de la ejecución, etapa por etapa

**Generación 1 — salto rápido.**
Desde la población inicial (cuyo mejor era `11001`, f = 625) aparece `11101`
(x = 29, f = 841). La ruleta favoreció a los individuos grandes (`11001` y `10010`) y el
cruce combinó sus bits altos.

**Generaciones 2 a 15 — estancamiento.**
La mejor aptitud se queda en 841 durante 15 generaciones. La población se llena de
copias de `11101`: en las generaciones 3, 4, 7, 8, 9, 12, 13 y 14 los cuatro individuos
son idénticos. El problema es el **cuarto bit**: ningún individuo tiene un 1 en esa
posición, y el cruce solo puede recombinar bits que ya existen, así que no puede crear
`11111`. Aparecen algunas variantes por mutación (`01101`, `01001`, `11001`, `10101`),
pero son peores y desaparecen.

**Generación 16 — la mutación clave.**
Aparece `11111` (x = 31, f = 961). Solo pudo surgir porque una **mutación** cambió el
cuarto bit de 0 a 1 (`11101` → `11111`). Es el ejemplo directo de por qué la mutación
es necesaria: sin ella, el algoritmo se habría quedado en 841 para siempre.

**Generaciones 17 a 20 — convergencia.**
Gracias al elitismo, `11111` nunca se pierde. Siguen apareciendo individuos peores por
mutación (`00101`, `01111`, `01101`), pero la selección favorece al óptimo y en la
generación 20 los cuatro individuos son `11111`.

### Resultado final

| Resultado              | Valor      |
|------------------------|------------|
| Mejor cromosoma final  | `11111`    |
| Valor de x             | 31         |
| Aptitud                | 961        |

**Historial de la mejor aptitud por generación:**

| Generación | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|------------|---|---|---|---|---|---|---|---|---|----|
| Mejor f    |841|841|841|841|841|841|841|841|841|841 |

| Generación | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|------------|----|----|----|----|----|----|----|----|----|----|
| Mejor f    |841 |841 |841 |841 |841 |**961**|961|961|961|961|

La aptitud **nunca baja** entre generaciones; eso lo garantiza el elitismo.

---

**¿El algoritmo encontró el óptimo global?**
Sí. El máximo posible de la función en el dominio es f(31) = 31² = **961**, que
corresponde al cromosoma `11111` (todos los bits en 1). El algoritmo terminó con ese
individuo y esa aptitud, así que alcanzó el óptimo global.

**¿Por qué veinte generaciones no garantizan encontrarlo?**
- **El algoritmo es estocástico:** la selección, el cruce y la mutación dependen de
  números aleatorios. Con otra semilla el resultado puede ser distinto.
- **Dependió de una sola mutación:** la población estuvo atrapada 15 generaciones en
  `11101` porque nadie tenía un 1 en el cuarto bit. La probabilidad de mutar un bit es
  solo 0,05, así que esa mutación podía no ocurrir en las 20 generaciones.
- **La población es muy pequeña (4 individuos):** pierde diversidad rápidamente y
  converge pronto, posiblemente a una solución que no es la óptima.

En esta ejecución tuvo éxito, pero el algoritmo no ofrece garantía de encontrar el
óptimo en un número fijo de generaciones.
