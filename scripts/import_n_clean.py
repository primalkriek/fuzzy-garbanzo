import pandas as pd

#  Reading, cleaning & preprocessing users
all_users = pd.read_csv('../data/users.csv', encoding="windows-1252", sep="|")
all_users['gender'] = all_users['gender'].str.replace('female', 'F')
all_users['gender'] = all_users['gender'].str.replace('male', 'M')

#  Reading, cleaning & preprocessing clicks
all_clicks = pd.read_csv('../data/clicks.csv', encoding="windows-1252", sep=";")
all_clicks['website'] = all_clicks['website'].str.replace('http://', '')

# Reading, cleaning & preprocessing websites
all_websites = pd.read_csv('../data/websites.csv', encoding="windows-1252", sep=",")

#  Reading, cleaning & preprocessing ads
all_ads = pd.read_excel('../data/ads.xlsx')

# create a seperate DF for de target_age verification and clean this
unique_target_age = pd.DataFrame(all_ads['target_age'].unique())
unique_target_age = unique_target_age.set_axis(['target_age'], axis=1)
unique_target_age[['lower', 'upper']] = unique_target_age['target_age'].str.split('-', expand=True)
unique_target_age.iloc[4, 1:2] = unique_target_age.iloc[4, :1].str.replace('+','')
unique_target_age.iloc[4, 2:3] = unique_target_age.iloc[4, 2:3].isnull()
unique_target_age.iloc[4, 2:3] = unique_target_age.iloc[4, 2:3].astype(int)
unique_target_age.iloc[4, 2:3]= 120
unique_target_age.iloc[:,1:3] = unique_target_age.iloc[:,1:3].astype('int')

# add target age to the users table
for id, record in unique_target_age.iterrows():
    all_users.loc[all_users['age'].between(record.loc['lower'],record.loc['upper']), 'user_age_intervals_ad'] = record.loc['target_age']

# merge the datasets, to create 1 DF and clean
clicks_n_users= all_users.merge(all_clicks, left_on='id',right_on='user_id')
clicks_n_users_n_ads = clicks_n_users.merge(all_ads, left_on='ad_id', right_on='id')
clicks_n_users_n_ads_n_websites = clicks_n_users_n_ads.merge(all_websites, left_on='website', right_on='url', how='left')
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.rename(columns = {'age':'user_age_exact'})
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.rename(columns = {'target_age_x':'target_age_ad'})
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.rename(columns = {'target_age_y':'target_age_website'})
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.rename(columns = {'category_y':'category_website'})
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.rename(columns = {'category_x':'category_ads'})
clicks_n_users_n_ads_n_websites =clicks_n_users_n_ads_n_websites.drop(columns = {'id_x','id_y'})
