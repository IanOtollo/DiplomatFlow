from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse

def debug_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(f'<h1>Login Successful!</h1><p>Welcome, {user.username}!</p><p><a href="/tasks/dashboard/">Go to Dashboard</a></p>')
        else:
            return HttpResponse('<h1>Login Failed!</h1><p>Invalid credentials.</p><p><a href="/debug-login/">Try Again</a></p>')
    
    return render(request, 'debug_login.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('reports/', include('reports.urls')),
    path('equipment/', include('equipment.urls')),
    path('debug-login/', debug_login_view, name='debug_login'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)