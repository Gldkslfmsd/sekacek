import re
def rozliš(slovo):
	# TODO: přepsat
	# vypadá to hrozně, i když to funguje
	slovo=slovo.lower()
	for i in range(1,len(slovo)):
		x=slovo[i-1]	
		b=slovo[i-1:]
		b=re.sub(x+x,x+'0',b) #jde to zrychlit, tohle je O(N^2)
		slovo=slovo[:i-1]+b

	slovo=re.sub('ch','c0',slovo)
	slovo=re.sub('s(t(?!(r|ř|n|l))|p)','s0',slovo)
	slovo=re.sub('th','t0',slovo)

	slovo=re.sub('a(u|e)','a0',slovo)
	slovo=re.sub('e(u|i)','e0',slovo)
	slovo=re.sub('o(u|i)','o0',slovo)

	slovo=re.sub('s((t((r|l)(?!$)|ř|n))|kv)','s00',slovo)
	slovo=re.sub('štn','š00',slovo)

	
	vokály=r'(a|e|i|y|o|u|á|é|í|ý|ó|é|ů|ú|ě)'
	slovo=re.sub(vokály,'V',slovo)

	slovo=re.sub(r'(b|c|č|d|ď|f|g|h|j|k|m|n|ň|p|q|s(?!k)|š(?!t)|t|ť|w|x|z|ž)','K',slovo) # některé konzonanty
	slovo=re.sub('Ksk','Ks0',slovo)
	slovo=re.sub('Kšt','Kš0',slovo)

	slovo=re.sub('K(l|r)K','KVK',slovo)
	slovo=re.sub('K(l|r)$','KV',slovo)
	slovo=re.sub('K0(l|r)K','K0VK',slovo)
	slovo=re.sub('K0(l|r)$','K0V',slovo)


	slovo=re.sub('K(r|l|ř|v)V','K0V',slovo)
	
	slovo=re.sub('K(sk|št)','KK0',slovo)
	slovo=re.sub('^(sk|št)','K0',slovo)

	slovo=re.sub('(l|s|ř|v|r)','K',slovo) # zbytek

	return slovo

def sekejmasku(maska):
	z=''
	#začíná se vokálem
	if re.search(r'^VK[^VK]*K',maska): # případ Anna, apostrof
		z=re.sub(r'(^VK)(.*$)',r'\1',maska)
		maska=re.sub(r'(^VK)(.*$)',r'\2',maska)
	elif re.search(r'^V0*K0*[^K]',maska): # případ Antonín
		z=re.sub(r'(^V0*)(.*$)',r'\1',maska)
		maska=re.sub(r'(^V0*)(.*$)',r'\2',maska)
	maska=re.sub(r'(K[^V]*V(K$)?)',r'\1/',maska)
	maska=re.sub(r'/(K0*)K',r'\1/K',maska) # skupina KK uvnitř slova, z /KK dělá K/K
	maska=((z+'/') if z else '') + maska
	return maska

def sekejslovo(slovo,oddělovač):
	maska=rozliš(slovo)
	maska=sekejmasku(maska)
	if maska[-1]=='/': # oddělám poslední /
		maska=maska[:-1]
	vys=''
	j=0
	for i in maska:
		if i!='/':
			vys=vys+slovo[j]
			j+=1
		else:
			vys=vys+oddělovač
	return vys
def oddělslova(text):
	vys=[]
	p=''
	for i in text:
		if re.search(r'\w',i): # je to písmenko
			p=p+i
		else: # je to nějaká interpunkční nebo oddělovací značka
			vys.append(p)
			vys.append(i)
			p=''
	return vys
		
def sekejtext(text,spojovník='~',oddělovač='/'):
	text=re.sub(r'([vszkVSZK]) ',r'\1'+spojovník,text)
	a=oddělslova(text)
	vys=''
	for i in a:
		if re.search(r'\w',i):
			vys=vys+sekejslovo(i,oddělovač)
		else:
			vys=vys+i
	print(vys)

def sek(slovo): # na debugování, vypíše všecky mezivýsledky sekání slova, aby se dalo debugovat
	m=rozliš(slovo)
	print('původní slovo:\t',slovo)
	print('maska:\t',m)
	n=sekejmasku(m)
	print('rozsekaná maska:\t',n)
	print('rozsekané slovo:\t',sekejslovo(slovo,'/'))
	print()
text='''
Z Rudoltic k domovu s kamarádem
Na počátku stvořil Bůh nebe a zemi.
Země byla pustá a prázdná a nad propastnou tůní byla tma. Ale nad vodami vznášel se duch Boží.
I řekl Bůh: „Buď světlo!“ A bylo světlo.
Viděl, že světlo je dobré, a oddělil světlo od tmy.
Světlo nazval Bůh dnem a tmu nazval nocí. Byl večer a bylo jitro, den první.
I řekl Bůh: „Buď klenba uprostřed vod a odděluj vody od vod!“
Učinil klenbu a oddělil vody pod klenbou od vod nad klenbou. A stalo se tak.
Klenbu nazval Bůh nebem. Byl večer a bylo jitro, den druhý.
I řekl Bůh: „Nahromaďte se vody pod nebem na jedno místo a ukaž se souš!“ A stalo se tak.
Souš nazval Bůh zemí a nahromaděné vody nazval moři. Viděl, že to je dobré.
Bůh také řekl: „Zazelenej se země zelení: bylinami, které se rozmnožují semeny, a ovocným stromovím rozmanitého druhu, které na zemi ponese plody se semeny!“ A stalo se tak.
'''
#sek('krok')
#sek('vichr')
sek('bystřina')
#sek('břicho')
#sek('bysta')
#sek('přeskvělý')
#sek('koniklec')
#sek('pekl')
#sek('postla')
#sek('skoro')
#sek('Anna')
sek('Antonín')
sek('lopata')
#sek('postavit')
#sek('automobil')
#sek('poloautomaticky') # asi budu řešit, až s předponami a známými
#sek('automat')
#sek('pěkně')
#sek('jak')
#sek('poddaný')
#sek('pododdělení')
#sek('trojúhelník')
#sek('a')
#sek('od')
sek('propastnou')
sek('duch')
##asi bude lepší ou měnit za 0V, ne V0

##spravit: propastnou, duch

sekejtext(text)
