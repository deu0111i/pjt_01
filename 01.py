# 1. 50주차 불러오기
import csv
import requests
from decouple import config
from datetime import timedelta, datetime
from pprint import pprint


result = {}

for i in range(1):

	#1-1. 필수요청 쿼리 준비(key, targetDt)
    key = config('API_KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')
    

		# timedelta(weeks=i) -> i 이전의 시각을 구함(seconds, hours, days, weeks 가능)
		# 2019년 7월 13일을 기준으로 계속 1주일 전을 의미함(07-13 -> 07-06...)
		# weeks=1은 1주전 시각을 구함
		

	#1-2. 요청 보내고 json -> dict로 변환
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&key={key}&targetDt={targetDt}'
    api_data = requests.get(url).json()
    # pprint(api_data)


	#1-3. 주간/주말 박스오피스 데이터 리스트로 가져오기(movies -> list)
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    # pprint(movies)

	#1-4. 영화 대표코드(movieCd), 영화명(mvoieNm), 해당일 누적관객수(audiAcc) 준비
    for movie in movies:
        code = movie.get('movieCd')
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면, 
        # 그게 가장 마지막 주 데이터가,. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
        if code not in result:
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'), 
                'audiAcc': movie.get('audiAcc'),
            }

# pprint(result)

	#1-5. 영화정보가 담긴 딕셔너리(movie)에서 영화 대표 코드를 추출
		# movieCd(실제 movieCd코드)가 딕셔너리의 key가 되고 
		# movieCd / movieNm / audiAcc) -> 필드: movieCd / mmovieNm / audiAcc -> 값}
		



# 2. 결과 저장하기
with open('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
		
	#2-1. 저장할 데이터들의 필드 이름을 미리 지정한다.
    fieldnames = ('movieCd', 'movieNm', 'audiAcc') # 필드 -> 리스트, 튜플 모두  가능
    writer = csv.DictWriter(f, fieldnames=fieldnames)
		
	#2-2. 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader()

	#2-3. 반복을 돌며 value 값들을 해당 필드의 row에 작성한다.
    for value in result.values(): 
        print(value)
        writer.writerow(value)
