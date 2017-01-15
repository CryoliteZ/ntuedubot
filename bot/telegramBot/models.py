from django.db import models

class Course(models.Model):
    cid = models.CharField(u'ID', max_length=9, primary_key = True)
    semester = models.IntegerField(u'semester', blank = False)
    name = models.CharField(u'Name', max_length=50)
    courseNum = models.CharField(u'courseNum', max_length=50)
    classNo = models.CharField(u'classNo',max_length=50, blank = True)
    credit = models.IntegerField(u'Credit', blank = True)
    # instructor = models.ForeignKey(u'Instructor',  blank = False, on_delete = models.PROTECT)  #deletion raise integrity error
    time = models.CharField(u'classTime', max_length=15)

    def __str__(self):
	    return self.name

# class Instructor(models.Model):
# 	name = models.CharField(u'Name', max_length=50)
# 	number_of_rollcall = models.IntegerField(u'number_of_rollcall', blank = False)

class Event(models.Model):
	name = models.CharField(u'Name', max_length=50)
	action = models.TextField(u'action')

	def __str__(self):
		return self.name
	
class Grade(models.Model):
    courseID = models.CharField(u'courseID',max_length=20, primary_key = True) #foreign key
    semester = models.IntegerField(u'semester', blank = False)
    gradeA1 = models.IntegerField(u'AplusNum', blank = False)
    gradeA2 = models.IntegerField(u'ANum', blank = False)
    gradeA3 = models.IntegerField(u'AminusNum', blank = False)
    gradeB1 = models.IntegerField(u'BplusNum', blank = False)
    gradeB2 = models.IntegerField(u'BNum', blank = False)
    gradeB3 = models.IntegerField(u'BminusNum', blank = False)
    gradeC1 = models.IntegerField(u'CplusNum', blank = False)
    gradeC2 = models.IntegerField(u'CNum', blank = False)
    gradeC3 = models.IntegerField(u'CminusNum', blank = False)
    gradeF = models.IntegerField(u'FNum', blank = False)
    predictable = models.BooleanField(u'Predictable', blank = False)

    def __str__(self):
	    return self.courseID

class Student(models.Model):
    sid = models.CharField(u'ID', max_length=9, primary_key = True)
    name = models.CharField(u'Name', max_length=50)
    department = models.CharField(u'department', max_length=20, blank = True)
    chat_id = models.CharField(u'chat_id', max_length= 50,blank = False)

    def __str__(self):
	    return self.name

class Take_Course(models.Model):
	sid = models.ForeignKey(u'Student', max_length=9) #foreign key
	cid = models.ForeignKey(u'Course', max_length=9) #foreign key
	def __str__(self):
		return self.cid

class Event_Occur(models.Model):
	eid = models.ForeignKey(u'Event', max_length=9) #foreign key
	cid = models.ForeignKey(u'Course', max_length=9) #foreign key
	def __str__(self):
		return self.eid

class Store(models.Model):
	name = models.CharField(u'name', max_length=9, primary_key = True)
	location = models.CharField(u'location', max_length=50)
	def __str__(self):
		return self.name

class Store_Food(models.Model):
	sid = models.ForeignKey(u'Store') #foreign key
	food = models.CharField(u'food', max_length=50)
	price = models.IntegerField(u'price', primary_key = True)
	def __str__(self):
		return self.food

class Office(models.Model):
	name = models.CharField(u'food', max_length=50)
	phone = models.CharField(u'food', max_length=50)
	startTime = models.TimeField(u'startTime')
	EndTime = models.TimeField(u'EndTime')
	def __str__(self):
		return self.name

	#constraint startTime < EndTime

class Command(models.Model):
	name = models.CharField(u'name', max_length=50)
	information = models.TextField(u'information')
	def __str__(self):
		return self.name

class Log(models.Model):
	isbotmessage = models.BooleanField(u'isbotmessage')
	context = models.TextField(u'context')
	def __str__(self):
		return self.context