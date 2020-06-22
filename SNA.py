import tweepy
import pandas as pd

def lookup_user_list(user_id_list, api):
    full_users = []
    users_count = len(user_id_list)
    try:
        for i in range(int(users_count / 100) + 1):
            print (i)
            full_users.extend(api.lookup_users(user_ids=user_id_list[i * 100:min((i + 1) * 100, users_count)]))
        return full_users
    except tweepy.TweepError:
        print ('Something went wrong, quitting...')

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def get_influences(user):
    
    ids = []
    for page in tweepy.Cursor(api.followers_ids, screen_name=user).pages():
        ids.extend(page)

        results = lookup_user_list(ids, api)
        all_users = [{'id': user.id,
             'Name': user.name,
             'Statuses Count': user.statuses_count,
             'Friends Count': user.friends_count,
             'Screen Name': user.screen_name,
             'Followers Count': user.followers_count,
             'Location': user.location,
             'Description': user.description}
             for user in results]

        df = pd.DataFrame(all_users)
        file_name = user + "_influences " + ".csv"
        df.to_csv(file_name,index=False, encoding='utf-8')
#print(df.head())

        df1 = df[df['Description'].str.contains("Professor")]
        file_name_imp_contacts = user +"_imp_influences"+ ".csv"
        df1.to_csv(file_name_imp_contacts,index=False, encoding='utf-8')
#print (df1.head(5))
#df1.to_csv('Imp_Contacts.csv', index=False, encoding='utf-8')
        
get_influences("nitiniitk")

def get_influencers(user):
    
    ids = []
    for page in tweepy.Cursor(api.friends_ids, screen_name=user).pages():
        ids.extend(page)

        results = lookup_user_list(ids, api)
        all_friends = [{'id': user.id,
             'Name': user.name,
             'Statuses Count': user.statuses_count,
             'Friends Count': user.friends_count,
             'Screen Name': user.screen_name,
             'Followers Count': user.followers_count,
             'Location': user.location,
             'Description': user.description}
             for user in results]

        df3 = pd.DataFrame(all_friends)
        file_name = user +"_influencers "+ " .csv"
        df3.to_csv(file_name,index=False, encoding='utf-8')
        df4 = df3[df3['Description'].str.contains("Professor")]
        file_name_imp_contacts = user +"_imp_influencers"+ ".csv"
        df4.to_csv(file_name_imp_contacts,index=False, encoding='utf-8')
    
get_influencers("nitiniitk")





























