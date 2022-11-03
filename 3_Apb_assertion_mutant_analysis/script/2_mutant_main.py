# Copyright (C) 2022 Hossein Rostami (Rostami.Hossein@znu.ac.ir)

'''
script for doing mutant analysis

'''

# importing library's
import os
import shutil
from typing import TextIO
import pandas as pd
import csv
from xml.etree import ElementTree as et

# specifying path of the folders and files
mutants_path = "../mutants"
rtl_path = "../rtl"
sim_path = "../sim"
simulated_mutants_path = "../simulated_mutants"
faulty_mutants_path = "../faulty_mutants"
# simulation_results_cover_path = "../simulation_results/cover"
simulation_results_assertion_path = "../simulation_results/assertion"
simulation_results_assertion_path_csv = "../simulation_results/assertion/csv"
simulation_results_assertion_path_csv_final = "../simulation_results/assertion/csv/final"
final_reports = "../final_reports"

# make sure that "rtl" folder does contain "apb.sv" file
if os.path.exists("../rtl/apb.sv"):
    os.remove("../rtl/apb.sv")

# remove unnecessary files that created after simulation from "sim" folder
if os.path.exists("../sim/vsim.wlf"):
    os.remove("../sim/vsim.wlf")

if os.path.exists("../sim/work"):
    shutil.rmtree("../sim/work")

if os.path.exists("../sim/transcript"):
    os.remove("../sim/transcript")

# create "simulated_mutants" folder to store simulated mutants that have been simulated
if not os.path.exists(simulated_mutants_path):
    os.makedirs(simulated_mutants_path)

# create "faulty_mutants" folder to store faulty mutants
if not os.path.exists(faulty_mutants_path):
    os.makedirs(faulty_mutants_path)

# list all files in mutant folder
# save files name with .sv extension in 'mutant_files_name.txt'
files = os.listdir(mutants_path)
with open(r"../script/mutant_files_name.txt", "w") as files_names_list:
    for entry in files:
        if entry.endswith(".sv"):
            files_names_list.write(entry)
            files_names_list.write('\n')
files_names_list.close()

# read mutant file's names one by one  from 'mutant_files_name.txt' and move it to rtl foldr and rename it to "apb.sv"
files_names_list: TextIO = open(r"../script/mutant_files_name.txt", 'r')
for file in files_names_list:
    os.rename(os.path.join(mutants_path, file.rstrip('\n')), os.path.join(rtl_path, 'apb.sv'))

    # run "sim_apb.do" to simulate "apb.sv"
    os.chdir(sim_path)

    os.system('cmd /c "vsim -do sim_apb.do"')

    # move "apb.sv" from "rtl" folder and rename it to its real name and save it to "simulated_mutants" folder
    # remove "mutant"
    os.rename(os.path.join(rtl_path, "apb.sv"),
              os.path.join(simulated_mutants_path, file.replace("mutant", "").rstrip('\n')))

    # create "simulation_results_cover And simulation_results_assertion" folders
    # to store simulation cover and assertion results
    # if not os.path.exists(simulation_results_cover_path):
    # os.makedirs(simulation_results_cover_path)

    if not os.path.exists(simulation_results_assertion_path):
        os.makedirs(simulation_results_assertion_path)

    # move simulation results from "sim" folder to "simulation_results" folder
    # move faulty mutant from simulation_results folder to faulty mutant folder
    try:
        os.rename(os.path.join(sim_path, "apb_assertion_report.xml"),
                  os.path.join(simulation_results_assertion_path,
                               file.rstrip('.sv\n') + "_apb_assertion_report.xml"))

    #  os.rename(os.path.join(sim_path, "Arbiter_cover_report_req_grant_check.xml"),
    #            os.path.join(simulation_results_cover_path, file.rstrip('.sv\n') + "_Arbiter_cover_report_req_grant_check.xml"))
    except:
        print("error")
        print("faulty mutant detected")
        os.rename(os.path.join(simulated_mutants_path, file.replace("mutant", "").rstrip('\n')),
                  os.path.join(faulty_mutants_path, file.replace("mutant", "").rstrip('\n')))
        pass

files_names_list.close()

# xml to csv
if not os.path.exists(simulation_results_assertion_path_csv):
    os.makedirs(simulation_results_assertion_path_csv)

files = os.listdir(simulation_results_assertion_path)
with open(r"../script/xml_result_files_name.txt", "w") as files_names_list:
    for entry in files:
        if entry.endswith(".xml"):
            files_names_list.write(entry)
            files_names_list.write('\n')
files_names_list.close()

files_names_list: TextIO = open(r"../script/xml_result_files_name.txt", 'r')
for file in files_names_list:
    # print(file)
    tree = et.parse(os.path.join(simulation_results_assertion_path, file.rstrip('\n')))
    with open(os.path.join(simulation_results_assertion_path_csv, file.rstrip('.xml\n') + ".csv"),
              'w', newline='', encoding='utf8') as sitescope_data:
        csvwriter = csv.writer(sitescope_data)
        col_names = 'asrtname  failcount'.split()
        for event in tree.findall('asrtReport/asrt'):
            event_data = ['' if (e := event.find(col)) is None else e.text for col in col_names]
            csvwriter.writerow(event_data)

