# SAM File Processing

This project aims to analyze and extract relevant information from SAM (Sequence Alignment/Map) files, a standard format used to store alignment data from genomic sequencing.

---
## 🚀 Main Features

- **SAM Format Validation**: Validates headers and the minimum number of columns.
- **Key Information Extraction**: Extracts read names, flags, chromosome, position, quality, and sequence.
- **Data Analysis**: Calculates important metrics such as mapping quality.

---
## 📂 Project Structure

- `README.md`: Documentation for the project.-
- `verif_sam.sh`: A Bash script to validate the SAM file format.
- `analyse_sam.py`: A Python script to extract data and perform analyses.
- `headmapping.sam`: An example SAM file for testing the workflow.
- `Figure_exemple-headmapping.png`: An example of graphical results generated using `headmapping.sam`.
---
## 🛠 Prerequisites
Before you start, make sure to have installed:
- [Python 3.x](https://www.python.org/) (or Bash, depending on your preferred version of the script).
- Git (optional, for cloning the repository).

##  SAM file validation in bash
Example outputs:
* If the file is valid:
  The file test.sam is in SAM format.
  You can continue with this file for the next steps in the program.
* If the file is invalid:
  Error: The file test.sam is not in SAM format.
  Please choose a different input file.
