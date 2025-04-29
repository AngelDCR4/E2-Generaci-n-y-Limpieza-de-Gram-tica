import nltk
from nltk import CFG

gramatica = CFG.fromstring("""
S -> Oracion ST
Oracion -> OracionAdjetivo | OracionConector | Sujeto VP | VP
OracionAdjetivo -> Sujeto Adjetivo AdjT
AdjT -> VP | 
OracionConector -> Sujeto Conector | Sujeto Adjetivo Conector
VP -> Verbo VPT | Adverbio Verbo VPT
VPT -> Sustantivo | Preposicion Sustantivo | 
ST -> Conector Oracion ST | 
Sujeto -> "ya" | "ty" | "on" | "ona" | "my" | "oni"
Verbo -> "lyublyu" | "zhivu" | "khochu" | "uchus'" | "vizhu" | "rabotayu"
Conector -> "i" | "ili" | "no" | "potomu_chto" | "khotya" | "togda" | "yesli" | "tozhe"
Preposicion -> "v" | "na" | "s" | "bez" | "dlya" | "k" | "iz"
Sustantivo -> Adjetivo Sustantivo1 | "papa" | "mama" | "kot" | "sobaka" | "dom" | "shkola" | "drug" | "lyubov" | "rabota"
Sustantivo1 -> Conector Adjetivo Sustantivo1 | 
Adverbio -> "bystro" | "medlenno" | "vsegda" | "nikogda" | "inogda" | "segodnya" | "vchera" | "khorosho" | "plokho" | "mnogo" | "malo"
Adjetivo -> "bolshoy" | "krasivaya" | "nekrasivyy" | "novyy" | "staryy" | "umnyy" | "sil'nyy" | "slabyy" | "khoroshiy" | "plokhoy" | "chornyy" | "belyy" | "krasnyy" | "malen'kiy" | "bystryy" | "medlennyy"
""")

parser = nltk.ChartParser(gramatica)

oracion = "ona umnyy bystro vizhu sobaka no my khochu dom".split()

trees = list(parser.parse(oracion))

if trees:
    print(f"Árboles generados: {len(trees)}")
    for i, tree in enumerate(trees, 1):
        print(f"\nÁrbol {i}:")
        tree.pretty_print()
else:
    print("No se generaron árboles.")
