import os
import matplotlib.pyplot as plt
import re  # To manipulate CIGAR strings

# Prompt the user for the file path
def get_file_path():
    filePath = input("Path to your SAM file: ")
    
    # If the file path does not exist, print "Error" to the terminal.
    if not os.path.exists(filePath): 
        print("Error") 
        return None 
    return filePath

def read_sam_file(filePath): 
    # Dictionary to store the data
    sam_data = {}
    try:
        # Open and read the SAM file
        with open(filePath, "r") as sam_file:
            i = 0
            for line in sam_file:
                i += 1
                # Skip header lines
                if line.startswith('@'):
                    continue 

                # Split the line into columns
                columns = line.strip().split('\t')

                # Extract information
                read_name = columns[0]  # Column 1: Read name
                flag = int(columns[1])  # Column 2: Flag
                chromosome = columns[2]  # Column 3: Chromosome
                position = int(columns[3])  # Column 4: Position
                quality = int(columns[4])  # Column 5: Quality
                sequence = columns[9]  # Column 10: Nucleotide sequence
                cigar = columns[5]  # Column 6: CIGAR

                # Add the information to the dictionary
                sam_data[i] = {
                    "flag": flag,
                    "chromosome": chromosome,
                    "position": position,
                    "quality": quality,
                    "sequence": sequence,
                    "cigar": cigar
                }
                
        print(f"\nSAM dictionary created with {len(sam_data)} entries.\n")
        return sam_data 
    except Exception as e: 
        print("Error reading file")
        return None 

def is_partially_mapped(cigar):
    """
    Checks if a read is partially mapped based on its CIGAR string.
    A partially mapped read will have a soft-clipped or unmapped portion in the CIGAR string.
    """
    if re.search(r'(\d+)S', cigar):  # Look for soft clips ('S') in the CIGAR string
        return True
    if re.search(r'(\d+)H', cigar):  # Look for hard clips ('H') in the CIGAR string
        return True
    return False

