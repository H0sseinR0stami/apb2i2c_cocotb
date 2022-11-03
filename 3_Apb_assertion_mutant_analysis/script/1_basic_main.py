# Copyright (C) 2022 Hossein Rostami (Rostami.Hossein@znu.ac.ir)
'''
This script simulate the APBI2C model and comment the Assertions which fail at the simulation
and make clean 'Apb_properties.sva' for mutant analysis

'''

# importing library's
import os
import shutil
from typing import TextIO
import pandas as pd
import csv
from xml.etree import ElementTree as et
from sva_handle import *

# specifying path of the folders and files
rtl_path = "../rtl"
sim_path = "../sim"
simulation_results_assertion_path = "../simulation_results/assertion"
simulation_results_assertion_path_csv = "../simulation_results/assertion/csv"
properties_sva_path = "../properties_sva"


# remove unnecessary files that is created after simulation in previous runs (if exists)
if os.path.exists("../properties_sva/failed_assertions.txt"):
    os.remove("../properties_sva/failed_assertions.txt")

if os.path.exists("../sim/vsim.wlf"):
    os.remove("../sim/vsim.wlf")

if os.path.exists("../simulation_results"):
    shutil.rmtree("../simulation_results")

if os.path.exists("../simulated_mutants"):
    shutil.rmtree("../simulated_mutants")

if os.path.exists("../faulty_mutants"):
    shutil.rmtree("../faulty_mutants")

if os.path.exists("../final_reports"):
    shutil.rmtree("../final_reports")

if os.path.exists("../sim/work"):
    shutil.rmtree("../sim/work")

if os.path.exists("../sim/transcript"):
    os.remove("../sim/transcript")

# rtl folder should have 4 files: fifo.sv, i2c.sv, module_i2c.sv, apb.sv 
# the mutant analysis is on apb.sv that is why this file is omited from rtl folder to be replaced with mutant ones
# for the first simulation the original apb.sv in needed.
shutil.copyfile("../apb.sv", "../rtl/apb.sv")

# run "sim_apb.do" to simulate "apb.sv"
os.chdir(sim_path)

os.system('cmd /c "vsim -do sim_apb.do"')

# create "../simulation_results/assertion" folders
# to store simulation assertion results

if not os.path.exists(simulation_results_assertion_path):
    os.makedirs(simulation_results_assertion_path)

# move simulation results from "sim" folder to "../simulation_results/assertion" folder
try:
    os.rename(os.path.join(sim_path, "apb_assertion_report.xml"),
              os.path.join(simulation_results_assertion_path, "apb_assertion_report.xml"))

except:
    print("error")
    print("faulty design detected")
pass

# create "../simulation_results/assertion/csv" to store the csv file which is extracted from xml files
if not os.path.exists(simulation_results_assertion_path_csv):
    os.makedirs(simulation_results_assertion_path_csv)

# xml to csv
tree = et.parse(os.path.join(simulation_results_assertion_path, "apb_assertion_report.xml"))
with open(os.path.join(simulation_results_assertion_path_csv, "apb_assertion_report.csv"),
          'w', newline='', encoding='utf8') as sitescope_data:
    csvwriter = csv.writer(sitescope_data)
    col_names = 'asrtname  failcount'.split()
    for event in tree.findall('asrtReport/asrt'):
        event_data = ['' if (e := event.find(col)) is None else e.text for col in col_names]
        csvwriter.writerow(event_data)



# extract assertions with fail count > 0
with open(os.path.join(simulation_results_assertion_path_csv, "apb_assertion_report.csv"), 'r') as csvinput:
    with open(os.path.join(properties_sva_path, "failed_apb_assertion_report.txt"),
              'w') as csvoutput:
        writer = csv.writer(csvoutput)
        reader = csv.reader(csvinput)
        for row in reader:
            if int(row[1]) > 0:
                writer.writerow([row[0].strip("/tb/property_").rstrip('_assert\n')])
    csvoutput.close()
csvinput.close()


# list and save the Assertions which are failed in "failed_apb_assertion_report.txt" file located in  "../properties_sva" folder
os.chdir(properties_sva_path)
with open("failed_apb_assertion_report.txt","r") as f, open("failed_assertions.txt","w") as outfile:
 for i in f.readlines():
       if not i.strip():
           continue
       if i:
           outfile.write(i)

os.remove("failed_apb_assertion_report.txt")

# comment the failed Assertions in "Apb_properties.sva" file
os.chdir('../properties_sva')
with open("failed_assertions.txt", "r") as f:
    for number in f.readlines():
        add_text_to_beginning_of_the_line(Apb_properties_sva, 'property_' + str(number.strip('\n')) + '_assert', "//", 0)

if os.path.exists("../simulation_results"):
    shutil.rmtree("../simulation_results")

