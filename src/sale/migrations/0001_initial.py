# Generated by Django 4.1.7 on 2024-05-03 17:12

from django.db import migrations, models
import django.db.models.deletion
import sale.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ref_code', models.CharField(max_length=15, null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('delivery_option', models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('object_id', models.UUIDField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='OrderTrack_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_track', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pack_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, default=20, max_digits=6)),
                ('thumbnail', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_1', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_2', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_3', models.ImageField(blank=True, null=True, upload_to='products')),
            ],
            bases=(sale.models.ImageConversionMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Product_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=3000)),
                ('thumbnail', models.ImageField(upload_to='products')),
                ('thumbnail_1', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_2', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_3', models.ImageField(blank=True, null=True, upload_to='products')),
                ('thumbnail_4', models.ImageField(blank=True, null=True, upload_to='products')),
                ('video', models.FileField(blank=True, null=True, upload_to='products')),
                ('problem', models.BooleanField(default=False)),
            ],
            bases=(sale.models.ImageConversionMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Size_m',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('worker', models.CharField(choices=[('0', '0'), ('5', '5'), ('10', '10'), ('15', '15'), ('30', '30'), ('50', '50'), ('100', '100'), ('200', '200')], default='5', max_length=20)),
                ('gyne', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('10', '10'), ('+ 10', '+ 10'), ('Gamergate', 'Gamergate')], default='1', max_length=20)),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='Ant_m',
            fields=[
                ('product_m_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sale.product_m')),
                ('localisation', models.CharField(blank=True, choices=[("Afrique de l'Est", 'East Africa'), ("Afrique de l'Ouest", 'West Africa'), ('Afrique du Nord', 'North Africa'), ('Amérique du sud', 'South America'), ('Amérique du nord', 'North America'), ('Algérie', 'Algeria'), ('Australie', 'Australia'), ('Bangladesh', 'Bangladesh'), ('Belgique', 'Belgium'), ('Bhoutan', 'Bhutan'), ('Brunei', 'Brunei'), ('Burundi', 'Burundi'), ('Cambodge', 'Cambodia'), ('Chine', 'China'), ('Comores', 'Comoros'), ('Corée', 'Korea'), ('Corse', 'Corsica'), ("Côte d'Ivoire", 'Ivory Coast'), ('Espagne', 'Spain'), ('Émirats Arabes Unis', 'United Arab Emirates'), ('Égypte', 'Egypt'), ('Éthiopie', 'Ethiopia'), ('Europe Centrale', 'Central Europe'), ("Europe de l'Est", 'Eastern Europe'), ("Europe de l'Ouest", 'Western Europe'), ('Europe du Nord', 'Northern Europe'), ('Europe du Sud-Est', 'Southeastern Europe'), ('France', 'France'), ('Gambie', 'Gambia'), ('Ghana', 'Ghana'), ('Grèce', 'Greece'), ('Inde', 'India'), ('Indonésie', 'Indonesia'), ('Iran', 'Iran'), ('Irak', 'Iraq'), ('Irlande', 'Ireland'), ('Israël', 'Israel'), ('Italie', 'Italy'), ('Japon', 'Japan'), ('Jordanie', 'Jordan'), ('Kazakhstan', 'Kazakhstan'), ('Kenya', 'Kenya'), ('Laos', 'Laos'), ('Liban', 'Lebanon'), ('Liberia', 'Liberia'), ('Libye', 'Libya'), ('Luxembourg', 'Luxembourg'), ('Madagascar', 'Madagascar'), ('Malaisie', 'Malaysia'), ('Maroc', 'Morocco'), ('Mauritanie', 'Mauritania'), ('Méditerranée', 'Mediterranean'), ('Mongolie', 'Mongolia'), ('Mozambique', 'Mozambique'), ('Myanmar', 'Myanmar'), ('Népal', 'Nepal'), ('Nigeria', 'Nigeria'), ('Nord de la France', 'North France'), ('Nouvelle-Zélande', 'New Zealand'), ('Océan Indien', 'Indian Ocean'), ('Oman', 'Oman'), ('Pakistan', 'Pakistan'), ('Papouasie-Nouvelle-Guinée', 'Papua New Guinea'), ('Philippines', 'Philippines'), ('Polynésie française', 'French Polynesia'), ('Portugal', 'Portugal'), ('Qatar', 'Qatar'), ('Russie', 'Russia'), ('Rwanda', 'Rwanda'), ('Samoa', 'Samoa'), ('Scandinavie', 'Scandinavia'), ('Sénégal', 'Senegal'), ('Seychelles', 'Seychelles'), ('Sicile', 'Sicily'), ('Sierra Leone', 'Sierra Leone'), ('Singapour', 'Singapore'), ('Soudan', 'Sudan'), ('Sri Lanka', 'Sri Lanka'), ('Sud de la France', 'South France'), ('Suisse', 'Switzerland'), ('Syrie', 'Syria'), ('Tadjikistan', 'Tajikistan'), ('Tanzanie', 'Tanzania'), ('Thaïlande', 'Thailand'), ('Timor Oriental', 'East Timor'), ('Togo', 'Togo'), ('Tunisie', 'Tunisia'), ('Turkménistan', 'Turkmenistan'), ('Turquie', 'Turkey'), ('Ukraine', 'Ukraine'), ('Union Européenne', 'European Union'), ('Uruguay', 'Uruguay'), ('Vanuatu', 'Vanuatu'), ('Vatican', 'Vatican'), ('Venezuela', 'Venezuela'), ('Viêt Nam', 'Vietnam'), ('Yémen', 'Yemen'), ('Zambie', 'Zambia'), ('Zimbabwe', 'Zimbabwe')], default='France', max_length=50)),
                ('spece', models.CharField(choices=[('Acamatus', 'Acamatus'), ('Acanthognathus', 'Acanthognathus'), ('Acanthomyops', 'Acanthomyops'), ('Acanthostichus', 'Acanthostichus'), ('Acromyrmex', 'Acromyrmex'), ('Adetomyrma', 'Adetomyrma'), ('Aenictus', 'Aenictus'), ('Amblyopone', 'Amblyopone'), ('Amblyteles', 'Amblyteles'), ('Anergates', 'Anergates'), ('Anochetus', 'Anochetus'), ('Anonychomyrma', 'Anonychomyrma'), ('Aphaenogaster', 'Aphaenogaster'), ('Asphinctanilloides', 'Asphinctanilloides'), ('Atta', 'Atta'), ('Ateca', 'Ateca'), ('Brachymyrmex', 'Brachymyrmex'), ('Bothriomyrmex', 'Bothriomyrmex'), ('Camponotus', 'Camponotus'), ('Cardiocondyla', 'Cardiocondyla'), ('Carebara', 'Carebara'), ('Cephalotes', 'Cephalotes'), ('Cerapachys', 'Cerapachys'), ('Chelaner', 'Chelaner'), ('Cheliomyrmex', 'Cheliomyrmex'), ('Colobopsis', 'Colobopsis'), ('Crematogaster', 'Crematogaster'), ('Cryptocerus', 'Cryptocerus'), ('Cyphomyrmex', 'Cyphomyrmex'), ('Daceton', 'Daceton'), ('Diacamma', 'Diacamma'), ('Dinoponera', 'Dinoponera'), ('Diplomorium', 'Diplomorium'), ('Discothyrea', 'Discothyrea'), ('Dolichoderus', 'Dolichoderus'), ('Donisthorpea', 'Donisthorpea'), ('Dorymyrmex', 'Dorymyrmex'), ('Dorylus', 'Dorylus'), ('Eciton', 'Eciton'), ('Ectatomma', 'Ectatomma'), ('Ephebomyrmex', 'Ephebomyrmex'), ('Epoecus', 'Epoecus'), ('Epipheidole', 'Epipheidole'), ('Erebomyrma', 'Erebomyrma'), ('Euponera', 'Euponera'), ('Forelius', 'Forelius'), ('Formica', 'Formica'), ('Formicoxenus', 'Formicoxenus'), ('Gigantiops', 'Gigantiops'), ('Harpagoxenus', 'Harpagoxenus'), ('Harpegnathos', 'Harpegnathos'), ('Holcoponera', 'Holcoponera'), ('Hypoclinea', 'Hypoclinea'), ('Hypoponera', 'Hypoponera'), ('Ichnomyrmex', 'Ichnomyrmex'), ('Iridomyrmex', 'Iridomyrmex'), ('Janetia ', 'Janetia '), ('Lasius', 'Lasius'), ('Leptanilloides', 'Leptanilloides'), ('Leptogenys', 'Leptogenys'), ('Leptomyrmex', 'Leptomyrmex'), ('Leptothorax', 'Leptothorax'), ('Linepithema', 'Linepithema'), ('Liometopum', 'Liometopum'), ('Lobopelta', 'Lobopelta'), ('Macromischa', 'Macromischa'), ('Manica', 'Manica'), ('Megaponera', 'Megaponera'), ('Melophorus', 'Melophorus'), ('Messor', 'Messor'), ('Monomorium', 'Monomorium'), ('Myrmecia', 'Myrmecia'), ('Myrmecina', 'Myrmecina'), ('Myrmecocystus', 'Myrmecocystus'), ('Myrmelachista', 'Myrmelachista'), ('Myrmica', 'Myrmica'), ('Mystrium', 'Mystrium'), ('Neivamyrmex', 'Neivamyrmex'), ('Neoponera', 'Neoponera'), ('Notoncus', 'Notoncus'), ('Novomessor', 'Novomessor'), ('Odontomachus', 'Odontomachus'), ('Oecophylla', 'Oecophylla'), ('Pachycondyla', 'Pachycondyla'), ('Paraponera', 'Paraponera'), ('Parasyscia', 'Parasyscia'), ('Paratrechina', 'Paratrechina'), ('Peronomyrmex', 'Peronomyrmex'), ('Pheidole', 'Pheidole'), ('Pheidologeton', 'Pheidologeton'), ('Pismire', 'Pismire'), ('Plagiolepis', 'Plagiolepis'), ('Platythyrea', 'Platythyrea'), ('Pogonomyrmex', 'Pogonomyrmex'), ('Polyergus', 'Polyergus'), ('Polyrhachis', 'Polyrhachis'), ('Ponera', 'Ponera'), ('Prenolepis', 'Prenolepis'), ('Proceratium', 'Proceratium'), ('Pseudomyrma', 'Pseudomyrma'), ('Pseudomyrmex', 'Pseudomyrmex'), ('Pseudoneoponera', 'Pseudoneoponera'), ('Quartina', 'Quartina'), ('Rhytidoponera', 'Rhytidoponera'), ('Rogeria', 'Rogeria'), ('Solenopsis', 'Solenopsis'), ('Stenamma', 'Stenamma'), ('Stigmatomma', 'Stigmatomma'), ('Streblognathus', 'Streblognathus'), ('Strongylognathus', 'Strongylognathus'), ('Strumigenys', 'Strumigenys'), ('Sympheidole', 'Sympheidole'), ('Sysphincta', 'Sysphincta'), ('Tapinoma', 'Tapinoma'), ('Technomyrmex', 'Technomyrmex'), ('Temnothorax', 'Temnothorax'), ('Tetramorium', 'Tetramorium'), ('Tetraogmus', 'Tetraogmus'), ('Typhlomyrmex', 'Typhlomyrmex'), ('Tyrannomyrmex', 'Tyrannomyrmex'), ('Wheeleriella', 'Wheeleriella'), ('Wasmannia', 'Wasmannia'), ('Xenomyrmex', 'Xenomyrmex'), ('Xiphomyrmex', 'Xiphomyrmex')], max_length=100)),
                ('under_spece', models.CharField(blank=True, max_length=100)),
            ],
            bases=('sale.product_m',),
        ),
        migrations.CreateModel(
            name='Other_m',
            fields=[
                ('product_m_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sale.product_m')),
                ('stock', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('type', models.CharField(blank=True, choices=[('nid', 'nid'), ('accessoire', 'accessoire'), ('nourriture', 'nourriture'), ('matériaux', 'materiaux'), ('élevage nourricier', 'élevage nourricier')], default='accessoire', max_length=50)),
            ],
            bases=('sale.product_m',),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('success', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sale.order_m')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
