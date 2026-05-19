
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Users, Genders, Admin, Products, Product_Gender
import json


def Log_in(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = Users.objects.filter(username=username).first()
            if user is None:
                admin = Admin.objects.filter(username=username).first()
                if admin and check_password(password, admin.password):
                    request.session['admin_id'] = admin.admin_id
                    return redirect('/admin/admin_home')
                else:
                    messages.error(request, 'Invalid username or password!')
                    return redirect('/page/Log_in')
            if user and check_password(password, user.password):
                request.session['user_id'] = user.user_id
                return redirect('/page/home')
            else:
                messages.error(request, 'Invalid username or password!')
                return redirect('/page/Log_in')
        else:
            return render(request, 'page/Log_in.html')
    except Exception as e:
        return HttpResponse(f"An error occurred during login: {e}")


def home(request):
    shoes = [
        {'name': 'Classic Runner',  'desc': 'Premium leather sole',    'price': 2499, 'old': 3200, 'img': 'picture/shop/shoes1.png'},
        {'name': 'Urban Elite',     'desc': 'Breathable mesh upper',   'price': 2799, 'old': 3500, 'img': 'picture/shop/shoes2.png'},
        {'name': 'Street King',     'desc': 'Rubber grip outsole',     'price': 1999, 'old': 2800, 'img': 'picture/shop/shoes3.png'},
        {'name': 'Gold Series',     'desc': 'Limited edition drop',    'price': 3499, 'old': 4200, 'img': 'picture/shop/shoes4.png'},
        {'name': 'Night Stepper',   'desc': 'Reflective detailing',    'price': 2299, 'old': 3000, 'img': 'picture/shop/shoes5.png'},
        {'name': 'Apex Trainer',    'desc': 'Dual-density cushioning', 'price': 2999, 'old': 3800, 'img': 'picture/shop/shoes6.png'},
        {'name': 'Phantom Pro',     'desc': 'Lightweight foam base',   'price': 3199, 'old': 4000, 'img': 'picture/shop/shoes7.png'},
        {'name': 'Velo Boost',      'desc': 'Speed-engineered sole',   'price': 2699, 'old': 3400, 'img': 'picture/shop/shoes8.png'},
        {'name': 'Terra Grip',      'desc': 'All-terrain outsole',     'price': 2899, 'old': 3600, 'img': 'picture/shop/shoes9.png'},
        {'name': 'Crown Edition',   'desc': 'Signature collection',    'price': 3999, 'old': 4800, 'img': 'picture/shop/shoes10.png'},
    ]
    for shoe in shoes:
        shoe['savings']  = shoe['old'] - shoe['price']
        shoe['discount'] = round((shoe['savings'] / shoe['old']) * 100)

    avg_discount = round(sum(s['discount'] for s in shoes) / len(shoes))
    best_savings = max(s['savings'] for s in shoes)

    return render(request, 'page/home.html', {
        'shoes':        shoes,
        'avg_discount': avg_discount,
        'best_savings': best_savings,
    })

def shop(request):
    shoes = [
        {'name': 'Classic Runner',  'desc': 'Premium leather sole',    'price': 2499, 'old': 3200, 'img': 'picture/shop/shoes1.png'},
        {'name': 'Urban Elite',     'desc': 'Breathable mesh upper',   'price': 2799, 'old': 3500, 'img': 'picture/shop/shoes2.png'},
        {'name': 'Street King',     'desc': 'Rubber grip outsole',     'price': 1999, 'old': 2800, 'img': 'picture/shop/shoes3.png'},
        {'name': 'Gold Series',     'desc': 'Limited edition drop',    'price': 3499, 'old': 4200, 'img': 'picture/shop/shoes4.png'},
        {'name': 'Night Stepper',   'desc': 'Reflective detailing',    'price': 2299, 'old': 3000, 'img': 'picture/shop/shoes5.png'},
        {'name': 'Apex Trainer',    'desc': 'Dual-density cushioning', 'price': 2999, 'old': 3800, 'img': 'picture/shop/shoes6.png'},
        {'name': 'Phantom Pro',     'desc': 'Lightweight foam base',   'price': 3199, 'old': 4000, 'img': 'picture/shop/shoes7.png'},
        {'name': 'Velo Boost',      'desc': 'Speed-engineered sole',   'price': 2699, 'old': 3400, 'img': 'picture/shop/shoes8.png'},
        {'name': 'Terra Grip',      'desc': 'All-terrain outsole',     'price': 2899, 'old': 3600, 'img': 'picture/shop/shoes9.png'},
        {'name': 'Crown Edition',   'desc': 'Signature collection',    'price': 3999, 'old': 4800, 'img': 'picture/shop/shoes10.png'},
    ]
    return render(request, 'page/shop.html', {'shoes': shoes})


# ── Cart helpers ──────────────────────────────────────────────────────────────

def get_cart(request):
    if 'cart' not in request.session:
        request.session['cart'] = []
    return request.session['cart']

def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def cart(request):
    cart_items = get_cart(request)
    
    # Safe fallback wrapper to ensure empty prices don't trigger base 10 int errors
    subtotal = sum(int(item['price'] if item['price'] else 0) * item['qty'] for item in cart_items)
    
    return render(request, 'page/cart.html', {
        'cart_items': cart_items,
        'subtotal':   subtotal,
        'total':      subtotal,
    })


def cart_add(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            if 'cart' not in request.session:
                request.session['cart'] = []
            cart = request.session['cart']
            existing = next((i for i in cart if i['name'] == data.get('name')), None)
            if existing:
                existing['qty'] += 1
            else:
                cart.append({
                    'name':  data.get('name'),
                    'desc':  data.get('desc'),
                    'price': data.get('price'),
                    'old':   data.get('old'),
                    'img':   data.get('img'),
                    'qty':   1,
                })
            request.session['cart'] = cart
            request.session.modified = True
            return JsonResponse({'success': True, 'cart_count': sum(i['qty'] for i in cart)})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False})