def main(): 
    file_path = get_file_path()
    if not file_path:
        return 
    sam_data = read_sam_file(file_path) 
    if not sam_data:
        return 

    # Variables for mapped, unmapped, and partially mapped reads
    mapped_reads = 0
    unmapped_reads = 0
    partially_mapped_reads = 0

    # Iterate through the dictionary of reads
    for read_name, info in sam_data.items():
        flag = info["flag"]
        cigar = info["cigar"]

        # Check if the read is mapped, unmapped, or partially mapped
        is_unmapped = flag & 4  # Flag 4 indicates an unmapped read
        if is_unmapped:
            unmapped_reads += 1
        elif is_partially_mapped(cigar):
            partially_mapped_reads += 1
        else:
            mapped_reads += 1

    # Calculate the percentages of mapped, unmapped, and partially mapped reads
    total_reads = mapped_reads + unmapped_reads + partially_mapped_reads

    if total_reads == 0:
        mapped_percentage = unmapped_percentage = partially_mapped_percentage = 0
    else:
        mapped_percentage = (mapped_reads / total_reads) * 100
        unmapped_percentage = (unmapped_reads / total_reads) * 100
        partially_mapped_percentage = (partially_mapped_reads / total_reads) * 100

    # Create a dictionary with the new results
    mapping_results = {
        "mapped": mapped_percentage,
        "unmapped": unmapped_percentage,
        "partially_mapped": partially_mapped_percentage
    }

    # Display the results for mapped, unmapped, and partially mapped reads
    print(f"\n### Results for mapped, unmapped, and partially mapped reads ###")
    print(f"Number of mapped reads: {mapped_reads}")
    print(f"Number of unmapped reads: {unmapped_reads}")
    print(f"Number of partially mapped reads: {partially_mapped_reads}")
    print(f"Percentage of mapped reads: {mapped_percentage:.2f}%")
    print(f"Percentage of unmapped reads: {unmapped_percentage:.2f}%")
    print(f"Percentage of partially mapped reads: {partially_mapped_percentage:.2f}%")

    # Prompt and validate the minimum quality level
    min_mapping_quality = 30
    modify_quality = input(f"\nThe minimum quality level is set to {min_mapping_quality}. \nWould you like to change it? (yes/no): ").strip().lower()
    if modify_quality == "yes":
        new_quality = input("Enter the new minimum quality level: ")
        try:
            min_mapping_quality = int(new_quality)
            print(f"New minimum quality level: {min_mapping_quality}")
        except ValueError:
            print("Invalid value. The minimum quality level remains " + str(min_mapping_quality))

    # Dictionaries to store calculation results
    reads_per_flag = {}
    reads_per_chromosome = {}
    reads_per_quality = {}

    # Iterate through the dictionary again to count flags, chromosomes, and quality
    for read_name, info in sam_data.items():
        flag = info["flag"]
        chromosome = info["chromosome"]
        quality = info["quality"]

        # Filter reads based on the minimum quality level
        if quality < min_mapping_quality:
            continue  # Skip reads with quality below the threshold

        # Count reads by flag
        reads_per_flag[flag] = reads_per_flag.get(flag, 0) + 1

        # Count reads by chromosome
        reads_per_chromosome[chromosome] = reads_per_chromosome.get(chromosome, 0) + 1

        # Count reads by mapping quality
        reads_per_quality[quality] = reads_per_quality.get(quality, 0) + 1

    # Display the results for flags, chromosomes, and quality on the terminal (sorted)
    print("\nResults by flag")
    for flag, count in sorted(reads_per_flag.items()):
        print(f"Flag {flag}: {count} reads")

    print("\nResults by chromosome")
    for chromosome, count in sorted(reads_per_chromosome.items()):
        print(f" Chromosome {chromosome}: {count} reads")

    print("\nResults by mapping quality")
    for quality, count in sorted(reads_per_quality.items()):
        print(f" Quality {quality}: {count} reads")

    # Combine my graphs into a single figure
    def save_all_results():
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))

        # Graph 1: Number of reads by flag
        axs[0, 0].bar(reads_per_flag.keys(), reads_per_flag.values())
        axs[0, 0].set_xlabel('Flag')
        axs[0, 0].set_ylabel('Number of reads')
        axs[0, 0].set_title('Number of reads by flag')

        # Graph 2: Number of reads by chromosome
        chromosomes = list(reads_per_chromosome.keys())
        percentages = [(reads_per_chromosome[chrom] / total_reads) * 100 for chrom in chromosomes]
        axs[0, 1].bar(chromosomes, percentages)
        axs[0, 1].set_xlabel('Chromosome')
        axs[0, 1].set_ylabel('Percentage of reads (%)')
        axs[0, 1].set_title('Percentage of reads by chromosome')

        # Graph 3: Number of reads by quality
        axs[1, 0].bar(reads_per_quality.keys(), reads_per_quality.values())
        axs[1, 0].set_xlabel('Mapping quality')
        axs[1, 0].set_ylabel('Number of reads')
        axs[1, 0].set_title('Number of reads by mapping quality')

        # Graph 4: Distribution of mapped, unmapped, and partially mapped reads
        axs[1, 1].bar(['Mapped reads', 'Unmapped reads', 'Partially mapped reads'],
                      [mapped_percentage, unmapped_percentage, partially_mapped_percentage],
                      color=['green', 'red', 'orange'])
        axs[1, 1].set_xlabel('Read category')
        axs[1, 1].set_ylabel('Percentage')
        axs[1, 1].set_title('Distribution of mapped, unmapped, and partially mapped reads')

        # Adjust spacing between graphs
        plt.subplots_adjust(hspace=0.8)  # Increase vertical spacing between rows

        plt.tight_layout()

        # Save the image as a PDF file
        pdf_filename = "results_graphics.pdf"
        plt.savefig(pdf_filename, format='pdf')
        print(f"\nThe graphs have been saved to the file {pdf_filename}.")
        plt.show()

    save_all_results()

if __name__ == "__main__":
    main()
