## Dataset

Za potrebe projekta korišćen je skup podataka o kupcima koji sadrži informacije o transakcijama, datumu kupovine, vrijednosti kupovine i identifikatorima kupaca.

Prije analize izvršeno je:

- čišćenje podataka,
- uklanjanje nedostajućih vrijednosti,
- transformacija atributa,
- priprema podataka za segmentaciju.

## Metodologija

Projekat koristi kombinaciju analitičkih i Data Mining tehnika:

### 1. Eksplorativna analiza podataka (EDA)

Izvršena je analiza osnovnih karakteristika podataka, distribucija i međusobnih odnosa atributa.

### 2. RFM analiza

Kupci su evaluirani na osnovu tri pokazatelja:

- Recency (vrijeme od posljednje kupovine),
- Frequency (učestalost kupovine),
- Monetary (ukupna vrijednost kupovina).

Na osnovu ovih pokazatelja formirani su različiti segmenti kupaca.

### 3. K-Means klasterovanje

Za segmentaciju kupaca korišćen je K-Means algoritam.

Postupak uključuje:

- standardizaciju podataka,
- određivanje optimalnog broja klastera,
- formiranje segmenata kupaca,
- analizu karakteristika svakog segmenta.

### 4. Cohort analiza

Cohort analiza omogućava praćenje zadržavanja kupaca tokom vremena i procjenu njihove lojalnosti.

## Rezultati

Aplikacija omogućava:

- identifikaciju najvrijednijih kupaca,
- identifikaciju kupaca sa rizikom od odlaska,
- grupisanje kupaca prema ponašanju,
- analizu zadržavanja korisnika,
- donošenje informisanih marketinških odluka.

## Korisnički interfejs

Aplikacija sadrži više interaktivnih stranica za:

- pregled podataka,
- RFM analizu,
- K-Means segmentaciju,
- cohort analizu,
- prikaz grafikona i izvještaja.


## Buduća unapređenja

- Dodavanje novih algoritama segmentacije.
- Predikcija budućeg ponašanja kupaca.
- Integracija sa bazama podataka.
- Automatsko generisanje izvještaja.
- Personalizovane marketinške preporuke.
