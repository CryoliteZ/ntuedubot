from telegramBot.models import Store_Food

fo = open("dish.txt", 'r')

string = fo.read()

store = string.split('\n')

storeNum = len(store)

for i in range(0,storeNum-1):
	store[i] = store[i].split(',')
	store[i][2] = int(store[i][2])
	print(store[i])

Store_Food.objects.all().delete()

for i in range(0,storeNum):
	print(i)
	Store_Food.objects.create(name = store[i][0], food = store[i][1], price = store[i][2])