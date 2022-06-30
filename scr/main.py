from evaluation import vary_fw_similarity, compare_models
from evaluation import show_boolean_means

import os

# os.chdir('scr')
# a = os.getcwd()

print('····································································')
print('················SISTEMA DE EXTRACCIÓN DE INFORMACIÓN················')
print('····································································')
print('··············· Nadia Glez  &  Alejandro Labourdette ···············')
print('····································································')
while True:
    print('Por favor ingrese alguna de las siguientes instrucciones:')
    print('# ~ test <framework> <dataset>')
    print('#     Computa todas las queries del dataset usando un framework(modelo)')
    print('# ~ compare <dataset>')
    print('#     Compara los frameworks vetorial y booleano usando el dataset especificado')
    print('#     <framework>: framework a probar ("vector","boolean")')
    print('#     <dataset>: dataset que será utilizado ("cran","vaswani")')

    instruction = input('   ~ ')
    if len(instruction.split()) == 2:
        command, dataset = instruction.split()
        if command == 'compare':
            # Compare both models using  dataset
            compare_models(dataset)
    if len(instruction.split()) == 3:
        command, framework, dataset = instruction.split()
        if command == 'test':
            if framework == 'vector':
                # Run test vector cran
                vary_fw_similarity(dataset)
            if framework == 'boolean':
                # Run test vector cran
                show_boolean_means(dataset)
    print('Done!')