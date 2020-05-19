import requests 
import json
import os
import _thread

current_path = os.path.dirname(__file__)
download_path = os.path.join(current_path,'CCTalk')

def init_path(log_list_name):
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    log_list_path = os.path.join(download_path,log_list_name)
    if not os.path.exists(log_list_path):
        os.makedirs(log_list_path)
    return log_list_path

def get_log_list(list_id):
    log_url = "https://www.cctalk.com/webapi/content/v1.2/series/all_video_list?seriesId=" + str(list_id)
    log_request = requests.get(log_url)
    return json.loads(log_request.text)

def download_video(save_path, course_name, r):
    file_path = os.path.join(save_path,course_name + ".mp4")
    f = open(file_path, "wb")
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)

def set_download(list_id):
    log_list = get_log_list(list_id)['data']['items']
    #log_list_name = get_log_list(list_id)['data']['seriesName']
    save_path = init_path(log_list_name)
    for item in log_list:
        course_name = item['videoName']
        course_id = item['videoId']
        course_url = "https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId=" + str(course_id) + "&seriesId=" + str(list_id)
        course_request = requests.get(course_url)
        course_info = json.loads(course_request.text)
        course_download_url = course_info['data']['videoUrl']
        r = requests.get(course_download_url, stream = True)
        try:            
            _thread.start_new_thread(download_video, (save_path, course_name, r))
            print("正在下载",course_name)
            time.sleep(3)            
        except:
            pass
    print("所有内容已经下载完成！")
    os.system("pause")

def set_download_item(list_id):
    log_list = get_log_list(list_id)['data']['items']
    #log_list_name = get_log_list(list_id)['data']['seriesName']
    save_path = init_path(log_list_name)
    for item in log_list:
        item_number = log_list.index(item)
        course_name = item['videoName']
        print("[", item_number, "]", course_name)
    download_item_number = input("\n请输入需要下载的节目序号后回车: ")
    set_item = log_list[int(download_item_number)]
    course_name = set_item['videoName']
    course_id = set_item['videoId']
    course_url = "https://www.cctalk.com/webapi/content/v1.1/video/detail?videoId=" + str(course_id) + "&seriesId=" + str(list_id)
    course_request = requests.get(course_url)
    course_info = json.loads(course_request.text)
    course_download_url = course_info['data']['videoUrl']
    r = requests.get(course_download_url, stream = True)
    try:            
        _thread.start_new_thread(download_video, (save_path, course_name, r))
        print("正在下载",course_name)
        time.sleep(3)            
    except:
        pass
    print("所有内容已经下载完成！")
    os.system("pause")

def select_function(list_id):
    os.system("cls")
    chose = input("=========CCTalk免费节目下载=========\n\
    \nVersion: 0.0.1\n\
    \nAuthor: Terry Li\n\
    \n当前节目名:" + log_list_name + "\n\
    \n[ 1 ].下载 " + log_list_name + " 所有 视频\n\
    \n[ 2 ].下载 " + log_list_name + " 指定 视频\n\
    \n保存位置：" + download_path + " \
    \n\n请输入需要的功能序号后回车：")
    if chose is '1':
        set_download(list_id)
        
    if chose is '2':
        print("\n所有视频清单:\n")
        set_download_item(list_id)
    select_function(list_id)

if __name__ == '__main__':
    while True:
        list_id = input("=========CCTalk免费节目下载=========\n\
        \n如网址:\n\
        \nhttps://www.cctalk.com/m/program/1587353365514987\n\
        \nhttps://www.cctalk.com/v/15873559021607?sid=1587353365514987\n\
        \n节目id就为最后一串数字 1587353365514987\n\
        \n请输入你要下载节目的id:\n")
        try:
            str(list_id)
            break
        except:
            print("节目id输入有误, 请重新输入!")
    log_list_name = get_log_list(list_id)['data']['seriesName']
    select_function(list_id)