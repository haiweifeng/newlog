from django.db import models

# Create your models here.

class Dept(models.Model):
    name=models.CharField(max_length=20,unique=True)
    note=models.CharField(max_length=20,null=True)
    class Meta:
        db_table="t_dept"

class Emp(models.Model):
    name=models.CharField(max_length=20)
    salary=models.FloatField()
    age=models.SmallIntegerField(null=True)
    depts=models.ForeignKey(to=Dept,db_column="dept_id",on_delete=models.SET(5))
    headimg = models.FileField(upload_to="emp", null=True)

    class Meta:
        db_table="t_emp"

class Admin137(models.Model):
    username=models.CharField(max_length=20)
    realname=models.CharField(max_length=20)
    password=models.CharField(max_length=100)
    age=models.SmallIntegerField(null=True,default=18)
    gender=models.SmallIntegerField(default=True)
    birth=models.DateField(null=True)
    head_img=models.FileField(upload_to="headimg")
    registtime=models.DateTimeField(auto_now=True)
    modifytime=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="t_admin"




