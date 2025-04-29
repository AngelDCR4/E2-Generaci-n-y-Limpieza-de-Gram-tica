import nltk
from nltk import CFG

# Definición de la gramática
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

# Lista de oraciones para probar (True si se espera que sea válida)
pruebas = {
    "ona vizhu kot": True,
    "ona bystro vizhu kot": True,
    "ty lyublyu papa i ya khochu sobaka": True,
    "ya krasivaya lyublyu kot": True,
    "ona umnyy bystro vizhu sobaka no my khochu dom": True,
    "ona i kot": False,
    "bystro krasivaya sobaka": False,
    "ya papa i mama": False,
    "lyublyu ya dom": False,
    "dom i ya uchus'": False
}

print("\n====== RESULTADOS ======\n")

# Ejecutar pruebas automáticamente
for frase, es_valida_esperada in pruebas.items():
    oracion = frase.split()
    trees = list(parser.parse(oracion))

    print(f"Frase: '{frase}'")
    if trees:
        print(f"Frase aceptada. Árboles generados: {len(trees)}")
        for i, tree in enumerate(trees, 1):
            print(f"\nÁrbol {i}:")
            tree.pretty_print()
    else:
        print(f"Frase no aceptada por la gramática.")
    print("-" * 50)
