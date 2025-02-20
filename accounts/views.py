from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,FileResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from employee.models import *
from .forms import UserLogin,UserAddForm
from reportlab.pdfgen import canvas

def changepassword(request):
	if not request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save(commit=True)
			update_session_auth_hash(request,user)

			messages.success(request,'Password changed successfully',extra_tags = 'alert alert-success alert-dismissible show' )
			return redirect('accounts:changepassword')
		else:
			messages.error(request,'Error,changing password',extra_tags = 'alert alert-warning alert-dismissible show' )
			return redirect('accounts:changepassword')
			
	form = PasswordChangeForm(request.user)
	return render(request,'accounts/change_password_form.html',{'form':form})

def register_user_view(request):
    if request.method == 'POST':
        form = UserAddForm(data=request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account created for {username}!', extra_tags='alert alert-success alert-dismissible show')
            return redirect('accounts:register')
        else:
            messages.error(request, 'Please correct the errors below.', extra_tags='alert alert-warning alert-dismissible show')
    else:
        form = UserAddForm()
    
    dataset = {
        'form': form,
        'title': 'Register Users'
    }
    return render(request, 'accounts/register.html', dataset)

def login_view(request):
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    
                    next_url = request.GET.get('next', 'dashboard:dashboard')
                    messages.success(request, f'Welcome back, {username}!', extra_tags='alert alert-success alert-dismissible show')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Your account is inactive. Please contact the admin.', extra_tags='alert alert-warning alert-dismissible show')
            else:
                messages.error(request, 'Invalid username or password.', extra_tags='alert alert-danger alert-dismissible show')
        else:
            messages.error(request, 'Invalid form data. Please try again.', extra_tags='alert alert-danger alert-dismissible show')
    else:
        form = UserLogin()

    return render(request, 'accounts/login.html', {'form': form})

def user_profile_view(request):
	user = request.user
	if user.is_authenticated:
		employee = Employee.objects.filter(user = user).first()
		emergency = Emergency.objects.filter(employee = employee).first()
		relationship = Relationship.objects.filter(employee = employee).first()
		bank = Bank.objects.filter(employee = employee).first()

		dataset = dict()
		dataset['employee'] = employee
		dataset['emergency'] = emergency
		dataset['family'] = relationship
		dataset['bank'] = bank

		return render(request,'dashboard/employee_detail.html',dataset)
	return HttpResponse("Sorry , not authenticated for this,admin or whoever you are :)")

def logout_view(request):
	logout(request)
	return redirect('accounts:login')

def users_list(request):
	employees = Employee.objects.all()
	return render(request,'accounts/users_table.html',{'employees':employees,'title':'Users List'})

def users_unblock(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = False
	emp.save()
	user.is_active = True
	user.save()

	return redirect('accounts:users')

def users_block(request,id):
	user = get_object_or_404(User,id = id)
	emp = Employee.objects.filter(user = user).first()
	emp.is_blocked = True
	emp.save()
 
	user.is_active = False
	user.save()
	
	return redirect('accounts:users')

def users_blocked_list(request):
	blocked_employees = Employee.objects.all_blocked_employees()
	return render(request,'accounts/all_deleted_users.html',{'employees':blocked_employees,'title':'blocked users list'})

def download_excel(request):
    data = {
        'Username': [user.username for user in User.objects.all()],
        'Email': [user.email for user in User.objects.all()],
        'Status': ['Active' if user.is_active else 'Inactive' for user in User.objects.all()],
    }

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="users.xlsx"'
    
    df.to_excel(response, index=False, engine='openpyxl')  
    return response

def download_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="users.pdf"'
    
    pdf_canvas = canvas.Canvas(response)
    pdf_canvas.drawString(100, 800, "User List Report")

    y_position = 780
    for user in User.objects.all():
        pdf_canvas.drawString(100, y_position, f"Username: {user.username}, Email: {user.email}")
        y_position -= 20  

    pdf_canvas.save()
    return response