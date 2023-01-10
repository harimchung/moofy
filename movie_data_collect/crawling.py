#필요한 라이브러리

#import time #페이지 로드에 걸리는 시간조절
import json #데이터 저장

from selenium import webdriver
from bs4 import BeautifulSoup

import requests

date = ['20210101','20210110','20210120','20210130',
'20210201','20210210','20210220',
'20210301','20210310','20210320','20210330',
'20210401','20210410','20210420','20210430',
'20210501','20210510','20210520','20210530',
'20210601','20210610','20210620','20210630',
'20220101','20220110','20220120','20220130',
'20220201','20220210','20220220',
'20220301','20220310','20220320','20220330',
'20220401','20220410','20220420','20220430',
'20220501','20220510','20220520','20220530',
'20220601','20220610','20220620','20220630',
'20220701','20220710','20220720','20220730',
'20220801','20220810','20220820','20220830',
'20220901','20220910','20220920','20220930',
'20221001','20221010','20221020','20221030',
'20221101']

title_list = set()

for d in date:

    url = f'https://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=01d6af266369c5a5a496ef0f24fcff46&targetDt={d}'

    response = requests.get(url).json()

    for item in response['boxOfficeResult']['weeklyBoxOfficeList']:
        
        title_list.add(item['movieNm'])

print(title_list)
print(len(title_list))
# tmdb api => overview, poster_path, backdrop_path, popularity
# naver => 장르, 개봉일, 국가, 러닝타임, 관람등급, 전체평점, 나이대별 평점

#제어를 위한 웹 드라이버를 부른다.
path = 'chromedriver.exe' #basic directory
driver = webdriver.Chrome(path)

#네이버 영화페이지 로드
url = 'https://movie.naver.com/'
driver.get(url)

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
my_movie_genres = {}
genre_id = 1
for key, value in tmdb_movie_genres.items():
    my_movie_genres[value] = genre_id
    genre_id += 1

data_list = []
id = 1

