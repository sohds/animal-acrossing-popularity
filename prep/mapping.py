def mapping_social(df, column_name):
    # 먼저 매핑을 수행, 문자열을 해당하는 값으로 변환
    #df[column_name] = df[column_name].replace(dict)
    # 매핑 후, 데이터 타입을 int로 변경
    
    dic = {
    '↓': 1,
    'Middel': 2,
    '↑': 3
}
    
    df[column_name] = df[column_name].astype(str).replace(dic)
    
    return df


def making_appear_possibility(df):
    num_villagers_species = 34
    
    # 'Bull'을 'Cow'로 치환
    df['Species'] = df['Species'].replace('Bull', 'Cow')
    species_name =  df['Species'].unique().tolist()
    in_df_species_count = dict(df['Species'].value_counts())
    
    real_species_in_ACNH = {'Cat': 23, 'Rabbit': 22, 'Frog': 18, 'Squirrel': 19, 'Duck': 17, 'Dog': 17, 'Cub': 17, 
                        'Pig': 15, 'Bear': 15, 'Mouse': 16, 'Horse': 15, 'Bird': 14, 'Penguin': 14, 'Sheep': 14, 
                        'Elephant': 12, 'Wolf': 11, 'Ostrich': 11, 'Deer': 12, 'Eagle': 10, 'Gorilla': 10, 'Chicken': 9, 
                        'Koala': 10, 'Goat': 8, 'Hamster': 9, 'Kangaroo': 8, 'Monkey': 9, 'Anteater': 8, 'Hippo': 7, 
                        'Tiger': 7, 'Alligator': 8, 'Lion': 7, 'Rhino': 7, 'Cow': 10, 'Octopus': 3}
    
    # 'Bull'을 'Cow'로 치환
    df['Species'] = df['Species'].replace('Bull', 'Cow')

    # Species 열의 값을 딕셔너리의 값으로 매핑하여 새로운 열 AP에 저장
    df['AP'] = df['Species'].map(real_species_in_ACNH)

    # AP 열을 계산
    df['AP'] = round(1/num_villagers_species * 1/df['AP'] * 100, 4)
    
    return df, species_name, in_df_species_count