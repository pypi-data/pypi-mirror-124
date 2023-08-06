La librairie niiif-niiif crée et publie le manifeste IIIF d'une donnée Nakala. 

Plus précisément, niiif-niiif : 
- Vérifie si la donnée Nakala dont l'identifiant lui est donné en paramètre existe. Le cas échéant,
- Supprime s'il existe l'ancien fichier metadata.json des fichiers de la donnée,
- Crée un manifeste IIIF à partir des fichiers JPEG ou TIFF de la donnée Nakala, 
- Ajoute à la donnée Nakala le fichier metadata.json contenant le manifeste.

Vous pouvez ensuite copier l'URL de téléchargement du fichier metadata.json et la transmettre à une visionneuse IIIF 
(ex. [Mirador](https://mirador-dev.netlify.app/__tests__/integration/mirador/)).

L'URL d'un fichier déposé sur Nakala est unique. L'URL du manifeste d'une donnée changera donc à chaque fois que vous le créerez avec niiif-niiif. Pensez à soumettre cette nouvelle URL à la visionneuse. 

# Installation
 
Pour utiliser le script, utilisez de préférence un gestionnaire d'environnement Python tel que [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

```bash
# Vous pouvez définir le nom de l'environnement Python à votre convenance avec le paramètre -n.
conda create -n niiif-niiif python=3.8
# Activez l'environnement
conda activate niiif-niiif
# Installez la librairie niiif
pip install niiif-niiif
```

# Utilisation

Le script a besoin pour fonctionner des clés d'API d'un compte utilisateur Nakala ayant des droits d'écriture sur 
la donnée Nakala pour laquelle vous souhaitez créer un manifeste. Cette clé d'API est à créer et à copier 
depuis le profil du compte Nakala.

## En ligne de commande

```bash
# Activez l'environnement (si ce n'est pas déjà fait)
conda activate niiif-niiif 
# Pour créer le manifeste de la donnée Nakala dont l'ID = 10.34847/nkl.12121212
python -m niiif -apikey 12345678-12345678-1234578-12345678 -dataid 10.34847/nkl.12121212
```

## Dans un script Python

La fonction `create_data_manifest_if_data_exists(apiKey, dataIdentifier)` peut être importée depuis un script Python.

```bash
# Activez l'environnement (si ce n'est pas déjà fait)
conda activate niiif-niiif 
# Lancez python
python
>>> from niiif import create_data_manifest_if_data_exists
>>> create_data_manifest_if_data_exists(apiKey='12345678-12345678-1234578-12345678', dataIdentifier='10.34847/nkl.12121212')
```