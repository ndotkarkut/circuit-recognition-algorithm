from os import error
import subprocess

def retrieve_circuit(parallel, series):
    ''' 
    Function for retrieving multisim circuit 
    and copying it to Downloads
    '''
    multisim_circuit = None
    
    
    if len(parallel) == 1 and series == 1:
        multisim_circuit = 'multisim_circuits/1_Series_Resistors_1_Battery.ms14'
    elif len(parallel) == 3 and series == 3:
        multisim_circuit = 'multisim_circuits/3_Series_Resistors_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 3:
        multisim_circuit = 'multisim_circuits/3_Parallel_Resistors_1_Battery.ms14'
    elif len(parallel) == 6 and series == 6:
        multisim_circuit = 'multisim_circuits/2_Parallel_4_Series_1_Short_Resistors_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 1:
        multisim_circuit = 'multisim_circuits/1_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 2:
        multisim_circuit = 'multisim_circuits/2_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 3:
        multisim_circuit = 'multisim_circuits/3_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 4:
        multisim_circuit = 'multisim_circuits/4_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 5:
        multisim_circuit = 'multisim_circuits/5_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 6:
        multisim_circuit = 'multisim_circuits/6_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 7:
        multisim_circuit = 'multisim_circuits/7_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 8:
        multisim_circuit = 'multisim_circuits/8_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 9:
        multisim_circuit = 'multisim_circuits/9_Parallel_1x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 1:
        multisim_circuit = 'multisim_circuits/1_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 2:
        multisim_circuit = 'multisim_circuits/2_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 3:
        multisim_circuit = 'multisim_circuits/3_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 4:
        multisim_circuit = 'multisim_circuits/4_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 5:
        multisim_circuit = 'multisim_circuits/5_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 6:
        multisim_circuit = 'multisim_circuits/6_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 7:
        multisim_circuit = 'multisim_circuits/7_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 8:
        multisim_circuit = 'multisim_circuits/8_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and parallel[0] == 9:
        multisim_circuit = 'multisim_circuits/9_Parallel_2x_0_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 1:
        multisim_circuit = 'multisim_circuits/2_Parallel_1_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 2:
        multisim_circuit = 'multisim_circuits/2_Parallel_2_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 3:
        multisim_circuit = 'multisim_circuits/2_Parallel_3_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 4:
        multisim_circuit = 'multisim_circuits/2_Parallel_4_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 5:
        multisim_circuit = 'multisim_circuits/2_Parallel_5_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 6:
        multisim_circuit = 'multisim_circuits/2_Parallel_6_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 7:
        multisim_circuit = 'multisim_circuits/2_Parallel_7_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 8:
        multisim_circuit = 'multisim_circuits/2_Parallel_8_Series_1_Battery.ms14'
    elif len(parallel) == 2 and series == 9:
        multisim_circuit = 'multisim_circuits/2_Parallel_9_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 1:
        multisim_circuit = 'multisim_circuits/3_Parallel_1_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 2:
        multisim_circuit = 'multisim_circuits/3_Parallel_2_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 3:
        multisim_circuit = 'multisim_circuits/3_Parallel_3_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 4:
        multisim_circuit = 'multisim_circuits/3_Parallel_4_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 5:
        multisim_circuit = 'multisim_circuits/3_Parallel_5_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 6:
        multisim_circuit = 'multisim_circuits/3_Parallel_6_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 7:
        multisim_circuit = 'multisim_circuits/3_Parallel_7_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 8:
        multisim_circuit = 'multisim_circuits/3_Parallel_8_Series_1_Battery.ms14'
    elif len(parallel) == 3 and series == 9:
        multisim_circuit = 'multisim_circuits/3_Parallel_9_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 3:
        multisim_circuit = 'multisim_circuits/4_Parallel_1_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 1:
        multisim_circuit = 'multisim_circuits/4_Parallel_2_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 2:
        multisim_circuit = 'multisim_circuits/4_Parallel_3_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 3:
        multisim_circuit = 'multisim_circuits/4_Parallel_4_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 4:
        multisim_circuit = 'multisim_circuits/4_Parallel_5_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 5:
        multisim_circuit = 'multisim_circuits/4_Parallel_6_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 6:
        multisim_circuit = 'multisim_circuits/4_Parallel_7_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 7:
        multisim_circuit = 'multisim_circuits/4_Parallel_8_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 8:
        multisim_circuit = 'multisim_circuits/4_Parallel_9_Series_1_Battery.ms14'
    elif len(parallel) == 4 and series == 9:
        multisim_circuit = 'multisim_circuits/4_Parallel_1_Series_1_Battery.ms14'
    if len(parallel) == 3 and series == 3:
        multisim_circuit = 'multisim_circuits/3_Series_Resistors_1_Battery.ms14'
    elif len(parallel) == 1 and parallel[0] == 3:
        multisim_circuit = 'multisim_circuits/3_Parallel_Resistors_1_Battery.ms14'
    elif len(parallel) == 5 and series == 5:
        multisim_circuit = 'multisim_circuits/2_Parallel_4_Series_1_Short_Resistors_1_Battery.ms14'
    elif len(parallel) == 1 and series == 1:
        multisim_circuit = 'multisim_circuits/1_Series_Resistors_1_Battery.ms14'
    copying_process = ['cp', multisim_circuit, '/mnt/c/Users/nkkar/Downloads']

    if multisim_circuit != None:
        try:
            result = subprocess.run(copying_process, check=True, cwd='..')
        except:
            pass
    
    print('ADDED CORRESPONDING MULTISIM CIRCUIT TO DOWNLOADS FOLDER')