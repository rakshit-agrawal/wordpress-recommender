import json
import os
import random
from string import lower
from datetime import datetime
import numpy as np
import pickle

__author__ = 'rakshit'

"""
File for data fetch operations
"""


def normalize_dict(data_dict):
    new_dict = {}
    for k,v in data_dict.iteritems():
        sum = 0
        new_dict[k] = {}
        if v is not None:
            for j,b in v.iteritems():
                sum+=b
            for j,b in v.iteritems():
                b = 0.0 + (0.0 + b/(0.0 + sum))
                new_dict[k][j] = b
    return new_dict


class DataFetch:


    POST_DATA_FILE = "../data/trainPosts.json"

    NVAL = 50000 # To limit data


    def __init__(self):
        self.user_list = set()
        self.post_list = set()
        self.blog_list = set()
        self.author_list = set()
        self.tag_list = set()

        self.user_author = {}
        self.user_blog = {}
        self.user_post = {}
        self.user_tags = {}
        self.user_language = {}

        self.posts_dict = {}

        self.test_sample = []

    def check_pickles(self):
        # Check for existence of pickles
        pass
    
    def load_data(self, datafile):
        if datafile == "user_author.p":
            if os.path.isfile("user_author.p"):
                print("loading <user_author> from datastore")
                user_author = pickle.load(open("user_author.p", "rb"))
                print("data loaded")
                return user_author
            else:
                print("generating <user_author>")
                self.read_file(self.POST_DATA_FILE,type="author")
                print("dumping to data store")
                self.user_author = normalize_dict(self.user_author)
                pickle.dump(self.user_author, open("user_author.p", "wb"))
                print("data dumped")
                return self.user_author

        elif datafile == "user_blog.p":
            if os.path.isfile("user_blog.p"):
                print("loading <user_blog> from datastore")
                user_blog = pickle.load(open("user_blog.p", "rb"))
                print("data loaded")
                return user_blog
            else:
                print("generating <user_blog>")
                self.read_file(self.POST_DATA_FILE,type="blog")
                self.user_blog = normalize_dict(self.user_blog)
                print("dumping to data store")
                pickle.dump(self.user_blog, open("user_blog.p", "wb"))
                print("data dumped")
                return self.user_blog

        elif datafile == "user_tags.p":
            if os.path.isfile("user_tags.p"):
                print("loading <user_tags> from datastore")
                user_tags = pickle.load(open("user_tags.p", "rb"))
                print("data loaded")
                return user_tags
            else:
                print("generating <user_tags>")
                self.read_file(self.POST_DATA_FILE,type="tags")
                self.user_tags = normalize_dict(self.user_tags)
                print("dumping to data store")
                pickle.dump(self.user_tags, open("user_tags.p", "wb"))
                print("data dumped")
                return self.user_tags


        elif datafile == "user_language.p":
            if os.path.isfile("user_language.p"):
                print("loading <user_language> from datastore")
                user_language = pickle.load(open("user_language.p", "rb"))
                print("data loaded")
                return user_language
            else:
                print("generating <user_language>")
                self.read_file(self.POST_DATA_FILE,type="tags")
                self.user_language = normalize_dict(self.user_language)
                print("dumping to data store")
                pickle.dump(self.user_language, open("user_language.p", "wb"))
                print("data dumped")
                return self.user_language


    def read_file(self, filename, type):
        f = open(filename, 'r')
        strf = f.read()
        strarr = strf.split('\n')
        NVAL = self.NVAL
        if NVAL:
            strarr = strarr[:NVAL]
        #self.file_parse(strarr)


    #def file_parse(self, strarr):

        for i,v in enumerate(strarr):
            # Extract elements from json here.
            try:
                v = json.loads(v)
            except:
                continue
            #print v
            post_id = v["post_id"]
            blog_id = v["blog"]
            author = v["author"]
            tags = v["tags"]
            language = v["language"]

            self.posts_dict[post_id] = {}
            #self.posts_dict[post_id]["blog"] = blog_id
            #self.posts_dict[post_id]["author"] = author
            #self.posts_dict[post_id]["tags"] = tags
            self.posts_dict[post_id] = v

            self.post_list.add(post_id)
            self.blog_list.add(blog_id)
            self.author_list.add(author)


            for i in tags:
                tag = lower(i)
                self.tag_list.add(tag)

            users = v["likes"]
            for el in users:
                uid = el["uid"]

                # Create test files
                #if random.randint(1,10)>8:
                    # Add entry into test list
                #    self.test_sample.append((uid,post_id,1))

                if type=="blog":

                    if(self.user_blog.has_key(uid)):
                        if blog_id in self.user_blog[uid]:
                            self.user_blog[uid][blog_id]+=1
                        else:
                            self.user_blog[uid][blog_id] = 1
                    else:
                        self.user_blog[uid] = {}
                        self.user_blog[uid][blog_id] = 1

                elif type=="language":

                    if(self.user_language.has_key(uid)):
                        if language in self.user_language[uid]:
                            self.user_language[uid][language]+=1
                        else:
                            self.user_language[uid][language] = 1
                    else:
                        self.user_language[uid] = {}
                        self.user_language[uid][language] = 1

                elif type=="author":

                    if(self.user_author.has_key(uid)):
                        if author in self.user_author[uid]:
                            self.user_author[uid][author]+=1
                        else:
                            self.user_author[uid][author] = 1
                    else:
                        self.user_author[uid] = {}
                        self.user_author[uid][author] = 1

                elif type=="tags":

                    if(self.user_tags.has_key(uid)):
                        for tag in tags:
                            try:
                                tag = lower(tag)
                                if tag in self.user_tags[uid]:
                                    self.user_tags[uid][tag]+=1
                                else:
                                    self.user_tags[uid][tag] = 1
                            except Exception, e:
                                pass
                    else:
                        for tag in tags:
                            try:
                                tag = lower(tag)
                                self.user_tags[uid] = {}
                                self.user_tags[uid][tag] = 1
                            except Exception,e:
                                pass

        # Put posts_dict into a pickle
        pickle.dump(self.posts_dict, open("posts_dict.p", "wb"))






    def create_post_dict(self, filename):
        f = open(filename, 'r')
        strf = f.read()
        strarr = strf.split('\n')

        st1 = strarr[:200]
        posts_dict = {}
        for i,v in enumerate(st1):
            # Extract elements from json here.
            try:
                v = json.loads(v)
            except:
                continue

            post_id = v["post_id"]
            blog_id = v["blog"]
            author = v["author"]
            tags = v["tags"]

            posts_dict[post_id] = {}
            posts_dict[post_id]["blog"] = blog_id
            posts_dict[post_id]["author"] = author
            posts_dict[post_id]["tags"] = tags

        pickle.dump(posts_dict, open("posts_dict_complete.p", "wb"))




    def mat_initiate(self, column_list):
        # Initiate a matrix with dimensions from lists.
        dimx = len(self.user_list)
        dimy = len(column_list)

        self.ymat = np.zeros((dimx, dimy))


    def print_lists(self):
        for k,v in self.user_blog.iteritems():
            print unicode(k) + "--" + unicode(v)

        print len(self.author_list)


    def write_test_to_file(self):
        filename = "test_sample.txt"
        f = open(filename, "w")
        for (i,j,l) in self.test_sample:
            f.write(str(i) + " " + str(j) + " " + str(l))
            f.write("\n")



if __name__ == "__main__":
    POST_DATA_FILE = "../data/trainPosts.json"

    NVAL = 50000 # To limit data

    USER_AUTHOR = "user_author.p"
    USER_BLOG = "user_blog.p"
    USER_TAGS = "user_tags.p"

    c = DataFetch()
    #c.read_file(POST_DATA_FILE)

    t1 = datetime.now()
    c.create_post_dict(POST_DATA_FILE)

    #data_dict = c.load_data(USER_TAGS)
    #normal_dict = normalize_dict(data_dict)
    t2 = datetime.now()
    #for k,v in data_dict.iteritems():
    #    print k
    #    print v
    #print len(data_dict)
    print "time taken" + str(t2-t1)

    #c.write_test_to_file()

    #print c.posts_dict
    #c.print_lists()
