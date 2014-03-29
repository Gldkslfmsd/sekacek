#!/usr/bin/python3
#coding=utf-8

# Sekáček -- dělení českého textu na slabiky
# Autor: Dominik Macháček, gldkslfmsd@gmail.com
# Creative Commons 2013/14

import sys
import re
import os.path

##########################
## FUNKCE NA SEKÁNÍ TEXTU:

def rozliš(slovo):
	slovo=slovo.lower()
	konzonanty=r'bcčdďfghjklmnňpqrřsštťvwxzž'
	vyměň=[
		('ch','c0'),
		(r'rr','r0'), (r'll','l0'),
		(r'nn','n0'), 
		(r'th','t0'),
		(r'[ao]u',r'0u'), # diftongy au, ou 
		(r'^eu',r'0u'), # eu nedělitelný jen na začátku slova, Ze/us ne
		(r'[ao]i','0V'),
		(r'[aeiyouáéěíýóůú]','V'), # vokály	

		(r'([^V])([rl])(0*[^0Vrl]|$)',r'\1V\3'), # slabikotvorné l, r
		(r's[pt]','s0'), # nedělitelné sp a st
		(r'([^V0lr]0*)[řlrv]',r'\g<1>0'), # Kr, Kř, Kl, Kv

		(r's(tr|tř|kv)',r's00'), # str, stř, skv
		(r'zdn','z00'), (r'zd','z0'), # zdn a zd přidávám sám! podle příruček to není nedělitelné
		# stn, stl, štn ignoruju, narozdíl od příruček
		(r'([^V0]0*)sk',r'\g<1>s0'), # poziční digramy (nedělitelné jenom v případě Ksk atp.)
		(r'([^V0]0*)št',r'\g<1>š0'),

		(r'['+konzonanty+']','K')
	]
	for (a,b) in vyměň: 
		slovo=re.sub(a,b,slovo)
	return slovo

def sekejmasku(maska):
	vyměň=[
		#slovo začíná vokálem
		(r'(^0*V)(K0*V)',r'\1/\2'), # případ apostrof -- VKV... -> V/KV...
		(r'(^0*V0*K0*)K',r'\1/K'), # případ Antonín -- VKKV... -> VK/KV...

		#prostředek slova
		(r'(K0*V(K0*$)?)',r'\1/'), # KVKV... -> KV/KV/...
		(r'/(K0*)K',r'\1/K'), # skupina KK uvnitř slova, z /KK dělá K/K
		(r'/(0*V)(0*K0*V)',r'/\1/\2'), # když slabika začíná V: VK/V/KV jako třeba hemi/e/dr
		(r'/(0*V0*K0*)K',r'/\1/K'), # VKVKKV -> VK/VK/KV... např pale/on/tolog

		#konec
		(r'/(K0*)$',r'\1/') # poslední K se připojí k předcházející slabice
	]
	for (a,b) in vyměň:
		maska=re.sub(a,b,maska)
	return maska

def sekejslovo(slovo):
	global oddělovač
	maska=sekejmasku(rozliš(slovo))
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
	vys.append(p)
	return vys
		
def zpracujvýjimky(v):
	global výjimky
	for (a,b) in výjimky:
		try:
			v=re.sub(a,b,v)
		except:
			chybašpatnýregex(v)
	return v


def rozlišvýjimkyazbytek(text):
	global výjimky
	značka=chr(0x4885)
	značkavýjimky=chr(0x8906)
	for (a,b) in výjimky:
		text=re.sub(r'('+a+')',značka+značkavýjimky+r'\1'+značka,text)
	kousky=re.split(značka,text)

	return kousky

def spojneslabičnépředložky(text):
	global spojovník
	return re.sub(r'([\s^])([vszkVSZK]) ',r'\1\2'+spojovník,text)

def sekejtext(text):
	značkavýjimky=chr(0x8906)
	text=spojneslabičnépředložky(text)

	samostatnáslova=oddělslova(text)
	slovanebovýjimky=[]
	for i in samostatnáslova:
		slovanebovýjimky+=rozlišvýjimkyazbytek(i) # nesčítá se, pole se zřetězují

	vys=''
	p=False
	for k in slovanebovýjimky:
		if k and k[0]==značkavýjimky:
			vys=vys+('/' if p else '')+zpracujvýjimky(k[1:])
			p=True
		elif re.search(r'\w',k):
			vys=vys+('/' if p else '')+sekejslovo(k)
			p=True
		else:
			vys=vys+k
			p=False
	print(vys)


def sek(slovo): # na debugování, vypíše všecky mezivýsledky sekání slova
	m=rozliš(slovo)
	print('původní slovo:\t\t',slovo)
	print('maska:\t\t\t',m)
	n=sekejmasku(m)
	print('rozsekaná maska:\t',n)
	print('rozsekané slovo:\t',sekejslovo(slovo,'/'))
	print()

#############################################
## NAČTENÍ VSTUPU A KOMUNIKACE S UŽIVATELEM:

