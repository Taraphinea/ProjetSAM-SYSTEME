# Dictionnaire pour stocker les données
sam_data = {}
## test
# Ouvrir et lire le fichier SAM
with open("headmapping.sam", "r") as sam_file:
    for line in sam_file:
        # Ignorer les lignes de header
        if line.startswith('@'):
            continue

        # Séparer les colonnes de la ligne
        columns = line.strip().split('\t')

        # Extraire les informations
        read_name = columns[0]  # Colonne 1 : Nom du read
        flag = int(columns[1])  # Colonne 2 : Flag
        chromosome = columns[2]  # Colonne 3 : Chromosome
        position = int(columns[3])  # Colonne 4 : Position
        quality = int(columns[4])  # Colonne 5 : Qualité
        sequence = columns[9]  # Colonne 10 : Séquence nucléotidique

        # Ajouter les informations dans le dictionnaire
        sam_data[read_name] = {
            "flag": flag,
            "chromosome": chromosome,
            "position": position,
            "quality": quality,
            "sequence": sequence
        }
print(f"\nDictionnaire SAM créé avec {len(sam_data)} entrées.\n")

import matplotlib.pyplot as plt

    # Dictionnaires pour stocker les résultats des calculs
reads_per_flag_interval = {}
reads_per_chromosome = {}
reads_per_quality = {}

# Paramètres de filtrage
min_mapping_quality = 30
only_fully_mapped = True  # Filtrer les reads non mappés

# Parcourir le dictionnaire des reads
for read_name, info in sam_data.items():
    flag = info["flag"]
    chromosome = info["chromosome"]
    quality = info["quality"]

    # Filtrer les reads si nécessaire
    is_unmapped = flag & 4  # Flag 4 indique un read non mappé
    if only_fully_mapped and is_unmapped:
        continue
    if quality < min_mapping_quality:
        continue

    # Compter les reads par intervalle de flag
    flag_interval = (flag // 10) * 10
    reads_per_flag_interval[flag_interval] = reads_per_flag_interval.get(flag_interval, 0) + 1

    # Compter les reads par chromosome
    reads_per_chromosome[chromosome] = reads_per_chromosome.get(chromosome, 0) + 1

    # Compter les reads par qualité de mapping
    reads_per_quality[quality] = reads_per_quality.get(quality, 0) + 1

    # Calculer le nombre total de reads valides après filtrage
    total_reads = sum(reads_per_chromosome.values())

# Afficher les résultats
print("Nombre de reads par intervalle de flag (par 10) :")
for interval, count in sorted(reads_per_flag_interval.items()):
    print(f"  Intervalle {interval}-{interval+9} : {count} reads")

print("\nNombre de reads par chromosome :")
for chrom, count in reads_per_chromosome.items():
    print(f"  Chromosome {chrom} : {count} reads")

print("\nNombre de reads par chromosome (en pourcentage) :")
for chrom, count in reads_per_chromosome.items():
    percentage = (count / total_reads) * 100  # Calcul du pourcentage
    print(f"  Chromosome {chrom} : {count} reads ({percentage:.2f}%)")

print("\nNombre de reads par qualité de mapping :")
for quality, count in sorted(reads_per_quality.items()):
    print(f"  Qualité {quality} : {count} reads")



# Graphique du nombre de reads par intervalle de flag
plt.figure(figsize=(10, 6))
plt.bar(reads_per_flag_interval.keys(), reads_per_flag_interval.values(), width=8)
plt.xlabel('Intervalle de flag')
plt.ylabel('Nombre de reads')
plt.title('Nombre de reads par intervalle de flag')
plt.xticks(list(reads_per_flag_interval.keys()))
plt.show()

# Graphique du nombre de reads par chromosome en pourcentage
chromosomes = list(reads_per_chromosome.keys())
percentages = [(reads_per_chromosome[chrom] / total_reads) * 100 for chrom in chromosomes]

plt.figure(figsize=(10, 6))
plt.bar(chromosomes, percentages)
plt.xlabel('Chromosome')
plt.ylabel('Pourcentage de reads (%)')
plt.title('Pourcentage de reads par chromosome')
plt.xticks(rotation=90)
plt.show()

# Graphique du nombre de reads par qualité de mapping
plt.figure(figsize=(10, 6))
plt.bar(reads_per_quality.keys(), reads_per_quality.values())
plt.xlabel('Qualité de mapping')
plt.ylabel('Nombre de reads')
plt.title('Nombre de reads par qualité de mapping')
plt.show()
