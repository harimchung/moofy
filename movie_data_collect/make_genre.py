import json

# tmdb 영화 장르 변환을 위한 딕셔너리
tmdb_movie_genres = {
    28 : '액션',
    12 : '모험',
    16 : '애니메이션',
    35 : '코미디',
    80 : '범죄',
    99 : '다큐멘터리',
    18 : '드라마',
    10751 : '가족',
    14 : '판타지',
    36 : '서사',
    27 : '공포',
    10402 : '뮤지컬',
    9648 : '미스터리',
    10749 : '로맨스',
    878 : 'SF',
    10770 : 'TV영화',
    53 : '스릴러',
    10752 : '전쟁',
    37 : '서부',
}

# tmdb_movie_genres = {

#     28: 'Action',
#     12: 'Adventure',
#     16: 'Animation',
#     35: 'Comedy',
#     80: 'Crime',
#     99: 'Documentary',
#     18: 'Drama',
#     10751: 'Family',
#     14: 'Fantasy',
#     36: 'History',
#     27: 'Horror',
#     10402: 'Music',
#     9648: 'Mystery',
#     10749: 'Romance',
#     878: 'Science Fiction',
#     10770: 'TV Movie',
#     53: 'Thriller',
#     10752: 'War',
#     37: 'Western',
# }


data = []

genre_id = 1

for key, value in tmdb_movie_genres.items():
    
    my_movie_genres = {}

    my_movie_genres['model'] = "movies.genre"

    my_movie_genres['pk'] = genre_id
    genre_id += 1

    my_movie_genres['fields'] = {
        'genre':value
    }

    data.append(my_movie_genres)

file_path = 'genre.json'

with open(file_path,'w', encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)

#load data

with open(file_path, "r", encoding="utf-8") as json_file:
    data_dict = json.load(json_file)
    print(data_dict)