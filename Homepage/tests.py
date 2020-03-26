from Homepage.models import *
from django.contrib.auth.models import User
from django.shortcuts import render
from django.test import TestCase
from .forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.core.files import File
from sandslecture.settings import BASE_DIR

class HomePageTest(TestCase):

    def test_adding_new_model_Profile(self):
        password = 'newPassword'
        newUser = User.objects.create_user('newUser', password)
        newProfile = Profile()
        newProfile.user = newUser
        newProfile.save()
        self.assertEqual('newUser',newProfile.user.username)
        
    def test_saving_and_retrieving_lecture_title(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.title, 'The first (ever) lecture title')
        self.assertEqual(secondLecture.title, 'lecture title the second')

    def test_saving_lecture_id_auto_increment_start_at_1(self):
        firstLecture = Lecture()
        firstLecture.title = 'The first (ever) lecture title'
        firstLecture.save()

        secondLecture = Lecture()
        secondLecture.title = 'lecture title the second'
        secondLecture.save()

        lectures = Lecture.objects.all()
        self.assertEqual(lectures.count(), 2)

        firstLecture = lectures[0]
        secondLecture = lectures[1]
        self.assertEqual(firstLecture.id, 1)
        self.assertEqual(secondLecture.id, 2)

    def test_upload_pic_Profile(self):
        c = Client()
        form=Profileform()
        localtion=BASE_DIR
        Tim=User.objects.create_user(username='Timmy',password='2542')
        ProfileTim=Profile.objects.create(user=Tim)
        response = c.post('/profile/'+str(ProfileTim)+'/', {'profilePicture':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) 
        Count_object=Profile.objects.filter(id=1)[0].profilePicture 

        self.assertNotEquals(Count_object,"<ImageFieldFile: None>")





    def test_submit_Lecture(self):
        c = Client()
        
        localtion=BASE_DIR
        Tim=User.objects.create_user(username='Timmy',password='2542')
        ProfileTim=Profile.objects.create(user=Tim)
        self.client.post('/accounts/login/', {'username':'Timmy','password':"2542" } ) 
        self.client.post('/upload/', {'title':'tim','description':"555" ,'image':SimpleUploadedFile('666.png', content=open(localtion+'/red.png', 'rb').read())} ) 
        CountLec=Lecture.objects.count()
        Count_object=Lecture_img.objects.count()

        self.assertEqual(CountLec,1)
        self.assertEqual(Count_object,1)


    def test_upload_Muti_Pic_Lecture(self):
        c=Client()
        localtion=BASE_DIR
        Tim=User.objects.create_user(username='tim',password='pass')
        ProfileTim=Profile.objects.create(user=Tim)

        self.client.post('/accounts/login/', {'username':'tim','password':"pass" } ) 
        self.client.post('/upload/', {'submitbutton':'Submit','title':'tim','description':"555" ,'image':{SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read()),SimpleUploadedFile('666_1.png', content=open(localtion+'/red.png', 'rb').read())}} )
        self.assertEqual(Lecture.objects.count(),1)
        self.assertEqual(Lecture_img.objects.count(),2)

    
    def test_counting_saves(self):
        creator = User.objects.create_user(username = 'tim01',password = 'pass')
        userB = User.objects.create_user(username = 'tim21',password = 'pass')
        userA = User.objects.create_user(username = 'tim11',password = 'pass')
        creatorProfile = Profile.objects.create(user = creator)
        
        userAProfile = Profile.objects.create(user = userA)
        
        userBProfile = Profile.objects.create(user = userB)
        noteObj = Lecture.objects.create(title = 'test', description = 'test',author = creatorProfile)
        
        useA=noteObj.userSaved.add(userAProfile)
        
        self.assertEqual(noteObj.userSaved.count(),1)
        useB=noteObj.userSaved.add(userBProfile)
        
        self.assertEqual(noteObj.userSaved.count(),2)


       