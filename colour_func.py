
# import random
import colour
import pylab
from colour.plotting import *
from my_cri import colour_rendering_index
from my_cqs import colour_quality_scale
from new_word import *
import pandas as pd
import numpy as np



def open_spd(sample,name):
	sample_spd_data = {}
	with open(sample) as f:
	    for iii in f:
	       (key, val) = iii.split()
	       key=float(key)
	       val=float(val)
	       key=round(key)       
	       val=round(val,5)
	       sample_spd_data[key] = float(val)
	spd = colour.SpectralPowerDistribution(name, sample_spd_data)
	clone_spd = spd.clone()
	clone_spd.interpolate(colour.SpectralShape(200, 800, 1))
	return clone_spd


def XYZ_xyz_Luv_uv_Tc_lum_Eff_lum_KPD(spd,T_method='Robertson1968'):
	cmfs = colour.STANDARD_OBSERVERS_CMFS['CIE 1931 2 Degree Standard Observer']
	# illuminant = colour.ILLUMINANTS_RELATIVE_SPDS['A']
	XYZ=colour.spectral_to_XYZ(spd, cmfs)
	x, y = colour.XYZ_to_xy(XYZ / 100)
	xyz=[x,y,1-x-y]
	Luv=colour.XYZ_to_Luv(XYZ)
	uv = colour.UCS_to_uv(colour.XYZ_to_UCS(XYZ))

	if T_method=='Robertson1968':
		CCT, _D_uv = colour.uv_to_CCT_Robertson1968(uv)
	elif T_method=='Ohno2013':
		CCT, _D_uv = colour.uv_to_CCT_Ohno2013(uv)

	Tc=[CCT, _D_uv]
	lum_Eff=colour.luminous_efficacy(spd)
	lum_KPD=colour.luminous_efficiency(spd)
	return (XYZ,xyz,Luv,uv,Tc,lum_Eff,lum_KPD)

def CQS_CRI(spd,T):
	(_,CRI_Qa,CRI_Qas,_)=colour_rendering_index(spd,T, additional_data=True)
	(_,CQS_Qa,_,_,_,_,CQS_Qas,_)=colour_quality_scale(spd,T, additional_data=True)
	return (CRI_Qa,CRI_Qas,CQS_Qa,CQS_Qas)


def save_diagram(xyz,flnm,name='Sample'):
	x,y=xyz[0],xyz[1]
	CIE_1931_chromaticity_diagram_plot(standalone=False)
	pylab.plot(x, y, 'o-', color='white')
	pylab.annotate(name,
	                 xy=(x, y),
	                 xytext=(-50, 30),
	                 textcoords='offset points',
	                 arrowprops=dict(arrowstyle='->', connectionstyle='arc3, rad=-0.2'))
	# # # Displaying the plot.
	display(filename=flnm)

