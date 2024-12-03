import os 
import matplotlib.pyplot as plt

def get_file_path():
    filePath = input("Chemin de votre fichier SAM : ")

    if not os.path.exists(filePath): 
        print("Erreur") 
        return None 
    return filePath

def read_sam_file(filePath): 
    # Dictionnaire pour stocker les données
    sam_data = {}
    try:
        # Ouvrir et lire le fichier SAM
        with open(filePath, "r") as sam_file:
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
        return sam_data 
    except Exception as e: 
        print("Erreur de lecture fichier")
        return None 

def main(): 
    file_path = get_file_path()
    if not file_path:
        return 
    sam_data = read_sam_file(file_path) 
    if not sam_data:
        return 

    # Dictionnaires pour stocker les résultats des calculs
    reads_per_flag_interval = {}
    reads_per_chromosome = {}
    reads_per_quality = {}

    # Paramètres de filtrage
    min_mapping_quality = 30
    only_fully_mapped = True  # Filtrer les reads non mappés

    # Variables de read mappées et non mappées 
    mapped_reads = 0
    unmapped_reads = 0

    # Parcourir le dictionnaire des reads
    for read_name, info in sam_data.items():
        flag = info["flag"]
        chromosome = info["chromosome"]
        quality = info["quality"]

        # Vérifier si le read est mappé ou non
        is_unmapped = flag & 4  # Flag 4 indique un read non mappé
        if is_unmapped:
            unmapped_reads += 1
        else:
            mapped_reads += 1

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
    
    # Calculer le pourcentage de reads non mappés par rapport aux mappés
    if mapped_reads == 0:
        unmapped_percentage = 100 if unmapped_reads > 0 else 0
    else:
        unmapped_percentage = (unmapped_reads / mapped_reads) * 100
    mapped_percentage = 100 - unmapped_percentage

    # Création d'un dictionnaire avec les nouveaux résultats 
    mapping_resultats = {
        "mapped": mapped_percentage,
        "unmapped": unmapped_percentage
    }
    print(f"\nDictionnaire des résultats de mapping : {mapping_resultats}")
    
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

    print(f"\nNombre de reads mappés: {mapped_reads}")
    print(f"Nombre de reads non mappés: {unmapped_reads}")
    print(f"Pourcentage de reads mappés: {mapped_percentage:.2f}%")
    print(f"Pourcentage de reads non mappés: {unmapped_percentage:.2f}%")

    def saveResultats(reads_per_flag_interval, plotFilename='graph1.png'): 
        # Graphique du nombre de reads par intervalle de flag
        plt.figure(figsize=(10, 6))
        plt.bar(reads_per_flag_interval.keys(), reads_per_flag_interval.values(), width=8)
        plt.xlabel('Intervalle de flag')
        plt.ylabel('Nombre de reads')
        plt.title('Nombre de reads par intervalle de flag')
        plt.xticks(list(reads_per_flag_interval.keys())) 
        plt.show()

    saveResultats(reads_per_flag_interval)

    def saveResultats2(reads_per_chromosome, total_reads, plotFilename='graph2.png'):
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

    saveResultats2(reads_per_chromosome, total_reads) 

    def saveResultats3(reads_per_quality, plotFilename='graph3.png'):
        # Graphique du nombre de reads par qualité de mapping
        plt.figure(figsize=(10, 6))
        plt.bar(reads_per_quality.keys(), reads_per_quality.values())
        plt.xlabel('Qualité de mapping')
        plt.ylabel('Nombre de reads')
        plt.title('Nombre de reads par qualité de mapping')
        plt.show()

    saveResultats3(reads_per_quality)

    # Création d'un dictionnaire avec les nouveaux résultats
    mapping_resultats = {
        "mapped": mapped_percentage,
        "unmapped": unmapped_percentage
    }
    print(f"\nDictionnaire des résultats de mapping :")
    print(mapping_resultats)

    # Graphique pour la répartition des reads mappés et non mappés
    def saveResultats4(mapping_resultats, plotFilename='graph4.png'):
        plt.figure(figsize=(10, 6))
        plt.bar(['Reads mappés', 'Reads non mappés'], [mapped_percentage, unmapped_percentage], color=['green', 'red'])
        plt.xlabel('Catégorie de reads')
        plt.ylabel('Pourcentage')
        plt.title('Répartition des reads mappés et non mappés')
        plt.show()

    saveResultats4(mapping_resultats)


if __name__ == "__main__":
    main()
