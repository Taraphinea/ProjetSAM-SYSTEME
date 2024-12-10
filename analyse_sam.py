import os
import matplotlib.pyplot as plt
import re  # Pour manipuler les CIGAR strings

# Demander le chemin du fichier à utiliser
def get_file_path():
    filePath = input("Chemin de votre fichier SAM : ")
    
    # Si le chemin du fichier n'existe pas, alors le terminal affiche "Erreur". 
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
            i = 0
            for line in sam_file:
                i += 1
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
                cigar = columns[5]  # Colonne 6 : CIGAR

                # Ajouter les informations dans le dictionnaire
                sam_data[i] = {
                    "flag": flag,
                    "chromosome": chromosome,
                    "position": position,
                    "quality": quality,
                    "sequence": sequence,
                    "cigar": cigar
                }
                
        print(f"\nDictionnaire SAM créé avec {len(sam_data)} entrées.\n")
        return sam_data 
    except Exception as e: 
        print("Erreur de lecture fichier")
        return None 

def is_partially_mapped(cigar):
    """
    Vérifie si un read est partiellement mappé en fonction de sa chaîne CIGAR.
    Un read partiellement mappé aura une partie soft-clipped ou non mappée dans le CIGAR.
    """
    if re.search(r'(\d+)S', cigar):  # Recherche des soft-clips ('S') dans le CIGAR
        return True
    if re.search(r'(\d+)H', cigar):  # Recherche des hard-clips ('H') dans le CIGAR
        return True
    return False

