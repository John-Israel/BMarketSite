from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .models import Payment, Product_Size, Users, Genders, Admin, Products, Product_Gender, Cart, History
import json, uuid
from django.db.models import Sum
from functools import wraps
from django.db import IntegrityError


# ── Session Guard Decorators ──────────────────────────────────────────────────


# ── Auth ──────────────────────────────────────────────────────────────────────

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

## ── Paste these functions into your views.py ────────────────────────────────

def forgot_password(request):
    try:
        if request.method == 'POST':
            step = request.POST.get('step', '1')

            if step == '1':
                email = request.POST.get('email', '').strip()
                user  = Users.objects.filter(email=email).first()

                if user is None:
                    messages.error(request, 'No account found with that email address.')
                    return redirect('/page/forgot_password')

                # Store verified email in session so step-2 knows who to update
                request.session['reset_email'] = email
                # Render same template but now show the reset-password form
                return render(request, 'page/forgot_password.html', {
                    'step': 2,
                    'email': email,
                })

            # ── STEP 2: reset password ────────────────────────────────────
            elif step == '2':
                email            = request.session.get('reset_email')
                new_password     = request.POST.get('new_password', '')
                confirm_password = request.POST.get('confirm_password', '')

                if not email:
                    messages.error(request, 'Session expired. Please start over.')
                    return redirect('/page/forgot_password')

                if new_password != confirm_password:
                    messages.error(request, 'Passwords do not match.')
                    return render(request, 'page/forgot_password.html', {
                        'step': 2,
                        'email': email,
                    })

                if len(new_password) < 8:
                    messages.error(request, 'Password must be at least 8 characters.')
                    return render(request, 'page/forgot_password.html', {
                        'step': 2,
                        'email': email,
                    })

                user = Users.objects.filter(email=email).first()
                if user is None:
                    messages.error(request, 'User not found.')
                    return redirect('/page/forgot_password')

                user.password = make_password(new_password)
                user.save()

                # Clean up session
                del request.session['reset_email']

                messages.success(request, 'Password updated successfully! You can now log in.')
                return redirect('/page/Log_in')

        # GET – show step 1
        return render(request, 'page/forgot_password.html', {'step': 1})

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")

