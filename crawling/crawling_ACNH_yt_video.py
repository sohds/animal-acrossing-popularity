from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import json
import requests
import pandas as pd

with open('youtube_api.json', 'r', encoding='utf8') as f:
    data = json.load(f)
    print(data)

youtube = build(data['YOUTUBE_API_SERVICE_NAME'], data['YOUTUBE_API_SERVICE_VERSION'], developerKey = data['API_KEY'])

# searchACNH = youtube.search().list(
#     q = '모동숲 주민',
#     part = 'snippet, statistics',
#     order = 'viewCount',
#     maxResults = 5,
# ).execute()


#channelId

def set_video(word, maxCount):  
    print(f'Crawling Setting: {word}')
    
    print('Crawling START!')
  	# 먼저 search 함수를 통해 조회 수(viewCount)가 높은 영상을 파라미터로 받아 준 maxCount만큼 조회한다.
    search_response = youtube.search().list(
        q = word,
        order = 'viewCount',
        part = 'snippet',
        maxResults = maxCount
        ).execute()
    print('search_response DONE \n')
  
    # channel_response = youtube.channels().list(
    # part="statistics",
    # id=channelId
    # ).execute()  # 채널 정보를 가지고 오면 구독자를 가지고 올 수 있다. search()가 아닌 channels()로 조회해서 채널 정보를 조회한다.
    
    
    video_ids = []
    for i in range(0, len(search_response['items'])):
        video_ids.append((search_response['items'][i]['id']['videoId'])) # videoId의 리스트를 만들어 둔다 (videoId로 조회할 수 있게)
    print('making videoID list DONE \n')
  
  	# 추출할 정보의 list들과 그 모든 정보를 key-value로 저장할 딕셔너리 변수를 하나 생성한다.
    channel_video_id = []
    channel_video_title = []
    channel_rating_view = []
    channel_rating_comments = []
    channel_rating_good = []
    channel_published_date = []
    channel_thumbnails_url = []
    channel_video_description = []
    data_dicts = { }
    
    print("info extraction start")
    # 영상 이름, 조회수, 좋아요수 등 정보 등 추출
    for k in range(0, len(search_response['items'])):
        video_ids_lists = youtube.videos().list(
            part='snippet, statistics',
            id=video_ids[k],
        ).execute()
        
        # print(video_ids_lists)
    
        str_video_id = video_ids_lists['items'][0]['id']
        str_thumbnails_url = str(video_ids_lists['items'][0]['snippet']['thumbnails']['high'].get('url'))
        str_video_title = video_ids_lists['items'][0]['snippet'].get('title')
        str_view_count = video_ids_lists['items'][0]['statistics'].get('viewCount')
        str_video_description = video_ids_lists['items'][0]['snippet']['description']
        
        if str_view_count is None:
            str_view_count = "0"
        str_comment_count = video_ids_lists['items'][0]['statistics']['commentCount']
        if str_comment_count is None:
            str_comment_count = "0"
        str_like_count = video_ids_lists['items'][0]['statistics'].get('likeCount')
        if str_like_count is None:
            str_like_count = "0"
        if str_video_description is None:
            str_video_description = "No description"
        str_published_date = str(video_ids_lists['items'][0]['snippet'].get('publishedAt'))
        # str_subscriber_count = channel_response['items'][0]['statistics']['subscriberCount']
        # if str_subscriber_count is None:
        #     str_subscriber_count = "0"

        # 비디오 ID 
        channel_video_id.append(str_video_id)
        # 비디오 제목 
        channel_video_title.append(str_video_title)
        # 조회수 
        channel_rating_view.append(str_view_count)
        # 댓글수 
        channel_rating_comments.append(str_comment_count)
        # 좋아요 
        channel_rating_good.append(str_like_count)
        # 게시일 
        channel_published_date.append(str_published_date)
        # 썸네일
        channel_thumbnails_url.append(str_thumbnails_url)
        # 동영상 정보
        channel_video_description.append(str_video_description)


    data_dicts['id'] = channel_video_id
    data_dicts['title'] = channel_video_title
    data_dicts['viewCount'] = channel_rating_view
    data_dicts['commentCount'] = channel_rating_comments
    data_dicts['likeCount'] = channel_rating_good
    data_dicts['publishedDate'] = channel_published_date
    data_dicts['thumbnail'] = channel_thumbnails_url
    data_dicts['description'] = channel_video_description
    
    print("Making data dictionary DONE \n")
    print("Crawling DONE! \n \n")
    return data_dicts


# crawling
viral1 = set_video('모동숲 주민',  100)
viral2 = set_video('모동숲 주민 이사',  100)
viral3 = set_video('모동숲 인기 주민 공략', 100)
viral = set_video('모동숲',  100)
v = set_video('마일섬 주민', 200)
v_1 = set_video('마일섬 티켓', 200)


# 마일섬 티켓
d_1 = pd.DataFrame([v_1['id'], v_1['title'], v_1['viewCount'], v_1['commentCount'], 
                v_1['likeCount'], v_1['publishedDate'], v_1['thumbnail'], v_1['description']]).T

# 마일섬 주민
d = pd.DataFrame([v['id'], v['title'], v['viewCount'], v['commentCount'], 
                v['likeCount'], v['publishedDate'], v['thumbnail'], v['description']]).T

# 모동숲
df = pd.DataFrame([viral['id'], viral['title'], viral['viewCount'], viral['commentCount'], 
                    viral['likeCount'], viral['publishedDate'], viral['thumbnail'], viral['description']]).T

# 모동숲 주민
df1 = pd.DataFrame([viral1['id'], viral1['title'], viral1['viewCount'], viral1['commentCount'], 
                    viral1['likeCount'], viral1['publishedDate'], viral1['thumbnail'], viral1['description']]).T

# 모동숲 주민 이사
df2 = pd.DataFrame([viral2['id'], viral2['title'], viral2['viewCount'], viral2['commentCount'], 
                    viral2['likeCount'], viral2['publishedDate'], viral2['thumbnail'], viral2['description']]).T

# 모동숲 인기 주민 공략
df3 = pd.DataFrame([viral3['id'], viral3['title'], viral3['viewCount'], viral3['commentCount'], 
                    viral3['likeCount'], viral3['publishedDate'], viral3['thumbnail'], viral3['description']]).T


print("Dataframe Constructed DONE!")

# 열 이름 바꾸기
col_name = ["영상ID", "제목", "조회수", "댓글수", "좋아요수", "게시일", "썸네일", "영상설명"]
df.columns, df1.columns, df2.columns, df3.columns = col_name, col_name, col_name, col_name
d.columns, d_1.columns = col_name, col_name

print('----')
# 확인용
print(d.head(2))
print(df.head(2))
print(df1.head(2))
print(df2.head(2))
print(df3.head(2))
print(d.head(2))
print(d_1.head(2))
print('----')

print('Raw Data Concatenate Start!')

yt_raw_total = pd.concat([df, df1, df2, df3, d, d_1], axis=0)
yt_raw_total['바이럴지표'] = yt_raw_total['댓글수']+yt_raw_total['좋아요수']+yt_raw_total['조회수']
yt_raw_total.drop_duplicates(['영상ID'], keep='first', inplace=True)

print('\n Concatenate is Done, and making viral metric.')
print('Youtube Crawling FINISHED')

yt_raw_total.to_csv('../prep_data_files/youtube/yt_raw_total.csv', index=False, encoding='utf-8')