import pickle
import random
import json
from data_fetch import DataFetch
from average_precision import mapk, apk

__author__ = 'rakshit'


USER_AUTHOR = "user_author.p"
USER_BLOG = "user_blog.p"
USER_TAGS = "user_tags.p"
USER_LANGUAGE = "user_language.p"


class Predictions:
    def __init__(self):

        self.df = DataFetch()

        self.ua = self.df.load_data(USER_AUTHOR)
        self.ub = self.df.load_data(USER_BLOG)
        self.ut = self.df.load_data(USER_TAGS)
        self.ul = self.df.load_data(USER_LANGUAGE)

        self.posts = pickle.load(open("posts_dict_complete.p", "rb"))


        self.a_coef = 0.33
        self.b_coef = 0.33
        self.t_coef = 0.33


    def no_logic(self, test_sample):
        # Operate on values without any modification of weights.
        threshold = 0.00072
        predicted_list = []

        for (i,j,b,a,t,l) in test_sample:
            U = str(i)
            post = str(j)
            try:
                P = self.posts[post]
                A = self.posts[post]["author"] if not None else 0
                B = self.posts[post]["blog"] if not None else 0
                T = self.posts[post]["tags"] if not None else 0

                a_val = 0.0 + self.ua[U][A]
                b_val = 0.0 + self.ub[U][B]
                t_val = 0.0
                for tag in T:
                    try:
                        t_val+= 0.0 + self.ut[U][tag]
                    except:
                        t_val+= 0.0

            except:
                print "In except"
                A = a
                B = b
                T = t

                try:
                    a_val = 0.0 + self.ua[U][A]
                except:
                    a_val = 0.0

                try:
                    b_val = 0.0 + self.ub[U][B]
                except:
                    b_val = 0.0

                t_val = 0.0
                try:
                    for tag in T:
                        try:
                            t_val+= 0.0 + self.ut[U][tag]
                        except:
                            t_val+= 0.0
                except:
                    t_val+=0.0




            print "Values for a_val {}, b_val {} and t_val {}".format(a_val,b_val,t_val)
            val = 0.0 + (self.a_coef * a_val) + (self.b_coef * b_val) + (self.t_coef * t_val)

            if val>threshold:
                label = 1
            else:
                label = 0

            predicted_list.append((i,j,l,label))

        return predicted_list


def generate_test_sample():

    filename = "test_sample.txt"
    test_sample = []
    f = open(filename, "r")
    for i in f:
        isplit = i.split()
        u = isplit[0]
        p = isplit[1]
        l = isplit[2]

        test_sample.append((u,p,l))

    return test_sample


def new_test(filename):
    f = open(filename, 'r')
    strf = f.read()
    strarr = strf.split('\n')
    strarr = strarr[50002:70000]

    test_sample = []

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

        users = v["likes"]
        for el in users:
            uid = el["uid"]

            # Create test files
            if random.randint(1,10)>7:
                # Add entry into test list
                test_sample.append((uid,post_id,blog_id, author, tags,1))
    return test_sample

if __name__=="__main__":

    TEST_SAMPLE = [(31367867,1329369)]
    POST_DATA_FILE = "../data/trainPosts.json"

    c = Predictions()
    TEST_SAMPLE = new_test(POST_DATA_FILE)
    predicted_list = c.no_logic(TEST_SAMPLE)

    actual = []
    predicted = []

    for (i,j,l,label) in predicted_list:
        actual.append(l)
        predicted.append(label)

    map_val = apk(actual,predicted,100)

    print "Mean Average Precision at 10"
    print map_val

