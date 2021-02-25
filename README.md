# Medi_Knowledge_Graph

Contributors : Pratheek Balaji, Sharad Narayan Sharma

Knowledge Graph which serves as a one stop shop containing information pertaining to diseases, medicines and health specialists (doctors) related to the specific disease in a given area.

# The knowledge graph that we built looks as follows:
![Alt Text](https://github.com/pratheekbalaji/Medi_Knowledge_Graph/blob/main/example.jpg?raw=true)

The different steps involved in building our knowledge graph is as described below:

# 1. Crawling/ Data Acquistion

We Crawled and extracted from a combination of structured unstructured and semi-structured sources which are listed below:

1. Disease information was obtained from Wikidata.org such as disease name, descriptions,symptoms,medicines used for treatment,etc
2. Details related to meidicines was crawled from webmd.com such as it's generic name, brand name, side effects, mode of administration.
3. Lastly, we crawled information pertaining to doctors specializing in treating a disease of certain kind from healthgrades.com such as doctor's name, age, gender,

# 2. Information Extraction

From webmd we had to extract specific information pertaining to side effects and uses of medicines from long paragraphs of text. For this purpose we carefully defined syntactical extractors using spaCy taking into account POS tags. Additionally, we had to remove certain stop words and commonly found phrases found in the website for our extractor to be more effective . To evaluate the performance of extractor we created a ground truth development set for uses and side effects and evaluated the recall of our extractor. The result are as follows:

For Side Effects : Recall = 0.84
For Uses : Recall = 0.76

# 3. Entity Linking

We performed entity linking for the below entities:

1. Medicines : WikiData stores the generic name of medicines, which are not the exact names under which a medicine is sold in a pharmacy. WedMD on the other hand has medicines with their generic and brand/store name. This gave rise to the challenge of mapping generic names from WikiData to either the brand or generic name in WedMD. For this, we split the names in WedMD into separate individual strings, and carried out exact matching with the generic name in WikiData. To reduce
the number of comparisons, we employed tri-gram blocking. The results were evaluated using a development set of 50 medicines

2) Health Specialty: Each disease in WikiData could have one or multiple health specialties. These health specialties had to be mapped to the different health specialists or doctors on HealthGrades. One of the challenges here was that the names of these health specialties were different for both the data sources. For example, Hematology in WikiData should be mapped to Hematology as well as Pediatric Hematology & Oncology in HealthGrades. For this, we first filtered out the stop words such as care, disease, medicine, which would lead to many false matches. Then, we divided each specialty in both WikiData and healthgrades into separate strings, and carried out Levenshtein based matching between each of these strings. To reduce the number of comparisons, we employed fivegram blocking. The doctors were subsequently mapped to the matching similarities. The results were evaluated using a development set of 40 specialties.

# 4. Ontology

It was difficult to construct a schema from scratch which could link different data sources effectively. Hence, we leveraged from the existing ontologies
of XSD, RDF, RDFS, SCHEMA, as well as defined some of our own classes and properties. The custom classes were Diseases, Drugs, Health Specialty and
Doctors. Additionally, we borrowed from Schema.org to build some of the properties for the above defined classes. For example, description of Diseases,administrationRoute of Drugs, etc. The custom defined properties include cause of Diseases, age of Doctors, etc. All our custom ontologies were defined using the ontology of MY_NS.

# 5. Graph Embeddings

We noticed that in spite of linking data from various sources, a few diseases lacked their respective causes or symptoms in our knowledge graph. We
employed link prediction using AmpliGraph’s Complex Embeddings model (ComplEx) to predict the missing linksbetween diseases and their symptoms. This
approach did give us some false positives as well. To reduce this, we set a high threshold of 0.95 or above on the probability score. We also tried to implement link prediction between medicines and their missing side effects, but the results for that were not encouraging enough to be incorporated.Furthermore, we used DBSCAN clustering to identify similar medicines and diseases in our knowledge graph. To generate clusters for diseases, we used causes andsymptoms, whereas the clusters for medicines made use of uses and side effects. We got 47 clusters of similar diseases and 4 clusters of similar medicines


The link to our video demonstration : https://www.youtube.com/watch?v=3ClLxR7qtLM