def LED_3D(l_red,l_green,l_blue,T,h,spd3_name,image):
	def aprocsimate_CIA(l0,l05):
		sample_spd_data={}
		for lamb in np.arange(200,800,0.9):
			g=np.exp(-((lamb-l0)/l05)**2)
			Phi_led=(g+2*g**5)/3
			sample_spd_data[lamb] = float(Phi_led)
		return sample_spd_data

	def colour_spectr(sample_spd_data,name):
		spd = colour.SpectralPowerDistribution(name, sample_spd_data)
		spd.interpolate(colour.SpectralShape(200, 800, 1))
		return spd

	spd_red0=aprocsimate_CIA(l_red[0],l_red[1])
	spd_green0=aprocsimate_CIA(l_green[0],l_green[1])
	spd_blue0=aprocsimate_CIA(l_blue[0],l_blue[1])

	spd_red=colour_spectr(spd_red0,'red')
	spd_green=colour_spectr(spd_green0,'green')
	spd_blue=colour_spectr(spd_blue0,'blue')

	blackbody_spd = colour.blackbody_spd(T)

	cmfs = colour.STANDARD_OBSERVERS_CMFS['CIE 1931 2 Degree Standard Observer']
	# # # # Calculating the sample spectral power distribution *CIE XYZ* tristimulus values.
	XYZ_blackbody=colour.spectral_to_XYZ(blackbody_spd, cmfs)

	XYZ_red=colour.spectral_to_XYZ(spd_red, cmfs)
	XYZ_green=colour.spectral_to_XYZ(spd_green, cmfs)
	XYZ_blue=colour.spectral_to_XYZ(spd_blue, cmfs)

	#print(XYZ_blackbody,XYZ_red,XYZ_green,XYZ_blue)
	XYZ=np.vstack((XYZ_red,XYZ_green,XYZ_blue))
	XYZ=XYZ.transpose()
	XYZ=np.linalg.inv(XYZ)
	XYZ_blackbody=XYZ_blackbody.transpose()
	abc=np.dot(XYZ,XYZ_blackbody)
	abc=abc/max(abc)

	def spectr_LED(abc,spd_red0,spd_green0,spd_blue0):
		sample_spd_data={}
		a,b,c=abc[0],abc[1],abc[2]
		for lamb in np.arange(200,800,0.9):
			chip_3d=a*spd_red0[lamb]+b*spd_green0[lamb]+c*spd_blue0[lamb]
			sample_spd_data[lamb] = float(chip_3d)
		spd = colour.SpectralPowerDistribution('Sample', sample_spd_data)
		spd.interpolate(colour.SpectralShape(200, 800, 1))
		return spd

	spd_3=[spd_red, spd_green,spd_blue]
	spd_3d=spectr_LED(abc,spd_red0,spd_green0,spd_blue0)
	b1,b2,b3=abc[0],abc[1],abc[2]
	c1=1
	c2=(b2/b1)*(l_red[0]/l_green[0])
	c3=(b3/b1)*(l_red[0]/l_blue[0])
	h1,h2,h3=h[0],h[1],h[2]
	h_sum=(c1*h1+c2*h2+c3*h3)/(c1+c2+c3)
	multi_spd_plot(spd_3, bounding_box=[300,800, 0, 1],filename=spd3_name)
	image.append(spd3_name)
	return spd_3,spd_3d,h_sum,image,abc


def aprocsimate_CIA(l0,l05):
	sample_spd_data={}
	for lamb in np.arange(200,800,0.9):
		g=np.exp(-((lamb-l0)/l05)**2)
		Phi_led=(g+2*g**5)/3
		sample_spd_data[lamb] = float(Phi_led)
	return sample_spd_data

def colour_spectr(sample_spd_data,name):
	spd = colour.SpectralPowerDistribution(name, sample_spd_data)
	spd.interpolate(colour.SpectralShape(200, 800, 1))
	return spd

def spectr_LED4(abca,spd_red0,spd_green0,spd_blue0,spd_yellow0):
	sample_spd_data={}
	b1,b2,b3,a=abca[0],abca[1],abca[2],abca[3]
	chip_values=[]
	for lamb in np.arange(200,800,0.9):
		chip_4d=b1*spd_red0[lamb]+b2*spd_green0[lamb]+b3*spd_blue0[lamb]+a*spd_yellow0[lamb]
		sample_spd_data[lamb] = float(chip_4d)
		chip_values.append(chip_4d)
	max_del=max(chip_values)
	for sample in sample_spd_data:
		sample_spd_data[sample]=sample_spd_data[sample]/max_del
	spd = colour.SpectralPowerDistribution('Sample', sample_spd_data)
	spd.interpolate(colour.SpectralShape(200, 800, 1))
	return spd


