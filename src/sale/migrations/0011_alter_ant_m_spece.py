# Generated by Django 4.1.7 on 2023-12-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0010_pack_m_thumbnail_1_pack_m_thumbnail_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ant_m',
            name='spece',
            field=models.CharField(choices=[('Acamatus', 'Acamatus'), ('Acanthognathus', 'Acanthognathus'), ('Acanthomyops', 'Acanthomyops'), ('Acanthostichus', 'Acanthostichus'), ('Acromyrmex', 'Acromyrmex'), ('Adetomyrma', 'Adetomyrma'), ('Aenictus', 'Aenictus'), ('Amblyopone', 'Amblyopone'), ('Amblyteles', 'Amblyteles'), ('Anergates', 'Anergates'), ('Anochetus', 'Anochetus'), ('Anonychomyrma', 'Anonychomyrma'), ('Aphaenogaster', 'Aphaenogaster'), ('Asphinctanilloides', 'Asphinctanilloides'), ('Atta', 'Atta'), ('Ateca', 'Ateca'), ('Brachymyrmex', 'Brachymyrmex'), ('Bothriomyrmex', 'Bothriomyrmex'), ('Camponotus', 'Camponotus'), ('Cardiocondyla', 'Cardiocondyla'), ('Carebara', 'Carebara'), ('Cephalotes', 'Cephalotes'), ('Cerapachys', 'Cerapachys'), ('Chelaner', 'Chelaner'), ('Cheliomyrmex', 'Cheliomyrmex'), ('Colobopsis', 'Colobopsis'), ('Crematogaster', 'Crematogaster'), ('Cryptocerus', 'Cryptocerus'), ('Cyphomyrmex', 'Cyphomyrmex'), ('Daceton', 'Daceton'), ('Diacamma', 'Diacamma'), ('Dinoponera', 'Dinoponera'), ('Diplomorium', 'Diplomorium'), ('Discothyrea', 'Discothyrea'), ('Dolichoderus', 'Dolichoderus'), ('Donisthorpea', 'Donisthorpea'), ('Dorymyrmex', 'Dorymyrmex'), ('Dorylus', 'Dorylus'), ('Eciton', 'Eciton'), ('Ectatomma', 'Ectatomma'), ('Ephebomyrmex', 'Ephebomyrmex'), ('Epoecus', 'Epoecus'), ('Epipheidole', 'Epipheidole'), ('Erebomyrma', 'Erebomyrma'), ('Euponera', 'Euponera'), ('Forelius', 'Forelius'), ('Formica', 'Formica'), ('Formicoxenus', 'Formicoxenus'), ('Gigantiops', 'Gigantiops'), ('Harpagoxenus', 'Harpagoxenus'), ('Harpegnathos', 'Harpegnathos'), ('Holcoponera', 'Holcoponera'), ('Hypoclinea', 'Hypoclinea'), ('Hypoponera', 'Hypoponera'), ('Ichnomyrmex', 'Ichnomyrmex'), ('Iridomyrmex', 'Iridomyrmex'), ('Janetia ', 'Janetia '), ('Lasius', 'Lasius'), ('Leptanilloides', 'Leptanilloides'), ('Leptogenys', 'Leptogenys'), ('Leptomyrmex', 'Leptomyrmex'), ('Leptothorax', 'Leptothorax'), ('Linepithema', 'Linepithema'), ('Liometopum', 'Liometopum'), ('Lobopelta', 'Lobopelta'), ('Macromischa', 'Macromischa'), ('Manica', 'Manica'), ('Megaponera', 'Megaponera'), ('Melophorus', 'Melophorus'), ('Messor', 'Messor'), ('Monomorium', 'Monomorium'), ('Myrmecia', 'Myrmecia'), ('Myrmecina', 'Myrmecina'), ('Myrmecocystus', 'Myrmecocystus'), ('Myrmelachista', 'Myrmelachista'), ('Myrmica', 'Myrmica'), ('Mystrium', 'Mystrium'), ('Neivamyrmex', 'Neivamyrmex'), ('Neoponera', 'Neoponera'), ('Notoncus', 'Notoncus'), ('Novomessor', 'Novomessor'), ('Odontomachus', 'Odontomachus'), ('Oecophylla', 'Oecophylla'), ('Pachycondyla', 'Pachycondyla'), ('Paraponera', 'Paraponera'), ('Parasyscia', 'Parasyscia'), ('Paratrechina', 'Paratrechina'), ('Peronomyrmex', 'Peronomyrmex'), ('Pheidole', 'Pheidole'), ('Pheidologeton', 'Pheidologeton'), ('Pismire', 'Pismire'), ('Plagiolepis', 'Plagiolepis'), ('Platythyrea', 'Platythyrea'), ('Pogonomyrmex', 'Pogonomyrmex'), ('Polyergus', 'Polyergus'), ('Polyrhachis', 'Polyrhachis'), ('Ponera', 'Ponera'), ('Prenolepis', 'Prenolepis'), ('Proceratium', 'Proceratium'), ('Pseudomyrma', 'Pseudomyrma'), ('Pseudomyrmex', 'Pseudomyrmex'), ('Pseudoneoponera', 'Pseudoneoponera'), ('Quartina', 'Quartina'), ('Rhytidoponera', 'Rhytidoponera'), ('Rogeria', 'Rogeria'), ('Solenopsis', 'Solenopsis'), ('Stenamma', 'Stenamma'), ('Stigmatomma', 'Stigmatomma'), ('Streblognathus', 'Streblognathus'), ('Strongylognathus', 'Strongylognathus'), ('Strumigenys', 'Strumigenys'), ('Sympheidole', 'Sympheidole'), ('Sysphincta', 'Sysphincta'), ('Tapinoma', 'Tapinoma'), ('Technomyrmex', 'Technomyrmex'), ('Temnothorax', 'Temnothorax'), ('Tetramorium', 'Tetramorium'), ('Tetraogmus', 'Tetraogmus'), ('Typhlomyrmex', 'Typhlomyrmex'), ('Tyrannomyrmex', 'Tyrannomyrmex'), ('Wheeleriella', 'Wheeleriella'), ('Wasmannia', 'Wasmannia'), ('Xenomyrmex', 'Xenomyrmex'), ('Xiphomyrmex', 'Xiphomyrmex')], max_length=100),
        ),
    ]