__author__ = 'jason'


def fscore(test_file, true_file):
    test = open(test_file, "r")
    true = open(true_file, "r")
    test_line = test.readline()
    true_line = true.readline()
    true_positive = 0
    false_positive = 0
    false_negative = 0
    while test_line and true_line:
        predicted = int(test_line.split()[2])
        actual = int(true_line.split()[2])
        if predicted == 1:
            if actual == 0:
                false_positive += 1
            else:
                true_positive += 1
        else:
            if actual == 1:
                false_negative += 1

        test_line = test.readline()
        true_line = true.readline()
    precision = (true_positive/(true_positive+false_positive))
    recall = (true_positive/(true_positive+false_negative))
    fscore = 2*precision*recall/(precision+recall)

    return "precision = {}\nrecall = {}\nfscore = {}\n".format(precision, recall, fscore)


def mean_avg_p(test_file, true_file):
    test = open(test_file, "r")
    true = open(true_file, "r")
    user_purchase_dict_test = {}
    user_purchase_dict_actual = {}

    for line in test.readlines():
        user, item, purchase, ranking = line.split()
        #user, item, ranking = line.split() # lena mode
        if user_purchase_dict_test.get(user):
            user_purchase_dict_test[user].append((item, ranking))
        else:
            user_purchase_dict_test[user] = [(item, ranking)]

    outfile_new = open("o.txt", "w+")
    acc = []
    for user, purchases in user_purchase_dict_test.items():
        acc.append(["{} {} {}\n".format(user, item[0], item[1]) for item in zip(map(lambda x: x[0], sorted(purchases, key=lambda x: x[1], reverse=True)), range(1, len(purchases)+1))])

    for list in acc:
        for item in list:
            outfile_new.write(item)
    outfile_new.close()

    test = open("o.txt", "r")
    user_purchase_dict_test = {}
    for line in test.readlines():
        user, item, ranking = line.split()
        if user_purchase_dict_test.get(user):
            user_purchase_dict_test[user][item] = ranking
        else:
            user_purchase_dict_test[user] = {item: ranking}

    for line in true.readlines():
        user, item, purchase, ranking = line.split()
        if int(purchase):
            if user_purchase_dict_actual.get(user):
                user_purchase_dict_actual[user][item] = ranking
            else:
                user_purchase_dict_actual[user] = {item: ranking}

    overall_sum = 0
    for user, purchases in user_purchase_dict_actual.items():
        second_multiplier = 1/len(purchases)
        sum_thingy = 0
        for item in purchases.keys():
            actual_rank = int(user_purchase_dict_actual[user][item])
            predicted_rank = int(user_purchase_dict_test[user][item])
            print(actual_rank, predicted_rank)
            sum_thingy += actual_rank/predicted_rank
        overall_sum += second_multiplier*sum_thingy

    first_multiplier = 1/len(user_purchase_dict_actual)
    _map = overall_sum * first_multiplier
    return str(_map)



#mean_avg_p("outfile.txt", "testing_data.txt")