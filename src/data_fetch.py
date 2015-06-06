import json
import numpy as np

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

        self.user_author = {}
        self.user_blog = {}
        self.user_post = {}

    def read_file(self, filename):
        f = open(filename, 'r')
        strf = f.read()
        strarr = strf.split('\n')

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

            self.post_list.add(post_id)
            self.blog_list.add(blog_id)
            self.author_list.add(author)

            users = v["likes"]
            for el in users:
                uid = el["uid"]

                if(self.user_post.has_key(uid)):
                    self.user_post[uid].append(dict(post=post_id, likes = 1))
                else:
                    self.user_post[uid] = []
                    self.user_post[uid].append(dict(post=post_id, likes = 1))



                if(self.user_blog.has_key(uid)):
                    if blog_id in self.user_blog[uid]:
                        self.user_blog[uid][blog_id]
                        self.user_blog[uid].append({blog_id:})
                else:
                    self.user_blog[uid] = []
                    self.user_blog[uid].append(dict(blog=blog_id, likes =1))



                if(self.user_author.has_key(uid)):
                    self.user_author[uid].append(dict(author=author, likes = 1))
                else:
                    self.user_author[uid] = []
                    self.user_author[uid].append(dict(author=author, likes = 1))


    def mat_initiate(self, column_list):
        # Initiate a matrix with dimensions from lists.
        dimx = len(self.user_list)
        dimy = len(column_list)

        self.ymat = np.zeros((dimx, dimy))

    def mat_update(self):
        # Update values in matrix
        f = open(filename, 'r')
        strf = f.read()
        strarr = strf.split('\n')

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

            self.post_list.add(post_id)
            self.blog_list.add(blog_id)
            self.author_list.add(author)

            users = v["likes"]
            for el in users:
                uid = el["uid"]
                self.user_list.add(uid)


        pass

    def print_lists(self):
        for k,v in self.user_post.iteritems():
            print unicode(k) + "--" + unicode(v)

        print len(self.author_list)


    pass


if __name__ == "__main__":
    USER_DATA_FILE = "../data/sample011.json" # 5000 lines from trainPosts

    c = DataFetch()
    c.read_file(USER_DATA_FILE)
    c.print_lists()