def login_required(view_func):
    """Redirects to login page if no user session is found."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            messages.error(request, 'You must be logged in to access that page.')
            return redirect('/page/Log_in')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Redirects to login page if no admin session is found."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_id'):
            messages.error(request, 'Admin access required.')
            return redirect('/page/Log_in')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_current_user(request):
    """Returns the logged-in User object, or None."""
    user_id = request.session.get('user_id')
    if not user_id:
        return None
    try:
        return Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return None


def log_out(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('/page/Log_in')

# ── User Views ────────────────────────────────────────────────────────────────

@login_required
def home(request):
    try:
        user = get_current_user(request)
        recent_orders = History.objects.filter(buyer=user)[:3]
        products = Products.objects.select_related('product_gender', 'product_size')[:4]
        data = {
            'products': products,
            'recent_orders': recent_orders,
            'user': user
        }
        return render(request, 'page/home.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during home view: {e}")


@login_required
def shop(request):
    try:
        products = Products.objects.select_related('product_gender', 'product_size')
        data = {
            'products': products
        }
        return render(request, 'page/shop.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during shop view: {e}")


# ── Cart ──────────────────────────────────────────────────────────────────────

@login_required
def cart(request):
    try:
        user = get_current_user(request)
        cart_items = Cart.objects.filter(user=user).select_related('product_name', 'product_size')
        subtotal = sum(int(item.product_price if item.product_price else 0) * item.quantity for item in cart_items)
        data = {
            'cart': cart_items,
            'subtotal': subtotal,
            'total': subtotal,
        }
        return render(request, 'page/cart.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during cart retrieval: {e}")


@login_required
def cart_add(request, productId):
    if request.method == 'POST':
        try:
            user = get_current_user(request)
            product = Products.objects.get(pk=productId)
            product_size = Product_Size.objects.get(pk=product.product_size_id)

            cart_item, created = Cart.objects.get_or_create(
                product_name=product,
                product_size=product_size,
                user=user,
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


@login_required
def cart_update(request):
    cart_id = request.GET.get('cart_id')
    delta_raw = request.GET.get('delta', '0').strip()
    delta = int(delta_raw) if delta_raw.lstrip('-').isdigit() else 0

    if cart_id is not None:
        try:
            cart_item = Cart.objects.get(cart_id=cart_id)
            product = cart_item.product_name
            new_quantity = cart_item.quantity + delta

            if new_quantity < 1:
                cart_item.delete()
            elif new_quantity <= product.product_quantity:
                cart_item.quantity = new_quantity
                cart_item.save()

        except Cart.DoesNotExist:
            pass

    return redirect('/page/cart')


@login_required
def cart_remove(request):
    try:
        cart_id = request.GET.get('cart_id')
        if cart_id is not None:
            Cart.objects.filter(cart_id=cart_id).delete()
    except Exception as e:
        messages.error(request, f'Could not remove item: {e}')
    return redirect('/page/cart')


# ── Payment ───────────────────────────────────────────────────────────────────

@login_required
def payment(request):
    user = get_current_user(request)
    cart_items = Cart.objects.filter(user=user)

    if not cart_items.exists():
        return redirect('/page/cart')

    subtotal = sum(item.product_price * item.quantity for item in cart_items)

    if request.method == 'POST':
        method_name  = request.POST.get('payment_method')
        gcash_number = request.POST.get('gcash_number', '')
        gcash_name   = request.POST.get('gcash_name', '')
        order_ref    = str(uuid.uuid4())[:8].upper()

        try:
            payment_method = Payment.objects.get(payment_method=method_name)
        except Payment.DoesNotExist:
            messages.error(request, 'Invalid payment method.')
            return redirect('/page/payment')

        for item in cart_items:
            History.objects.create(
                order_ref      = order_ref,
                buyer          = user,
                product_name   = item.product_name,
                quantity       = item.quantity,
                payment_method = payment_method,
                product_price  = item.product_price,
                product_total  = subtotal
            )
            product = Products.objects.get(pk=item.product_name_id)
            product.product_quantity = max(product.product_quantity - item.quantity, 0)
            product.save()

        cart_items.delete()

        request.session['last_order'] = {
            'subtotal':     float(subtotal),
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


# ── History ───────────────────────────────────────────────────────────────────

@login_required
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


@login_required
def remove_history(request):
    try:
        user = get_current_user(request)
        History.objects.filter(buyer=user).delete()
        messages.success(request, 'Order history cleared successfully.')
        return redirect('/page/history')
    except Exception as e:
        return HttpResponse(f"An error occurred while clearing history: {e}")


def contact(request):
    return render(request, 'page/contact.html')


# ── Sign Up ───────────────────────────────────────────────────────────────────

def sign_up(request):
    try:
        if request.method == 'POST':
            fullname         = request.POST.get('full_name')
            gender           = request.POST.get('gender')
            birthdate        = request.POST.get('birth_date')
            address          = request.POST.get('address')
            contactNumber    = request.POST.get('contact_number')
            email            = request.POST.get('email')
            username         = request.POST.get('username')
            password         = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            profile_pic      = request.FILES.get('profile_pic')
            security_question = request.POST.get('security_question', '').strip()
            security_answer   = request.POST.get('security_answer', '').strip().lower()

            if password != confirm_password:
                messages.error(request, 'Passwords do not match!')
                return redirect('/page/sign_up')

            if len(password) < 8:
                messages.error(request, 'Password must be at least 8 characters!')
                return redirect('/page/sign_up')

            hashed_password = make_password(password)

            Users.objects.create(
                full_name         = fullname,
                gender            = Genders.objects.get(pk=gender),
                birthdate         = birthdate,
                address           = address,
                contact_number    = contactNumber,
                email             = email,
                username          = username,
                password          = hashed_password,
                profile_pic       = profile_pic,
                security_question = security_question,
                security_answer   = make_password(security_answer),
            )
            messages.success(request, 'Account created successfully!')
            return redirect('/page/Log_in')
        else:
            data = {'genders': Genders.objects.all()}
            return render(request, 'page/sign_up.html', data)

    except IntegrityError:
        messages.error(request, 'Username or email is already taken. Please choose another.')
        return redirect('/page/sign_up')
    except Exception as e:
        messages.error(request, f'An unexpected error occurred: {e}')
        return redirect('/page/Log_in')


# ── Manage Account ────────────────────────────────────────────────────────────

@login_required
def manage(request):
    user_id = request.session.get('user_id')
    try:
        user = Users.objects.get(pk=user_id)
    except Users.DoesNotExist:
        return redirect('/page/Log_in')

    if request.method == 'POST':
        full_name      = request.POST.get('full_name', '').strip()
        email          = request.POST.get('email', '').strip()
        username       = request.POST.get('username', '').strip()
        gender         = request.POST.get('gender', '').strip()
        birth_date     = request.POST.get('birth_date', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        address        = request.POST.get('address', '').strip()
        new_password   = request.POST.get('new_password', '').strip()
        confirm_new    = request.POST.get('confirm_new_password', '').strip()
        profile_pic    = request.FILES.get('profile_pic')

        if new_password:
            if new_password != confirm_new:
                return redirect('/page/manage?status=error&reason=password_mismatch')
            if len(new_password) < 8:
                return redirect('/page/manage?status=error&reason=password_too_short')
            user.password = make_password(new_password)

        if username and username != user.username:
            if Users.objects.filter(username=username).exclude(pk=user_id).exists():
                return redirect('/page/manage?status=error&reason=username_taken')

        user.full_name      = full_name
        user.username       = username
        user.email          = email
        user.birthdate      = birth_date
        user.contact_number = contact_number
        user.address        = address

        if gender:
            try:
                user.gender = Genders.objects.get(pk=gender)
            except Genders.DoesNotExist:
                pass

        if profile_pic:
            user.profile_pic = profile_pic

        try:
            user.save()
        except Exception as e:
            return HttpResponse(f"Save failed: {e}")

        return redirect('/page/manage?status=success')

    genders = Genders.objects.all()
    return render(request, 'page/manage.html', {
        'user':    user,
        'genders': genders,
    })


# ── Delete Account ────────────────────────────────────────────────────────────

@login_required
def delete_account(request):
    try:
        if request.method == 'POST':
            user_id = request.session.get('user_id')
            user = Users.objects.get(pk=user_id)
            user.delete()
            request.session.flush()
            messages.success(request, 'Your account has been deleted.')
            return redirect('/page/Log_in')
        return redirect('/page/manage')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


# ── Admin Views ───────────────────────────────────────────────────────────────

@admin_required
def admin_home(request):
    try:
        users     = Users.objects.all()
        products  = Products.objects.all()
        orders    = History.objects.all()
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'users':     users,
            'products':  products,
            'orders':    orders,
            'low_stock': low_stock
        }
        return render(request, 'admin/admin_home.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


@admin_required
def product_list(request):
    try:
        products  = Products.objects.select_related('product_gender')
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'products':  products,
            'low_stock': low_stock
        }
        return render(request, 'admin/product_list.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during product list retrieval: {e}")


@admin_required
def add_product(request):
    try:
        if request.method == 'POST':
            Products.objects.create(
                product_name     = request.POST.get('product_name'),
                product_brand    = request.POST.get('brand'),
                product_gender   = Product_Gender.objects.get(pk=request.POST.get('product_gender')),
                product_size     = Product_Size.objects.get(pk=request.POST.get('product_size')),
                product_image    = request.FILES.get('product_image'),
                product_price    = request.POST.get('price'),
                product_quantity = request.POST.get('quantity')
            )
            messages.success(request, 'Product added successfully!')
            return redirect('/admin/product_list')
        else:
            data = {
                'product_genders': Product_Gender.objects.all(),
                'product_sizes':   Product_Size.objects.all()
            }
            return render(request, 'admin/add_product.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during add product: {e}")


@admin_required
def delete_product(request, id):
    try:
        product = Products.objects.get(pk=id)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            return redirect('/admin/product_list')
        return render(request, 'admin/delete_product.html', {'product': product})
    except Exception as e:
        return HttpResponse(f"An error occurred during delete: {e}")


@admin_required
def update_product(request, productId):
    try:
        product = Products.objects.get(pk=productId)
        if request.method == 'POST':
            product.product_price    = request.POST.get('price')
            product.product_quantity = request.POST.get('quantity')
            product.product_size     = Product_Size.objects.get(pk=request.POST.get('product_size'))
            product.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('/admin/product_list')
        data = {
            'product':       product,
            'product_sizes': Product_Size.objects.all()
        }
        return render(request, 'admin/update_product.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during update: {e}")


@admin_required
def user_list(request):
    try:
        users     = Users.objects.select_related('gender')
        low_stock = Products.objects.filter(product_quantity__lte=10).select_related('product_gender', 'product_size')
        data = {
            'users':     users,
            'low_stock': low_stock
        }
        return render(request, 'admin/user_list.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during user list retrieval: {e}")


@admin_required
def admin_stack(request):
    try:
        products = Products.objects.all().order_by('-created_at')
        return render(request, 'admin/stack.html', {'products': products})
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


@admin_required
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


@admin_required
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


@admin_required
def delete_user(request, user_id):
    try:
        if request.method == 'POST':
            user = Users.objects.get(pk=user_id)
            user.delete()
            messages.success(request, 'User deleted successfully.')
            return redirect('/admin/user_list')
        return redirect('/admin/user_list')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")


@admin_required
def admin_history(request):
    try:
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
            'subtotal':       subtotal,
        }
        return render(request, 'admin/admin_history.html', data)
    except Exception as e:
        return HttpResponse(f"An error occurred during history retrieval: {e}")


@admin_required
def admin_remove_history(request):
    try:
        History.objects.all().delete()
        messages.success(request, 'Order history cleared successfully.')
        return redirect('/admin/admin_history')
    except Exception as e:
        return HttpResponse(f"An error occurred while clearing history: {e}")