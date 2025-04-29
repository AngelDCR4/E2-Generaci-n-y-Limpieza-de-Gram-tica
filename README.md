# E2-Generaci-n-y-Limpieza-de-Gram-tica

Ángel David Candelario Rolon

A01712387

# Introducción
El lenguaje seleccionado para el desarrollo de este proyecto es el **Ruso**. Sin embargo para tener una mejor comprensión del lenguaje no usaramos el *alfabeto círilico (А-Я)*. En su lugar haremos uso de una **transliteración fonética al alfabeto latino**, es decir estariamos trabajando con palabras rusas normales, pero **escritas con nuestro alfabeto latino (A-Z)**. Aquí algunos ejemplos:
| Español | Ruso (cirílico) | Transliteración fonética |
|---------|------------------|---------------------------|
| Hola    | Привет           | privet                    |
| Adios   | Пока             | poka                      |
| Gracias | Спасибо          | spasibo                   |
| Gato    | Кот              | kot                       |
| Perro   | Собака           | sobaka                    |

## Estructura del lenguaje

En el lenguaje Ruso no tiende a cambiar mucho el orden en que deben de ir las palabras para generar una oración, siendo similar al español: **Sujeto + Verbo + Objeto**, aunque en ciertas ocaciones si puede llegar a variar sin afectar el significado, nos apegaremos a esta estructura para mantener la coherencia y facilitar su entendimiento.

Se han definido las siguiente categorías de palabras para formar oraciones:
 - Pronombres (yo, tú, él…)
 - Sustantivos comunes (mamá, casa, perro…)
 - Verbos en primera persona (amo, estudio, veo…)
 - Conectores (y, pero, porque…)
 - Preposiciones (en, sobre, con)
 - Adverbios (siempre, nunca, lentamente)
 - Adjetivos (grande, bonita, feo)

## Implementación

Para implementar esta solución, utilizaremos un analizador LL(1), una técnica de análisis descendente frecuentemente empleada en la lingüística computacional. El término "LL" hace referencia a una lectura de izquierda a derecha de la entrada y a una derivación del extremo más a la izquierda en la construcción del árbol sintáctico. El número "(1)" indica que el analizador utiliza un solo token de anticipación para tomar decisiones sobre el análisis sintáctico, lo cual agiliza el proceso y evita retrocesos innecesarios durante el reconocimiento de las cadenas.

Esta metodología permite analizar de manera eficiente las oraciones generadas a partir de nuestra gramática simplificada, garantizando una validación rápida y precisa.

## Gramatica Inicial

En la primera fase de creación de la gramática, identifiqué las unidades **terminales** y **no terminales**, partiendo de una estructura básica de **Sujeto + Verbo + Sustantivo**. Posteriormente, se agregó complejidad incorporando **conectores**, **adverbios**, **adjetivos** y **preposiciones**.

### No Terminales

{S, Oracion, VP, Sustantivo, Conector, Sujeto, Verbo, Preposicion, Adverbio, Adjetivo}

### Terminales