nápověda='''
Sekáček -- sekání českého textu na slabiky
Použití: sekacek.py [PŘEPÍNAČ]… [SOUBOR]…
nebo: sekacek.py [PŘEPÍNAČ]…
V každém souboru na vstupu očekává český text, všechna slova v něm rozdělí na slabiky. Bude-li zadán více než jeden soubor, otevře všechny, naseká a vypíše za sebe.
Jestliže SOUBOR nebude zadán nebo bude „-“, bude čten standardní vstup. Slovo je neprázdná posloupnost znaků oddělená jakýmikoliv znaky kromě písmen.
Lze zvolit následující přepínače:
	-ox, -o x, --oddělovač=x		slabiky se budou oddělovat řetězcem x, standartně /
	-sy, -s y, --spojovník=y		neslabičná slova se ke slabice budou připojovat řetězcem y, standartně ~
	-v SOUBOR [SOUBOR]…, --výjimky=SOUBOR	otevře SOUBOR a z něj načte slova, která má dělit jinak než standartně
	-t, --tiše				nevypisuje žádné chybové hlášky
	-i					ignoruje všechna varování
	--help					vypíše tuto nápovědu a skončí
'''

ignorovatvarování=False
hlásitochybách=True
def chyba_konec():
	global ignorovatvarování
	if not ignorovatvarování:
		sys.exit(1)
def chybašpatnýpřepínač():
	sys.stderr.write('chyba špatný přepínač\n')
	chyba_konec()
def chybasouborneexistuje(s):
	if hlásitochybách:
		sys.stderr.write('chyba, soubor „'+s+'“ nelze otevřít\n')
	chyba_konec()
def chybašpatnýformát(s,ř):
	if hlásitochybách:
		sys.stderr.write('nesprávný formát v souboru výjimek „'+s+'“ na řádku '+str(ř)+'\n')
	chyba_konec()
def chybašpatnýregex(s):
	if hlásitochybách:
		sys.stderr.write('špatný regulární výraz u slova „'+s+'“\n')
	chyba_konec()

if '-i' in sys.argv:
	ignorovatvarování=True
if '--help' in sys.argv:
	print(nápověda)
	sys.exit(1)	

souboryvýjimek=['.sekacek']
oddělovač='/'
spojovník='~'
souborynavstupu=[]
def argumentjevstup(i):
	global souborynavstupu
	while i<len(sys.argv):
		if os.path.isfile(sys.argv[i]):
			souborynavstupu.append(sys.argv[i])
		elif sys.argv[i][0]=='-':
			chybašpatnýpřepínač()
		else:
			chybasouborneexistuje(sys.argv[i])
		i+=1
i=1
while i<len(sys.argv):
	a=sys.argv[i]
	if a=='-v':
		try: 
			i+=1
			while i<len(sys.argv) and os.path.isfile(sys.argv[i]):
				if sys.argv[i] not in souboryvýjimek: 
					souboryvýjimek.append(sys.argv[i])
				i+=1
			i-=1
		except: chybašpatnýpřepínač()
	elif re.search(r'^--výjimky=',a):
		try: 
			f=a[10:]
			if os.path.isfile(f):
				souboryvýjimek.append(f)
			else:
				chybasouborneexistuje(f)
		except: chybašpatnýpřepínač()
	elif a in ['-t','--tiše']:
		hlásitochybách=False
	elif a=='-o':
		i+=1
		if i<len(sys.argv):
			oddělovač=sys.argv[i]
		else:
			chybašpatnýpřepínač()
	elif re.search(r'^-o',a):
		oddělovač=a[2:]
	elif re.search(r'^--oddělovač=',a):
		oddělovač=a[12:]
	elif a=='-s':
		i+=1
		if i<len(sys.argv):
			spojovník=sys.argv[i]
		else:
			chybašpatnýpřepínač()
	elif re.search(r'^-s',a):
		spojovník=a[2:]
	elif re.search(r'^--spojovník=',a):
		spojovník=a[12:]
	elif a=='-i':
		0
	elif a in ['-','--']:
		argumentjevstup(i+1)
		break
	else:
		argumentjevstup(i)
		break
	i+=1

výjimky=[]
for s in souboryvýjimek:
	řádek=1
	try: f=open(s,'r')
	except: chybasouborneexistuje(s)
	else:
		for v in f:
			for k in ['#','%','//','"']: # odstranění komentářů
				v=re.sub(k+r'.*$','',v)
			if re.search(r'\S',v): # je to neprázdný řádek
				if re.search(r'^\s*\S+\s+\S+\s*$',v): # jsou tam dvě slova
					v=re.split(r'\s+',v)[:-1]
					try:
						[a,b]=v
						výjimky.append((a,b))
					except:	chybašpatnýformát(s,řádek)
				else: chybašpatnýformát(s,řádek)	
			řádek+=1
		f.close()

for (a,b) in výjimky:
	b=re.sub(r'/',oddělovač,b)

vstup=''
if souborynavstupu:
	for s in souborynavstupu:
		f=open(s,'r')
		vstup=vstup+f.read()
		f.close()
else:
	while True: # čte se standartní vstup
		i=''
		try: i=input()
		except (KeyboardInterrupt,EOFError): 
			vstup+=str(i)
			break
		else: vstup+=i+'\n'
sekejtext(vstup)
