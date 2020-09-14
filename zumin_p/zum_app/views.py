from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'home.html')

def welcome(request,id):
    context = {
            'one_user': User.objects.get(id=id),
        }
    return render(request, 'welcome.html', context)

def one_user(request,id):
    context = {
            'one_user': User.objects.get(id=id),
            'all_props': Property.objects.all(),
        }
    return render(request, 'user.html', context)


def one_prop(request,id):
    context = {
        'prop': Property.objects.get(id=id),
        'one_user': User.objects.get(id=id),
        'all_props': Property.objects.all(),
    }
    return render(request, 'one_prop.html', context)

def tenant(request,id):
    context = {
            'tenant': User.objects.get(id=id),
            'all_props': Property.objects.all(),
            'prop': Property.objects.get(id=id),
        }
    return render(request, 'tenant.html', context)

def tenant_oneprop(request,id):
    context = {
            'prop': Property.objects.get(id=id),
            'all_props': Property.objects.all(),
            'one_user': User.objects.get(id=id),
        }
    return render(request, 'tenant_oneprop.html', context)

def profile(request,id):
    context = {
            'one_user': User.objects.get(id=id),
            'all_props': Property.objects.all(),
        }
    return render(request, 'my_profile.html', context)


def edit_prof(request, id):
    context = {
            'one_user': User.objects.get(id=id),
        }
    return render(request, 'edit.html', context)


#REGISTRATION

def register(request):
    if request.method == 'POST':
        errors = User.objects.basic_val(request.POST)
        if len(errors) > 0:
            for key, values in errors.items():
                messages.error(request, values)
            return redirect('/')
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash)
        request.session['name'] = new_user.first_name 
        request.session['last_name'] = new_user.last_name 
        request.session['email'] = new_user.email 
        request.session['user_id']= new_user.id
        return redirect(f'/welcome/{new_user.id}')
    return redirect('/')


def login(request):
    if request.method == 'POST':
        logged_user = User.objects.filter(email=request.POST['email'])
        if len(logged_user) > 0:
            logged_user = logged_user [0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['name'] = logged_user.first_name 
                request.session['last_name'] = logged_user.last_name 
                request.session['email'] = logged_user.email 
                request.session['user_id'] = logged_user.id
                return redirect(f'/welcome/{logged_user.id}')
    return redirect('/')   

def logout(request):
    request.session.flush()
    return redirect('/')


def new_prop(request):
    user = User.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        _, file = request.FILES.popitem()
        file = file[0]
        new_property= Property.objects.create(title=request.POST['title'], description=request.POST['description'], price=request.POST['price'], property_type=request.POST['property_type'], n_bedrooms=request.POST['n_bedrooms'], n_bathrooms=request.POST['n_bathrooms'], location=request.POST['location'], landlord=User.objects.get(id=request.session['user_id']),prop_image=file)
        print('New prop')
        request.session['name'] = new_property.title
        request.session['prop_id'] = new_property.id
    return redirect(f'/user/{one_user.id}')

def search(request):    
    context = {
        'prop': Property.objects.filter(location=request.POST['location']),
    }

    return render (request,'tenant.html')
    
def post(request):
        file_model = FileModel()
        _, file = request.FILES.popitem()
        file = file[0]

        file_model.file = file
        file_model.save()

        return HttpResponse(content_type='text/plain', content='File uploaded')

def delete_prop(request,id):
    Property.objects.get(id=id).delete()
    return redirect(f'/user/{id}')

def apply_prop(request,id):
    prop_applied = Property.objects.get(id=id)
    new_tenant = User.objects.get(id=request.session['user_id'])
    prop_applied.new_tenant.add(new_tenant)
    request.session['tenant_name'] = new_tenant.first_name + ' ' + new_tenant.last_name 
    request.session['tenant_id'] = new_tenant.id
    return redirect(f'/one_prop/{id}')

def new_review(request):
       return render(request, 'my_profile.html', context)