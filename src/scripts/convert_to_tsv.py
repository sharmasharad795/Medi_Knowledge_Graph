from collections import  defaultdict
import json
import csv
d = defaultdict(list)
cnt = 0
with open('./WebMD_Crawler/WebMD_Crawler/spiders/webmd_medicines.jl','r') as f:
    for line in f:
        temp = json.loads(line)
        url = temp['url']
        name = temp['name']
        generic_name = temp['generic_name']
        side_effects = temp['side_effects']
        usage = temp['usage']
        d['required'].append((url,name,generic_name,side_effects,usage))

tsv_file = open("data.tsv", "w")
tsv_writer = csv.writer(tsv_file,delimiter='\t')

value = d['required']
for row in value:
    url = row[0]
    name = row[1]
    generic_name = row[2]
    side_effects = row[3]
    usage = row[4]
    fields = [url,name,generic_name,side_effects,usage]
    tsv_writer.writerow(fields)
tsv_file.close()