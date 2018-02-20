

from colour_func import *

path_spd='spectr/'
path='render/'


image=[]

#Colour Temperuture
T=3000

#red chip 
l_red=[625,20]
#green chip
l_green=[525,40]
#blue chip
l_blue=[470,25]
#blue chip
l_yellow=[590,75]

#Light Efficient
h=[30.6,67.2,8.2,20.6]

#yellow dep
a=0.55

#Lx
Fi_4d=2177.6
Fi_red=75
Fi_green=122
Fi_blue=51.7
Fi_yellow=87.4


#my lamp
#T=3000
h0=110
spd=open_spd(path_spd+'222.dat','spectr')
image=all_save(spd,h0,image,'-','spectr.png','diagram.png',path+'cree.xlsx')
create_word(path+'calculate.docx',image)

image=[]

spd_4,spd_4d,h4_sum,image,abca,F_4d,F_red,F_green,F_blue,F_yellow=LED_4D(l_red,l_green,l_blue,l_yellow,T,a,h,'new_spd4.png',image,Fi_4d,Fi_red,Fi_green,Fi_blue,Fi_yellow)
image=all_save(spd_4d,h4_sum,image,abca,'spd_4.png','spd_4_diagram.png',path+'spd_4_output.xlsx')
create_word(path+'spd_4_calculate.docx',image)


print('Fin')

