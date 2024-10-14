from django.shortcuts import render
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, UserLoginForm, SellerRegisterForm
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from products.models import Products
from django.contrib.auth.decorators import login_required
from products.models import Category
from products.models import Products, Order, Review
from django.contrib import messages

User = get_user_model()
from django.db.models import Min, Max
from django.shortcuts import render, get_object_or_404
from .models import Profile
from chats.models import Mychats
from django.db.models import Q  # Import Q for more complex queries

@login_required(login_url='login')
def index(request):
    # Get price range from the database
    price_range = Products.objects.aggregate(min_price=Min('price'), max_price=Max('price'))
    
    # Get user input for price range, default to None if not provided
    min_price = request.GET.get('min_price') or price_range['min_price']
    max_price = request.GET.get('max_price') or price_range['max_price']
    
    # Fetch categories and get selected category
    category_list = Category.objects.all()
    category = request.GET.get('category') 
    search_query = request.GET.get('search')
    
    # Fetch all products initially
    products = Products.objects.all()


    # Apply search filter (even if category is provided)
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Apply category filter (if selected)
    if category:
        products = products.filter(category=category)

    # Apply price filter
    products = products.filter(price__gte=min_price, price__lte=max_price)

    # Build the context for rendering
    context = {
        'products': products,
        'category_list': category_list,
        'category': category,
        'selected_category': category,
        'search_query': search_query,
        'price_min': min_price,
        'price_max': max_price,
        'min_price': price_range['min_price'],
        'max_price': price_range['max_price'],
    }
    
    return render(request, 'index.html', context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Successfully Registered!")
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

def UserLogin(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST or None)
        print(form)  # Debug: Check form data
        if form.is_valid():
            user = form.get_user()
            print(user)  # Debug: Check if user is fetched correctly
            request.session['user_convo'] = Mychats.objects.filter(me=user).count()
            login(request, user)
            messages.success(request, "Successfully Logged In!")
            return redirect('index')  # Redirect after successful login
    else:
        form = UserLoginForm()
    return render(request, 'auth/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')



@login_required
def seller_register(request):
    # Ensure the user is authenticated
    if request.method == 'POST':
        seller_form = SellerRegisterForm(request.POST)

        if seller_form.is_valid():
            # Get the currently logged-in user
            user = request.user
            # user.seller = True  # Mark user as a seller
            user.save()

            # Create the Seller profile and link it to the logged-in user
            seller = seller_form.save(commit=False)
            seller.user = user  # Link the seller to the user
            seller.save()
            messages.success(request, "Account Successfully Registered As Seller!")
            return redirect('index')  # Redirect to index after registration
    else:
        seller_form = SellerRegisterForm()

    return render(request, 'auth/seller_register.html', {'seller_form': seller_form})


@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    
    
    # Get products posted by the logged-in user
    user_products = Products.objects.filter(seller=request.user)
    user_orders = Order.objects.filter(user=request.user)
    user_reviews = Review.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'products': user_products,  # Updated to include only products posted by the user
        'orders': user_orders,
        'reviews': user_reviews,
        'profile_picture': profile.profile_picture,
    }
    
    return render(request, 'profile/profile_view.html', context)

def EditProfile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        profile.profile_picture = request.FILES.get('profile_picture', profile.profile_picture)
        profile.save()
        return redirect('profile')
    return render(request, 'profile/profile_view.html', {'profile': profile})

