from django.shortcuts import render, redirect


def Log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            return redirect('/page/home')
        else:
            return render(request, 'page/Log_in.html', {'error': 'Please fill in all fields.'})

    return render(request, 'page/Log_in.html')


def home(request):
    return render(request, 'page/home.html')


def shop(request):
    return render(request, 'page/shop.html')


def cart(request):
    return render(request, 'page/cart.html')


def payment(request):
    return render(request, 'page/payment.html')