from rdflib import Graph, URIRef, Literal, XSD, Namespace, RDF, RDFS
import json
def get_hash(value):
    return hash(value)
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
    specialty_uri = URIRef(MYNS['Specialty'])
    my_kg.add((disease, SCHEMA['relevantSpecialty'], specialty_uri))
    my_kg.add((specialty_uri,RDF.type,SCHEMA['class']))
    my_kg.add((specialty_uri,RDFS.subClassOf,SCHEMA['MedicalSpecialty']))
    # doctors
    doctors_uri = URIRef(MYNS['doctors'])
    my_kg.add((specialty_uri,doctors_uri,XSD.text))
    my_kg.add((doctors_uri,RDF.type,SCHEMA['class']))
    my_kg.add((doctors_uri,RDFS.subClassOf,SCHEMA['Person']))
    my_kg.add((doctors_uri,SCHEMA['name'],XSD.text))
    my_kg.add((doctors_uri,SCHEMA['gender'],XSD.text))
    age_uri = URIRef(MYNS['age'])
    my_kg.add((doctors_uri,age_uri,XSD.text))
    my_kg.add((age_uri,RDF.type,SCHEMA['property']))
    my_kg.add((age_uri,RDFS.domain,doctors_uri))
    my_kg.add((age_uri,RDFS.range,XSD.int))
    my_kg.add((doctors_uri,SCHEMA['address'],XSD.text))
    my_kg.add((doctors_uri,SCHEMA['telephone'],XSD.text))
    score_uri = URIRef(MYNS['score'])
    my_kg.add((doctors_uri,score_uri,XSD.float))
    my_kg.add((score_uri, RDFS.domain, doctors_uri))
    my_kg.add((score_uri, RDFS.range, XSD.float))



    # drug
    drug_uri =URIRef(MYNS['Drugs'])
    my_kg.add((drug_uri, RDF.type, SCHEMA['Class']))
    my_kg.add((drug_uri, RDFS.subClassOf, SCHEMA['Drug']))
    my_kg.add((drug_uri,SCHEMA['name'],XSD.text))
    my_kg.add((drug_uri, SCHEMA['nonProprietaryName'], XSD.text))
    my_kg.add((drug_uri, SCHEMA['administrationRoute'], XSD.text))
    #uses
    uses_uri = URIRef(MYNS['Uses'])
    my_kg.add((drug_uri,uses_uri,XSD.text))
    my_kg.add((uses_uri, RDF.type, SCHEMA['property']))
    my_kg.add((uses_uri, RDFS.domain, drug_uri))
    my_kg.add((uses_uri, RDFS.range, XSD.text))
    # side_effect
    side_effect_uri = URIRef(MYNS['side_effect'])
    my_kg.add((drug_uri,side_effect_uri,XSD.text))
    my_kg.add((side_effect_uri, RDF.type, SCHEMA['property']))
    my_kg.add((side_effect_uri, RDFS.domain, side_effect_uri))
    my_kg.add((side_effect_uri, RDFS.range, XSD.text))
    my_kg.add((disease, SCHEMA['drug'], drug_uri))
    # cause
    cause_uri = URIRef(MYNS['cause'])
    my_kg.add((cause_uri, RDF.type, SCHEMA['property']))
    my_kg.add((cause_uri, RDFS.domain, disease))
    my_kg.add((cause_uri, RDFS.range, XSD.text))
    my_kg.add((disease,cause_uri,XSD.text))


    # SYMPTOM
    medicine_details_dict = {}

    my_kg.add((disease, SCHEMA['signOrSymptom'], SCHEMA['MedicalSignOrSymptom']))
    with open('/Users/pratheek/Documents/Medi_Knowledge_Graph/OutputFiles/MedicineLinkageData.jl','r') as f: # path of jl file containing details about medicines
        for line in f:
            details = json.loads(line)
            medicine_details_dict[details['GenericName']] = details
    with open('/Users/pratheek/Documents/Medi_Knowledge_Graph/OutputFiles/HealthSpecialityLinkage.json', 'r') as f:
        speciality_details_dict = json.load(f)

    doctor_details_dict = {}
    with open('/Users/pratheek/Documents/Medi_Knowledge_Graph/OutputFiles/DoctorData.jl','r') as f:
        for line in f:
            obj = json.loads(line)
            doctor_details_dict[obj['DoctorURI']] = obj
    #print(doctor_details_dict)



    with open('/Users/pratheek/Documents/Medi_Knowledge_Graph/OutputFiles/WikiDiseaseData.jl','r') as f:
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
                    temp = speciality.split()
                    temp = '_'.join(temp)

                    speciality_node = URIRef(MYNS[temp])
                    my_kg.add((target_uri,SCHEMA['relevantSpeciality'],speciality_node))
                    my_kg.add((speciality_node,RDF.type,specialty_uri))
                    my_kg.add((speciality_node,SCHEMA['name'],Literal(speciality)))
                    if speciality in speciality_details_dict:
                        doctors = speciality_details_dict[speciality]
                        for doc in doctors:
                            object = doctor_details_dict[doc]
                            doc_identifier = doc.split('/')[-1]
                            doc_node = URIRef(MYNS[doc_identifier])
                            my_kg.add((speciality_node,doctors_uri,doc_node))
                            my_kg.add((doc_node,RDF.type,doctors_uri))
                            my_kg.add((doc_node,SCHEMA['name'],Literal(object['Doctor_Name'])))
                            if len(object['Doctor_Age']) > 0:
                                my_kg.add((doc_node,age_uri,Literal(object['Doctor_Age'])))
                            if len(object['Doctor_Gender']) > 0:
                                my_kg.add((doc_node,SCHEMA['gender'],Literal(object['Doctor_Gender'])))
                            if len(object['Doctor_Address']) > 0:
                                my_kg.add((doc_node, SCHEMA['address'], Literal(object['Doctor_Address'])))
                            if object['Doctor_PhoneNo'] is not None and len(object['Doctor_PhoneNo']) > 0:
                                my_kg.add((doc_node, SCHEMA['telephone'], Literal(object['Doctor_PhoneNo'])))
                            if len(object['Doctor_Score']) > 0:

                                my_kg.add((doc_node,score_uri, Literal(object['Doctor_Score'])))



                    #my_kg.add((target_uri,SCHEMA['relevantSpecialty'],Literal(speciality)))
            if  len(obj['TreatmentDrugs'])>0:
               for name in obj['TreatmentDrugs']:
                   if name in medicine_details_dict:
                       value = medicine_details_dict[name]
                       drugs_identifier = value['MedicineURI'].split('/')[-1]
                       drugs_node = URIRef(MYNS[drugs_identifier])
                       my_kg.add((target_uri,SCHEMA['drug'],drugs_node))
                       my_kg.add((drugs_node,RDF.type,drug_uri))
                       if 'BrandName' in value and len(value['BrandName']) > 0:
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



    my_kg.serialize('/Users/pratheek/Documents/Medi_Knowledge_Graph/OutputFiles/Medigraph_triples.ttl', format='turtle')

if __name__ == '__main__':
    generate_triples()








