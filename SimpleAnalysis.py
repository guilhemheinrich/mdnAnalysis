#!/usr/bin/python

import csv
import numpy as np
import statistics
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import time, datetime
import re
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
    new_string = "".join(map(chr,purified_str_as_int))
    new_string = re.sub(' +', ' ', new_string)
    new_string = re.sub(', ', '\n', new_string)
    return new_string

def purify_int(integer):
    out = None
    try:
        out = int(integer)
    except:
        pass
    return out

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
        'dataTypeMapping' : purify_int,
    },
    "Nombre de séances de préparation à l'accouchement" : {
        'grouping' : 'ALL',
        'dataTypeMapping' : purify_int,
    },
    "Durée de maintien de la femme dans la MDN après la délivrance  en heure": {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : string_to_datetime,
    },
    "*Nombre de TV réalisés pendant le travail" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "*Alimentation pendant le travail: 0 = pas d'alimentation 1= liquide,                               2 = solide,                              3= solide+liquide" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "Nombre de séances de préparation à l'accouchement" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "* acct Hands 0=Off / 1=On" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "*Durée efforts expulsifs en heure": {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : string_to_datetime,
    },
    "*Durée d'ouverture de l'œuf en heure": {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : string_to_datetime,
    },
    # # "* pesée total saignements en grammes entre acct et  2h après délivrance en grammes" : {
    # #     'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
    # #     'dataTypeMapping' : purify_int,
    # # },
    "Poids de naissance en grammes " : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "Age gestationnel en SA révolues" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "Age gestationnel en SA révolues" : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
    "Mode d'alimentation à 7 jours : 1= allaitement maternel 2= allaitement artificiel 3= allaitement mixte " : {
        'grouping' : ['ACCOUCHEMENTS A LA MDN ET RAD MERE ET NNE'],
        'dataTypeMapping' : purify_int,
    },
}


# figure related code
# all_bxpl = []
# all_hstpl = []
all_plots = []
all_plots_per_variable = []

# bxpl = plt.figure()
# bxpl.suptitle('Graphical overview - Boxplot', fontsize=14, fontweight='bold')
# hstpl = plt.figure()
# hstpl.suptitle('Graphical overview - Histogram', fontsize=14, fontweight='bold')

cpt = 0
with open('SimpleAnalysis.txt', 'w') as f:
    for variable in variables_of_interest:
        plot_per_page = 4
        plot_indicator  = cpt % plot_per_page
        if plot_indicator == 0:
            # current_bxpl = plt.figure()
            # current_bxpl.suptitle('Boxplot', fontsize=14, fontweight='bold')
            # current_hstpl = plt.figure()
            # current_hstpl.suptitle('Histogram', fontsize=14, fontweight='bold')
            # all_bxpl.append(current_bxpl)
            # all_hstpl.append(current_hstpl)
            current_plot = plt.figure()
            current_plot.subplots_adjust(hspace = 0.7)
            # current_plot.suptitle('Boxplot', fontsize=14, fontweight='bold')
            all_plots.append(current_plot)
        current_plot_variable = plt.figure()
        current_plot_variable.suptitle(purify_string_to_unicode(variable), fontsize=14, fontweight='bold')
        all_plots_per_variable.append(current_plot_variable)
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
        mappedValue = filter(lambda ele: ele is not None, mappedValue)
        print >> f, "Nombre d'individus :", len(mappedValue)
        print >> f, "Moyenne :", statistics.mean(mappedValue)
        print >> f, "Mediane :", statistics.median(mappedValue)
        print >> f, "Minimum :", min(mappedValue)
        print >> f, "Maximum :", max(mappedValue)
        # ax = current_bxpl.add_subplot(plot_per_page, 1, plot_indicator + 1)
        # ax.boxplot(mappedValue)
        # ax.set_title(purify_string_to_unicode(variable))        
        # ax = current_hstpl.add_subplot(plot_per_page, 1, plot_indicator + 1)        
        # ax.hist(mappedValue)
        # ax.set_title(purify_string_to_unicode(variable))
        ax = current_plot.add_subplot(plot_per_page, 2, plot_indicator * 2 + 1)
        # ax.SubplotParams(hspace = 0.5)
        ax.boxplot(mappedValue)
        ax.set_title(purify_string_to_unicode(variable))        
        ax = current_plot.add_subplot(plot_per_page, 2, plot_indicator * 2 + 2)
        # ax.SubplotParams(hspace = 0.5)
        ax.hist(mappedValue)
        # ax.set_title(purify_string_to_unicode(variable))
        ax_v = current_plot_variable.add_subplot(1, 2, 1)
        # ax.SubplotParams(hspace = 0.5)
        ax_v.boxplot(mappedValue)
        ax_v.set_title('Boxplot')
        ax_v = current_plot_variable.add_subplot(2, 2, 2)
        # ax.SubplotParams(hspace = 0.5)
        ax_v.hist(mappedValue)
        ax_v.set_title('Histogram')
        print >> f, "\n\n"
        cpt += 1

# plt.show()

pp = PdfPages('Graphical overview_per_variables.pdf')
for fig in all_plots_per_variable:
    pp.savefig(fig)

pp.close()

# pp = PdfPages('Graphical overview.pdf')
# for fig_index in range(len(all_plots)):
#     # pp.savefig(all_bxpl[fig_index])
#     # pp.savefig(all_hstpl[fig_index])
#     pp.savefig(all_plots[fig_index])

# pp.close()


# variable = "Mode d'alimentation à 7 jours : 1= allaitement maternel 2= allaitement artificiel 3= allaitement mixte "
# grouping = variables_of_interest[variable]['grouping']
# mapping = variables_of_interest[variable]['dataTypeMapping']
# datacolumn = []
# for value_group in content_data[variable]:
#     if (isinstance(mapping, list)):
#         if value_group['group'] in grouping:
#             datacolumn.append(value_group['value'])
#     # Assuming it's 'ALL' then
#     else:
#         datacolumn.append(value_group['value'])
# mappedValue = map(mapping, datacolumn)
# mappedValue = filter(lambda ele: ele is not None, mappedValue)
# plt.autoscale()
# plt.savefig('SimpleAnalysis.pdf', bbox_inches='tight')




