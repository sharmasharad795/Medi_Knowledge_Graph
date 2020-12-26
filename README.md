# Medi_Knowledge_Graph
Knowledge Graph for Medicines and Diseases

# The knowlede graph that we built looks as follows:
![Alt Text](https://github.com/pratheekbalaji/Medi_Knowledge_Graph/blob/main/example.jpg?raw=true)

The different steps involved in building our knowledge graph is as described below:

# 1. Crawling/ Data Acquistion

We Crawled and extracted from a combination of structured unstructured and semi-structured sources which are listed below:

1. Disease information was obtained from Wikidata.org such as disease name, descriptions,symptoms,medicines used for treatment,etc
2. Details related to meidicines was crawled from webmd.com such as it's generic name, brand name, side effects, mode of administration.
3. Lastly, we crawled information pertaining to doctors specializing in treating a disease of certain kind from healthgrades.com such as doctor's name, age, gender,

# 2. Information Extraction

Since we dealt with unstructured and semi-structured data we had to design extractors(sybtactial) using tools like spacy to obtain relevant 

