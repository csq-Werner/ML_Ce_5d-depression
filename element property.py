# -*- coding: utf-8 -*-
"""
Created on Fri Jul 29 00:01:02 2022

@author: Songqi Cao
"""

import pandas as pd

EN=pd.read_csv(r'electronegativity.csv')

alpha=pd.read_csv(r'polarizability.csv')

def electronegativity():
    print('Please type the kind and number of cations in a formula here')
    print('example: "Ba 1 Mg 2" for BaMg2F6')
    elements=input('')
    elements=elements.split()
    n,en=0,0
    for i in range(int(len(elements)/2)):
        n+=int(elements[2*i+1])
        en+=float(list(EN['EN'])[list(EN['element']).index(elements[2*i])])*int(elements[2*i+1])
    print('average electronegativity of the cations is: '+str(en/n))

def a():
    print('Please type the kind and number of anions in a formula here')
    print('example: "F 6" for BaMg2F6')
    elements=input('')
    elements=elements.split()
    n,en=0,0
    for i in range(int(len(elements)/2)):
        n+=int(elements[2*i+1])
        en+=float(list(alpha['alpha'])[list(alpha['element']).index(elements[2*i])])*int(elements[2*i+1])
    print('average polarizability of the anions is: '+str(en/n))

def main():
    while True:
        print('Please type ENTER to continue; or type "quit" to quit.')
        b=input('')
        if b=='quit':
            break
        #'''
        a()
        '''
        electronegativity()
        #'''
        
if __name__=='__main__':
    main()