{ya, ty, on, ona, my, oni, lyublyu, zhivu, khochu, uchus', vizhu, rabotayu, papa, mama, kot, sobaka, dom, shkola, drug, lyubov, rabota, i, ili, no, potomu_chto, khotya, togda, yesli, tozhe, v, na, s, bez, dlya, k, iz, bystro, medlenno, vsegda, nikogda, inogda, segodnya, vchera, khorosho, plokho, mnogo, malo, bolshoy, krasivaya, nekrasivyy, novyy, staryy, umnyy, sil'nyy, slabyy, khoroshiy, plokhoy, chornyy, belyy, krasnyy, malen'kiy, bystryy, medlennyy}

### Inicial

```python
NT   = (Sujeto, Verbo, Conector, Sustantivo)
Terminales  = (ya, ty,...)

S -> Advervio Oracion | Oracion

Oracion -> 	Sujeto VP |
		Sujeto Conector |
		Sujeto Adjetivo |
		Sujeto Adjetivo VP |
		Sujeto Adjetivo Conector |
		VP 

VP -> 	VP Sustantivo |			(amo perro)
	VP Preposición Sustantivo |	(estudio en la escuela)
	Adverbio VP Sustantivo |	(siempre amo perro)
	Adverbio VP Preposición Sustantivo |	(siempre estudio en la escuela)

Sustantivo -> 	Adjetivo Sustantivo |
		Sustantivo Conector |

Conector -> Conector VP | Conector S

Sujeto ->ya | ty | on | ona | my | oni
VP -> lyublyu | zhivu | khochu | uchus’ | vizhu | 
Conector -> i | ili | no | potomu chto | khotya | togda | yesli | tozhe
Sustantivo -> papa | mama | kot | sobaka | dom | shkola | drug | lyubov
Preposicion -> v | na | s | bez | dlya | k | iz
Adverbio → bystro | medlenno | vsegda | nikogda | inogda | segodnya | vchera | khorosho | plokho | mnogo | malo
Adjetivo → bolshoy | krasivaya | nekrasivyy | novyy | staryy | umnyy | sil'nyy | slabyy | khoroshiy | plokhoy | chornyy | belyy | krasnyy | malen’kiy | bystryy | medlennyy
```
---

Con esta gramática podemos generar oraciones como:
 1. ```ya lyublyu sobaka``` → yo amo al perro
 2. ```ya umnyy no ty tozhe``` → Yo soy inteligente pero tú también
 3. ```ona krasivaya i segodnya vizhu sobaka``` → Ella es hermosa y hoy veo un perro

Esta gramática inicial permite generar **oraciones simples y compuestas** en ruso básico. Sin embargo, presenta dos problemas principales:

- **Ambigüedad**: una misma oración puede derivarse de varias maneras.
- **Recursión por la izquierda**: algunas reglas se refieren a sí mismas en primera posición.

Estos problemas impiden que la gramática sea compatible con un analizador **LL(1)**, por lo que fue necesario realizar procesos de **limpieza y reestructuración** para adaptarla.

## Eliminación de ambiguedad

Durante la revisión de la gramática inicial, se detectaron tres principales problemas que provocaban ambigüedad:

1. Se definia en conector dos caminos posibles en la que una oración puede iniciar con un ```verbo```
```python
Conector -> Conector S -> Oracion -> VP (Verbo)
Conector -> Conector VP (Verbo)
```
2. El ```Adverbio``` se define en dos caminos posibles al inicio de una oración
```python
   S -> Adverbio Oracion -> Oracion -> VP
   VP -> Adverbio VP ...
```
3. La clase Oración repite la misma secuencia para ```Sujeto Adjetivo```
```python
Oracion ->	Sujeto VP |
		Sujeto Conector |
		Sujeto Adjetivo |
		Sujeto Adjetivo VP |
		Sujeto Adjetivo Conector |
```

Para resolver estos problemas, se reestructuró la gramática de la siguiente forma, agrupando de manera ordenada las opciones y eliminando definiciones redundantes:
```python
S -> Oracion ST

Oracion -> OracionAdjetivo |
	   OracionConector |
	   Sujeto VP |
	   VP

OracionConector -> Sujeto Conector |
		   Sujeto Adjetivo Conector 

OracionAdjetivo -> Sujeto Adjetivo AdjT

AdjT -> VP | ε

VP -> 	VP Sustantivo |
	VP Preposicion Sustantivo |
	Adverbio Verbo VPT

Sustantivo -> 	Adjetivo Sustantivo |
		Sustantivo Conector

ST -> Conector Oracion ST | ε 
```
NOTA: se cambio  ```Conector -> Conector VP | Conector S``` por ```ST -> Conector Oracion ST | ε``` es una manera más sencilla de hacer que la oración puede terminar con **otra oracion completa** o en **ε**

Sin embargo la gramatica sigue teniendo problemas para que sea considerado un LL(1) ya que aún existe recursión izquierda en ciertas producciones

## Eliminación de Recursión Izquierda
Revisando la gramatica anterior encontre recursión izquierda en los siguientes apartados:
1. En la definición de conector
```python
**Conector** -> Conector VP | **Conector S**
```
2. En la definición de VP
```python
**VP** -> **VP** Sustantivo |
	  **VP** Preposicion Sustantivo |
	    ...
```
3. Dentro de la definición de Sustantivo
```python
**Sustantivo** -> Adjetivo Sustantivo |
		  **Sustantivo* Conector
```
Para resolver estos problemas, se reestructuro la gramática de la siguiente manera, eliminando las recursiones izquierdas encontradas
```python
S -> Oracion ST

Oracion -> 	OracionAdjetivo | 
		OracionConector | 
		Sujeto VP | 
		VP

OracionAdjetivo -> Sujeto Adjetivo AdjT

AdjT -> VP | ε

OracionConector -> Sujeto Conector | Sujeto Adjetivo Conector

VP -> Verbo VPT | Adverbio Verbo VPT

VPT -> Sustantivo | Preposicion Sustantivo |  ε

ST -> Conector Oracion ST |  ε
 
Sustantivo -> Adjetivo Sustantivo1

Sustantivo1 -> Conector Adjetivo Sustantivo' |  ε
```

## Pruebas

Ya que la gramática no cuenta con ambiguedad y recursión izquierda, procederemos a probarla. Para ello, utilizaremos la biblioteca **(NLTK)** es una biblioteca ampliamente utilizada para el procesamiento de lenguaje natural en Python, el cual nos ayudara a validar la gramática de manera rápida.

Dentro de este repositorio esta el archivo ```gramatica mejorada.py``` para poder ejecutarlo solo tienes que intalar NLTK con ```pip install nltk```

A continuación se presentan ejemplos de frases que **son aceptadas** y **no son aceptadas** por la gramática desarrollada.

### 5 Ejemplos aceptados por la gramática

1. *Sujeto + Verbo + Sustantivo* -> **```ona vizhu kot```** -> ella ve un gato
2. *Sujeto + Adverbio + Verbo + Sustantivo* -> **```ona bystro vizhu kot```** -> ella rápidamente ve un gato
3. *Dos oraciones simples unidas por conector* -> **```ty lyublyu papa i ya khochu sobaka```** -> tú amas al papá y yo quiero un perro
4. *Sujeto + Adjetivo + Verbo + Sustantivo* -> **```ya krasivaya lyublyu kot```** -> yo (que soy hermoso) amo un gato
5. *Oración compleja con adjetivo, adverbio y conector* -> **```ona umnyy bystro vizhu sobaka no my khochu dom```** -> ella inteligente ve rápidamente al perro pero nosotros queremos una casa

### Ejemplos no aceptados por la gramática

1. **```ona i kot```** -> ella y el gato -> falta verbo; no basta conectar dos sustantivos sin acción
2. **```bystro krasivaya sobaka```** -> rápidamente hermoso perro -> orden incorrecto: adverbio antes de adjetivo
3. **```ya papa i mama```** -> yo papá y mamá ->falta verbo para unir sujeto y sustantivos
4. **```lyublyu ya dom```** -> amo yo casa -> el verbo aparece antes del sujeto; estructura incorrecta
5. **```dom i ya uchus'```** -> la casa y yo estudio -> sujeto compuesto mal estructurado

### Explicación rápida del patrón de frases aceptadas

Las frases válidas en esta gramática respetan los siguientes patrones:

- Siguen una estructura tipo: **Sujeto + (Adjetivo) + (Adverbio) + Verbo + (Preposición) + Sustantivo**.
- Pueden unir varias oraciones usando **conectores** como `i`, `no`, `potomu_chto`, entre otros.
- Admiten secuencias de **adjetivo + sustantivo** siempre que mantengan el orden correcto.

Aquí estan algunos ejemplos de la generación de algunos de los arboles

**```ona i kot```**

![image](https://github.com/user-attachments/assets/4d78e61c-0851-4115-b9eb-b363908a1651)

**```ty lyublyu papa i ya khochu sobaka```**

![image](https://github.com/user-attachments/assets/d70c1b12-c928-4aed-a92b-0f7cecc45230)

**```ona umnyy bystro vizhu sobaka no my khochu dom```**

![image](https://github.com/user-attachments/assets/123c3eb9-cc0a-43f5-b233-159c0ce21a32)

## Analisis
