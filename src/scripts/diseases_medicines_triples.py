from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS
import json
def generate_triples():
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    MYNS = Namespace('http://inf558.org/medgraph#')
    SCHEMA = Namespace('http://schema.org/')

    my_kg = Graph()
    my_kg.bind('myns', MYNS)
    my_kg.bind('myns', MYNS)
    my_kg.bind('foaf', FOAF)
    my_kg.bind('schema', SCHEMA)
    disease = URIRef(MYNS['Disease'])

    my_kg.add((disease, RDF.type, SCHEMA['Class']))
    my_kg.add((disease, RDFS.subClassOf, SCHEMA['MedicalCondition']))
    # name
    my_kg.add((disease, SCHEMA['name'], XSD.text))
    # description
    my_kg.add((disease, SCHEMA['description'], XSD.text))

    # speciality
    my_kg.add((disease, SCHEMA['relevantSpecialty'], SCHEMA['MedicalSpecialty']))
    # drug
    drug_uri =URIRef(MYNS['Drugs'])
    my_kg.add((drug_uri, RDF.type, SCHEMA['Class']))
    my_kg.add((drug_uri, RDFS.subClassOf, SCHEMA['Drug']))
    my_kg.add((drug_uri,SCHEMA['name'],XSD.text))
    my_kg.add((drug_uri, SCHEMA['nonProprietaryName'], XSD.text))
    my_kg.add((drug_uri, SCHEMA['administrationRoute'], XSD.text))
    #uses
    uses_uri = URIRef(MYNS['Uses'])
    my_kg.add((uses_uri, RDF.type, SCHEMA['property']))
    my_kg.add((uses_uri, RDFS.domain, drug_uri))
    my_kg.add((uses_uri, RDFS.range, XSD.text))
    # side_effect
    side_effect_uri = URIRef(MYNS['side_effect'])
    my_kg.add((side_effect_uri, RDF.type, SCHEMA['property']))
    my_kg.add((side_effect_uri, RDFS.domain, side_effect_uri))
    my_kg.add((side_effect_uri, RDFS.range, XSD.text))

    # cause
    cause_uri = URIRef(MYNS['cause'])
    my_kg.add((cause_uri, RDF.type, SCHEMA['property']))
    my_kg.add((cause_uri, RDFS.domain, disease))
    my_kg.add((cause_uri, RDFS.range, XSD.text))

    my_kg.add((disease,SCHEMA['drug'],drug_uri))
    # SYMPTOM
    medicine_details_dict = {}
    my_kg.add((disease, SCHEMA['signOrSymptom'], SCHEMA['MedicalSignOrSymptom']))
    with open('MedicineLinkageDATA.jl','r') as f:
        for line in f:
            details = json.loads(line)
            medicine_details_dict[details['GenericName']] = details



    with open('wikidata_test.jl','r') as f:
        for line in f:
            obj = json.loads(line)
            unique_id = obj["DiseaseURI"].split('/')[-1]
            target_uri = URIRef(MYNS[unique_id])
            my_kg.add((target_uri,RDF.type,MYNS['disease']))
            my_kg.add((target_uri,SCHEMA['name'],Literal(obj['Disease'])))
            if len(obj['Info']) >0:
                my_kg.add((target_uri,SCHEMA['description'],Literal(obj['Info'])))
            if len(obj['HealthSpecialty']) >0:
                for speciality in obj['HealthSpecialty']:
                    my_kg.add((target_uri,SCHEMA['relevantSpecialty'],Literal(speciality)))
            if  len(obj['TreatmentDrugs'])>0:
               for name in obj['TreatmentDrugs']:
                   if name in medicine_details_dict:
                       value = medicine_details_dict[name]
                       drugs_identifier = value['MedicineURI'].split('/')[-1]
                       drugs_node = URIRef(MYNS[drugs_identifier])
                       my_kg.add((target_uri,SCHEMA['drug'],drugs_node))
                       my_kg.add((drugs_node,RDF.type,drug_uri))
                       my_kg.add((drugs_node,SCHEMA['name'],Literal(value['BrandName'])))
                       my_kg.add((drugs_node, SCHEMA['nonProprietaryName'],Literal(value['GenericName'])))

                       if 'DrugAdministration' in value and len(value['DrugAdministration']) > 0:
                        my_kg.add((drugs_node, SCHEMA['administrationRoute'],Literal(value['DrugAdministration'])))

                       if 'Uses' in value and len(value['Uses']) > 0:
                          local_use = URIRef(MYNS['Uses'])
                          for use in value['Uses']:
                              my_kg.add((drugs_node,local_use,Literal(use)))
                       if 'SideEffects' in value and len(value['SideEffects']) > 0:
                           local_side_effect = URIRef(MYNS['side_effect'])
                           for effect in value['SideEffects']:
                               my_kg.add((drugs_node, local_side_effect, Literal(effect)))

            if len(obj['Cause'])>0:
                local_cause = URIRef(MYNS['Cause'])
                for cause in obj['Cause']:
                    my_kg.add((target_uri,local_cause,Literal(cause)))
            if len(obj['Symptons'])>0:
                for symptom in obj['Symptons']:
                    my_kg.add((target_uri, SCHEMA['signOrSymptom'], Literal(symptom)))



    my_kg.serialize('disease_schema_test.ttl', format='turtle')

if __name__ == '__main__':
    generate_triples()








