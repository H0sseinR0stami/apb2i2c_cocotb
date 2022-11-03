#cd C:\apb_assertion\sim
#vsim -do sim_apb.do

# create the Library working directory

vlib work

if {[catch {
    vlog -work work -vopt +incdir+../include -nocovercells "../rtl/apb.sv"
} result]} {
    quit -f
}

# compile the src and tb files along with the includes and options
vlog -work work -vopt +incdir+../include -nocovercells "../rtl/apb.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../rtl/fifo.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../rtl/i2c.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../rtl/module_i2c.sv"
vlog -work work -vopt +incdir+../include -nocovercells "../tb/tb.sv" -assertdebug -cover bcefsx
 

# simulate the top file(testbench)
vsim -assertdebug -t 1ns -coverage -voptargs="+cover=bcesfx" work.tb



# View Assertions
view assertions

#add waveform
add wave -position insertpoint sim:/tb/*

# run the simulation
run -all                                                     

#vcd flush

# txt reports
#coverage report -assert -detail -verbose -output apb_assertion_report.txt :
#coverage report -detail -cvg -directive -comments -output apb_cover_report.txt :




# xml reports
coverage report -assert -detail -verbose -xml -output apb_assertion_report.xml  :
#coverage report -detail -cvg -directive -comments -xml -output apb_cover_report.xml  :

quit -f