# ── Updated Safe View Logic ───────────────────────────────────────────────────

def cart_update(request):
    try:
        idx_raw = request.GET.get('index')
        dlta_raw = request.GET.get('delta')

        # Checks whether the data exists and is a true digit before evaluating int()
        index = int(idx_raw) if idx_raw and idx_raw.strip().replace('-', '').isdigit() else 0
        delta = int(dlta_raw) if dlta_raw and dlta_raw.strip().replace('-', '').isdigit() else 0
        
        cart = request.session.get('cart', [])
        if 0 <= index < len(cart):
            cart[index]['qty'] += delta
            if cart[index]['qty'] <= 0:
                cart.pop(index)
        request.session['cart'] = cart
        request.session.modified = True
    except Exception as e:
        messages.error(request, f'Could not update cart: {e}')
    return redirect('/page/cart')


def cart_remove(request):
    try:
        idx_raw = request.GET.get('index')
        index = int(idx_raw) if idx_raw and idx_raw.strip().isdigit() else 0
        
        cart = request.session.get('cart', [])
        if 0 <= index < len(cart):
            cart.pop(index)
        request.session['cart'] = cart
        request.session.modified = True
    except Exception as e:
        messages.error(request, f'Could not remove item: {e}')
    return redirect('/page/cart')


# ── Payment ───────────────────────────────────────────────────────────────────

def payment(request):
    cart_items = get_cart(request)
    if not cart_items:
        return redirect('/page/cart')
        
    subtotal = sum(int(item['price'] if item['price'] else 0) * item['qty'] for item in cart_items)

    if request.method == 'POST':
        method       = request.POST.get('payment_method')
        gcash_number = request.POST.get('gcash_number', '')
        gcash_name   = request.POST.get('gcash_name', '')
        request.session['last_order'] = {
            'items':        cart_items,
            'subtotal':     subtotal,
            'method':       method,
            'gcash_number': gcash_number,
            'gcash_name':   gcash_name,
        }
        save_cart(request, [])
        messages.success(request, 'Order placed successfully!')
        return redirect('/page/home')

    return render(request, 'page/payment.html', {
        'cart_items': cart_items,
        'subtotal':   subtotal,
        'total':      subtotal,
    })


# ── Contact ───────────────────────────────────────────────────────────────────

def contact(request):
    return render(request, 'page/contact.html')


# ── Sign Up ───────────────────────────────────────────────────────────────────

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


# ── Admin ─────────────────────────────────────────────────────────────────────

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
def admin_stack(request):
    try:
        products = Products.objects.all().order_by('-created_at')
        return render(request, 'admin/stack.html', {'products': products})
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def admin_update_stock(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            quantity   = request.POST.get('quantity')
            product    = Products.objects.get(pk=product_id)
            product.product_quantity = int(quantity if quantity else 0)
            product.save()
            messages.success(request, f'Stock for "{product.product_name}" updated to {quantity}.')
        except Products.DoesNotExist:
            messages.error(request, 'Product not found.')
        except Exception as e:
            messages.error(request, f'Error updating stock: {e}')
    return redirect('/admin/stack')

def admin_delete_product(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product_id')
            product    = Products.objects.get(pk=product_id)
            name       = product.product_name
            product.delete()
            messages.success(request, f'"{name}" has been deleted.')
        except Products.DoesNotExist:
            messages.error(request, 'Product not found.')
        except Exception as e:
            messages.error(request, f'Error deleting product: {e}')
    return redirect('/admin/stack')
