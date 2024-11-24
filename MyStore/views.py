from django.shortcuts import render,redirect


def home(request):
	if request.method == 'GET':
		if request.user.is_authenticated:
			return redirect('store:dashboard')
		return redirect('accounts:login')
	return render(request, 'home.html',)