import newspaper
import sys

goodNews = []
badNews = []

if len(sys.argv) != 2:
	print("invalid use, exit...")
	exit(0)


urls = open(sys.argv[1], "r").readlines()
badwords = open("bad-words.txt", "r").readlines()
badwords = set(word.strip() for word in badwords)

count = 0
for url in urls:
	try: 
		url = url.strip()
		article = newspaper.Article(url, language='en')
		article.download()
		article.parse()
		words = set(article.text.split())
		badwords_apperance = words.intersection(badwords)
		if len(badwords_apperance) >= 2:
			print(badwords_apperance)
			badNews.append(url)
		else:
			goodNews.append(url)
		count+=1 
		print(count)
	except:
		continue

res = open("result","w")
for gn in goodNews:
	res.write(gn + ", 1" + "\n")
for bn in badNews:
	res.write(bn + ", 0" + "\n")

res.close()