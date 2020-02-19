from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .forms import *
from .models import Lecture,Profile,Lecture_img
from django.forms import modelformset_factory

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            newUser = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            Profile.objects.create(user = newUser)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')

def upload(request):
    if Profile.objects.filter(user=request.user):
        Profile_filter=Profile.objects.filter(user=request.user)
        ImageFormSet=modelformset_factory(Lecture_img,form=Lecture_imgForms, extra=3)
        if request.method == 'POST':

            LectureForm = LectureForms(request.POST)
            Imageform = ImageFormSet(request.POST,request.FILES,queryset=Lecture_img.objects.none())


            if LectureForm.is_valid() and Imageform.is_valid():
                LectureForm_title=LectureForm.cleaned_data.get('title')
                LectureForm_description=LectureForm.cleaned_data.get('description')
                LectureForm = LectureForm.save(commit=False)
                LectureForm.author = Profile_filter[0] 
                LectureForm.save()

                for form in Imageform.cleaned_data:
                    image = form['image']
                    photo = Lecture_img(LectureKey=LectureForm , image=image)
                    photo.save()
                photo_filter=Lecture_img.objects.filter(LectureKey=LectureForm)

                return render(request, 'lecture.html',{"photo":photo_filter , 'title':LectureForm_title , "description":LectureForm_description})          
            else:
                print(LectureForm.errors, Imageform.errors)
        else:
            LectureForm = LectureForms()
            Imageform = ImageFormSet(queryset=Lecture_img.objects.none())
        return render(request, 'upload.html',{'LectureForm': LectureForm, 'Imageform': Imageform})

'''List_object_Lecture=[]
List_object_image={}
List_object_image_value_dirt=[]
List_name_img=[]


def upload(request):
    V=0
    found=""
    if Profile.objects.filter(user=request.user):
        Profile_filter=Profile.objects.filter(user=request.user)
        if request.method == 'POST' and 'uploadbutton' in request.POST:
            LectureForms_upload=LectureForms(request.POST)
            Lecture_imgForms_upload = Lecture_imgForms(request.POST,request.FILES)
            if LectureForms_upload.is_valid() and  Lecture_imgForms_upload.is_valid() and request.FILES :
                title_name=LectureForms_upload.cleaned_data.get("title")
                for i in List_object_Lecture:
                    if str(i)==title_name:
                        found=str(i)
                        V+=1

                if V>0 :
                    Lec=LectureForms_upload.save(commit=False)
                    Lec.author=Profile_filter[0]
                    Saveimg=Lecture_imgForms_upload.save()
                    List_object_image_value_dirt.append(Saveimg)
                    #Saveimg.LectureKey=Lec
                    #List_object_image.update({title_name:List_object_image_value_dirt.append(Saveimg)})

                else:
                    Lec=LectureForms_upload.save(commit=False)
                    Lec.author=Profile_filter[0]
                    List_object_Lecture.append(Lec)
                    Saveimg=Lecture_imgForms_upload.save()
                    #Saveimg.LectureKey=Lec
                    List_object_image_value_dirt.append(Saveimg)
                List_name_img.append(Lecture_imgForms_upload.cleaned_data.get("image").name)
                List_object_image.update({title_name:List_object_image_value_dirt})
                return render(request, 'upload.html',{'Image':Lecture_imgForms_upload , 'Lecture':LectureForms_upload, 'L':List_object_Lecture ,"I":List_name_img})
        elif request.method == 'POST' and 'submitbutton' in request.POST:
            
            LectureForms_upload_1=LectureForms(request.POST)
            
            if LectureForms_upload_1.is_valid():
                if List_object_Lecture:
                    title_name=LectureForms_upload_1.cleaned_data.get('title')
                    for i in List_object_Lecture:
                        if str(i)==title_name:
                            i.save()
                            
                            if List_object_image:
                                for P in List_object_image:
                                    if P == title_name:
                                        L=List_object_image[P]
                                        for M in L:
                                            M.LectureKey=i
                                            M.save()
                                List_object_image.pop(title_name)
                            List_object_Lecture.remove(i)
                
            Obj_Lec=Lecture.objects.filter(title=LectureForms_upload_1.cleaned_data.get('title'))
            Img_obj=Lecture_img.objects.all().filter(LectureKey=Obj_Lec[0])
            List_object_Lecture.clear()
            List_object_image.clear()
            List_object_image_value_dirt.clear() 
            List_name_img.clear()
            return render(request, 'lecture.html',{"Lecture_img":Img_obj, 'Lecture':LectureForms_upload_1 })
        else:
            Lecture_imgForms1=Lecture_imgForms()
            LectureForms1=LectureForms()
            return render(request, 'upload.html',{'Image':Lecture_imgForms1 , 'Lecture':LectureForms1})'''

            


def lecture(request,lectue_id):
    pass

def profile(request, username):
    userObj = User.objects.get(username = username)
    profileObj = Profile.objects.get(user = userObj)
    if request.method == 'POST':
        form=Profileform(request.POST , request.FILES)
        if form.is_valid():
            profileObj.profilePicture = form.cleaned_data.get('profilePicture')
            profileObj.save()
            
            return HttpResponseRedirect("/profile/"+username)
    else:
        form=Profileform()
    return render(request,'profile.html',{'form': form, 'profile': profileObj})

