# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 11:55:05 2022

@author: Songqi Cao
"""

import numpy
import pandas as pd
import pymatgen.core.composition as mg
from pymatgen.ext.matproj import MPRester
#key=input('type the key of your Materials Project account here: ')
key='Uw1jHI2Ln79TUPHoEx'

# This part transforms the correct structure found in Material Project into descriptors.
# It also generates a POSCAR file.
def make(i):
    features=[]
    data=[]
    with MPRester(key) as mpr:
        criteria = {"material_id":i}
        properties = ['spacegroup','volume','density','nsites','pretty_formula']
        result = mpr.query(criteria,properties)
        struct = mpr.get_structure_by_material_id(i)
    formula=result[0]['pretty_formula']
    comp = mg.Composition(formula)
    Z=comp.num_atoms
    data.append(formula)
    data.append(result[0]['spacegroup']['number'])
    data.append(float(result[0]['volume'])*1E-3)
    data.append(result[0]['density'])
    struct=str(struct).splitlines()
    abc=struct[2].split()
    a,b,c=float(abc[-3]),float(abc[-2]),float(abc[-1])
    abc=struct[3].split()
    al,be,ga=float(abc[-3]),float(abc[-2]),float(abc[-1])
    data.append(a/b)
    data.append(b/c)
    data.append(c/a)
    data.append(al/be)
    data.append(be/ga)
    data.append(ga/al)
    if result[0]['spacegroup']['point_group'] in ['-1','2/m','mmm','-3','-3m','4/m','4/mmm','6/m','6/mmm','m-3','m-3m']:
        data.append(1)
    else:
        data.append(0)
    if result[0]['spacegroup']['point_group'] in ['1','2','m','mm2','3','3m','4','4mm','6','6mm']:
        data.append(1)
    else:
        data.append(0)
    data.append(Z*float(result[0]['volume'])*1E-3/float(result[0]['nsites']))
    data.append(float(result[0]['volume'])*1E-3/float(result[0]['nsites']))
    features.append(data)
    
    print(features)
    
    data=pd.DataFrame(features,columns=['formula','SG no. (std.)','V (std.) (nm…)','Density (calc.) (Mg m‰…)','a/b','b/c','c/a','alpha/beta','beta/gamma','gamma/alpha','Inv. center','Polar axis','V/Z','V/Atoms'])
    data.to_excel('to_predict_relative_permittivity_crystal.xlsx',index=False)
    POSCAR=[]
    POSCAR.append(formula)
    POSCAR.append(1.0)
    POSCAR.append(str(a)+' 0.0 0.0')
    POSCAR.append(str(float(b)*numpy.cos(ga*numpy.pi/180))+' '+str(float(b)*numpy.sin(ga*numpy.pi/180))+' 0.0')
    POSCAR.append(str(float(c)*numpy.cos(be*numpy.pi/180))+' '+str(float(b)*(numpy.cos(al*numpy.pi/180)-numpy.cos(be*numpy.pi/180)*numpy.cos(ga*numpy.pi/180)/numpy.sin(ga*numpy.pi/180)))+' '+str(float(c)*numpy.sqrt(1+2*numpy.cos(be*numpy.pi/180)*numpy.cos(al*numpy.pi/180)*numpy.cos(ga*numpy.pi/180)-numpy.cos(be*numpy.pi/180)**2-numpy.cos(al*numpy.pi/180)**2-numpy.cos(ga*numpy.pi/180)**2)))
    POSCAR.append('element')
    POSCAR.append('number')
    POSCAR.append('Direct')
    element=[]
    number=[]
    for i in range(8,len(struct)):
        k=struct[i].split()
        POSCAR.append(k[-4]+' '+k[-3]+' '+k[-2])
        if k[1] in element:
            number[-1]+=1
        else:
            element.append(k[1])
            number.append(1)
            POSCAR[5]=' '.join(element)
    number=[str(i) for i in number]
    POSCAR[6]=' '.join(number)
    file=open('POSCAR_'+formula,'w')
    file.write(str(POSCAR[0])+'\n')
    for i in range(1,len(POSCAR)):
        file.write(str(POSCAR[i])+'\n')
    file.close()
    print('The structural imformation of '+formula+' has been transformed into descriptors in file "to_predict_relative_permittivity_crystal.xlsx". Please check whether it is correct.')

formula=input('type the formula here: ')
with MPRester(key) as mpr:
    ids=mpr.get_materials_ids(formula)
    if len(ids)==0:
        print('No structure of '+formula+' is found in Material Project. Please check your input.')
    elif len(ids)==1:
        make(ids[0])
    else:
        for i in ids:
            
            print('--------id:'+i+'--------')
            '''
            struct=mpr.get_structure_by_material_id(i)
            print(struct)
            '''
            
            with MPRester(key) as mpr:
                criteria = {"material_id":i}
                properties = ['spacegroup']
                result = mpr.query(criteria,properties)
                
            print(result[0]['spacegroup']['number'])
            print('')
        print('More than one structure of '+formula+' are found in Materials Project. Please check which one is correct.')
        print('Type the id of the correct structure here: ')
        mpid=input()
        if mpid in ids:
            make(mpid)
        elif 'mp-'+mpid in ids:
            make('mp-'+mpid)
        else:
            print('A wrong id of structure was given. Please check.')