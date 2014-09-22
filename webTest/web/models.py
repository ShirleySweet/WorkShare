from django.db import models

# Create your models here.
class Person(models.Model):
    person_id = models.IntegerField(max_length=9)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    status = models.IntegerField(max_length=2)
    remark = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name;

class Mission(models.Model):
    mission_id = models.IntegerField(max_length=9)
    mission_name = models.CharField(max_length=100)
    accomplish = models.IntegerField(max_length=3)
    remark = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name;

class Submission(models.Model):
    submission_id = models.IntegerField(max_length=9)
    mission = models.ForeignKey(Mission)
    mission_order_id = models.IntegerField(max_length=9)
    status = models.IntegerField(max_length=2)
    content = models.CharField(max_length=200)
    remark = models.CharField(max_length=200)
    person = models.ManyToManyField(Person)

    def __unicode__(self):
        return self.name;

class Daily_report(models.Model):
    report_id = models.IntegerField(max_length=9)
    report_date = models.DateField()
    person = models.ForeignKey(Person)

    def __unicode__(self):
        return self.name;

class Report_describe(models.Model):
    describe_id = models.IntegerField(max_length=9)
    report = models.ForeignKey(Daily_report)
    report_order_id = models.IntegerField(max_length=9)
    mission = models.ForeignKey(Mission)
    submission = models.ForeignKey(Submission)
    content = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name;

class Code(models.Model):
    key = models.IntegerField(max_length=9)
    name = models.CharField(max_length=20)
    value = models.IntegerField(max_length=9)

    def __unicode__(self):
        return self.name;