from django.shortcuts import render, redirect
from .forms import RegisterForm, OrderForm
from django.contrib import messages
from .models import Customer, Order
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .decorators import allowed_users, admin_only
# Create your views here.
def registerPage(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			Customer.objects.create(user = user, name = user.username)
			return redirect('register')
			messages.success(request,'Accounts was created' +username)
	context = {'form':form}

	return render(request,'accounts/register.html', context)

def loginPage(request):
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username = username, password = password)
		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request,f'Username or Password is incorrect')
	return render(request,'accounts/login.html')


def logoutPage(request):
	logout(request)
	return redirect('login')


@admin_only
def homePage(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	#counting the total customers and orders
	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status = "Delivered").count()
	pending = orders.filter(status = "Pending").count()

	context = {'orders':orders,'customers':customers,'total_orders':total_orders,
	'total_customers':total_customers,'delivered':delivered,'pending':pending}

	return render(request,'accounts/dashboard.html', context)

@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all() #orders object of particular
	total_orders = orders.count()
	delivered = orders.filter(status='delivered').count()
	pending = orders.filter(status='pending').count()

	context ={'orders':orders,'total_orders':total_orders,
	'delivered':delivered,'pending':pending}

	return render(request,'accounts/user.html', context)



#update the order
def order_update(request, pk):
	form = OrderForm()
	order = Order.objects.get(id = pk)
	if request.method == "POST":
		form = OrderForm(request.POST, instance = order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form':form}
	return render(request,'accounts/order_form.html', context)


#delete the order
def order_delete(request, pk):
	order = Order.objects.get(id = pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')
	context = {'item':order}
	return render(request,'accounts/delete_order.html', context)
