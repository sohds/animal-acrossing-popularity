from googleapiclient.discovery import build
from collections import defaultdict
import json
import pandas as pd
import re

with open('youtube_api.json', 'r', encoding='utf8') as f:
    data = json.load(f)
    print(data)

youtube = build(data['YOUTUBE_API_SERVICE_NAME'], data['YOUTUBE_API_SERVICE_VERSION'], developerKey = data['API_KEY'])


# excel 파일 로드
video_file_path = '../prep_data_files/youtube/yt_villagervideo_wlog.csv'
name_file_path = '../prep_data_files/handwriting_exist_before.csv'

video_data = pd.read_csv(video_file_path)
name_data = pd.read_csv(name_file_path)

# 'Korean Name' 열의 고유 값 리스트로 추출
korean_names = name_data['Korean Name'].unique()

# 이름 카운트를 위한 딕셔너리 초기화
name_count = defaultdict(int)
viral_score_dict = defaultdict(float)

# 댓글 데이터 프레임 초기화
comment_df = pd.DataFrame(columns=['Korean Name', 'Mention Count', 'Viral'])


print("Initialize DONE!")

# Youtube Comments Crawling & add to DataFrame
def count_names_in_comments(video_id, name_list, log_bv):
    next_page_token = None
    mentioned_names = set()  # 언급된 이름을 추적하기 위한 set 초기화

    try:
        print()
        print(f"Crawling START: {video_id}")
        while True:
            comment_response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            for item in comment_response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

                # 댓글 내에서 각 이름이 단어 단위로 언급된 경우 set에 추가
                for name in name_list:
                    # 정규 표현식을 사용하여 전체 단어로만 이루어진 경우를 찾음
                    if re.search(r'\b' + re.escape(name) + r'\b', comment):
                        mentioned_names.add(name)
                        name_count[name] += 1  # 언급된 횟수를 카운트
            
            next_page_token = comment_response.get('nextPageToken')
            if not next_page_token:
                break
        
    except Exception as e:
        print(f"Error processing video ID {video_id}: {e}")

    print("Crawling DONE!")
    print("\n Calculate the VIRAL Metric")
    
    # 언급된 주민 이름에 대해 로그 바이럴 지표 누적
    for name in mentioned_names:
        viral_score_dict[name] += log_bv

# 모든 비디오 ID에 대해 이름 언급 횟수와 바이럴 점수 계산
for index, row in video_data.iterrows():
    count_names_in_comments(row['영상ID'], korean_names, row['로그_바이럴지표'])
    

print("ALL Crawling is finally COMPLETE.")

# 결과 데이터 프레임 생성
for name, count in name_count.items():
    try:
        comment_df = comment_df.append({
            'Korean Name': name,
            'Mention Count': count,
            'Viral': viral_score_dict[name]
        }, ignore_index=True)
    
    except:
        comment_df.loc[len(comment_df)] = [name, count, viral_score_dict[name]]


# 결과 데이터 프레임을 Excel 파일로 저장
comment_df.to_csv('../prep_data_files/youtube/final_comment_data_with_viral.csv', index=False, encoding='utf-8')
print()
print("Results saved.")