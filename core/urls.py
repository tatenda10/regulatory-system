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
    
    # Institution Management
    path('institutions/', views.institutions_list, name='institutions-list'),
    path('institutions/add/', views.institution_add, name='institution-add'),
    path('institutions/<int:institution_id>/', views.institution_detail, name='institution-detail'),
    path('institutions/<int:institution_id>/edit/', views.institution_edit, name='institution-edit'),
    
    # IFRS 17 Submissions
    path('ifrs17-submissions/', views.ifrs17_submissions, name='ifrs17-submissions'),
    path('ifrs17-submissions/<int:submission_id>/', views.ifrs17_submission_detail, name='ifrs17-submission-detail'),
    path('upload-ifrs17-data/', views.upload_ifrs17_data, name='upload_ifrs17_data'),
    
    # Institution Data
    path('institutions/<int:institution_id>/data/', views.institution_data, name='institution-data'),
    path('institutions/<int:institution_id>/validate/', views.validate_institution_data, name='institution-validate'),
    
    # File Data Parsing
    path('parse-file-data/<int:submission_id>/', views.parse_file_data, name='parse-file-data'),
    
    # Data Quality & Governance
    path('data-quality-review/', views.data_quality_review, name='data-quality-review'),
    path('reporting-period/<int:year>/<int:month>/', views.reporting_period_detail, name='reporting-period-detail'),
    path('run-data-quality-checks/', views.run_data_quality_checks, name='run-data-quality-checks'),
]
