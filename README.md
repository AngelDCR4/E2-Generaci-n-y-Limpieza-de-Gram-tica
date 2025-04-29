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

AdjT -> Continuacion | ε

Continuacion -> VP | Oracion ST

VP -> 	Verbo VPT |
	Adverbio Verbo VPT

VPT -> Sustantivo | Preposicion Sustantivo | ε

Sustantivo -> 	Adjetivo Sustantivo |
		Sustantivo Conector |

ST -> Conector Oracion ST | ε
```

Sin embargo la gramatica sigue teniendo problemas para que sea considerado un LL(1) ya que aún existe recursión izquierda en ciertas producciones

## Eliminación de Recursión Izquierda
Revisando la gramatica encontre recursión izquierda en los siguientes apartados:
1. 
```python```
