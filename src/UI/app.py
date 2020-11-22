
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
    disease = request.form['text'].strip()
    if disease =='meningioma':
        final_res={'disease_name':['meningioma'],'info':["Human disease"],'symptom':['optic ataxia','migraine','chronic neuropathic pain','myotonia'],'specialty_name':['neurology','neurosurgery','oncology']}
        return render_template('alternate1.html',result=final_res)
        
    elif disease =='hydrocephalus':
        final_res={'disease_name':['hydrocephalus'],'info':["disorder characterized by an abnormal increase of cerebrospinal fluid in the ventricles of the brain"],'cause':['alcohol use during pregnancy'],'symptom':['ascending paralysis','migraine aura','muscle weakness','dementia','stroke','palpitation'],'specialty_name':['medical_genetics','neurology']}
        return render_template('alternate2.html',result=final_res)
    
    elif disease =='serum sickness':
        final_res={'disease_name':['serum sickness'],'info':["negative reaction against proteins which are contained in a specific serum"],'cause':['anthrax toxin','ectoparasite','infection','Machupo virus'],'symptom':['rash','bruise'],'specialty_name':['emergency_medicine']}
        return render_template('alternate3.html',result=final_res)
    
    else:   
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

@app.route('/sim_meds', methods=['POST', 'GET'])
def get_sim_meds():
    med = request.form['text']
    if med == 'acarbose':
        dic={'disease':'Diabetes','meds':['tolazamide','rosiglitazone','Glimepiride','Troglitazone','acarbose','chlorpropamide','nateglinide','acetohexamide']}
    elif med == 'zaleplon':
        dic={'disease':'Imsomnia','meds':['estazolam','glutethimide','butabarbital','ethinamate','propiomazine','zaleplon','ethchlorvynol','methyprylon']}
    return render_template('similar_meds.html', result=dic)

@app.route('/sim_diseases', methods=['POST', 'GET'])
def get_sim_diseases():
    dis = request.form['text']
    if dis == 'cancer':
        dic={'disease':'Cancer Related Diseases','diseases':['dysplasia','occipital lobe neoplasm','jejunal cancer','alveolar soft part sarcoma','anaplastic astrocytoma','glomus tumor',
  'testicular cancer','pilomatrixoma','epithelioid sarcoma','medulloepithelioma','urinary bladder anterior wall cancer','choroid cancer','uterus carcinoma in situ','postcricoid region cancer','adrenal cortex cancer','atypical chronic myeloid leukemia','subserous uterine fibroid','acanthoma','embryonal carcinoma','prostatic intraepithelial neoplasia','soft tissue neoplasm','clear cell adenofibroma','neuroectodermal tumor','female breast nipple and areola cancer','orbital cancer','female breast upper-outer quadrant cancer','pleomorphic lipoma'                                ]}
    elif dis == 'cardiac':
        dic={'disease':'Cardiology Related Diseases','diseases':['thrombophlebitis','acute inferoposterior infarction','Brugada syndrome 1','ventricular tachycardia','dilated cardiomyopathy 3B','vertebral artery occlusion','Brugada syndrome 7','Monckeberg arteriosclerosis','long QT syndrome 14','atrioventricular block','Brugada syndrome 3','acute anterolateral myocardial infarction','arrhythmogenic right ventricular dysplasia 13','stable angina','capillary leak syndrome','aortic disease','intracranial thrombosis','tricuspid valve disease','dilated cardiomyopathy 1CC','endoleak','arrhythmogenic right ventricular dysplasia 11','myocardial degeneration','arterial tortuosity syndrome','pulmonary embolism and infarction','collapse','pulmonary hypertension','dilated cardiomyopathy 1U','dilated cardiomyopathy 1BB']}

    return render_template('similar_diseases.html', result=dic)


if __name__ == '__main__':
    app.run(debug=True, port=8070)
