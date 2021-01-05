import spacy
import csv
import nltk
from nltk.corpus import stopwords
import json
import re
import sys

nlp = spacy.load('en_core_web_md')

def extract_side_effects(excerpt):


    stop = stopwords.words('english')
    stop_words = ['a', 'trouble', 'warning', 'something', 'of', 'your', 'this', 'the', 'pharmacist', 'physician',
                  'doctor', 'side effects', 'see usage', 'effects', 'medical', 'advice', 'stomach', 'smell', 'taste',
                  'you','he','she','an','most','use','section','1','2','3','4','5','6','7','8','9','use','section',"people",'one',
                  'week','symptoms','recommended','vitamin','about','lack','energy','no','report','sections']

    stop_words.extend(stop_words)
    stop_words = set(stop_words)
    regex1 = r"\w*\s+of\s+\w*"
    regex2 = r'\w+\s+in\s*\w+\s*\w+\s+\w+\s+\w+'
    regex = [regex1, regex2]

    doc = nlp(excerpt)
    sent = list(doc.sents)
    side_effects = set()
    new_doc = nlp(str(sent[0:2]))
    for chunk in new_doc.noun_chunks:
        flag = True
        tokens = str(chunk).split()
        for tok in tokens:

            if str(tok.lower()) in stop_words:
                flag = False
                break
        if flag:
            side_effects.add(str(chunk).lower().strip())

        for r in regex:
            match = re.findall(r, str(new_doc))

            if match:

                temp = match[0].split()
                for t in temp:
                    if t in side_effects:
                        side_effects.remove(t)

                        break

    return list(side_effects)

def med_usage(doc):
    side_list=['medication','combination','symptoms','e','variety','children','weeks','protection','types','organisms','adults','kids','drugs','medications','diease','diseases','uses','people','levels','illness','illnesses','insects','type','virus','yeast','bacteria','eyes','eye','men','substance','treatment','kinds','urge','patients','patient']
    sym_set=set()
    for token in doc:
        if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and (token.text.lower() not in side_list) :
            if token.dep_=='compound' and token.head.pos_ == 'NOUN':
                sym_set.add(token.text+' '+token.head.text)
            elif token.dep_ in ['dobj','conj','pobj']:
                child_flag=False
                for child in token.children:
                    if child.dep_=='compound':
                        child_flag=True
                if not child_flag:
                    sym_set.add(token.text)

    sym_set=list(sym_set)
    return sym_set



def main_func(path):
    mode_dic = {'topical': 'Used as Cream', 'articular': 'Via Injection to Joints', 'buccal': 'Via the mouth',
                'cap': 'Apply lotion/shampoo on scalp',
                'cleanser': 'Via the mouth', 'dental': 'Apply to tooth/tooth pocket', 'drops': 'Via drops',
                'ear': 'Apply to ear',
                'epidural': 'Via Injection to Spine', 'eye': 'Apply to eye via drops',
                'eyelashes': 'Apply to eye via drops', 'gel': 'Apply to mouth',
                'implant': 'Surgically placed by doctors', 'inhalation': 'Via Inhaler', 'injection': 'Via Injection',
                'intracameral': 'Via injection into the eye cavity', 'intracavernosal': 'Via Injection to the penis',
                'intramuscular': 'Via injection into the muscles', 'intrathecal': 'Via Injection in the spinal canal',
                'intratympanic': 'Via Injection(Ear)', 'intrauterine': 'Via a Device placed in the Uterus',
                'intravenous': 'Via Injection into the Veins',
                'intravesical': 'Given into the bladder through a tube', 'intravitreal': 'Via Injection into the eye',
                'liquids': 'Oral Liquids',
                'membrane': 'Via the mouth', 'nasal': 'Via Nasal Spray/Liquid', 'oil': 'Apply oil to affected areas',
                'ophthalmic': 'Eye medicine', 'oral': 'Administered via the mouth', 'otic': 'Apply to ear',
                'pen': 'Via Injection', 'pf': 'Apply drops',
                'rectal': 'Apply to rectum area', 'scalp': 'Apply to head', 'subcutaneous': 'Via Injection to the Skin',
                'subdermal': 'Insert under the skin', 'sublingual': 'Applied under the tongue',
                'subretinal': 'Via Injection into the eye',
                'suspension': 'Apply as eye drops', 'topical': 'Apply as ointment to affected areas/skin',
                'transdermal': 'Apply as ointment/patch on skin',
                'urethral': 'Apply into the penis', 'vaginal': 'Apply to vagina', 'xenaflamm': 'Via the mouth'}


    fh = open('medicine_details.jl', 'a+')
    file = csv.reader(open(path), delimiter='\t')

    for (a, (url,name,generic_name,side_effect,usage)) in enumerate(file):

        medicine_final_list = []
        mode = ''
        if usage != '':
            use = usage.split()[0].lower()
            if use != 'consult':
                usage = usage.partition('.')[0]
                usage = nlp(usage)
                medicine_final_list = med_usage(usage)

        r = url.split('/')[-2]
        r = r.split('-')[-1]
        if r in mode_dic:
            mode = mode_dic[r]

        side_effects = extract_side_effects(side_effect)
        d = {"url": url,"Brand_Name":name,"Generic_Name":generic_name,"Uses":medicine_final_list,"Drug Administration":mode,"Side_Effects": side_effects}
        json.dump(d, fh)
        fh.write('\n')

if __name__ == "__main__":
    file_name = sys.argv[1]
    main_func(file_name)