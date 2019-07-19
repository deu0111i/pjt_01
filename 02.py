import requests
from decouple import config
import csv
from pprint import pprint
from datetime import datetime, timedelta


result = []
box = {}

for i in range(100):
    with open('boxOffice.csv', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row['movieCd']
            result.append(code)

    key = config('API_KEY')
    movie_code = result[i]


    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movie_code}'
    api_data = requests.get(url).json()

    movies = api_data.get('movieInfoResult').get('movieInfo')


    for movie in movies:
        code = movies.get('movieCd')
        box[code] = {
            'movieCd': movies.get('movieCd'),
            'movieNm': movies.get('movieNm'),
            'movieNmEn': movies.get('movieNmEn'),
            'movieNmOg': movies.get('movieNmOg'),
            'audits': movies.get('audits')[0].get('watchGradeNm') if movies.get('audits') else None,  
            'openDt': movies.get('openDt'),
            'showTm': movies.get('showTm'),           
            'genres': movies.get('genres')[0].get('genreNm') if movies.get('genres') else None,         
            'directors': movies.get('directors')[0].get('peopleNm') if movies.get('directors') else None
            }
    pprint(box)

    with open('movie.csv', 'w', newline='', encoding='utf-8') as f:
        fieldnames = ('movieCd', 'movieNm', 'movieNmEn', 'movieNmOg', 'audits', 'openDt', 'showTm', 'genres', 'directors')
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()

        for value in box.values():
            writer.writerow(value)