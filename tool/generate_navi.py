import csv
import pandas as pd

df = pd.read_csv("../resources/services.csv", encoding="utf_8_sig")

df_group = df.groupby('theme', sort=False)

groups = df_group.groups

theme_lists = list(groups.keys())
psid_lists = []

for group in groups:
    psid_lists.append(df_group.get_group(group).loc[:,["psid"]].to_dict(orient='list')["psid"])


csv_lists = []

csv_list = [
    "質問",
    "",
    "",
    "",
    ""
]
csv_lists.append(csv_list)
csv_list = [
    "メモ（表示されません）",
    "ID",
    "質問",
    "回答",
    "次"
]
csv_lists.append(csv_list)
csv_list = [
    "",
    0,
    "どのような対象者への支援情報をお探しですか？",
    "",
    ""
]
csv_lists.append(csv_list)
csv_list = [
    "",
    "",
    "",
    "事業者向け",
    1
]
csv_lists.append(csv_list)
csv_list = [
    "",
    "",
    "",
    "個人向け",
    2
]
csv_lists.append(csv_list)

for theme in range(len(theme_lists)):
    if theme_lists[theme] != '市町村の関連情報':
        # 個人向け
        if theme == 0:
            csv_list = [
                "",
                2,
                "どのようなテーマの支援情報をお探しですか？",
                "",
                ""
            ]
            csv_lists.append(csv_list)
        # 事業者向け
        if theme == 4:
            csv_list = [
                "",
                1,
                "どのようなテーマの支援情報をお探しですか？",
                "",
                ""
            ]
            csv_lists.append(csv_list)
        
        csv_list = [
            "",
            "",
            "",
            theme_lists[theme],
            theme + 3
        ]
        csv_lists.append(csv_list)

csv_list = [
    "",
    "",
    "",
    "",
    ""
]
csv_lists.append(csv_list)

csv_list = [
    "結果",
    "",
    "",
    "",
    ""
]
csv_lists.append(csv_list)
csv_list = [
    "メモ（表示されません）",
    "ID",
    "タイトル",
    "制度ID",
    ""
]
csv_lists.append(csv_list)


for theme in range(len(theme_lists)):
    if theme_lists[theme] != '市町村の関連情報':
        csv_list = [
            "",
            theme + 3,
            "",
            "\n".join(psid_lists[theme]),
            ""
        ]
        csv_lists.append(csv_list)

with open("../resources/navi.csv", "w", encoding="utf_8_sig", newline="") as file:
    writer = csv.writer(file)
    writer.writerows(csv_lists)