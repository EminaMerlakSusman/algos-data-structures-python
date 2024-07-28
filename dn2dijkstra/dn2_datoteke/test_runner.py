import subprocess
import os
import argparse
import pandas as pd
from time import time




tests_path = 'Tests'
python_path = 'python3'

def run_tests(script_name, python_path = 'python3'):
    # Najdemo vse testne primere
    tests = sorted([i for i in os.listdir(tests_path) if i.endswith('in')])    
    n_tests = len(tests)
    
    # Poženemo test za vsak testni primer
    for i in range(n_tests):
        run_test(script_name, python_path=python_path, test_nb=i)
    




def run_test(script_name, python_path = 'python3', test_nb = 0):

    # Oblikujemo ime testa, glede na njegovo številko
    if test_nb < 10:
        test_name = f'test0{str(test_nb)}.in'
    else:
         test_name = f'test{str(test_nb)}.in'
    if os.path.exists(f'{tests_path}/{test_name}'):
       
       # Odpremo .out testno datoteko in preberemo izhod
        with open(f'{tests_path}/{test_name.replace("in", "out")}', 'r') as out_file:
            result = out_file.readlines()

        # Odpremo .in testno datoteko ter preberemo vhodne podatke
        with open(f'{tests_path}/{test_name}', 'r') as test_file:

            # Zaženemo podano skripto z vhodnimi podatki.
            print(f'Zaganjam test {test_name}',end='\r')

            # Začnemo merit čas
            # Opozorilo: .Popen funkcija potrebuje nekaj časa, 
            # da zažene proces. Izmerjen čas zato ni najbolj natančen.
            start = time()
            r = subprocess.Popen(
                [python_path, script_name],                               
                stdin=test_file,
                stdout=subprocess.PIPE,               
                stderr=subprocess.PIPE, 
                text=True
                )
            
            # Preberemo odgovor in morebitne napake
            stdout, errors = r.communicate()
            end = time()
            elapsed = end - start

            # Če smo dobili napako
            if r.returncode != 0:
                # Proces se ni izvedel uspešno
                err_msg = errors
                print(f'Test {test_name} je sprožil napako: \n {err_msg}')                
            
            # Če napake ni, potem izvlečemo rezultat in ga primerjamo z pravilnim
            else:                                          
                output = stdout#.splitlines()
                result_nums = list(map(float, result))
            
                out_nums =  list(map(float, stdout.splitlines()))              
                correct = True
                for r1, r2 in zip(result_nums, out_nums):
                    if abs(r1 - r2) > 10**(-5):
                        print(f'Test {test_name} je vrnil napačen odgovor! Čas: {str(elapsed)}')
                        print(f'Test {test_name} je vrnil: {output}')
                        print(f'Pravilen odgovor je: {result}') 
                        correct = False   

                if  correct:
                    print(f'Test {test_name} uspešen. Čas: {str(round(elapsed, 3))} sekunde.')
                
                                           
                
              

    else:
        print(f'Testna datoteka {test_name} ne obstaja!')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()    
    ap.add_argument("-script", "--script", required=True,
    help="python script to test")
    ap.add_argument("-pypath", "--pypath", required=False,
    help="Python path to use.")
    ap.add_argument("-test_nb", "--test_nb", required=False,
    help="Which test to execute. If not supplied all tests are executed.")
    args = vars(ap.parse_args())
    
  
    script_name = args['script']   
    if args['pypath'] is not None:
        python_path = args['pypath']
    if args['test_nb'] is not None:
         test_nb = int(args['test_nb'])
         run_test(script_name, python_path=python_path, test_nb=test_nb)
    else:
        run_tests(script_name, python_path=python_path)