for title in title_list:

    try:

        data = {}

        # API를 이용한 영화 검색

        tmdb_search_url = f'https://api.themoviedb.org/3/search/movie?api_key=ff4caacdbe9a0908cabba9596e863c7a&language=ko-KR&query={title}&page=1&include_adult=false/'
        
        try:

            response = requests.get(tmdb_search_url).json()['results'][0]
        
        except:

            continue


        ############################################################

        #영화검색창의 Xpath를 찾고 해당 태그를 찾는다.
        input_xpath = '//*[@id="ipt_tx_srch"]'
        input = driver.find_element_by_xpath(input_xpath)
        #영화제목을 넘겨준다
        # title = "공조2: 인터내셔날"
        #input.clear()
        input.click() #검색창을 클릭하고,
        input.send_keys(title) #검색창에 영화제목 입력

        #검색버튼의 xpath를 찾는다.
        search_button_xpath = '//*[@id="jSearchArea"]/div/button'
        search_button = driver.find_element_by_xpath(search_button_xpath)

        #버튼을 클릭하여 검색 수행
        search_button.click()
        #예시2확인

        ####################################################

        #첫번째 영화 제목 링크의 xpath를 찾는다
        try:
            first_title_xpath = '//*[@id="old_content"]/ul[2]/li[1]/dl/dt/a'
            first_title = driver.find_element_by_xpath(first_title_xpath)

            #제목을 클릭하고 상세정보로 들어간다.
            first_title.click()
            #예시3확인
        except:
            continue

        ###################################################

        #평점버튼을 찾고 클릭하여 평점 메뉴를 부른다.
        vote_button_xpath = '//*[@id="movieEndTabMenu"]/li[5]/a/em'
        vote_button = driver.find_element_by_xpath(vote_button_xpath)

        vote_button.click()

        #해당 페이지의 html 소스를 읽어온다.
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')

        # 영화 정보 박스를 태그를 이용해서 가져온다.
        movie_information = {
        'nation': '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[2]/a',
        'running_time' : '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[3]',
        # 'grade' : '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[4]/p/a',
        'year' : '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[4]/a[1]',
        'date' : '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[1]/p/span[4]/a[2]',
        }

        movie_information_list = {}
        movie_information_list['title'] = title

        year_date = ''

        try:

            for key,information in movie_information.items():
                
                movie_information_data = driver.find_element_by_xpath(information).text

                if key == 'running_time':

                    movie_information_list[key] = int(movie_information_data.rstrip()[:-1])
                
                elif key == 'year' or key == 'date':

                    year_date += movie_information_data
                
                else:

                    movie_information_list[key] = movie_information_data
        
        except:

            continue
            
            
        year_date = year_date.replace('.','-')


        movie_information_list['release_date'] = year_date

        #print(response)

        movie_information_list['overview'] = response['overview']

        my_genre = []
        # 장르를 순회해서 바꿔주기
        for genre in response['genre_ids']:
            my_genre.append(my_movie_genres[tmdb_movie_genres[genre]])

        movie_information_list['genre_ids'] = my_genre
        movie_information_list['poster_path'] = response['poster_path']
        movie_information_list['backdrop_path'] = response['backdrop_path']
        movie_information_list['popularity'] = float(response['popularity'])

        #태그를 이용해 관람객평점리스트를 찾는다.

        actual_vote_list = soup.find('div',{'id':'actual_point_tab_inner'}).find_all('em')

        #print(actual_vote_list)

        actual_vote = ''

        for tag in actual_vote_list[:4]:
            actual_vote += tag.get_text() #.get_text()하면 태그 내의 텍스트를 가져옴

        #print(actual_vote)

        movie_information_list['actual_vote_average'] = float(actual_vote) 

        #태그를 이용해 나이대별 평점?

        age_vote_list = soup.find_all('strong',{'class':'graph_point'})

        movie_information_list['man_vote'] = float(age_vote_list[7].get_text()) 
        movie_information_list['woman_vote'] = float(age_vote_list[8].get_text()) 
        movie_information_list['vote_10'] = float(age_vote_list[9].get_text()) 
        movie_information_list['vote_20'] = float(age_vote_list[10].get_text()) 
        movie_information_list['vote_30'] = float(age_vote_list[11].get_text()) 
        movie_information_list['vote_40'] = float(age_vote_list[12].get_text()) 
        movie_information_list['vote_50'] = float(age_vote_list[13].get_text())

        ##관람등급

        transform_grade = {
            '전체 관람가':0,
            '12세 관람가':1,
            '15세 관람가':2,
            '청소년 관람불가':3,
            '제한상영가':4,
            '등급보류':5
        }

        try:

            information = '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[3]/p/a'

            movie_information_data = driver.find_element_by_xpath(information).text

            movie_information_list['grade'] = transform_grade[movie_information_data]
        
        except:
            

            information = '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[4]/p/a'

            movie_information_data = driver.find_element_by_xpath(information).text

            movie_information_list['grade'] = transform_grade[movie_information_data]
        

        ##출연배우

        try:

            information = '//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[3]/p'

            movie_information_data = driver.find_element_by_xpath(information)

            movie_information_list['actors'] = movie_information_data.text
        
        except:

            movie_information_list['actors'] = ''

        

        #print(age_vote)
        #예시4확인

        data['model'] = 'movies.movie'
        data['pk'] = id
        id += 1
        data['fields'] = movie_information_list

        data_list.append(data)

    except:

        continue

################################################
# 수집한 데이터 저장

# 방법은 여러가지
# pandas의 csv로 저장할수도 있고, pickle로 저장할수도 있고
#  일단 여기서는 json으로 저장

#data = {'actual_vote':actual_vote, 'age_vote':age_vote}

print(len(data_list))

file_path = 'data_200.json'

with open(file_path,'w', encoding="utf-8") as f:
    json.dump(data_list, f, ensure_ascii=False)

#load data

# with open(file_path, "r", encoding="utf-8") as json_file:
#     data_dict = json.load(json_file)
#     print(data_dict)

'''

'''