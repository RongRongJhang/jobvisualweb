from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import threading
import requests
import time
import queue
import json
import re

def get_total_page(my_params, headers):
    url = requests.get('https://www.104.com.tw/jobs/search/?', my_params, headers=headers).url
    rs = requests.get(url=url)
    data = rs.text

    '''此段程式目的是抓取總頁數'''
    start = data.find('var initFilter =') #找到initFilter的位置
    if start == -1:
        print('未找到initFilter')
    else:
        #找到{}內的字串
        start += len('var initFilter =')
        end = data.find('};', start) + 1
        if end == -1:
            print('未找到{}')
        else:
            #將{}內的字串轉換為dict
            json_str = data[start:end]
            init_filter = json.loads(json_str)
            page_max = init_filter['totalPage'] #取得所有頁數
            return page_max


def get_job_id():
    global job_id_list
    job_id_list = []

    while Que.qsize() > 1: #因為是專門為消化隊伍所使用，所以在隊伍沒有結束之前都要不斷運作著
        all_jobs = [] #先宣告一個所有職務的保存陣列
        page_num = Que.get() #用get取得要爬的頁數

        url = requests.get('https://www.104.com.tw/jobs/search/?&page=' + format(page_num) + '&', my_params, headers=headers).url
        rs = requests.get(url=url)
        page_data = rs.text

        soup = BeautifulSoup(page_data, 'html.parser')

        for item in soup.find_all('a', class_='js-job-link'):
            all_jobs.append(item.get('href'))

        for id in all_jobs:
            match = re.search(r'/(\w+)\?', id)
            if match:
                job_id_list.append(match.group(1))

        print("頁數：{} 爬取成功!".format(page_num))
        time.sleep(1)


def get_job_info(job_id):

    """取得職缺詳細資料"""
    url = f'https://www.104.com.tw/job/ajax/content/{job_id}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'Referer': f'https://www.104.com.tw/job/{job_id}'
    }

    r = requests.get(url, headers=headers)
    if r.status_code != requests.codes.ok:
        print('請求失敗', r.status_code)
        return

    data = r.json()
    return data['data']

def get_json_data(i,job_id):

    global JobList
    try:
        job_info = get_job_info(job_id)

        df = pd.DataFrame(
            data = [{
                "model":"mainsite.baseinfo",
                "pk":str(i+1),
                "fields":{
                'company_name':job_info['header']['custName'],
                'job_title':job_info['header']['jobName'],
                'job_cate':','.join(item['description'] for item in job_info['jobDetail']['jobCategory']),
                'job_salary':job_info['jobDetail']['salary'],
                'job_location':job_info['jobDetail']['addressRegion'] + job_info['jobDetail']['addressDetail'],
                'job_work_experience':job_info['condition']['workExp'],
                'job_edu_require':job_info['condition']['edu'],
                'job_require_major':','.join(job_info['condition']['major']) if job_info['condition']['major'] else '不拘',
                'job_tool_require':','.join(item['description'] for item in job_info['condition']['specialty']) if job_info['condition']['specialty'] else '不拘',
                'job_applicant':job_info['jobDetail']['needEmp'],
                'date':datetime.strftime(datetime.strptime(job_info['header']['appearDate'], "%Y/%m/%d"), "%Y-%m-%d"),
                'job_link':f'https://www.104.com.tw/job/{job_id}?jobsource=jolist_b_date'}
                }]
            )
        with lock: # 使用Lock避免多執行緒同時修改JobList
            JobList = pd.concat([JobList, df], ignore_index=True)
        print("目前正在組第" + str(i+1) + "筆職缺資訊")
        time.sleep(1)
    except AssertionError as msg:
        print(msg)


if __name__ == '__main__':
    # 加入使用者資訊(如使用什麼瀏覽器、作業系統...等資訊)模擬真實瀏覽網頁的情況
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    # 查詢的關鍵字
    my_params = {'ro':'1', # 限定全職的工作，如果不限定則輸入0
            'jobcat':'2007000000', # 職務類別選擇資訊軟體系統類
            'area':'6001006000', # 限定在新竹縣市的工作
            'isnew':'3', # 只要最近幾日內有更新的過的職缺，例：3就是三日內，7就是一週內，依此類推
            'mode':'l'} # 清單的瀏覽模式(是L不是1)

    max_pool = 20

    Que = queue.Queue() #初始化隊伍

    #將所有的頁數，分發進入隊伍
    for n in range(get_total_page(my_params, headers)): #針對頁數做一個迴圈
        page_num = n + 1 #因為頁碼會從0開始計算
        Que.put(page_num) #將頁碼送進去隊伍

    JobList = pd.DataFrame()
    lock = threading.Lock() # 建立Lock

    '''每初始化一個線程就代表一個線程的產生，所以要產生如10個線程，那就直接用迴圈產生10次就好了'''
    Thread_Team = [] #【線程工作收集陣列】用來收集工作中的線程好確認是不是都工作完成
    for x in range(max_pool):
        t = threading.Thread(target=get_job_id, args=()) #target這個參數為你要多線程運作的函式
        t.start() #一定要有start，不然線程會不工作
        Thread_Team.append(t) #要記得將線程加入到上面準備好的【線程工作收集陣列】

    #等待所有線程工作完成
    for t in Thread_Team:
        t.join() #join這個功能代表等待線程工作結束，如果沒有結束就會一直卡在這裡
    

    ThreadList = []
    for i, job_id in enumerate(job_id_list):
        t = threading.Thread(target=get_json_data, args=(i,job_id,))
        t.start()
        ThreadList.append(t)

    for t in ThreadList:
        t.join()

    print('Finished!')

    result = JobList.to_json(orient="records")
    parsed = json.loads(result)

    with open('/app/jobvisualweb/fixtures/data.json', 'w', encoding='utf-8') as f:
        json.dump(parsed, f, ensure_ascii=False, indent=4)