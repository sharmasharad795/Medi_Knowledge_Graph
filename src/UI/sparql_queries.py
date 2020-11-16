##medicine
from SPARQLWrapper import SPARQLWrapper, JSON
import re

sparql = SPARQLWrapper("http://localhost:3030/ds")

def get_medicine_details(med_name):
    sparql.setQuery("""
    PREFIX schema: <http://schema.org/>
    PREFIX myns: <http://inf558.org/medgraph#>
    select  ?gen_name ?brand_name ?uses ?side_eff ?admin
    where
    {
    ?x a myns:Drugs;
       schema:nonProprietaryName ?gen_name;
    OPTIONAL{?x schema:name ?brand_name}.
    OPTIONAL{?x  myns:Uses ?uses}.
    OPTIONAL{?x  myns:side_effect ?side_eff}.
    OPTIONAL{?x schema:administrationRoute ?admin}.
    FILTER regex(?gen_name,LCASE(""" + '"' + med_name + '"' + """)).
    }""")

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    gen_name = set()
    brand_name = set()
    uses = set()
    side_effect = set()
    admin_route = set()
    final_res = {}

    result = results["results"]["bindings"]
    for res in result:

        if 'gen_name' in res:
            gen_name.add(res['gen_name']['value'].title())
        if 'brand_name' in res:
            brand_name.add(res['brand_name']['value'].title())
        if 'uses' in res:
            uses.add(res['uses']['value'].title())
        if 'side_eff' in res:
            temp = re.sub(r'\([^)]*\)', ' ', res['side_eff']['value'].title())
            temp = temp.strip(',')
            temp = temp.strip('"')
            if temp =='Treatment':
                continue
            if temp == "Breath" or temp=="Shortness":
                side_effect.add('Shortness of Breath')
                continue
            side_effect.add(temp)
        if 'admin' in res:
            admin_route.add(res['admin']['value'].title())

    if len(gen_name) > 0:
        final_res['gen_name'] = gen_name

    if len(brand_name) > 0:
        final_res['brand_name'] = brand_name

    if len(uses) > 0:
        if len(uses) > 15:
            uses = list(uses)[:15]
        final_res['uses'] = uses

    if len(side_effect) > 0:
        if len(side_effect) > 15:
            side_effect = list(side_effect)[:15]
        final_res['side_effect'] = side_effect
    if len(admin_route) > 0:
        final_res['admin_route'] = admin_route

    return final_res


def get_disease_details(dis_name):
    sparql.setQuery("""
    PREFIX schema: <http://schema.org/>
    PREFIX myns: <http://inf558.org/medgraph#>

    select ?disease_name ?info ?cause ?symptom ?med_name ?specialty_name
    where
    {
    ?x a myns:disease;
       schema:name ?disease_name.

    OPTIONAL{?x  myns:Cause ?cause}.
    OPTIONAL{?x  schema:signOrSymptom ?symptom}.
    OPTIONAL {?x schema:description ?info}.
    OPTIONAL
        {
     ?x  schema:drug ?drug_uri.
    ?drug_uri  schema:nonProprietaryName ?med_name. }
    OPTIONAL
        {
     ?x  schema:relevantSpeciality ?sp_uri.
    ?sp_uri  schema:name ?specialty_name. }

    FILTER (LCASE(?disease_name)=LCASE(""" + '"' + dis_name + '"' + """) ) 
     }
    """)
    disease_name = set()
    info = set()
    cause = set()
    symptom = set()
    med_name = set()
    specialty_name = set()

    final_res = {}
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    result = results["results"]["bindings"]
    for res in result:

        if 'disease_name' in res:
            disease_name.add(res['disease_name']['value'].title())
        if 'info' in res:
            info.add(res['info']['value'])
        if 'cause' in res:
            cause.add(res['cause']['value'].title())
        if 'symptom' in res:
            symptom.add(res['symptom']['value'].title())
        if 'med_name' in res:
            med_name.add(res['med_name']['value'].title())
        if 'specialty_name' in res:
            specialty_name.add(res['specialty_name']['value'].title())

    if len(disease_name) > 0:
        final_res['disease_name'] = disease_name

    if len(info) > 0:
        final_res['info'] = info

    if len(cause) > 0:
        final_res['cause'] = cause

    if len(symptom) > 0:
        if len(symptom) > 15:
            symptom = list(symptom)[:15]
        final_res['symptom'] = symptom
    if len(med_name) > 0:
        if len(med_name) > 15:
            med_name = list(med_name)[:15]
        final_res['med_name'] = med_name
    if len(specialty_name) > 0:
        final_res['specialty_name'] = specialty_name

    return final_res




