from django.db import models

# Create your models here.
class BaseInfo(models.Model):
    job_id=models.AutoField(verbose_name='ID',primary_key=True)
    company_name=models.CharField(verbose_name='公司名稱',max_length=100)
    job_title=models.CharField(verbose_name='職稱',max_length=150)
    job_cate=models.CharField(verbose_name='職務類別',max_length=100)
    job_salary=models.CharField(verbose_name='薪資',max_length=50)
    job_location=models.CharField(verbose_name='上班地點',max_length=150)
    job_work_experience=models.CharField(verbose_name='工作經歷',max_length=20)
    job_edu_require=models.CharField(verbose_name='學歷要求',max_length=20)
    job_require_major=models.CharField(verbose_name='科系要求',max_length=100)
    job_tool_require=models.TextField(verbose_name='擅長工具')
    job_applicant=models.CharField(verbose_name='應徵人數',max_length=20)
    date=models.CharField(verbose_name='更新日期',max_length=10)
    job_link=models.TextField(verbose_name='連結')

    class Meta:
        managed = True
        verbose_name = '職缺基本資訊'
        db_table = 'jobbaseinfo'
        ordering=['-job_id']