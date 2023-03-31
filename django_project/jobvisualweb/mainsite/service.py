from .models import *
from django.core import serializers
from django.http import JsonResponse
from django.db.models import Count, When, Case
from collections import Counter
import json

def getJobLists():
    joblists = BaseInfo.objects.all()
    return joblists


def getRequireMajors():
    result = BaseInfo.objects.values('job_require_major')
    data = [{'item':item['job_require_major']} for item in result]    
    return data


def get_piechart_data():
    result = (BaseInfo.objects
        .values('job_work_experience')
        .annotate(count=Count('job_work_experience'))
        .order_by()
    )
    data = [{'name':item['job_work_experience'], 'y':item['count']} for item in result]
    return data


def get_lollipop_data():
    cnt = Counter()
    sql = '''
            SELECT job_id,
            CASE
                WHEN LEFT(job_location, 3) = '新竹市' THEN '新竹市'
                WHEN job_location = '新竹縣市' THEN '其他'
                WHEN LEFT(job_location, 3) <> '新竹市' THEN substring(job_location, 4, 3)
                ELSE '其他'
            END as locat
            FROM jobbaseinfo;
          '''
    sql_result = BaseInfo.objects.raw(sql)
    result = [item.locat for item in sql_result]
    for word in result: cnt[word] += 1
    data = [{'name':key, 'y':value} for key, value in cnt.items()]
    return data