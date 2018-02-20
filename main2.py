import sys
import random
import PySide.QtCore as PC
import PySide.QtGui as PG
import showGui
import numpy as np

from colour.plotting import *

from colour_func import *

from new_word import *	
 
import re 

class MainDialog(PG.QDialog,showGui.Ui_mainDialog):
	def __init__(self, parent=None):
		super(MainDialog, self).__init__(parent)
		self.setupUi(self)
		self.connect(self.ShowButton, PC.SIGNAL('clicked()'), self.Start)
	
	#def showMessageBox(self):
		#PG.QMessageBox.information(self,'Hello!','Hello there,'+self.nameEdit.text())
	def Start(self):
		

		path='render/'


		image=[]


		#red chip
		l_red=[int(self.nameEdit.text()),int(self.nameEdit_5.text())]
		#green chip
		l_green=[int(self.nameEdit_2.text()),int(self.nameEdit_6.text())]
		#blue chip
		l_blue=[int(self.nameEdit_3.text()),int(self.nameEdit_7.text())]
		#blue chip
		l_yellow=[int(self.nameEdit_4.text()),int(self.nameEdit_8.text())]

		T=int(self.nameEdit_9.text())


		h=[30.6,67.2,8.2,20.6]

		a=0.55

		#led4d=

		Fi_4d=2177.6
		Fi_red=75
		Fi_green=122
		Fi_blue=51.7
		Fi_yellow=87.4





		spd_4,spd_4d,h4_sum,image,abca,F_4d,F_red,F_green,F_blue,F_yellow=LED_4D(l_red,l_green,l_blue,l_yellow,T,a,h,'new_spd4.png',image,Fi_4d,Fi_red,Fi_green,Fi_blue,Fi_yellow)

		image=all_save(spd_4d,h4_sum,image,abca,'spd_4.png','spd_4_diagram.png',path+'4D_Data.xlsx')

		# random_Gray=[random.randint(0, 1),random.randint(0, 1),random.randint(0, 1),random.randint(0, 1)];
		# Gray=random_Gray;

		create_word(path+'new_4_calculate.docx',image)

		kkkk=[0.5,0.75,1,2,5,10,15];

		# argss=()
		NNN=16

		for j in range(NNN):
			a="{0:b}".format(j)
			nnn=len(a)
			c=[0,0,0,0]
			for i in range(nnn):
				c[4-nnn+i]=c[4-nnn+i]+int(a[i])
			print c
			Gray=c;
			par_colour0,par_colour,output_xlsx=LED_4D_Static(l_red,l_green,l_blue,l_yellow,abca,h,path+str(Gray)+'.xlsx',Gray,kkkk)
			K=0

			if j==0:
				max_Tc=par_colour['max_Tc']
				Gray_max_Tc=[str(j+1)];
				max_CRI=par_colour['max_CRI']
				Gray_max_CRI=[str(j+1)];
				max_CQS=par_colour['max_CQS']
				Gray_max_CQS=[str(j+1)];
				max_EFF=par_colour['max_EFF']
				Gray_max_EFF=[str(j+1)];

				min_Tc=par_colour['max_Tc']
				Gray_min_Tc=[str(j+1)];
				min_CRI=par_colour['max_CRI']
				Gray_min_CRI=[str(j+1)];
				min_CQS=par_colour['max_CQS']
				Gray_min_CQS=[str(j+1)];
				min_EFF=par_colour['max_EFF']
				Gray_min_EFF=[str(j+1)];


			else:	
				if par_colour['max_Tc'][K]>max_Tc[K]:
					max_Tc=par_colour['max_Tc']
					Gray_max_Tc=[str(j+1)];
				if par_colour['max_CRI'][K]>max_CRI[K]:
					max_CRI=par_colour['max_CRI']
					Gray_max_CRI=[str(j+1)];
				if par_colour['max_CQS'][K]>max_CQS[K]:
					max_CQS=par_colour['max_CQS']
					Gray_max_CQS=[str(j+1)];
				if par_colour['max_EFF'][K]>max_EFF[K]:
					max_EFF=par_colour['max_EFF']
					Gray_max_EFF=[str(j+1)];

				if par_colour['max_Tc'][K]<min_Tc[K]:
					min_Tc=par_colour['max_Tc']
					Gray_min_Tc=[str(j+1)];
				if par_colour['max_CRI'][K]<min_CRI[K]:
					min_CRI=par_colour['max_CRI']
					Gray_min_CRI=[str(j+1)];
				if par_colour['max_CQS'][K]<min_CQS[K]:
					min_CQS=par_colour['max_CQS']
					Gray_min_CQS=[str(j+1)];
				if par_colour['max_EFF'][K]<min_EFF[K]:
					min_EFF=par_colour['max_EFF']
					Gray_min_EFF=[str(j+1)];

			if j==0:
				argss=(par_colour,)
			else:
				argss+=(par_colour,)

		Gray_max_Tc.extend(max_Tc)
		Gray_max_CRI.extend(max_CRI)
		Gray_max_CQS.extend(max_CQS)
		Gray_max_EFF.extend(max_EFF)
		Gray_min_Tc.extend(min_Tc)
		Gray_min_CRI.extend(min_CRI)
		Gray_min_CQS.extend(min_CQS)
		Gray_min_EFF.extend(min_EFF)

		KKK=[kkkk[K]]
		KKK.extend(kkkk)
		par_colour0={'rgba':[l_red[0],l_green[0],l_blue[0],l_yellow[0]],'delta':KKK,
		'Tc_min':Gray_max_Tc,
		'CRI_max':Gray_max_CRI,
		'CQS_max':Gray_max_CQS,
		'EFF_max':Gray_max_EFF,
		'Tc_max':Gray_min_Tc,
		'CRI_min':Gray_min_CRI,
		'CQS_min':Gray_min_CQS,
		'EFF_min':Gray_min_EFF}	


		print(max_Tc)
		print(Gray_max_Tc)
		print(par_colour0)
		argss+=(par_colour0,)


		nnn=8
		
		LED_4D_Static_Excel_ALL(nnn,path+'ALL_IN'+'.xlsx',argss)

	
		print('123213')








app = PG.QApplication(sys.argv)
form = MainDialog()
form.show()
app.exec_()