# create final folder and list the csv folder content
if not os.path.exists(simulation_results_assertion_path_csv_final):
    os.makedirs(simulation_results_assertion_path_csv_final)

files = os.listdir(simulation_results_assertion_path_csv)
with open(r"../script/csv_result_files_name.txt", "w") as files_names_list:
    for entry in files:
        if entry.endswith(".csv"):
            files_names_list.write(entry)
            files_names_list.write('\n')
files_names_list.close()


# adding mutant's number to csv files and save it to final folder
files_names_list = open(r"../script/csv_result_files_name.txt", 'r')

for file in files_names_list:
    with open(os.path.join(simulation_results_assertion_path_csv, file.rstrip('\n')), 'r') as csvinput:
        with open(os.path.join(simulation_results_assertion_path_csv_final,
                               file.replace("mutant", "").rstrip('apb_assertion_report.csv\n'))
                  + ".csv", 'w') as csvoutput:
            writer = csv.writer(csvoutput)
            reader = csv.reader(csvinput)
            for row in reader:
                if int(row[1]) > 0:
                    writer.writerow([row[0].strip("/tb/property_").rstrip('_assert')] + [row[1]] +
                                    [file.replace("mutant", "").rstrip('apb_assertion_report.csv\n')] +
                                    [file.replace("mutant", "").rstrip('apb_assertion_report.csv\n')])
                else:
                    writer.writerow([row[0].strip("/tb/property_").rstrip('_assert')] + [row[1]] + ["0"] +
                                    ["0"])

# list the final folder content
files = os.listdir(simulation_results_assertion_path_csv_final)
with open(r"../script/csv_with_mutant_name.txt", "w") as files_names_list:
    for entry in files:
        if entry.endswith(".csv"):
            files_names_list.write(entry)
            files_names_list.write('\n')
files_names_list.close()

# adding header to each csv files in final folder

files_names_list = open(r"../script/csv_with_mutant_name.txt", 'r')
for file in files_names_list:
    df = pd.read_csv(os.path.join(simulation_results_assertion_path_csv_final, file.rstrip('\n')), header=None)

    df.to_csv(os.path.join(simulation_results_assertion_path_csv_final,
                           file.rstrip('\n')),
              header=['asrtname', 'failcount', 'mutantcnt', 'mutant'], index=False)

# create final report folder
if not os.path.exists(final_reports):
    os.makedirs(final_reports)

# concatenating all csv files and sort based on mutants count
files_names_list = open(r"../script/csv_with_mutant_name.txt", 'r')
df_list = []
for file in files_names_list:
    df_list.append(os.path.join(simulation_results_assertion_path_csv_final, file.rstrip('\n')))

df = pd.concat((pd.read_csv(f) for f in df_list), ignore_index=True)

list_agg = df.groupby(by='asrtname').agg({
                                          'mutantcnt': lambda x: len(list(filter((0).__ne__, x)))
                                          }) \
    .sort_values(by=["mutantcnt"], ascending=False).to_csv(os.path.join(final_reports,
                                                                        "final_result_sorted_mutants_count.txt"))

# concatenating all csv files, sort based on asrtname's
files_names_list = open(r"../script/csv_with_mutant_name.txt", 'r')
df_list = []
for file in files_names_list:
    df_list.append(os.path.join(simulation_results_assertion_path_csv_final, file.rstrip('\n')))

df = pd.concat((pd.read_csv(f) for f in df_list), ignore_index=True)

list_agg = df.groupby(by='asrtname').agg({'failcount': lambda x: sum(x),
                                          'mutantcnt': lambda x: len(list(filter((0).__ne__, x))),
                                          'mutant': lambda x: list(filter((0).__ne__, x))
                                          }) \
    .sort_values(by=["mutantcnt"], ascending=False).to_csv(os.path.join(final_reports,
                                                                        "final_result_sorted_asrtname.csv"))

# concatenating all csv files,sort based on mutants
files_names_list = open(r"../script/csv_with_mutant_name.txt", 'r')
df_list = []
for file in files_names_list:
    df_list.append(os.path.join(simulation_results_assertion_path_csv_final, file.rstrip('\n')))

df = pd.concat((pd.read_csv(f) for f in df_list), ignore_index=True)

df = df.loc[df['failcount'] != 0]

list_agg = df.groupby(by='mutant').agg({'failcount': lambda x: sum(x),
                                        'asrtname': lambda x: list(filter((0).__ne__, x))}) \
    .sort_values(by=["failcount"], ascending=False).to_csv(os.path.join(final_reports,
                                                                        "final_result_sorted_mutant.csv"))

