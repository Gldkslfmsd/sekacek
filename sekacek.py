#!/usr/bin/python3
import re

def rozliš(slovo):
	slovo=slovo.lower()
	konzonanty=r'bcčdďfghjklmnňpqrřsštťvwxzž'
	vyměň=[
		('ch','c0'),
		(r'rr','r0'), (r'll','l0'),
		(r'th','t0'),
		(r'[ao]u',r'0u'), # diftongy au, eu, ou 
		(r'^eu',r'0u'), # eu nedělitelný jen na začátku slova, Ze/us ne
		(r'[ao]i','0V'),
		(r'[aeiyouáéěíýóůú]','V'), # vokály	

		(r'([^V])([rl])(0*[^0Vrl]|$)',r'\1V\3'), # slabikotvorné l, r
		(r's[pt]','s0'), # nedělitelné sp a st
		(r'([^V0lr]0*)[řlrv]',r'\g<1>0'), # Kr, Kř, Kl, Kv

		(r's(tr|tř|kv)',r's00'), # str, stř, skv
		# TODO: stn, stl, štn ignorovat?
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

def zpracujvýjimky(slovo,oddělovač='/'):
	# TODO: načíst je na začátku programu ze souboru, / v něm bude oddělovač
	výjimky=[
		('podod','pod/od'),
		('polo','po/lo'),
		('troj','troj'),
		('dvoj','dvoj'),
		('Anna','A/nna'),
		('odopero','od/o/pe/ro'),
		('bezolovna','bez/o/lo/vna'),
		('leu','leu'),
		('podvod','pod/vod'),
	]
	for (a,b) in výjimky:
		re.sub(r'/',oddělovač,b)
		if re.search(a,slovo):
			return (b,slovo[len(a):])
	return ('',slovo)

def sekejslovo(slovo,oddělovač):
	(začátek,slovo)=zpracujvýjimky(slovo,oddělovač=oddělovač)
	if slovo=='':
		return začátek
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
	if začátek and vys:
		začátek=začátek+oddělovač
	return začátek+vys

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
	text=re.sub(r'([\s^])([vszkVSZK]) ',r'\1\2'+spojovník,text)
	a=oddělslova(text)
	vys=''
	for i in a:
		if re.search(r'\w',i):
			vys=vys+sekejslovo(i,oddělovač)
		else:
			vys=vys+i
	print(vys)

def sek(slovo): # na debugování, vypíše všecky mezivýsledky sekání slova
	m=rozliš(slovo)
	print('původní slovo:\t\t',slovo)
	print('maska:\t\t\t',m)
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
sek('stacionární')
sek('využívá')
#sek('vichr')
#sek('bystřina')
#sek('břicho')
#sek('bysta')
#sek('přeskvělý')
#sek('koniklec')
#sek('pekl')
sek('postl')
sek('arabština')
#sek('skoro')
#sek('Anna')
#sek('apostrof')
#sek('Antonín')
#sek('klenbou')
#sek('postavit')
sek('automobil')
sek('poloautomaticky')
sek('automat')
#sek('pěkně')
#sek('jak')
#sek('poddaný')
#sek('pododdělení')
#sek('trojúhelník')
#sek('Boccacio')
#sek('doktor')
#sek('propastnou')
#sek('první')
#sek('dveře')
#sek('podvod')
#sek('denní')
#sek('prázdná')
#sek('prázdniny')
#sek('prázdniny')
#sek('bezolovnatý')
#sek('bezouška')
#sek('bezdomovec')
#sek('bezinka')
#sek('bezohlednost')
#sek('dvojakord')
#sek('laickém')
#sek('paleontologa')
#sek('arch')
sek('autem')
sek('deismus')
sek('Zeus')
sek('eutanázie')
sek('leukémie')
sek('neonacista')
##asi bude lepší ou měnit za 0V, ne V0

text2='''
Stacionární duál odoperoval desetinásobnému geodetovi čtyřiadvacet hemiedrů doobléknuv ho asociací využívající dřevoobráběcí bibliograf.

Je libo hemiedr? Dodekaedr? Tetraedr? Paleontologa? Nebo fialku? 

Mein Luftkissenfahrzeug ist voller Aale.
Chrysanthemum leucanthemum
familia: Compositae (Asteraceae)
coemeterium

Tento program si s angličtinou správně neporadí, seká ji, jako by to byla čeština:
	A left-leaning red–black (LLRB) tree is a type of self-balancing binary search tree. It is a variant of the red–black tree and guarantees the same asymptotic complexity for operations, but is designed to be easier to implement.

To je, co?

Jak umí sekat latinu? Moc dobře ne:

In principio creavit Deus caelum et terram 2 terra autem erat inanis et vacua et tenebrae super faciem abyssi et spiritus Dei ferebatur super aquas 3 dixitque Deus fiat lux et facta est lux 4 et vidit Deus lucem quod esset bona et divisit lucem ac tenebras 5 appellavitque lucem diem et tenebras noctem factumque est vespere et mane dies unus

6 dixit quoque Deus fiat firmamentum in medio aquarum et dividat aquas ab aquis 7 et fecit Deus firmamentum divisitque aquas quae erant sub firmamento ab his quae erant super firmamentum et factum est ita 8 vocavitque Deus firmamentum caelum et factum est vespere et mane dies secundus
'''
sekejtext(text)
sekejtext(text2)
