from telegramBot.models import Course, Grade
from django.core.management.base import NoArgsCommand
import math

class Command(NoArgsCommand):
	def handle_noargs(self, **options):
		fo = open(r'C:\Users\user\Documents\djangotest\ntuedubot\bot\telegramBot\management\commands\GPA.txt', 'r')
		course = []
		string = fo.read()

		course = string.split('\n')

		courseNum = len(course)

		for i in range(0,courseNum-1):
			course[i] = course[i].split(',')
		if course[i][2] == '':
			course[i][2] = int('0')
		else:
			course[i][2] = int(course[i][2])
		for j in range(5,16):
			course[i][j] = int(course[i][j])
		course[i][15] = bool(course[i][15])



		Course.objects.all().delete()
		Grade.objects.all().delete()
		# # Course.objects.create(cid = 1, semester = 1, name = 'apple', courseNum = '15', classNo = 10, time = 'abc', credit = 3)
		for i in range(0,courseNum-1):
			if i < 5530:
				x = 1
			else:
				x = 2
			try:
				Course.objects.create(cid = str(i), semester = x, name = course[i][1], courseNum = course[i][3], classNo = course[i][0], time = course[i][4], credit = course[i][2])
				Grade.objects.create(courseID = str(i), semester = x, gradeF = course[i][5], gradeC3 = course[i][6], gradeC2 = course[i][7], gradeC1 = course[i][8], gradeB3 = course[i][9], gradeB2 = course[i][10], gradeB1 = course[i][11], gradeA3 = course[i][12], gradeA2 = course[i][13], gradeA1 = course[i][14], predictable = course[i][15])
			except ValueError:
				print (str(i) + " " + course[i][1] + " " + course[i][3] + " " + course[i][0] + " " + course[i][4] + " " + course[i][2])