def get_disease_from_symptoms(symptoms):
    main_set = set()
    cnt = 0
    for symptom in symptoms:
        sparql.setQuery("""
        PREFIX schema: <http://schema.org/>
        PREFIX myns: <http://inf558.org/medgraph#>

        SELECT ?disease_name?symptom
        WHERE {
          ?x a myns:disease;
             schema:name ?disease_name.
          {?x schema:signOrSymptom ?symptom.}
          FILTER (LCASE(?symptom)=LCASE(""" + '"' + symptom + '"' + """))
        }  

        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        temp_set = set()
        for result in results['results']['bindings']:
            temp_set.add(result['disease_name']['value'].strip())
        if cnt == 0:
            main_set = (temp_set)
        else:
            main_set = main_set.intersection(temp_set)
        cnt += 1

    return main_set


def get_disease_from_cause(causes):
    main_set = set()
    cnt = 0
    for cause in causes:
        sparql.setQuery("""
        PREFIX schema: <http://schema.org/>
        PREFIX myns: <http://inf558.org/medgraph#>

        SELECT ?disease_name
        WHERE {
          ?x a myns:disease;
             schema:name ?disease_name.
          {?x myns:Cause ?cause.}
          FILTER (LCASE(?cause)=LCASE("""+'"'+ cause+'"'+"""))
        }  

        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        temp_set = set()
        for result in results['results']['bindings']:
            temp_set.add(result['disease_name']['value'])
        if cnt == 0:
            main_set = (temp_set)
        else:
            main_set = main_set.intersection(temp_set)
        cnt += 1

    return main_set


def get_medicine_from_uses(uses):
    main_set = set()
    cnt = 0
    for use in uses:
        sparql.setQuery("""
        PREFIX schema: <http://schema.org/>
        PREFIX myns: <http://inf558.org/medgraph#>

        SELECT ?drugs_name
        WHERE {
          ?x a myns:Drugs;
              schema:nonProprietaryName ?drugs_name.

          {?x myns:Uses ?use.}
          FILTER (LCASE(?use)=LCASE(""" + '"' + use + '"' + """))
        }  

        """)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        temp_set = set()
        for result in results['results']['bindings']:
            temp_set.add(result['drugs_name']['value'])
        if cnt == 0:
            main_set = (temp_set)
        else:
            main_set = main_set.intersection(temp_set)
        cnt += 1

    return main_set

def get_specialty_details(specialty_name,scorer):

    sparql.setQuery("""
    PREFIX schema: <http://schema.org/>
    PREFIX myns: <http://inf558.org/medgraph#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    select  ?specialty_name ?doc_name ?doc_age ?doc_gender ?doc_address ?doc_telephone ?doc_score
    where
    {
    ?x a myns:Specialty;
        schema:name ?specialty_name;
    OPTIONAL{
    ?x myns:doctors ?doctor_uri.
    OPTIONAL{
    ?doctor_uri schema:name ?doc_name.
    ?doctor_uri  schema:address ?doc_address.
    ?doctor_uri  schema:telephone ?doc_telephone.
    ?doctor_uri  myns:score ?doc_score.
    ?doctor_uri  myns:age ?doc_age.
    ?doctor_uri   schema:gender ?doc_gender.}}
    FILTER (str(?doc_score) != "Not rated yet").
    FILTER (str(?doc_score) >= """ + '"' + scorer + '"' + """).
    FILTER (LCASE(?specialty_name)=LCASE(""" + '"' + specialty_name + '"' + """))
     }
    ORDER BY DESC(?doc_score)
    """)


    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results