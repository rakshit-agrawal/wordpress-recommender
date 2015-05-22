#!/usr/authoral/bin/python3

###############################
'''
This script will extract data from testPosts and test Users json files and then push it into the database.

First, testPosts would be extracted and all posts will get entered into Posts database. Tags and Categories get entries through posts entries only.

Then, each user will be extracted and inserted into Users database, and based on user's likes, entries into LikeMatrix will be done simultaneously.



'''
###############################



import json
import numpy as np


class Users:

	counter = 0
	indx = None
	
	bigElement = {}
	postsList = []
	userList = []

	pk_id = 0
	uid = 0
	user_in_test = False
	likes_count = 0
	extra = ''
	likes = []
	ymat = []
	
	def __init__(self):

		Users.counter = Users.counter + 1
		Users.bigElement = {}
		self.pk_id = Users.counter

	def ClassTransfer(self, pki, pju):
	

	
		if pju['uid']!=None:
			self.uid = pju['uid']

		if pju['inTestSet']!=None:
			self.user_in_test = pju['inTestSet']

	

		if pju['likes']!=None:
			self.likes = pju['likes']
			self.likes_count = len(self.likes)

	


		self.pk_id = pki				
			
		#self.updateDataset()

		Users.userList.append(int(self.uid))

		self.postsListUpdater()

		#self.PrintDetails()

		

	def PrintDetails(self):

		print("~~~~~~~~~~~~~~~~~~~~~~~~")
		print("\Post details:\n")
		print("\nUID: " + str(self.uid))
		for i in self.likes:
			print("\n\tLikes: " + str(i['post_id']))
		#print("\nUser in Test: " + str(self.user_in_test))
		

	def updateDataset(self):
	
		Users.bigElement[int(self.uid)] = {}
	
		for i in self.likes:
			Users.bigElement[int(self.uid)][int(i['post_id'])]= (1)

	
	def postsListUpdater(self):

		for i in self.likes:
			if int(i['post_id']) in Users.postsList:
				#print("Already there")
				cnt =1
			else:
				#print("New Entry")
				Users.postsList.append(int(i['post_id']))	
				#print(Users.postsList)


	def matInitiate(self):

		dimx = len(Users.userList)
		dimy = len(Users.postsList)

		self.ymat = np.zeros((dimx,dimy))

		#print("empty ymat")
		#print(self.ymat)



	def matUpdate(self,pki, pju):

		
		if pju['uid']!=None:
			self.uid = pju['uid']

		if pju['likes']!=None:
			self.likes = pju['likes']
			self.likes_count = len(self.likes)
	
		valx = Users.userList.index(int(self.uid))

		for i in self.likes:
			valy = Users.postsList.index(int(i['post_id']))

			self.ymat[valx][valy] = 1
		
	
		#print("updated ymat")
		#print(self.ymat)
		



class UserOperations:

	ulist = []
	plist = []

	def ParseOps(self, listlen):

		filestr = "../data/trainUsersSplits/data_" + str(listlen)

		#f_users = open('../Data/trainUsersSplits/aa_01','r')

		f_users = open(filestr,'r')

		strf2 = f_users.read()

		strarr2 = strf2.split('\n')
	
		parsed_json_users = []


		usersElement = Users()


		for j in range(len(strarr2)-1):

			parsed_json_users.append(json.loads(strarr2[j]))

			usersElement.ClassTransfer(j, parsed_json_users[j])

		usersElement.matInitiate()


		for j in range(len(strarr2)-1):

			parsed_json_users.append(json.loads(strarr2[j]))

			usersElement.matUpdate(j, parsed_json_users[j])


		#print("Final ymat: " + str(usersElement.ymat))
		print("Length of User list: " + str(len(usersElement.userList)))
		print("Length of Post list: " + str(len(usersElement.postsList)))
		#print (usersElement.bigElement)
		#print (usersElement.postsList)

		#x = numpy.array(usersElement.bigElement)

		#print(x)

		#return(usersElement.bigElement)

		self.ulist = usersElement.userList
		self.plist = usersElement.postsList

		return(usersElement.ymat)

if __name__ == "__main__":

	print("In user load 03")
	userOps = UserOperations()
	userOps.ParseOps()


