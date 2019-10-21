# Get instance
import instaloader
import json
import bson
import pymongo
from pymongo import MongoClient 
from bson import json_util
from bson.json_util import dumps


L = instaloader.Instaloader(max_connection_attempts=0)
# Login or load session
username = ''
password = ''
L.login(username, password)        #(login)

#mongo db
client = MongoClient()
myclient = MongoClient('localhost', 27017)
mydb = myclient["instagram_crawler"] #db name

# Obtain profile metadata
instagram_target = 'instaunjcrawl'
profile = instaloader.Profile.from_username(L.context, instagram_target)
instagram_target_copy = instagram_target 
print("Now Logged in as : " + username)
def get_instagram_post(profile):
    mycoll1 = mydb["insta_post"] #collection name for mongodb
    file1 = open("json_output_" + instagram_target + ".json", "w+")
    memory1 = []
    count_post = 1
    print("Mengekstrak post - post dari akun " + instagram_target + " :")
    for post in profile.get_posts():
            print(instagram_target, str(count_post), '/', str(profile.mediacount))
            if post.caption == None:
                captionn = " "
                post_caption = captionn
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments1 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    memory_comments1.append(data_commentt)
                data = {"account": instagram_target, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments1,
                        "shortcode": post_shortcode
                        }
                #Write it in mongodb format
                #Remove a document if its already on the collection
                query_check = {"shortcode" : post_shortcode }
                mycoll1.delete_one(query_check)
                #Insert the new document to the collection
                mycoll1.insert_one(data)

                #Append to list
                memory1.append(data)
                count_post += 1
            else:
                count_post += 1
                caption = post.caption

                #Remove spasi \n dan backslash dalam string
                captionn = caption.replace('\n', ' ').replace('\\', ' ')
                #captionn = re.sub('\\\\', '', captionn)

                #Remove huruf non alphabetic dan emoticon 
                post_caption = captionn.encode('ascii', 'ignore').decode('ascii')
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments11 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    memory_comments11.append(data_commentt)
                data = {"account": instagram_target, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments11,
                        "shortcode": post_shortcode
                        }
                #Write it in mongodb format
                #Remove a document if its already on the collection
                query_check = {"shortcode" : post_shortcode }
                mycoll1.delete_one(query_check)
                #Insert the new document to the collection
                mycoll1.insert_one(data)

                #Append to list
                memory1.append(data)
                
    #Write it in JSON using BSON
    x = json_util.dumps(memory1)
    file1.write(x)
    file1.close()

def get_instagram_follower_post(profile):
    mycoll2 = mydb["insta_follower_post"]
    file2 = open("json_output_" + instagram_target + "_followers.json", "w+")
    memory2 = []
    for follower in profile.get_followers(): 
        username = follower.username
        profile_dump = instaloader.Profile.from_username(L.context, username)
        count_post = 1
        print("Akun " + username + " :")
        for post in profile_dump.get_posts():
            print(username, str(count_post), '/', str(profile_dump.mediacount))
            if post.caption == None:
                captionn = " "
                post_caption = captionn
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments2 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    memory_comments2.append(data_commentt)
                data = {"account": instagram_target, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments2,
                        "shortcode": post_shortcode
                        }
                #Write it in mongodb format
                #Remove a document if its already on the collection
                query_check = {"shortcode" : post_shortcode }
                mycoll2.delete_one(query_check)
                #Insert the new document to the collection
                mycoll2.insert_one(data)

                #Append to list
                memory2.append(data)
                count_post += 1
            else:
                count_post += 1
                caption = post.caption
                captionn = caption.replace('\n', ' ').replace('\\', ' ')
                #captionn = re.sub('\\\\', '', captionn)
                post_caption = captionn.encode('ascii', 'ignore').decode('ascii')
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments22 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    #data_commentt = re.sub('\\\\', '', data_comment)
                    memory_comments22.append(data_commentt)
                data = {"account": username, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments22,
                        "shortcode": post_shortcode
                        }
                memory2.append(data)
                query_check = {"shortcode" : post_shortcode }
                mycoll2.delete_one(query_check)
                mycoll2.insert_one(data)
    y = json_util.dumps(memory2)
    file2.write(y)
    file2.close()


def get_follower_layer1(profile):
    print("------------------- Layer 1 Follower ----------------------------")
    get_instagram_follower_post(profile)

def get_follower_layer2(profile):
    follower_list = []
    for followers in profile.get_followers():
        username = followers.username
        follower_list.append(username)
    print("------------------- Layer 2 Follower ----------------------------")
    print("Follower " + instagram_target_copy + " : " + str(follower_list))
    for user_acc in follower_list:
        #print(user_acc)
        instagram_target = user_acc
        new_profile = instaloader.Profile.from_username(L.context, instagram_target)
        print("Mengekstrak post - post dari follower akun : " + user_acc)
        get_instagram_follower_post(new_profile)

def get_tagged_instagram_post(profile):
    mycoll3 = mydb["insta_tagged_post"] #collection name for mongodb
    file3 = open("json_output_" + instagram_target + "_tagged_post.json", "w+")
    memory3 = []
    count_list = []
    count_post = 1
    print("Mengekstrak tagged post dari akun " + instagram_target + " :")
    for posts in profile.get_tagged_posts():
        count_list.append(posts)
    byk_post_tagged = len(count_list)

    for post in profile.get_tagged_posts():
            print(instagram_target, str(count_post), '/', str(byk_post_tagged))
            if post.caption == None:
                captionn = " "
                post_caption = captionn
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments3 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    memory_comments3.append(data_commentt)
                data = {"account": instagram_target, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments3,
                        "shortcode": post_shortcode
                        }
                #Write it in mongodb format
                #Remove a document if its already on the collection
                query_check = {"shortcode" : post_shortcode }
                mycoll3.delete_one(query_check)
                #Insert the new document to the collection
                mycoll3.insert_one(data)

                #Append to list
                memory3.append(data)
                count_post += 1
            else:
                count_post += 1
                caption = post.caption

                #Remove spasi \n dan backslash dalam string
                captionn = caption.replace('\n', ' ').replace('\\', ' ')
                #captionn = re.sub('\\\\', '', captionn)

                #Remove huruf non alphabetic dan emoticon 
                post_caption = captionn.encode('ascii', 'ignore').decode('ascii')
                post_hashtag = post.caption_hashtags #list str
                post_likes = post.likes #int
                post_comments = post.get_comments()
                post_shortcode = post.shortcode
                memory_comments33 = []
                for post_comment in post_comments:
                    data_comment = post_comment.text.encode('ascii', 'ignore').decode('ascii')
                    data_commentt = data_comment.replace('\\', ' ')
                    memory_comments33.append(data_commentt)
                data = {"account": instagram_target, 
                        "post":post_caption, 
                        "tag":post_hashtag, 
                        "likes":str(post_likes), 
                        "comments":memory_comments33,
                        "shortcode": post_shortcode
                        }
                #Write it in mongodb format
                #Remove a document if its already on the collection
                query_check = {"shortcode" : post_shortcode }
                mycoll3.delete_one(query_check)
                #Insert the new document to the collection
                mycoll3.insert_one(data)

                #Append to list
                memory3.append(data)
                
    #Write it in JSON using BSON
    z = json_util.dumps(memory3)
    file3.write(z)
    file3.close()

#get_instagram_post(profile) #Get Instagram User Post 
#get_follower_layer1(profile) #Get the post of each layer 1 follower of Instagram User
#get_follower_layer2(profile) #Get the post of each layer 2 follower of Instagram User
#get_tagged_instagram_post(profile)