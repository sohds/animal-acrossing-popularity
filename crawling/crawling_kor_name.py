# 라이브러리 임포트
import requests
import pandas as pd
from lxml import html


# 가지고 있는 동물 이름 리스트 (너무 많은데... 다 넣어주기보다는 그냥 df로 불러오는게 나을듯)
# names = ['Admiral' 'Agent S' 'Agnes' 'Al' 'Alfonso' 'Alice' 'Alli' 'Amelia' 'Anabelle' 'Anchovy' 'Angus' 'Anicotti' 'Ankha' 'Annalisa' 'Annalise' 'Antonio' 'Apollo' 'Apple' 'Astrid' 'Audie' 'Aurora' 'Ava' 'Avery' 'Axel'
#  'Baabara' 'Bam' 'Bangle' 'Barold' 'Bea' 'Beardo' 'Beau' 'Becky' 'Bella' 'Benedict' 'Benjamin' 'Bertha' 'Bettina' 'Bianca' 'Biff' 'Big Top' 'Bill' 'Billy' 'Biskit' 'Bitty' 'Blaire' 'Blanche' 'Bluebear' 'Bob' 'Bonbon'
#  'Bones' 'Boomer' 'Boone' 'Boots' 'Boris' 'Boyd' 'Bree' 'Broccolo' 'Broffina' 'Bruce' 'Bubbles' 'Buck' 'Bud' 'Bunnie' 'Butch' 'Buzz' 'Cally' 'Camofrog' 'Canberra' 'Candi' 'Carmen' 'Caroline' 'Carrie' 'Cashmere'
#  'Celia' 'Cesar' 'Chadder' 'Charlise' 'Cheri' 'Cherry' 'Chester' 'Chevre' 'Chief' 'Chops' 'Chow' 'Chrissy' 'Claude' 'Claudia' 'Clay' 'Cleo' 'Clyde' 'Coach' 'Cobb' 'Coco' 'Cole' 'Colton' 'Cookie' 'Cousteau' 'Cranston' 'Croque' 'Cube' 'Curlos' 'Curly' 'Curt' 'Cyd' 'Cyrano' 'Daisy' 'Deena'
#  'Deirdre' 'Del' 'Deli' 'Derwin' 'Diana' 'Diva' 'Dizzy' 'Dobie' 'Doc' 'Dom' 'Dora' 'Dotty' 'Drago' 'Drake' 'Drift' 'Ed' 'Egbert' 'Elise'
#  'Ellie' 'Elmer' 'Eloise' 'Elvis' 'Erik' 'Eugene' 'Eunice' 'Fang' 'Fauna' 'Felicity' 'Filbert' 'Flip' 'Flo' 'Flora' 'Flurry' 'Francine' 'Frank'
#  'Freckles' 'Freya' 'Friga' 'Frita' 'Frobert' 'Fuchsia' 'Gabi' 'Gala' 'Gaston' 'Gayle' 'Genji' 'Gigi' 'Gladys' 'Gloria' 'Goldie' 'Gonzo'
#  'Goose' 'Graham' 'Greta' 'Grizzly' 'Groucho' 'Gruff' 'Gwen' 'Hamlet' 'Hamphrey' 'Hans' 'Harry' 'Hazel' 'Henry' 'Hippeux' 'Hopkins' 'Hopper'
#  'Hornsby' 'Huck' 'Hugh' 'Iggly' 'Ike' 'Jacob' 'Jacques' 'Jambette' 'Jay' 'Jeremiah' 'Jitters' 'Joey' 'Judy' 'Julia' 'Julian' 'June' 'Kabuki'
#  'Katt' 'Keaton' 'Ken' 'Ketchup' 'Kevin' 'Kid Cat' 'Kidd' 'Kiki' 'Kitt' 'Kitty' 'Klaus' 'Knox' 'Kody' 'Kyle' 'Leonardo' 'Leopold' 'Lily'
#  'Limberg' 'Lionel' 'Lobo' 'Lolly' 'Lopez' 'Louie' 'Lucha' 'Lucky' 'Lucy' 'Lyman' 'Mac' 'Maddie' 'Maelle' 'Maggie' 'Mallary' 'Maple' 'Marcel'
#  'Marcie' 'Margie' 'Marina' 'Marshal' 'Mathilda' 'Megan' 'Melba' 'Merengue' 'Merry' 'Midge' 'Mint' 'Mira' 'Miranda' 'Mitzi' 'Moe' 'Molly' 'Monique' 'Monty' 'Moose' 'Mott' 'Muffy' 'Murphy' 'Nan' 'Nana' 'Naomi' 'Nate' 'Nibbles' 'Norma' "O'Hare" 'Octavian' 'Olaf' 'Olive' 'Olivia'
#  'Opal' 'Ozzie' 'Pancetti' 'Pango' 'Paolo' 'Papi' 'Pashmina' 'Pate' 'Patty' 'Paula' 'Peaches' 'Peanut' 'Pecan' 'Peck' 'Peewee' 'Peggy'
#  'Pekoe' 'Penelope' 'Phil' 'Phoebe' 'Pierce' 'Pietro' 'Pinky' 'Piper' 'Pippy' 'Plucky' 'Pompom' 'Poncho' 'Poppy' 'Portia' 'Prince' 'Puck'
#  'Puddles' 'Pudge' 'Punchy' 'Purrl' 'Queenie' 'Quillson' 'Raddle' 'Rasher' 'Raymond' 'Renée' 'Reneigh' 'Rex' 'Rhonda' 'Ribbot' 'Ricky' 'Rizzo'
#  'Roald' 'Robin' 'Rocco' 'Rocket' 'Rod' 'Rodeo' 'Rodney' 'Rolf' 'Rooney' 'Rory' 'Roscoe' 'Rosie' 'Rowan' 'Ruby' 'Rudy' 'Sally' 'Samson' 'Sandy'
#  'Savannah' 'Scoot' 'Shari' 'Sheldon' 'Shep' 'Sherb' 'Simon' 'Skye' 'Sly' 'Snake' 'Snooty' 'Soleil' 'Sparro' 'Spike' 'Spork' 'Sprinkle' 'Sprocket'
#  'Static' 'Stella' 'Sterling' 'Stinky' 'Stitches' 'Stu' 'Sydney' 'Sylvana' 'Sylvia' 'T-Bone' 'Tabby' 'Tad' 'Tammi' 'Tammy' 'Tangy' 'Tank' 'Tasha'
#  'Teddy' 'Tex' 'Tia' 'Tiffany' 'Timbra' 'Tipper' 'Tom' 'Truffles' 'Tucker' 'Tutu' 'Twiggy' 'Tybalt' 'Ursala' 'Velma' 'Vesta' 'Vic' 'Victoria'
#  'Violet' 'Vivian' 'Vladimir' 'Wade' 'Walker' 'Walt' 'Wart Jr.' 'Weber' 'Wendy' 'Whitney' 'Willow' 'Winnie' 'Wolfgang' 'Yuka' 'Zell' 'Zucker']