def LED_4D(l_red,l_green,l_blue,l_yellow,T,a,h,spd4_name,image,Fi_4d,Fi_red,Fi_green,Fi_blue,Fi_yellow):

	spd_red0=aprocsimate_CIA(l_red[0],l_red[1])
	spd_green0=aprocsimate_CIA(l_green[0],l_green[1])
	spd_blue0=aprocsimate_CIA(l_blue[0],l_blue[1])
	spd_yellow0=aprocsimate_CIA(l_yellow[0],l_yellow[1])

	spd_red=colour_spectr(spd_red0,'red')
	spd_green=colour_spectr(spd_green0,'green')
	spd_blue=colour_spectr(spd_blue0,'blue')
	spd_yellow=colour_spectr(spd_yellow0,'yellow')


	blackbody_spd = colour.blackbody_spd(T)
	#single_spd_plot(blackbody_spd)
	cmfs = colour.STANDARD_OBSERVERS_CMFS['CIE 1931 2 Degree Standard Observer']
	# # # # Calculating the sample spectral power distribution *CIE XYZ* tristimulus values.

	blackbody_spd.normalise()

	XYZ_blackbody=colour.spectral_to_XYZ(blackbody_spd, cmfs)

	XYZ_red=colour.spectral_to_XYZ(spd_red, cmfs)
	XYZ_green=colour.spectral_to_XYZ(spd_green, cmfs)
	XYZ_blue=colour.spectral_to_XYZ(spd_blue, cmfs)
	XYZ_yellow=colour.spectral_to_XYZ(spd_yellow, cmfs)

	XYZ_blackbody[0]=XYZ_blackbody[0]-XYZ_yellow[0]*a
	XYZ_blackbody[1]=XYZ_blackbody[1]-XYZ_yellow[1]*a
	XYZ_blackbody[2]=XYZ_blackbody[2]-XYZ_yellow[2]*a


	#print(XYZ_blackbody,XYZ_red,XYZ_green,XYZ_blue)
	XYZ=np.vstack((XYZ_red,XYZ_green,XYZ_blue))
	XYZ=XYZ.transpose()
	XYZ=np.linalg.inv(XYZ)
	XYZ_blackbody=XYZ_blackbody.transpose()
	abc=np.dot(XYZ,XYZ_blackbody)
	abca=[abc[0],abc[1],abc[2],a]
	#abca=abca/max(abca)

	spd_4=[spd_red, spd_green,spd_blue,spd_yellow]
	spd_4d=spectr_LED4(abca,spd_red0,spd_green0,spd_blue0,spd_yellow0)
	b1,b2,b3,b4=abca[0],abca[1],abca[2],abca[3]
	c1=1
	c2=(b2/b1)*(l_red[0]/l_green[0])
	c3=(b3/b1)*(l_red[0]/l_blue[0])
	c4=(b4/b1)*(l_red[0]/l_yellow[0])
	h1,h2,h3,h4=h[0],h[1],h[2],h[3]
	h_sum=(c1*h1+c2*h2+c3*h3+c4*h4)/(c1+c2+c3+c4)
	multi_spd_plot(spd_4,bounding_box=[300,800, 0, 1],filename=spd4_name)
	image.append(spd4_name)
    
	from colour.colorimetry import PHOTOPIC_LEFS


	lef=PHOTOPIC_LEFS.get('CIE 1924 Photopic Standard Observer')
	lef_4d = lef.clone().align(spd_4d.shape,
	                        extrapolation_left=0,
	                        extrapolation_right=0)
	lef_red = lef.clone().align(spd_red.shape,
	                        extrapolation_left=0,
	                        extrapolation_right=0)
 	lef_green = lef.clone().align(spd_green.shape,
	                        extrapolation_left=0,
	                        extrapolation_right=0)
	lef_blue = lef.clone().align(spd_blue.shape,
	                        extrapolation_left=0,
	                        extrapolation_right=0)
	lef_yellow = lef.clone().align(spd_yellow.shape,
	                        extrapolation_left=0,
	                        extrapolation_right=0)
	#import numpy as np
	#spd_4d
	Fi_max_4d=(683*np.trapz(lef_4d.values *spd_4d.values, spd_4d.wavelengths))
	k_4d=Fi_4d/Fi_max_4d
	Fe_4d=(k_4d*np.trapz(spd_4d.values, spd_4d.wavelengths))
	F_4d=[Fi_max_4d,k_4d,Fe_4d,Fi_4d]
	#spd_red
	Fi_max_red=(683*np.trapz(lef_red.values *spd_red.values, spd_red.wavelengths))
	k_red=Fi_red/Fi_max_red
	Fe_red=(k_red*np.trapz(spd_red.values, spd_red.wavelengths))
	F_red=[Fi_max_red,k_red,Fe_red,Fi_red]

	#spd_green
	Fi_max_green=(683*np.trapz(lef_green.values *spd_green.values, spd_green.wavelengths))
	k_green=Fi_green/Fi_max_green
	Fe_green=(k_green*np.trapz(spd_green.values, spd_green.wavelengths))
	F_green=[Fi_max_green,k_green,Fe_green,Fi_green]
	#spd_blue
	Fi_max_blue=(683*np.trapz(lef_blue.values *spd_blue.values, spd_blue.wavelengths))
	k_blue=Fi_blue/Fi_max_blue
	Fe_blue=(k_blue*np.trapz(spd_blue.values, spd_blue.wavelengths))
	F_blue=[Fi_max_blue,k_blue,Fe_blue,Fi_blue]
	#spd_yellow
	Fi_max_yellow=(683*np.trapz(lef_yellow.values *spd_yellow.values, spd_yellow.wavelengths))
	k_yellow=Fi_yellow/Fi_max_yellow
	Fe_yellow=(k_yellow*np.trapz(spd_yellow.values, spd_yellow.wavelengths))
	F_yellow=[Fi_max_yellow,k_yellow,Fe_yellow,Fi_yellow]
	return spd_4,spd_4d,h_sum,image,abca,F_4d,F_red,F_green,F_blue,F_yellow

