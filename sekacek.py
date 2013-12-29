import re
def masky(slovo):
	slovo=slovo.lower()
	for i in range(1,len(slovo)):
		x=slovo[i-1]	
		b=slovo[i-1:]
		b=re.sub(x+x,x+'0',b)
		slovo=slovo[:i-1]+b
	slovo=re.sub('ch','c0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('s(t(?!(r|ř|n|l))|p)','s0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('th','t0',slovo,flags=re.IGNORECASE)
	print(slovo)
	slovo=re.sub('a(u|e)','a0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('e(u|i)','e0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('o(u|i)','o0',slovo,flags=re.IGNORECASE)

	slovo=re.sub('s((t((r|l)(?!$)|ř|n))|kv)','s00',slovo,flags=re.IGNORECASE)
	slovo=re.sub('štn','š00',slovo,flags=re.IGNORECASE)

	
	vokály=r'(a|e|i|y|o|u|á|é|í|ý|ó|é|ů|ú|ě)'
	slovo=re.sub(vokály,'@',slovo,flags=re.IGNORECASE)

	slovo=re.sub(r'(b|c|č|d|ď|f|g|h|j|k|m|n|ň|p|q|s(?!k)|š(?!t)|t|ť|w|x|z|ž)','ł',slovo,flags=re.IGNORECASE) # některé konzonanty
	slovo=re.sub('łsk','łs0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('łšt','łš0',slovo,flags=re.IGNORECASE)

	slovo=re.sub('ł(l|r)ł','ł@ł',slovo,flags=re.IGNORECASE)
	slovo=re.sub('ł(l|r)$','ł@',slovo,flags=re.IGNORECASE)
	slovo=re.sub('ł0(l|r)ł','ł0@ł',slovo,flags=re.IGNORECASE)
	slovo=re.sub('ł0(l|r)$','ł0@',slovo,flags=re.IGNORECASE)


	slovo=re.sub('ł(r|l|ř|v)@','ł0@',slovo,flags=re.IGNORECASE)
	
	slovo=re.sub('ł(sk|št)','łł0',slovo,flags=re.IGNORECASE)
	slovo=re.sub('^(sk|št)','ł0',slovo,flags=re.IGNORECASE)

	slovo=re.sub('(l|s|ř|v|r)','ł',slovo,flags=re.IGNORECASE) # zbytek



	return slovo

print(masky('vichr bystřina břicho bysta přeskvělý koniklec pekl'))
print(masky('postla'))
print(masky('skoro Anna lopata jak se Dominik Macháček Máte!šč'))

