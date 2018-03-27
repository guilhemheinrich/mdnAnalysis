df = read.table('CLEAN_data.tsv', sep="\t", header = TRUE, fill = TRUE)

variables_of_interest <- c('Nombre de consultations à la MDN')
df_of_interest = df[,variables_of_interest]