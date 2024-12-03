# SAM File Processing

This project aims to analyze and extract relevant information from SAM (Sequence Alignment/Map) files, a standard format used to store alignment data from genomic sequencing.

---
## 🚀 Main Features

- **SAM Format Validation**: Validates headers and the minimum number of columns.
- **Key Information Extraction**: Extracts read names, flags, chromosome, position, quality, and sequence.
- **Data Analysis**: Calculates important metrics such as mapping quality.

---
## 📂 Project Structure

- `verif_sam.sh`: Bash script to validate the SAM file.
- `analyse_sam.py`: Python script to extract data and perform analysis.
- `headmapping.sam`: Example SAM file for testing the workflow.
- `README.md`: Project documentation.

---
## 🛠 Prerequisites
Before you start, make sure to have installed:
- [Python 3.x](https://www.python.org/) (or Bash, depending on your preferred version of the script).
- Git (optional, for cloning the repository).

---
## 🚀 Usage
### 1. SAM file validation in bash
Example outputs:
* If the file is valid:
  The file test.sam is in SAM format.
  You can continue with this file for the next steps in the program.
* If the file is invalid:
  Error: The file test.sam is not in SAM format.
  Please choose a different input file.
### 2. Creating a dictionary:
The dictionary has been successfully created when the terminal displays: SAM Dictionary created with "n" entries. "Dictionnaire SAM créé avec "n" entrées."
### 3. File analysis