def save_table(n,prop):
    for pr in prop:
        l=['-']*n
        if isinstance(prop[pr], np.ndarray) or isinstance(prop[pr], list):
            for i in range(len(prop[pr])):
                l[i]=prop[pr][i]
        else:
            l[0]=prop[pr]
        prop[pr]=l
    #df = pd.DataFrame(data = DataSet, columns=prop.keys())
    df = pd.DataFrame(data = prop, index = np.arange(n))
    #df.to_excel(name, index=False)
    return df




def all_save(spd,h,image,abc,spd_png,diagram_png,output_xlsx):

	single_spd_plot(spd, bounding_box=[200,800, 0, 1],filename=spd_png)
	image.append(spd_png)
	#single_spd_plot(spd,filename=spd_png)
	(XYZ,xyz,Luv,uv,Tc,lum_Eff,lum_KPD)=XYZ_xyz_Luv_uv_Tc_lum_Eff_lum_KPD(spd)

	save_diagram(xyz,diagram_png)
	image.append(diagram_png)

	(CRI_Qa,CRI_Qas,CQS_Qa,CQS_Qas)=CQS_CRI(spd,Tc)


	par_colour={'XYZ':XYZ,'xyz':xyz,'Luv':Luv,'uv':uv,'Tc':Tc,'CRI':CRI_Qa,'CQS':CQS_Qa,
	'Efficacy':lum_Eff,'Efficiency':lum_KPD,'EFF':h,'led k':abc}

	par_CRI={}
	for i in CRI_Qas: par_CRI.update({CRI_Qas[i].name:CRI_Qas[i].Q_a})
	par_CQS={}
	for i in CQS_Qas: par_CQS.update({CQS_Qas[i].name:CQS_Qas[i].Q_a})

	if len(abc)>3:
		nnn=4
	else:
		nnn=3

	df1=save_table(nnn,par_colour)
	df2=save_table(1,par_CRI)
	df3=save_table(1,par_CQS)

	writer = pd.ExcelWriter(output_xlsx)
	df1.to_excel(writer,'colour', index=False)
	df2.to_excel(writer,'CRI', index=False)
	df3.to_excel(writer,'CQS', index=False)
	writer.save()

	return image

print('sdasd')


def Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max):

	spd_red0=aprocsimate_CIA(l_red[0],l_red[1])
	spd_green0=aprocsimate_CIA(l_green[0],l_green[1])
	spd_blue0=aprocsimate_CIA(l_blue[0],l_blue[1])
	spd_yellow0=aprocsimate_CIA(l_yellow[0],l_yellow[1])

	b1,b2,b3,b4=abca[0],abca[1],abca[2],abca[3]
	c1=1
	c2=(b2/b1)*(l_red[0]/l_green[0])
	c3=(b3/b1)*(l_red[0]/l_blue[0])
	c4=(b4/b1)*(l_red[0]/l_yellow[0])
	h1,h2,h3,h4=h[0],h[1],h[2],h[3]
	h_sum=(c1*h1+c2*h2+c3*h3+c4*h4)/(c1+c2+c3+c4)


	spd_4d=spectr_LED4(abca,spd_red0,spd_green0,spd_blue0,spd_yellow0)
	(XYZ,xyz,Luv,uv,Tc,lum_Eff,lum_KPD)=XYZ_xyz_Luv_uv_Tc_lum_Eff_lum_KPD(spd_4d)
	(CRI_Qa,CRI_Qas,CQS_Qa,CQS_Qas)=CQS_CRI(spd_4d,Tc)
	par_colour={'Tc':Tc[0],'CRI':CRI_Qa,'CQS':CQS_Qa,'EFF':h_sum,'delta':k_max}
	return par_colour

