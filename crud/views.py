
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Users, Genders, Admin, Products, Product_Gender


def Log_in(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = Users.objects.filter(username=username).first()
            # Check if user exists and password is correct, if not check if admin exists and password is correct
            if user == None:
                admin = Admin.objects.filter(username=username).first()
                if admin and check_password(password, admin.password):
                    return redirect('/admin/admin_home')
                else:
                    messages.error(request, 'Invalid username or password!')
                    return redirect('/page/Log_in')

            if user and check_password(password, user.password):
                return redirect('/page/home')
            else:
                messages.error(request, 'Invalid username or password!')
                return redirect('/page/Log_in')
        else:
            return render(request, 'page/Log_in.html')
    except Exception as e:
        return HttpResponse(f"An error occurred during login: {e}")


def home(request):
    return render(request, 'page/home.html')


def shop(request):
    return render(request, 'page/shop.html')


def cart(request):
    return render(request, 'page/cart.html')


def payment(request):
    return render(request, 'page/payment.html')

def sign_up(request):
    try:
        if request.method == 'POST':
            fullname = request.POST.get('full_name')
            gender = request.POST.get('gender')
            birthdate = request.POST.get('birth_date')
            address = request.POST.get('address')
            contactNumber = request.POST.get('contact_number')
            email = request.POST.get('email')
            username = request.POST.get('username')
            password = request.POST.get('password')
            hashed_password = make_password(password)
            profile_pic = request.FILES.get('profile_pic')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect('/users/add')

            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters!')
                return redirect('/users/add')
            Users.objects.create(
                full_name=fullname,
                gender=Genders.objects.get(pk=gender),
                birthdate=birthdate,
                address=address,
                contact_number=contactNumber,
                email=email,
                username=username,
                password=hashed_password,
                profile_pic=profile_pic
            )
            messages.success(request,'User added succesfully! ')
            return redirect('/page/Log_in')
        else:
            gender_list = Genders.objects.all()
            data = {
                'genders': gender_list
            }
            return render(request, 'page/sign_up.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during add user: {e}")
    

# page navigation for admin
def admin_home(request):
    return render(request, 'admin/admin_home.html')


def product_list(request):
    try:
        products = Products.objects.select_related('product_gender')
        data = {
            'products': products
        }
        return render(request, 'admin/product_list.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during product list retrieval: {e}")

def add_product(request):
    try:
        if request.method == 'POST':
            productName = request.POST.get('product_name')
            productBrand = request.POST.get('brand')
            productGender = request.POST.get('product_gender')
            productImage = request.FILES.get('product_image')
            productPrice = request.POST.get('price')
            productQuantity = request.POST.get('quantity')
            
            Products.objects.create(
                product_name = productName,
                product_brand = productBrand,
                product_gender = Product_Gender.objects.get(pk=productGender),
                product_image = productImage,
                product_price = productPrice,
                product_quantity = productQuantity
            )
            
            messages.success(request,'Product added succesfully! ')
            return redirect('/admin/product_list')
        else:
            product_gender_list = Product_Gender.objects.all()
            data = {
                'product_genders': product_gender_list
            }
            return render(request, 'admin/add_product.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during add product: {e}")
    
def delete_product(request, id):
    try:
        if request.method == 'POST':
            product = Products.objects.get(pk=id)
            product.delete()
            messages.success(request,'Product deleted succesfully! ')
            return redirect('/admin/product_list')
        else:
            product = Products.objects.get(pk=id)
            data = {
                'product': product
            }
            return render(request, 'admin/delete_product.html', data)
        
    except Exception as e:
        return HttpResponse(f"An error occurred during delete: {e}")
    
def update_product(request, productId):
    try:
        if request.method == 'POST':
            product = Products.objects.get(pk=productId)
            product.product_price = request.POST.get('price')
            product.product_quantity = request.POST.get('quantity')
            product.save()
            messages.success(request,'Product updated succesfully! ')

            data = {
                'product': product
            }
            return redirect('/admin/product_list')
        else:
            product = Products.objects.get(pk=productId)

            data = {
                'product': product
            }
            return render(request, 'admin/update_product.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during update: {e}")
    
def user_list(request):
    try:
        users = Users.objects.select_related('gender')
        data = {
            'users': users
        }
        return render(request, 'admin/user_list.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during user list retrieval: {e}")