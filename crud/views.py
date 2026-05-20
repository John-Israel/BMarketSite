
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Payment, Product_Size, Users, Genders, Admin, Products, Product_Gender, Cart, History
import json, uuid
from django.db.models import Sum


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

def get_current_user(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return None


def home(request):
    try:
        user = get_current_user(request)
        recent_orders = History.objects.filter(buyer=user)[:3]
        products = Products.objects.select_related('product_gender', 'product_size')[:4]
        data = {
            'products': products,
            'recent_orders': recent_orders
        }
        return render(request, 'page/home.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during home view: {e}")
    

def shop(request):
    try:
        products = Products.objects.select_related('product_gender', 'product_size')
        data = {
            'products': products
        }
        return render(request, 'page/shop.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during shop view: {e}")


# ── Cart helpers ──────────────────────────────────────────────────────────────

def cart(request):
    try:
        user = get_current_user(request)
        cart = Cart.objects.filter(user=user).select_related('product_name', 'product_size')
        subtotal = sum(int(item.product_price if item.product_price else 0) * item.quantity for item in cart)
        data = {
            'cart': cart,
            'subtotal': subtotal,
            'total': subtotal,
        }
        return render(request, 'page/cart.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during cart retrieval: {e}")


def cart_add(request, productId):
    if request.method == 'POST':
        try:
            user = get_current_user(request)
            product = Products.objects.get(pk=productId)
            product_size = Product_Size.objects.get(pk=product.product_size_id)
            cart_item, created = Cart.objects.get_or_create(
                product_name=product,
                product_size=product_size,
                user=user,          # ← scope to the logged-in user
                defaults={
                    'product_price': product.product_price,
                    'quantity': 1
                }
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()

            return JsonResponse({'success': True})

        except Products.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

# ── Updated Safe View Logic ───────────────────────────────────────────────────

def cart_update(request):
    cart_id = request.GET.get('cart_id')
    delta_raw = request.GET.get('delta', '0').strip()
    delta = int(delta_raw) if delta_raw.lstrip('-').isdigit() else 0

    if cart_id is not None:
        try:
            cart_item = Cart.objects.get(cart_id=cart_id)
            cart_item.quantity += delta

            if cart_item.quantity < 1:
                cart_item.delete()
            elif cart_item.quantity > 10:
                pass  # silently ignore, or return an error message
            else:
                cart_item.quantity = cart_item.quantity
                cart_item.save()

        except Cart.DoesNotExist:
             pass

        # sync session to match DB
    updated_cart = list(
        Cart.objects.values('cart_id', 'product_name_id', 'product_price', 'quantity')
    )
    return redirect('/page/cart')


def cart_remove(request):
    try:
        cart_id = request.GET.get('cart_id')
        if cart_id is not None:
            Cart.objects.filter(cart_id=cart_id).delete()
    except Exception as e:
        messages.error(request, f'Could not remove item: {e}')
    return redirect('/page/cart')


# ── Payment ───────────────────────────────────────────────────────────────────


def payment(request):
    user = get_current_user(request)
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('/page/cart')

    subtotal = sum(item.product_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        method_name  = request.POST.get('payment_method')  # should be 'Cash on Delivery' or 'GCash'
        gcash_number = request.POST.get('gcash_number', '')
        gcash_name   = request.POST.get('gcash_name', '')
        order_ref = str(uuid.uuid4())[:8].upper()

        try:
            payment_method = Payment.objects.get(payment_method=method_name)
        except Payment.DoesNotExist:
            messages.error(request, 'Invalid payment method.')
            return redirect('/page/payment')

        # save each cart item as a History record
        for item in cart_items:
            History.objects.create(
                order_ref = order_ref,
                buyer          = user,
                product_name   = item.product_name,
                quantity       = item.quantity,
                payment_method = payment_method,
                product_price  = item.product_price,
                product_total  = subtotal
            )
        products = Products.objects.get(pk=item.product_name_id)
        products.product_quantity = max(products.product_quantity - item.quantity, 0)
        products.save() 

        # clear the cart after order is placed
        cart_items.delete()

        request.session['last_order'] = {
            'subtotal':     subtotal,
            'method':       method_name,
            'gcash_number': gcash_number,
            'gcash_name':   gcash_name,
            'buyer_name':   user.full_name,
        }

        messages.success(request, 'Order placed successfully!')
        return redirect('/page/shop')

    return render(request, 'page/payment.html', {
        'cart_items': cart_items,
        'subtotal':   subtotal,
        'total':      subtotal,
        'user':       user,
    })
# ── Contact ───────────────────────────────────────────────────────────────────
def history(request):
    try:
        user = get_current_user(request)
        orders_qs = History.objects.filter(buyer=user).select_related('product_name', 'payment_method').order_by('-created_at')
        
        grouped_orders = {}
        for order in orders_qs:
            key = order.order_ref or order.history_id
            if key not in grouped_orders:
                grouped_orders[key] = {'items': [], 'total': 0}
            grouped_orders[key]['items'].append(order)
            grouped_orders[key]['total'] += order.product_price * order.quantity

        subtotal = sum(int(order.product_price if order.product_price else 0) * order.quantity for order in orders_qs)
        
        data = {
            'grouped_orders': grouped_orders,
            'subtotal': subtotal
        }
        return render(request, 'page/history.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during history retrieval: {e}")


def contact(request):
    return render(request, 'page/contact.html')

def remove_history(request):
    try:
        user = get_current_user(request)
        History.objects.filter(buyer=user).delete()
        messages.success(request, 'Order history cleared successfully.')
        return redirect('/page/history')
    except Exception as e:
        return HttpResponse(f"An error occurred while clearing history: {e}")


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
    
def manage(request):
    try:
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/page/Log_in')

        user = Users.objects.get(pk=user_id)

        if request.method == 'POST':
            full_name      = request.POST.get('full_name')
            email          = request.POST.get('email')
            gender         = request.POST.get('gender')
            birth_date     = request.POST.get('birth_date')
            contact_number = request.POST.get('contact_number')
            address        = request.POST.get('address')
            new_password   = request.POST.get('new_password')
            confirm_new    = request.POST.get('confirm_new_password')
            profile_pic    = request.FILES.get('profile_pic')

            # Password change is optional — only update if provided
            if new_password:
                if new_password != confirm_new:
                    messages.error(request, 'Passwords do not match!')
                    return redirect('/page/manage')
                if len(new_password) < 8:
                    messages.error(request, 'Password must be at least 8 characters!')
                    return redirect('/page/manage')
                user.password = make_password(new_password)

            user.full_name      = full_name
            user.email          = email
            user.gender         = Genders.objects.get(pk=gender)
            user.birthdate      = birth_date
            user.contact_number = contact_number
            user.address        = address

            if profile_pic:
                user.profile_pic = profile_pic

            user.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('/page/manage')

        genders = Genders.objects.all()
        return render(request, 'page/manage.html', {
            'user':    user,
            'genders': genders,
        })

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


def delete_account(request):
    try:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            if not user_id:
                return redirect('/page/Log_in')

            user = Users.objects.get(pk=user_id)
            user.delete()

            # Clear the session so they're fully logged out
            request.session.flush()

            messages.success(request, 'Your account has been deleted.')
            return redirect('/page/Log_in')

        return redirect('/page/manage')

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

# ── Admin ─────────────────────────────────────────────────────────────────────

def admin_home(request):
    try:
        users = Users.objects.all()
        products = Products.objects.all()
        orders = History.objects.all()
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'users': users,
            'products': products,
            'orders': orders,
            'low_stock': low_stock
        }
        return render(request, 'admin/admin_home.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")
    


def product_list(request):
    try:
        products = Products.objects.select_related('product_gender')
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'products': products,
            'low_stock': low_stock
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
            productSize = request.POST.get('product_size')
            productImage = request.FILES.get('product_image')
            productPrice = request.POST.get('price')
            productQuantity = request.POST.get('quantity')
            
            Products.objects.create(
                product_name = productName,
                product_brand = productBrand,
                product_gender = Product_Gender.objects.get(pk=productGender),
                product_size = Product_Size.objects.get(pk=productSize),
                product_image = productImage,
                product_price = productPrice,
                product_quantity = productQuantity
            )
            
            messages.success(request,'Product added succesfully! ')
            return redirect('/admin/product_list')
        else:
            product_gender_list = Product_Gender.objects.all()
            product_size_list = Product_Size.objects.all()
            data = {
                'product_genders': product_gender_list,
                'product_sizes': product_size_list
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
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'users': users,
            'low_stock': low_stock
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

def delete_user(request, user_id):
    try:
        if request.method == 'POST':
            user = Users.objects.get(pk=user_id)
            user.delete()
            messages.success(request, f'User deleted successfully.')
            return redirect('/admin/user_list')
        return redirect('/admin/user_list')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


def admin_history(request):
    try:
        user = get_current_user(request)
        users = Users.objects.get(pk=user.user_id)
        orders_qs = History.objects.all().select_related('product_name', 'payment_method').order_by('-created_at')
        
        grouped_orders = {}
        for order in orders_qs:
            key = order.order_ref or order.history_id
            if key not in grouped_orders:
                grouped_orders[key] = {'items': [], 'total': 0}
            grouped_orders[key]['items'].append(order)
            grouped_orders[key]['total'] += order.product_price * order.quantity

        subtotal = sum(int(order.product_price if order.product_price else 0) * order.quantity for order in orders_qs)
        
        data = {
            'grouped_orders': grouped_orders,
            'subtotal': subtotal,
            'user': users
        }
        return render(request, 'admin/admin_history.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during history retrieval: {e}")

def admin_remove_history(request):
    try:
        user = get_current_user(request)
        History.objects.all().delete()
        messages.success(request, 'Order history cleared successfully.')
        return redirect('/admin/admin_history')
    except Exception as e:
        return HttpResponse(f"An error occurred while clearing history: {e}")