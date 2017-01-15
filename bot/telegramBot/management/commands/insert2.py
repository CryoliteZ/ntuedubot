from telegramBot.models import Store

fo = open("rest.txt", 'r')

string = fo.read()

store = string.split('\n')

storeNum = len(store)

for i in range(0,storeNum-1):
	store[i] = store[i].split(',')
	store[i][1] = float(store[i][1])
	print(store[i])

Store.objects.all().delete()

for i in range(0,storeNum):
	print(i)
	Store.objects.create(name = store[i][0], rating = store[i][1], phone = store[i][2], location = store[i][3], time = store[i][4])