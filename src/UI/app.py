
from flask import Flask,render_template,request
import sparql_queries
import pandas as pd
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('test.html')

@app.route('/doc_filter',methods=['POST','GET'])
def  get_health_specialty():
    specialty = request.form['text']
    score = request.form["Dropdown1"]
    print(score)
    if score =='1+':
        score = '1.0'
    elif score =='2+':
        score ='2.0'
    elif score =='3+' :
        score = '3.0'
    elif score == '4+':
        score =='4.0'

    result = sparql_queries.get_specialty_details(specialty,score)
    doc_name = []
    doc_address = []
    doc_telephone = []
    doc_age = []
    doc_gender = []
    doc_score = []

    result = result["results"]["bindings"]
    for res in result:

        if 'doc_name' in res:
            doc_name.append(res['doc_name']['value'].title())
        else:
            doc_name.append('Not Available')

        if 'doc_telephone' in res:
            doc_telephone.append(res['doc_telephone']['value'])
        else:
            doc_telephone.append('Not Available')
        if 'doc_address' in res:
            doc_address.append(res['doc_address']['value'].title())
        else:
            doc_address.append('Not Available')
        if 'doc_age' in res:
            doc_age.append(res['doc_age']['value'])
        else:
            doc_age.append('Not Available')
        if 'doc_gender' in res:
            doc_gender.append(res['doc_gender']['value'].title())
        else:
            doc_gender.append('Not Available')
        if 'doc_score' in res:
            doc_score.append(res['doc_score']['value'].title())
        else:
            doc_score.append('Not Available')
    doctor_df = pd.DataFrame({'Doctor Name':doc_name,'Doctor Age':doc_age,'Doctor Gender':doc_gender,
                              'Doctor Address':doc_address, 'Doctor Telephone': doc_telephone, 'Doctor Score':doc_score
                              })
    return render_template('specialty.html',tables=[doctor_df.to_html(classes='data',header="true",index=False)])


@app.route('/drug_filter',methods=['POST','GET'])
def get_medicine_details():
    drug = request.form['text']
    result = sparql_queries.get_medicine_details(drug)

    return render_template('drugs.html',result=result)
@app.route('/uses_filter',methods=['POST','GET'])
def get_medicine_from_uses():
    uses = request.form['text']
    uses = uses.split(',')

    result = list(sparql_queries.get_medicine_from_uses(uses))
    if len(result) > 25:
        result=result[:25]

    return render_template('uses.html',result=result)

@app.route('/disease_filter',methods=['POST','GET'])
def get_disease_details():
    disease = request.form['text']
    result = sparql_queries.get_disease_details(disease)
    return render_template('disease.html',result=result)
@app.route('/symptom_filter',methods=['POST','GET'])
def get_symptom_filter():
    symptom = request.form['text']
    symptom = symptom.split(',')
    result = list(sparql_queries.get_disease_from_symptoms(symptom))
    if len(result) > 25:
        result = result[:25]

    return render_template('symptoms.html', result=result)


@app.route('/cause_filter', methods=['POST', 'GET'])
def get_cause_filter():
    cause = request.form['text']
    cause = cause.split(',')
    result = list(sparql_queries.get_disease_from_cause(cause))
    if len(result) > 25:
        result = result[:25]

    return render_template('cause.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, port=8080)
