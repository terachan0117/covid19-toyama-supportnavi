import sys
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# 富山県HPに掲載されている最新の支援情報を取得する
html = urlopen("http://www.pref.toyama.jp/sections/1118/virus/shien.html")
bsObj = BeautifulSoup(html, "html.parser")

# csvにするデータをここに追加していく
csv_lists = []

# ヘッダー追加
csv_list_header = [
    "psid",
    "serviceNumber",
    "provider",
    "theme",
    "name",
    "content.abstract",
    "content.provisions",
    "content.target",
    "content.application_start_date",
    "content.application_close_date",
    "content.how_to_apply",
    "content.url",
    "content.contact",
    "content.information_release_date",
    "tags",
    "updated_date"
]
csv_lists.append(csv_list_header)

tables = bsObj.findAll("table")
themes = bsObj.findAll("h5")

# テーブルごとにデータを追加していく
for table in range(len(tables)):
    # テーマはテーブルごとに割り当てられている
    theme = (themes[table].text + "（個人向け）") if (table < 4) else (themes[table].text + "（事業者向け）")
    # タグはテーブルナンバーで割り当てられる
    tag = ("個人向け") if (table < 4) else ("事業者向け")

    # テーブルの各行ごとに処理
    trs = tables[table].findAll("tr")
    for tr in range(len(trs)):
        # テーブルヘッダーは無視
        if tr > 0:
            tds = trs[tr].findAll("td")
            if len(tds) == 4 or len(tds) == 60: # 制度・内容・窓口・電話番号すべて揃っている場合(tr終了タグがない例外も含む)
                    if tds[0].text == '県営住宅家賃の減免及び徴収猶予': # 例外対応(td終了タグがない)
                        csv_list = [
                            "psid1.0+JA160008+" + str(10000000 + len(csv_lists)),
                            10000000 + len(csv_lists),
                            "",
                            theme,
                            tds[0].text,
                            tds[1].text,
                            "",
                            "",
                            "",
                            "",
                            "",
                            (tds[0].find('a').get('href')) if (len(tds[0].findAll('a')) > 0) else (""),
                            ('県建築住宅課（' + tds[3].text + '）') if (tds[3].text != '　') else (tds[2].text),
                            "",
                            tag,
                            ""
                        ]
                    else:
                        csv_list = [
                            "psid1.0+JA160008+" + str(10000000 + len(csv_lists)),
                            10000000 + len(csv_lists),
                            "",
                            theme,
                            tds[0].text,
                            tds[1].text,
                            "",
                            "",
                            "",
                            "",
                            "",
                            (tds[0].find('a').get('href')) if (len(tds[0].findAll('a')) > 0) else (""),
                            (tds[2].text + '（' + tds[3].text + '）') if (tds[3].text != '　') else (tds[2].text),
                            "",
                            tag,
                            ""
                        ]
                    csv_lists.append(csv_list)
            elif len(tds) == 3: # 内容・窓口・電話番号のみの場合
                csv_lists[len(csv_lists)-1][5] += '\n' + tds[0].text
                csv_lists[len(csv_lists)-1][12] += (', '+tds[1].text + '（' + tds[2].text + '）') if (tds[2].text != '　') else (', '+tds[1].text)
            elif len(tds) == 2: # 窓口・電話番号のみの場合
                if tds[0].text == '小学校休業等対応支援金（厚生労働省ホームページ）': # 例外対応(窓口・電話番号のみではない)
                    csv_list = [
                        "psid1.0+JA160008+" + str(10000000 + len(csv_lists)),
                        10000000 + len(csv_lists),
                        "",
                        theme,
                        tds[0].text,
                        tds[1].text,
                        "",
                        "",
                        "",
                        "",
                        "",
                        (tds[0].find('a').get('href')) if (len(tds[0].findAll('a')) > 0) else (""),
                        csv_lists[len(csv_lists)-1][12],
                        "",
                        tag,
                        ""
                    ]
                    csv_lists.append(csv_list)
                else:
                    csv_lists[len(csv_lists)-1][12] += (', '+tds[0].text + '（' + tds[1].text + '）') if (tds[1].text != '　') else (', '+tds[0].text)
            else:
                # 未知のエラーがあればデータ更新せず強制終了
                print('error: td len =', len(tds))
                print('table number=', table+1)
                print('tr number=', tr+1)
                sys.exit(1)

# 市町村の関連情報を追加
cities = [
    {
        "name": "富山市",
        "code": 162019,
        "url": "https://www.city.toyama.toyama.jp/shingatacorona/coronashieninfo.html"
    },
    {
        "name": "高岡市",
        "code": 162027,
        "url": "https://www.city.takaoka.toyama.jp/kenko/kenko/ryuko/covid-19.html"
    },
    {
        "name": "魚津市",
        "code": 162043,
        "url": "https://www.city.uozu.toyama.jp/event-topics/svTopiDtl.aspx?servno=6634"
    },
    {
        "name": "氷見市",
        "code": 162051,
        "url": "https://www.city.himi.toyama.jp/emergency/5496.html"
    },
    {
        "name": "滑川市",
        "code": 162060,
        "url": "https://www.city.namerikawa.toyama.jp/important_notice/5369.html"
    },
    {
        "name": "黒部市",
        "code": 162078,
        "url": "https://www.city.kurobe.toyama.jp/category/page.aspx?servno=19235"
    },
    {
        "name": "砺波市",
        "code": 162086,
        "url": "https://tonami-covid19.com/"
    },
    {
        "name": "小矢部市",
        "code": 162094,
        "url": "http://www.city.oyabe.toyama.jp/kinkyu/1582786672127.html"
    },
    {
        "name": "南砺市",
        "code": 162108,
        "url": "https://www.city.nanto.toyama.jp/cms-sypher/www/info/detail.jsp?id=22740"
    },
    {
        "name": "射水市",
        "code": 162116,
        "url": "https://www.city.imizu.toyama.jp/event-topics/svTopiDtl.aspx?servno=18796"
    },
    {
        "name": "舟橋村",
        "code": 163210,
        "url": "http://www.vill.funahashi.toyama.jp/"
    },
    {
        "name": "上市町",
        "code": 163228,
        "url": "https://www.town.kamiichi.toyama.jp/event-topics/svTopiDtl.aspx?servno=3210"
    },
    {
        "name": "立山町",
        "code": 163236,
        "url": "https://www.town.tateyama.toyama.jp/pub/event-topics/svTopiDtl.aspx?servno=8034"
    },
    {
        "name": "入善町",
        "code": 163422,
        "url": "https://www.town.nyuzen.toyama.jp/oshirase/info_korona.html"
    },
    {
        "name": "朝日町",
        "code": 163431,
        "url": "https://www.town.asahi.toyama.jp/kinkyujouhou/1608866639930.html"
    }
]
for city in range(len(cities)):
    csv_list = [
        "psid1.0+JA160008" + str(cities[city]["code"]) + "+" + str(10000000 + len(csv_lists)),
        10000000 + len(csv_lists),
        "",
        "市町村の関連情報",
        cities[city]["name"] + "の新型コロナウイルス感染症に関する支援情報",
        cities[city]["name"] + "における、新型コロナウイルス感染症に関する支援情報をご案内します。",
        "",
        "",
        "",
        "",
        "",
        cities[city]["url"],
        "",
        "",
        "市町村の関連情報\n" + cities[city]["name"],
        ""
    ]
    csv_lists.append(csv_list)

with open("../resources/services.csv", "w", encoding = "utf_8_sig", newline = "") as file:
    writer = csv.writer(file)
    writer.writerows(csv_lists)