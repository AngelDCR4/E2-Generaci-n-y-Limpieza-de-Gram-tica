import nltk
from nltk import CFG

gramatica = CFG.fromstring("""
S -> Adverbio Oracion | Oracion
Oracion -> Sujeto VP | Sujeto Conector | Sujeto Adjetivo | Sujeto Adjetivo VP | Sujeto Adjetivo Conector | VP
VP -> VP Sustantivo | VP Preposicion Sustantivo | Adverbio VP Sustantivo | Adverbio VP Preposicion Sustantivo | "lyublyu" | "zhivu" | "khochu" | "uchus'" | "vizhu" | "rabotayu"
Sustantivo -> Adjetivo Sustantivo | Sustantivo Conector | "papa" | "mama" | "kot" | "sobaka" | "dom" | "shkola" | "drug" | "lyubov" | "rabota"
Conector -> Conector VP | Conector S | "i" | "ili" | "no" | "potomu_chto" | "khotya" | "togda" | "yesli" | "tozhe"
Preposicion -> "v" | "na" | "s" | "bez" | "dlya" | "k" | "iz"
Sujeto -> "ya" | "ty" | "on" | "ona" | "my" | "oni"
Adverbio -> "bystro" | "medlenno" | "vsegda" | "nikogda" | "inogda" | "segodnya" | "vchera" | "khorosho" | "plokho" | "mnogo" | "malo"
Adjetivo -> "bolshoy" | "krasivaya" | "nekrasivyy" | "novyy" | "staryy" | "umnyy" | "sil'nyy" | "slabyy" | "khoroshiy" | "plokhoy" | "chornyy" | "belyy" | "krasnyy" | "malen'kiy" | "bystryy" | "medlennyy"
""")

parser = nltk.ChartParser(gramatica)

oracion = "ona umnyy bystro vizhu sobaka no my khochu dom i ona krasivaya".split()

trees = list(parser.parse(oracion))

if trees:
    print(f"Árboles generados: {len(trees)}")
    for i, tree in enumerate(trees, 1):
        print(f"\nÁrbol {i}:")
        tree.pretty_print()
else:
    print("No se generaron árboles.")
