import json
import os
from string import lower
from datetime import datetime
import numpy as np
import pickle

__author__ = 'rakshit'

"""
File for data fetch operations
"""


class DataFetch:

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
                self.read_file(POST_DATA_FILE,type="author")
                print("dumping to data store")
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
                self.read_file(POST_DATA_FILE,type="blog")
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
                self.read_file(POST_DATA_FILE,type="tags")
                print("dumping to data store")
                pickle.dump(self.user_tags, open("user_tags.p", "wb"))
                print("data dumped")
                return self.user_tags


    def read_file(self, filename, type):
        f = open(filename, 'r')
        strf = f.read()
        strarr = strf.split('\n')
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

            self.post_list.add(post_id)
            self.blog_list.add(blog_id)
            self.author_list.add(author)

            for i in tags:
                tag = lower(i)
                self.tag_list.add(tag)

            users = v["likes"]
            for el in users:
                uid = el["uid"]

                if type=="blog":

                    if(self.user_blog.has_key(uid)):
                        if blog_id in self.user_blog[uid]:
                            self.user_blog[uid][blog_id]+=1
                        else:
                            self.user_blog[uid][blog_id] = 1
                    else:
                        self.user_blog[uid] = {}
                        self.user_blog[uid][blog_id] = 1
                        
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
                            tag = lower(tag)
                            if tag in self.user_tags[uid]:
                                self.user_tags[uid][tag]+=1
                            else:
                                self.user_tags[uid][tag] = 1
                    else:
                        for tag in tags:
                            tag = lower(tag)
                            self.user_tags[uid] = {}
                            self.user_tags[uid][tag] = 1



    def mat_initiate(self, column_list):
        # Initiate a matrix with dimensions from lists.
        dimx = len(self.user_list)
        dimy = len(column_list)

        self.ymat = np.zeros((dimx, dimy))


    def print_lists(self):
        for k,v in self.user_blog.iteritems():
            print unicode(k) + "--" + unicode(v)

        print len(self.author_list)


    pass


if __name__ == "__main__":
    POST_DATA_FILE = "../data/sample011.json" # 5000 lines from trainPosts

    c = DataFetch()
    #c.read_file(POST_DATA_FILE)
    t1 = datetime.now()
    data_dict = c.load_data("user_tags.p")
    t2 = datetime.now()
    for k,v in data_dict.iteritems():
        print k
        print v
    print "time taken" + str(t2-t1)
    #c.print_lists()