# 가지고 있는 영어 동물 이름 리스트
df = pd.read_excel("../prep_data_files/eng_kor_init.csv")
names = df['Name'].tolist()
print(names)

# 결과를 저장할 리스트
results = []
final = []



# 각 이름에 대해 반복하면서 크롤링 시작!
for name in names:
    print()
    print(name, "crawling START")
    url = f"https://animalcrossing.soopoolleaf.com/ko/acna/{name}/"
    response = requests.get(url)  # URL에서 페이지 내용 가져오기
    response.encoding = 'utf-8'


    # 페이지 로드가 성공했다면
    if response.status_code == 200:
        tree = html.fromstring(response.content)  # 페이지 내용을 lxml tree로 파싱
        # XPath를 사용하여 원하는 텍스트 추출
        text = tree.xpath('/html/body/div[4]/div/div[2]/div[3]/article/div[2]/table/thead/tr/th/span/text()')
        
        if text:
            print(name, 'of Korean Name is: ', text)
            results.append((name, text[0]))  # 결과 리스트에 추가
        
        else:
            results.append((name, "No data found"))  # 텍스트를 찾을 수 없는 경우
            print('no text in here')
    
    else:
        results.append((name, "Failed to load page"))  # 페이지 로드 실패 처리
        print('page cannot loaded')

    print(name, "crawling DONE!")
    print()
    
    
    
# 결과 출력 (로그 확인 차)
for result in results:
    print(result)
    final.append(result[1])
    
# 결과 Korean Name에 매핑
df['Korean Name'] = final
# 결과물 csv 파일로 저장
df.to_csv('../prep_data_files/crawled_kor_name.csv', index=False)
