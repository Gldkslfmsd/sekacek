import re
def masky(slovo):
	slovo=slovo.lower()
	for i in range(1,len(slovo)):
		x=slovo[i-1]	
		b=slovo[i-1:]
		b=re.sub(x+x,x+'0',b)
		slovo=slovo[:i-1]+b
	slovo=re.sub('ch','c0',slovo)
	slovo=re.sub('s(t(?!(r|ř|n|l))|p)','s0',slovo)
	slovo=re.sub('th','t0',slovo)
	print(slovo)
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

print(masky('vichr bystřina břicho bysta přeskvělý koniklec pekl'))
print(masky('postla'))
print(masky('skoro Anna lopata jak se Dominik Macháček Máte!šč'))

