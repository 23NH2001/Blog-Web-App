# Importing Required Lib

from sqlite3 import Date
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import models,logout,login,authenticate
from Blog.models import user_model,blog_model
import smtplib

def SendEmail(fname,lname,user_email,query):
    
    sender = 'hinguneveel@gmail.com'
    receivers = [user_email]

    message = f"""From:<{0}>
    To:<{1}>
    Subject: Message from {2} {3}

    {4}
    """
    message.format(sender,receivers,fname,lname,query)
    try:
        smtpObj = smtplib.SMTP('127.0.0.1')
        smtpObj.sendmail(sender, receivers, message)         
        print("Successfully sent email")
    except Exception as e:
        print(f"Error: unable to send email\nError: {e}")

''' 
? Home Page 
'''
def index(request):
    # If any user try to enter the website without login then it will be redirect to the login page for crediantial
    if request.user.is_anonymous:
        return redirect("/login")

    # This will fetch the email address from the blo_model as per request.user(means the current login user)
    data = user_model.objects.filter(email=request.user) 
    
    # This will fetch data from blog_model database in which the visibility is "ON", in New First order
    if request.method == "POST":
        query = request.POST.get("query")
        query=query.capitalize()
        public_blogs = blog_model.objects.filter(visibility=True,title=query).order_by('pub_Date')[::-1]
    else:
        public_blogs = blog_model.objects.filter(visibility=True).order_by('pub_Date')[::-1]

    #  Soring data and public_blog wariable in dictionary which we will sent to the Homepage.html
    data = {'user':data,'blogs':public_blogs}

    # Now Rendering "Homepage.html" alone with sending data to the html page        
    return render( request, "Homepage.html",data)
    
# About Page
def aboutPage(request):
    return render(request,"AboutPage.html")

# Contact Page 
def contactPage(request):
    if request.method=="POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        query = request.POST.get("query")
        try:
            SendEmail(fname,lname,email,query)
        except:
            print("Unable to send")
    return render(request,"contactPage.html")


# New user Page
def register_new_user(request):

    # While Register new user we have used "form" in html file with "POST" method, so any user press submit after filling all the required information then it will controll by this function.
    if request.method == "POST":
        # Fetching data from html page in which user input it's data in form.
        fname = request.POST.get('fname') # request.POST.get('fname') - ('fname') is the name of html element.
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneNumber = request.POST.get('Phone_number')
        userImage = request.POST.get('user_image')
        
        # Here we are creating a user with django built-in User model
        user = models.User.objects.create_user(username=email,password=password,first_name=fname,last_name=lname,email=email)

        # Here we are creating a user with custom made user_model
        userModel = user_model(fname=fname,lname=lname,profile_image=userImage,email=email,phoneNumber=phoneNumber,password=password)
        
        # Saving User Data in model and in both user model (built-in and custom model). 
        user.save()
        userModel.save()
        
        # Redirect to login page
        return redirect("/login")
        # Rendering RegisterNewUser.html
    return render(request,'RegisterNewUser.html')


# Login Page
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        authUser = authenticate(username=email,password=password)
        if authUser is not None:
            login(request,authUser)
            return redirect('/')
    return render(request,'LoginPage.html')


# Logout Page
def logout_user(request):
    logout(request)
    return redirect('/login')



# Blog Page
def blogPage(request):
    # Try to go blog page without login 
    if request.user.is_anonymous:
        return redirect("/login")
    user_model_details = user_model.objects.filter(email=request.user)
    
    # Save blog
    if request.method=='POST':
        SaveBlog(request)

    # Delete Blog
    if request.method=="GET":
        deleteBlog(request)
    blog_model = fetchBlogs(request)
    data={
        'user':user_model_details,
        'blog':blog_model
        }

    return render(request,'MyBlog.html',data)


def fetchBlogs(request):
    user_blogs = blog_model.objects.filter(user_email=request.user).order_by('pub_Date')[::-1]
    return user_blogs
    
def SaveBlog(request):
    blog_title = request.POST.get("blog_title")
    blog_image = request.POST.get("blog_image")
    blog_description = request.POST.get("blog_description")
    blog_visibility = True if request.POST.get("isVisible")=='on' else False
    blog_brief = shortDescrition(blog_description)
    blog_pub_date = Date.today()
    blog = blog_model(
        user_email= request.user,
        title = blog_title,
        brief=blog_brief,
        discription = blog_description,
        visibility = blog_visibility,
        blogImage = blog_image,  
        pub_Date = blog_pub_date
    )
    blog.save()

def EditBlog(request):
    blog_id = request.POST.get("blog_id")
    blog_title = request.POST.get("blog_title")
    blog_description = request.POST.get("blog_description")
    blog_visibility = True if request.POST.get("isVisible")=='on' else False
    blog_brief = shortDescrition(blog_description)
    blog_pub_date = Date.today()
    blogModel = blog_model.objects.filter(user_email=request.user)

    for data in blogModel:

        if data.blog_id == int(blog_id):
            data.title = blog_title
            data.brief = blog_brief
            data.discription = blog_description
            data.visibility = blog_visibility
            data.pub_Date = blog_pub_date
            data.save()
    return redirect("/myblog")

def shortDescrition(paragraph):
    if len(paragraph)<=50:
        return paragraph
    else:
        return paragraph[:50]+'....'

def deleteBlog(request):
    blog_id = request.GET.get('delete')
    blog_model.objects.filter(blog_id=blog_id).delete()
    return redirect("/myblog")


def ReadMoreBlog(request):
    editable = False
    if request.method=='POST':
        print("Hello")
        EditBlog(request)
        
    if request.method=='GET':    
        blog_id = request.GET.get('blog_id_btn')
        user_blogs = blog_model.objects.filter(blog_id=blog_id)
        user_blogs2 = blog_model.objects.filter(blog_id=blog_id).values('user_email')
        for i in user_blogs2:
            editable = (str(i['user_email']) == str(request.user))

        
    return render(request,"ReadMorePage.html",{"data":user_blogs,"editable":editable})

    

