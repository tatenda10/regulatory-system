from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def home(request):
    """Home page view - redirects to login."""
    return redirect('core:login')


def login_view(request):
    """Login page view."""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'login.html')


def logout_view(request):
    """Logout view."""
    logout(request)
    return redirect('core:login')


def about(request):
    """About page view."""
    context = {
        'title': 'About IPEC',
        'message': 'Learn more about our project.'
    }
    return render(request, 'base.html', context)


@login_required
def dashboard(request):
    """Main dashboard view."""
    context = {
        'title': 'Enterprise Dashboard',
        'message': 'Welcome to your IPEC dashboard.'
    }
    return render(request, 'dashboard.html', context)


@login_required
def financial_performance(request):
    """Financial Performance & Position view."""
    context = {
        'title': 'Financial Performance & Position',
        'message': 'Insurance Contract Liabilities and IFRS 17 Analysis'
    }
    return render(request, 'financial_performance.html', context)


@login_required
def profitability_risk(request):
    """Profitability & Risk view."""
    context = {
        'title': 'Profitability & Risk',
        'message': 'Insurance Service Results and Risk Analysis'
    }
    return render(request, 'profitability_risk.html', context)


@login_required
def liquidity_solvency(request):
    """Liquidity & Solvency view."""
    context = {
        'title': 'Liquidity & Solvency',
        'message': 'Solvency II Ratios and Cashflow Analysis'
    }
    return render(request, 'liquidity_solvency.html', context)


@login_required
def compliance_alerts(request):
    """Compliance & Supervisory Alerts view."""
    context = {
        'title': 'Compliance & Supervisory Alerts',
        'message': 'Regulatory Compliance Monitoring and Alert Management'
    }
    return render(request, 'compliance_alerts.html', context)


@login_required
def industry_comparison(request):
    """Industry Comparison view."""
    context = {
        'title': 'Industry Comparison',
        'message': 'Peer Analysis and Industry Benchmarking'
    }
    return render(request, 'industry_comparison.html', context)


@login_required
def data_validation(request):
    """Data & Validation view."""
    context = {
        'title': 'Data & Validation',
        'message': 'Submission History and Data Quality Management'
    }
    return render(request, 'data_validation.html', context)


@login_required
def reports_exports(request):
    """Reports & Exports view."""
    context = {
        'title': 'Reports & Exports',
        'message': 'Regulatory Reporting and Custom Export Tools'
    }
    return render(request, 'reports_exports.html', context)


@login_required
def settings_admin(request):
    """Settings & Administration view."""
    context = {
        'title': 'Settings & Administration',
        'message': 'User Management and System Configuration'
    }
    return render(request, 'settings_admin.html', context)
