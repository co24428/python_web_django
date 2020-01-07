from django.db import models
from mpmath import clsin

# Create your models here.

# 1. 회원을 20명 추가
# ex) classroom : 101,102 ~~ 세 글자
# exam_insert
# exam_update
# exam_delete
# exam_select

class Table2(models.Model):
    object  = models.Manager()

    no          = models.AutoField(primary_key=True)
    name        = models.CharField(max_length=30)
    kor         = models.IntegerField(null=True)
    eng         = models.IntegerField(null=True)
    math        = models.IntegerField(null=True)
    classroom   = models.CharField(max_length=3)
    regdate     = models.DateField(auto_now_add=True)