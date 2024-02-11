import os
import django
import json
from sale.models import Ant_m
from admin_supplier.models import  Supplier_m

# Configuration de l'environnement Djangosaveos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LyAnt.settings')
django.setup()



def migrate_ant_data():
    # Charger les données depuis le fichier JSON
    with open('src/save-data/ant_data.json', 'r') as f:
        ant_data = json.load(f)

    # Récupérer le fournisseur avec l'ID spécifié
    try:
        supplier = Supplier_m.objects.get(id="a8e4da64-c6bf-4cbe-8278-2e3a2ec14076")
    except Supplier_m.DoesNotExist:
        print("Supplier with the specified ID does not exist.")
        return

    # Mettre à jour chaque objet Ant_m avec le supplier
    for data in ant_data:
        ant = Ant_m.objects.get(id=data['id'])  # Assurez-vous que l'id est présent dans le fichier JSON
        ant.supplier = supplier
        ant.save()
    # Votre code de migration ici...

if __name__ == '__main__':
    migrate_ant_data()
