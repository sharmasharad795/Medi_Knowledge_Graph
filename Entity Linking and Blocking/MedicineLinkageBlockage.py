from pathlib import Path
from typing import *
from re import sub as re_sub
import sys
import json
import rltk
from collections import defaultdict

global g_tokenizer
g_tokenizer = rltk.CrfTokenizer()

class WikiRecord(rltk.Record):
    ''' Record entry class for each of our IMDB records '''
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['MedicineURI']

    @rltk.cached_property
    def name_string(self):
        return self.raw_object['Medicine'].lower()

class WebMDRecord(rltk.Record):
    ''' Record entry class for each of our AFI records '''
    def __init__(self, raw_object):
        super().__init__(raw_object)
        self.name = ''

    @rltk.cached_property
    def id(self):
        return self.raw_object['url']

    @rltk.cached_property
    def genname_string(self):
        return self.raw_object['Generic_Name']

    @rltk.cached_property
    def brandname_string(self):
        return self.raw_object['Brand_Name'].lower()

def n_gram(s, n=3):
    return [s[i:i + n] for i in range(len(s) - (n - 1))]


def create_dataset(input_file: str, rcrd_class: rltk.Record) -> rltk.Dataset:
    ''' Create rltk dataset from a given jl file '''
    assert Path(input_file).suffix == ".jl"
    return rltk.Dataset(reader=rltk.JsonLinesReader(input_file), record_class=rcrd_class, adapter=rltk.MemoryKeyValueAdapter())


def get_ground_truth(input_file: str, ds1: rltk.Dataset, ds2: rltk.Dataset) -> rltk.GroundTruth:
    ''' Read the grouth truth from the given input file '''
    devset_file_handle = open(input_file, "r")
    devset_data = json.load(devset_file_handle)
    gt = rltk.GroundTruth()
    for item in devset_data:
        if  item['webmd_url'] != None:
            r_wiki = ds1.get_record(item['wiki_url'])
            r_webmd  = ds2.get_record(item['webmd_url'])
            gt.add_positive(r_wiki.raw_object['MedicineURI'], r_webmd.raw_object['url'])
    
    return gt

def med_name_similarity(r_wiki,r_webmd):
    name_wiki=r_wiki.name_string.lower()
    name_wedgenmd=r_webmd.genname_string.lower()
    name_wedbrandmd=r_webmd.brandname_string.lower()

    name_wedgenmd=name_wedgenmd.replace(" ", "")
    name_wedbrandmd=name_wedbrandmd.replace(" ", "")


    if ' ' in name_wiki:
        name_wiki=name_wiki.split(' ')
        name_wiki=max(name_wiki, key=len)
    elif '-' in name_wiki:
        name_wiki=name_wiki.split('-')
        name_wiki=max(name_wiki, key=len)
    elif '/' in name_wiki:
        name_wiki=name_wiki.split('/')
        name_wiki=max(name_wiki, key=len)

    if name_wiki in name_wedgenmd or name_wiki in name_wedbrandmd :
        return True,1
    else:
        return False,0


def main():
    wiki_file = "/Users/sharadsharma/Documents/KG/Project/WikiMedicineData.jl"
    webmd_file = "/Users/sharadsharma/Documents/KG/Project/WebMD_MedicineDetails.jl"
    ds_wiki = create_dataset(wiki_file, WikiRecord)
    ds_webmd = create_dataset(webmd_file, WebMDRecord)
    
    gt_file   = "/Users/sharadsharma/Documents/KG/Project/DevSet_Medicines.json"
    gt = get_ground_truth(gt_file, ds_wiki, ds_webmd)

    #########dev set testing####################
    gt.generate_all_negatives(ds_wiki, ds_webmd, range_in_gt=True)
    trial = rltk.Trial(gt)
    #candidate_pairs = rltk.get_record_pairs(ds_wiki, ds_webmd, ground_truth=gt)
    
    ######
    bg = rltk.TokenBlockGenerator()

    block = bg.generate(
    bg.block(ds_wiki, function_ = lambda r:n_gram(r.name_string,3)),
    bg.block(ds_webmd, function_=lambda r: n_gram(r.genname_string, 3))

    )
    block2  = bg.generate(
    bg.block(ds_wiki, function_ = lambda r:n_gram(r.name_string,3)),
    bg.block(ds_webmd, function_=lambda r: n_gram(r.brandname_string, 3))

    )


    pred_dic = defaultdict(set)
    pairs =list(set(block.pairwise(ds_wiki,ds_webmd)))
    pairs_2 = list(set(block2.pairwise(ds_wiki,ds_webmd)))
    pairs.extend(pairs_2)
    print(pairs[0])
    
    for a,b,c in pairs:

        flag = False
        r_wiki = ds_wiki.get_record(b)
        r_webmd = ds_webmd.get_record(c)

        value,conf=med_name_similarity(r_wiki, r_webmd)
        trial.add_result(b, c, value,conf)
        if value==True:
            flag=True



            pred_dic[b].add(c)


        if flag==False:
            pred_dic[b].add(None)

    for k,v in pred_dic.items():
        if len(pred_dic[k]) >1:
            pred_dic[k].remove(None)
    res = []
    for k,v in pred_dic.items():
        
        temp = {}
        temp['wiki_url'] =k
        temp['webmd_url'] = list(v)[0]
        res.append(temp)



    with open('/Users/sharadsharma/Downloads/MedicineLinkage.json','w') as op_file:
         json.dump(res,op_file,indent=2)

  
    trial.evaluate()
    print('precison:', trial.precision, 'recall:', trial.recall, 'f-measure:', trial.f_measure)
    print('Trial statistics based on Ground-Truth from development set data:')
    print(f'tp: {trial.true_positives:.06f} [{len(trial.true_positives_list)}]')
    print(f'fp: {trial.false_positives:.06f} [{len(trial.false_positives_list)}]')
    print(f'tn: {trial.true_negatives:.06f} [{len(trial.true_negatives_list)}]')
    print(f'fn: {trial.false_negatives:.06f} [{len(trial.false_negatives_list)}]')
    
  
if __name__ == '__main__':
    main()