from django.shortcuts import render
from .models import Destination
from .models import Detailed_desc
from .models import PassengerDetail
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import *
from django.utils.dateparse import parse_date
from django.views.decorators.cache import cache_control
from django.core.mail import send_mail
from django import forms
from django.forms.formsets import formset_factory
from django.shortcuts import render
from django.template import Library
from datetime import datetime
from .models import hotels,Booking
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
# from Paytm import Checksum
import razorpay
import requests



import random
# MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def index(request):
    dests = Destination.objects.all()
    dest1 = []
    temp =Detailed_desc.objects.get(dest_id=1)
    dest1.append(temp)

    return render(request, 'index.html',{'dests': dests, 'dest1' : dest1})

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, last_name=last_name,
                                                first_name=first_name)
                user.save()
                print('user Created')
                return redirect('login')
        else:
            messages.info(request, 'Password is not matching ')
            return redirect('register')
        return redirect('index')
    else:
        return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.first_name + ' ' + request.user.last_name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            dests = Destination.objects.all()
            return render(request, 'index.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('register')




@login_required(login_url='login')
def destination_list(request,city_name):
    dests = Detailed_desc.objects.all().filter(country=city_name)
    return render(request,'travel_destination.html',{'dests': dests})


def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'destination_details.html',{'dest':dest})


def search(request):
    try:
        place1 = request.session.get('place')
        print(place1)
        dest = Detailed_desc.objects.get(dest_name=place1)
        print(place1)
        return render(request, 'destination_details.html', {'dest': dest})
    except:
        messages.info(request, 'Place not found')
        return redirect('index')

def customize(request):
     return render(request, 'customized.html', {})
def hotel(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')
        try:
            check_in_date = datetime.strptime(check_in_date_str, '%d-%m-%Y').date()
            check_out_date = datetime.strptime(check_out_date_str, '%d-%m-%Y').date()

            hotels_list = hotels.objects.filter(city__iexact=city, check_in_date__lte=check_in_date, check_out_date__gte=check_out_date)
            return render(request, 'hotel.html', {'hotel1': hotels_list, 'city': city, 'check_in_date': check_in_date, 'check_out_date': check_out_date})
        except ValueError:
            return HttpResponse("Invalid date format")
    return render(request, 'search.html')

def flight(request):
    return render(request,'flight.html',{})
from django.shortcuts import render
from .models import Booking

def checkout(request):
    if request.method == "POST":
        booking_type = request.POST.get('booking_type')
        name = request.POST.get('name', '')
        amount = int(request.POST.get('totalAmount', 0)) * 100
        email = request.POST.get('email', '')
        address = request.POST.get('address', '') 
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        if booking_type == 'hotel':
            hotel_name = request.POST.get('hotel_name', '')
            client = razorpay.Client(auth=("rzp_test_C8d3vHaumly0RS", "FeA9Wry8ckIycxqutkcf2FzW"))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
            user = request.user
            order1 = Booking(user=user, items_json=hotel_name, name=name, email=email, address=address, city=city,
                            state=state, zip_code=zip_code, phone=phone, amount=amount, order_id=payment['id'], booking_type=booking_type)
            order1.save()

        else:
            destination_name = request.POST.get('destination_name', '')
            check_in_date = request.POST.get('check_in_date', '')
            num_passengers = request.POST.get('num_passengers', '')

            client = razorpay.Client(auth=("rzp_test_C8d3vHaumly0RS", "FeA9Wry8ckIycxqutkcf2FzW"))
            payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})

            user = request.user
            order1 = Booking(user=user, items_json=destination_name, name=name, email=email, address=address, city=city,
                            state=state, zip_code=zip_code, phone=phone, amount=amount, order_id=payment['id'], check_in_date=check_in_date, num_passengers=num_passengers, booking_type=booking_type)
            order1.save()

        return render(request, 'checkout.html', {'payment': payment})

    else:
        booking_type = 'hotel' if 'hotel' in request.resolver_match.url_name else 'package'
        context = {'booking_type': booking_type}
        return render(request, 'checkout.html', context)


@csrf_exempt
def success(request):
    if request.method == "POST":
        a =  (request.POST)
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        user = Booking.objects.filter(order_id = order_id).first()
        user.paid = True
        user.save()
        

    return render(request, "paymentstatus.html")


@login_required
def trips(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    hotel_bookings = []
    for booking in bookings:
        hotel = hotels.objects.get(name=booking.items_json)
        hotel_booking_info = {
            'hotel_name': hotel.name,
            'check_in_date': hotel.check_in_date,
            'check_out_date': hotel.check_out_date,
            'city':booking.city,
            'paid': booking.paid
        }
        hotel_bookings.append(hotel_booking_info)
    return render(request, 'trips.html', {'hotel_bookings': hotel_bookings})