def main(): 
    file_path = get_file_path()
    if not file_path:
        return 
    sam_data = read_sam_file(file_path) 
    if not sam_data:
        return 

    # Variables de read mappées, non mappées, et partiellement mappées
    mapped_reads = 0
    unmapped_reads = 0
    partially_mapped_reads = 0

    # Parcourir le dictionnaire des reads
    for read_name, info in sam_data.items():
        flag = info["flag"]
        cigar = info["cigar"]

        # Vérifier si le read est mappé, non mappé ou partiellement mappé
        is_unmapped = flag & 4  # Flag 4 indique un read non mappé
        if is_unmapped:
            unmapped_reads += 1
        elif is_partially_mapped(cigar):
            partially_mapped_reads += 1
        else:
            mapped_reads += 1

    # Calculer les pourcentages de reads mappés, non mappés et partiellement mappés
    total_reads = mapped_reads + unmapped_reads + partially_mapped_reads

    if total_reads == 0:
        mapped_percentage = unmapped_percentage = partially_mapped_percentage = 0
    else:
        mapped_percentage = (mapped_reads / total_reads) * 100
        unmapped_percentage = (unmapped_reads / total_reads) * 100
        partially_mapped_percentage = (partially_mapped_reads / total_reads) * 100

    # Création d'un dictionnaire avec les nouveaux résultats 
    mapping_resultats = {
        "mapped": mapped_percentage,
        "unmapped": unmapped_percentage,
        "partially_mapped": partially_mapped_percentage
    }

    # Afficher les résultats des reads mappés, non mappés et partiellement mappés
    print(f"\nRésultats des reads mappés, non mappés et partiellement mappés")
    print(f"Nombre de reads mappés: {mapped_reads}")
    print(f"Nombre de reads non mappés: {unmapped_reads}")
    print(f"Nombre de reads partiellement mappés: {partially_mapped_reads}")
    print(f"Pourcentage de reads mappés: {mapped_percentage:.2f}%")
    print(f"Pourcentage de reads non mappés: {unmapped_percentage:.2f}%")
    print(f"Pourcentage de reads partiellement mappés: {partially_mapped_percentage:.2f}%")

    # Demander et valider le niveau de qualité minimum
    min_mapping_quality = 30
    modify_quality = input(f"Le niveau de qualité minimum est défini sur {min_mapping_quality}. Souhaitez-vous le modifier ? (oui/non) : ").strip().lower()
    if modify_quality == "oui":
        new_quality = input("Entrez le nouveau niveau de qualité minimum : ")
        try:
            min_mapping_quality = int(new_quality)
            print(f"Nouveau niveau de qualité minimum : {min_mapping_quality}")
        except ValueError:
            print("Valeur invalide. Le niveau de qualité minimum reste à " + str(min_mapping_quality))

    # Dictionnaires pour stocker les résultats des calculs
    reads_per_flag = {}
    reads_per_chromosome = {}
    reads_per_quality = {}

    # Parcourir à nouveau le dictionnaire pour compter les flags, chromosomes et qualité
    for read_name, info in sam_data.items():
        flag = info["flag"]
        chromosome = info["chromosome"]
        quality = info["quality"]

        # Filtrer les reads selon la qualité minimum
        if quality < min_mapping_quality:
            continue  # Ignorer les reads avec une qualité inférieure au seuil

        # Compter les reads par flag
        reads_per_flag[flag] = reads_per_flag.get(flag, 0) + 1

        # Compter les reads par chromosome
        reads_per_chromosome[chromosome] = reads_per_chromosome.get(chromosome, 0) + 1

        # Compter les reads par qualité de mapping
        reads_per_quality[quality] = reads_per_quality.get(quality, 0) + 1

    # Afficher les résultats des flags, chromosomes et qualité sur le terminal triés
    print("\nRésultats des flags (triés)")
    for flag, count in sorted(reads_per_flag.items()):
        print(f" Flag {flag}: {count} reads")

    print("\nRésultats par chromosome (triés)")
    for chromosome, count in sorted(reads_per_chromosome.items()):
        print(f" Chromosome {chromosome}: {count} reads")

    print("\nRésultats par qualité de mapping (triés) ###")
    for quality, count in sorted(reads_per_quality.items()):
        print(f" Qualité {quality}: {count} reads")

    # Compilation de mes graphiques dans une seule figure
    def save_all_resultats():
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))

        # Graphique 1: Nombre de reads par flag
        axs[0, 0].bar(reads_per_flag.keys(), reads_per_flag.values())
        axs[0, 0].set_xlabel('Flag')
        axs[0, 0].set_ylabel('Nombre de reads')
        axs[0, 0].set_title('Nombre de reads par flag')

        # Graphique 2: Nombre de reads par chromosome
        chromosomes = list(reads_per_chromosome.keys())
        percentages = [(reads_per_chromosome[chrom] / total_reads) * 100 for chrom in chromosomes]
        axs[0, 1].bar(chromosomes, percentages)
        axs[0, 1].set_xlabel('Chromosome')
        axs[0, 1].set_ylabel('Pourcentage de reads (%)')
        axs[0, 1].set_title('Pourcentage de reads par chromosome')
        axs[0, 1].tick_params(axis='x', rotation=90)

        # Graphique 3: Nombre de reads par qualité
        axs[1, 0].bar(reads_per_quality.keys(), reads_per_quality.values())
        axs[1, 0].set_xlabel('Qualité de mapping')
        axs[1, 0].set_ylabel('Nombre de reads')
        axs[1, 0].set_title('Nombre de reads par qualité de mapping')

        # Graphique 4: Répartition des reads mappés, non mappés et partiellement mappés
        axs[1, 1].bar(['Reads mappés', 'Reads non mappés', 'Reads partiellement mappés'],
                      [mapped_percentage, unmapped_percentage, partially_mapped_percentage],
                      color=['green', 'red', 'orange'])
        axs[1, 1].set_xlabel('Catégorie de reads')
        axs[1, 1].set_ylabel('Pourcentage')
        axs[1, 1].set_title('Répartition des reads mappés, non mappés et partiellement mappés')

        # Ajuster l'espace entre les graphes
        plt.subplots_adjust(hspace=0.4)  # Augmenter l'espacement vertical entre les lignes

        plt.tight_layout()

        # Enregistrer l'image sous format PDF
        pdf_filename = "resultats_graphiques.pdf"
        plt.savefig(pdf_filename, format='pdf')
        print(f"Les graphiques ont été enregistrés dans le fichier {pdf_filename}.")
        plt.show()

    save_all_resultats()

if __name__ == "__main__":
    main()
