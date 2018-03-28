#!/usr/bin/python

import csv
import numpy as np
import statistics
import matplotlib.pyplot as plt
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

with open(csvFile) as csvfile:
    reader = csv.DictReader(csvfile, delimiter = '\t')
    fieldnames = reader.fieldnames
    content_data = {}
    for key in fieldnames:
        content_data[key] = []
    for row in reader:
        for key in row:
            content_data[key].append(row[key])

# Pour tous les individus

variables_of_interest = [
    "Nombre de consultations à la MDN",
    "Nombre de séances de préparation à l'accouchement"
]

# figure related code
fig = plt.figure()
fig.suptitle('Graphical overview', fontsize=14, fontweight='bold')

cpt = 1
for variable in variables_of_interest:
    intValue = map(int, content_data[variable])
    statistics.mean(intValue)
    statistics.median(intValue)
    min(intValue)
    max(intValue)
    ax = fig.add_subplot(len(variables_of_interest), 1, cpt)
    ax.boxplot(intValue)
    ax.set_title(purify_string_to_unicode(variable))
    # ax.set_ylabel(variable)
    cpt += 1

plt.show()