def new_led(l_red,l_green,l_blue,l_yellow,delta,gray):
	# random_Gray=[random.randint(0, 1),random.randint(0, 1),random.randint(0, 1),random.randint(0, 1)]
	array_Gray = np.asarray(gray)
	
	k_max=(-1)**array_Gray*delta
	array_leds=np.array([l_red[0], l_green[0],  l_blue[0],  l_yellow[0]]);

	new_leds=array_leds+k_max
#	for i in range(0, 3):

	l_red[0]=new_leds[0]
	l_green[0]=new_leds[1]
	l_blue[0]=new_leds[2]
	l_yellow[0]=new_leds[3]

	return l_red,l_green,l_blue,l_yellow,k_max



def LED_4D_Static(l_red,l_green,l_blue,l_yellow,abca,h,output_xlsx,gray,kkkk):
	nnn=4



	l_led=[l_red[0],l_green[0],l_blue[0],l_yellow[0]]

	par_colour0=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,0)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[0],gray)
	par_colour1=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[1],gray)
	par_colour2=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[2],gray)
	par_colour3=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[3],gray)
	par_colour4=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[4],gray)
	par_colour5=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[5],gray)
	par_colour6=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	l_red,l_green,l_blue,l_yellow,k_max=new_led(l_red,l_green,l_blue,l_yellow,kkkk[6],gray)
	par_colour7=Par_4D(l_red,l_green,l_blue,l_yellow,abca,h,k_max)

	

#EFF CRI CQS

	Tc=[abs(par_colour1['Tc']-par_colour0['Tc']),abs(par_colour2['Tc']-par_colour0['Tc']),
	abs(par_colour3['Tc']-par_colour0['Tc']),abs(par_colour4['Tc']-par_colour0['Tc']),
	abs(par_colour5['Tc']-par_colour0['Tc']),abs(par_colour6['Tc']-par_colour0['Tc']),
	abs(par_colour7['Tc']-par_colour0['Tc'])]

	EFF=[par_colour1['EFF']-par_colour0['EFF'],par_colour2['EFF']-par_colour0['EFF'],
	par_colour3['EFF']-par_colour0['EFF'],par_colour4['EFF']-par_colour0['EFF'],
	par_colour5['EFF']-par_colour0['EFF'],par_colour6['EFF']-par_colour0['EFF'],
	par_colour7['EFF']-par_colour0['EFF']]

	CRI=[par_colour1['CRI']-par_colour0['CRI'],par_colour2['CRI']-par_colour0['CRI'],
	par_colour3['CRI']-par_colour0['CRI'],par_colour4['CRI']-par_colour0['CRI'],
	par_colour5['CRI']-par_colour0['CRI'],par_colour6['CRI']-par_colour0['CRI'],
	par_colour7['CRI']-par_colour0['CRI']]

	CQS=[par_colour1['CQS']-par_colour0['CQS'],par_colour2['CQS']-par_colour0['CQS'],
	par_colour3['CQS']-par_colour0['CQS'],par_colour4['CQS']-par_colour0['CQS'],
	par_colour5['CQS']-par_colour0['CQS'],par_colour6['CQS']-par_colour0['CQS'],
	par_colour7['CQS']-par_colour0['CQS']]
	
	nnn=7
	par_colour={'lambda':l_led,'Eff':h,
	'max_Tc':Tc,'max_EFF':EFF,
	'max_CRI':CRI,'max_CQS':CQS,'Gray':gray}

	return par_colour0,par_colour,output_xlsx


def LED_4D_Static_Excel(nnn,par_colour0,par_colour,output_xlsx):

	writer = pd.ExcelWriter(output_xlsx)

	df=save_table(nnn,par_colour)	

	df0=save_table(nnn,par_colour0)


	df.to_excel(writer,'data', index=False)
	df0.to_excel(writer,'0', index=False)

	writer.save()

def LED_4D_Static_Excel_ALL(nnn,output_xlsx,args):

	writer = pd.ExcelWriter(output_xlsx)

	N=len(args)
	df0=save_table(nnn,args[N-1])	
	df0.to_excel(writer,'main', index=False)
	for ii in range(N-1):
		df=save_table(nnn,args[ii])	
		df.to_excel(writer,str(ii+1), index=False)


	writer.save()

