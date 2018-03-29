#!/usr/bin/python

import csv
import numpy as np
import statistics
import matplotlib.pyplot as plt
import time, datetime
# import matplotlib.lines as plot_draw

csvFile = '/home/heinrich/mdnAnalysis/CLEAN_data.tsv'

def purify_string_to_unicode(anystring):
    str_as_int = map(ord, anystring)
    purified_str_as_int = []
    for char in str_as_int:
        if char > 128:
            purified_str_as_int.append(63)
        else :
            purified_str_as_int.append(char)
    return "".join(map(chr,purified_str_as_int))

def string_to_datetime(hour_minute_sec_string, strtime_format = '%H:%M:%S'):
    try:
        parsed_value = datetime.datetime.strptime(hour_minute_sec_string, strtime_format)
        parsed_value = parsed_value - datetime.datetime(1900, 1, 1)
        parsed_value = parsed_value.total_seconds() / 3600
    except:
        parsed_value = None
        # pass
    return parsed_value


    

with open(csvFile) as csvfile:
    reader = csv.DictReader(csvfile, delimiter = '\t')
    fieldnames = reader.fieldnames
    content_data = {}
    for key in fieldnames:
        content_data[key] = []
    for row in reader:
        for key in row:
            content_data[key].append({'value' :row[key], 'group' : row['GROUP']})

# Pour tous les individus

variables_of_interest = {
    "Nombre de consultations à la MDN" : {
        'grouping' : 'ALL',
        'dataTypeMapping' : int,
    },
    "Nombre de séances de préparation à l'accouchement" : {
        'grouping' : 'ALL',
        'dataTypeMapping' : int,
    },
    "Durée de maintien de la femme dans la MDN après la délivrance  en heure": {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : string_to_datetime,
    }
}


# figure related code
fig = plt.figure()
fig.suptitle('Graphical overview', fontsize=14, fontweight='bold')

cpt = 1
with open('SimpleAnalysis.txt', 'w') as f:
    for variable in variables_of_interest:
        print >> f, variable + "\n"
        grouping = variables_of_interest[variable]['grouping']
        mapping = variables_of_interest[variable]['dataTypeMapping']
        datacolumn = []
        for value_group in content_data[variable]:
            if (isinstance(mapping, list)):
                if value_group['group'] in grouping:
                    datacolumn.append(value_group['value'])
            # Assuming it's 'ALL' then
            else:
                datacolumn.append(value_group['value'])
        mappedValue = map(mapping, datacolumn)
        mappedValue = filter(None, mappedValue)
        print >> f, "Nombre d'individus :", len(mappedValue)
        print >> f, "Moyenne :", statistics.mean(mappedValue)
        print >> f, "Mediane :", statistics.median(mappedValue)
        print >> f, "Minimum :", min(mappedValue)
        print >> f, "Maximum :", max(mappedValue)
        ax = fig.add_subplot(len(variables_of_interest), 1, cpt)
        ax.boxplot(mappedValue)
        ax.set_title(purify_string_to_unicode(variable))
        print >> f, "\n\n"
        # ax.set_ylabel(variable)
        cpt += 1

plt.show()

# plt.autoscale()
# plt.savefig('SimpleAnalysis.pdf', bbox_inches='tight')




