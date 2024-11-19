#!/bin/bash

# Fonction pour vérifier si un fichier est au format SAM
verifier_fichier_sam() {
    local fichier="$1"

    # Vérifie si le fichier existe
    if [[ ! -f "$fichier" ]]; then
        echo "Erreur : Le fichier $fichier n'existe pas."
        return 1
    fi

    # Vérifie les en-têtes et le nombre de colonnes
    while IFS= read -r ligne; do
        # Ligne d'en-tête commence par "@"
        if [[ "$ligne" == @* ]]; then
            continue
        fi

        # Vérifie le nombre de colonnes (au moins 11)
        colonnes=($(echo "$ligne" | tr '\t' ' '))
        if [[ ${#colonnes[@]} -ge 11 ]]; then
            echo "Le fichier est bien au format SAM."
            return 0
        else
            echo "Le fichier n'est pas au format SAM."
            return 1
        fi
    done < "$fichier"

    echo "Le fichier ne contient pas d'enregistrements valides."
    return 1
}

# Exemple d'utilisation
fichier="headmapping.sam"
verifier_fichier_sam "$fichier"

