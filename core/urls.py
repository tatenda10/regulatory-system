from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('financial-performance/', views.financial_performance, name='financial-performance'),
    path('profitability-risk/', views.profitability_risk, name='profitability-risk'),
    path('liquidity-solvency/', views.liquidity_solvency, name='liquidity-solvency'),
    path('compliance-alerts/', views.compliance_alerts, name='compliance-alerts'),
    path('industry-comparison/', views.industry_comparison, name='industry-comparison'),
    path('data-validation/', views.data_validation, name='data-validation'),
    path('reports-exports/', views.reports_exports, name='reports-exports'),
    path('settings-admin/', views.settings_admin, name='settings-admin'),
]
