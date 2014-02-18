import re
def rozliš(slovo):
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

def sekej(slovo):
	maska=rozliš(slovo)
	s=''
	vystup=''
	j=0
	for i in range(len(slovo)):
		s=s+maska[i]
		print(s)
		if re.match('K?K0*V',s):
			vystup=vystup+'/'+slovo[j:j+len(s)]
			j+=len(s)
			s=''
	print(vystup,maska)

#pravidla budou:
#1 začíná se V?
#2 KV
def sek(slovo):
	maska=rozliš(slovo)
	z=''
	if re.search(r'^VK[^VK]*K',maska):
		z=re.sub(r'(^VK)(.*$)',r'\1',maska)
		maska=re.sub(r'(^VK)(.*$)',r'\2',maska)
	elif re.search(r'^VK0*[^K]',maska):
		z='V'	
		maska=maska[1:]
	#chci, aby to V odřízlo i s K, pokud má být za ním, a dalo to do z, to se pak přilepí na začátek
	maska=re.sub(r'(K[^V]*V(K$)?)',r'\1/',maska)
	maska=((z+'/') if z else '') + maska
	print(maska)
#sekej('krok')
	
#print(masky('vichr bystřina břicho bysta přeskvělý koniklec pekl'))
sek('postla')
sek('skoro')
sek('Anna')
sek('Antonín')
sek('lopata')
sek('postavit')
# jak se Dominik Macháček Máte!šč'))

#asi bude lepší ou měnit za 0V, ne V0


