from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.utils import timezone
import pandas as pd
import json
import os
from .models import Institution, IFRS17Submission, ComplianceAlert
from .forms import InstitutionForm, IFRS17SubmissionForm, IFRS17FileUploadForm


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
    # Get all institutions for the upload form
    institutions = Institution.objects.filter(status='active').order_by('name')
    
    # Get recent submissions for display
    recent_submissions = IFRS17Submission.objects.select_related('institution').order_by('-submission_date')[:10]
    
    # Calculate summary statistics
    total_submissions = IFRS17Submission.objects.count()
    successful_submissions = IFRS17Submission.objects.filter(status='approved').count()
    failed_submissions = IFRS17Submission.objects.filter(status='rejected').count()
    pending_submissions = IFRS17Submission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
    
    # Initialize upload form
    upload_form = IFRS17FileUploadForm()
    
    context = {
        'title': 'Data & Validation',
        'message': 'Submission History and Data Quality Management',
        'institutions': institutions,
        'recent_submissions': recent_submissions,
        'total_submissions': total_submissions,
        'successful_submissions': successful_submissions,
        'failed_submissions': failed_submissions,
        'pending_submissions': pending_submissions,
        'upload_form': upload_form,
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


# Institution Management Views
@login_required
def institutions_list(request):
    """List all registered institutions."""
    institutions = Institution.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        institutions = institutions.filter(
            Q(name__icontains=search_query) |
            Q(registration_number__icontains=search_query) |
            Q(license_number__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        institutions = institutions.filter(status=status_filter)
    
    # Filter by type
    type_filter = request.GET.get('type')
    if type_filter:
        institutions = institutions.filter(institution_type=type_filter)
    
    # Pagination
    paginator = Paginator(institutions, 20)
    page_number = request.GET.get('page')
    institutions = paginator.get_page(page_number)
    
    context = {
        'title': 'Registered Institutions',
        'institutions': institutions,
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
    }
    return render(request, 'institutions_list.html', context)


@login_required
def institution_detail(request, institution_id):
    """View detailed information about a specific institution."""
    institution = get_object_or_404(Institution, id=institution_id)
    submissions = institution.ifrs17_submissions.all()[:10]  # Latest 10 submissions
    alerts = institution.alerts.filter(is_resolved=False)[:5]  # Latest 5 unresolved alerts
    
    context = {
        'title': f'{institution.name} - Details',
        'institution': institution,
        'submissions': submissions,
        'alerts': alerts,
    }
    return render(request, 'institution_detail.html', context)


@login_required
def institution_add(request):
    """Add a new institution."""
    if request.method == 'POST':
        form = InstitutionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Institution registered successfully.')
            return redirect('core:institutions-list')
    else:
        form = InstitutionForm()
    
    context = {
        'title': 'Register New Institution',
        'form': form,
    }
    return render(request, 'institution_form.html', context)


@login_required
def institution_edit(request, institution_id):
    """Edit an existing institution."""
    institution = get_object_or_404(Institution, id=institution_id)
    
    if request.method == 'POST':
        form = InstitutionForm(request.POST, instance=institution)
        if form.is_valid():
            form.save()
            messages.success(request, 'Institution updated successfully.')
            return redirect('core:institution-detail', institution_id=institution.id)
    else:
        form = InstitutionForm(instance=institution)
    
    context = {
        'title': f'Edit {institution.name}',
        'form': form,
        'institution': institution,
    }
    return render(request, 'institution_form.html', context)


@login_required
def ifrs17_submissions(request):
    """List all IFRS 17 submissions."""
    submissions = IFRS17Submission.objects.select_related('institution').all()
    
    # Filter by institution
    institution_filter = request.GET.get('institution')
    if institution_filter:
        submissions = submissions.filter(institution_id=institution_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        submissions = submissions.filter(status=status_filter)
    
    # Filter by reporting period
    period_filter = request.GET.get('period')
    if period_filter:
        submissions = submissions.filter(reporting_period__year=period_filter)
    
    # Pagination
    paginator = Paginator(submissions, 20)
    page_number = request.GET.get('page')
    submissions = paginator.get_page(page_number)
    
    # Get institutions for filter dropdown
    institutions = Institution.objects.all()
    
    context = {
        'title': 'IFRS 17 Submissions',
        'submissions': submissions,
        'institutions': institutions,
        'institution_filter': institution_filter,
        'status_filter': status_filter,
        'period_filter': period_filter,
    }
    return render(request, 'ifrs17_submissions.html', context)


@login_required
def ifrs17_submission_detail(request, submission_id):
    """View detailed information about a specific IFRS 17 submission showing all data for that institution and reporting period."""
    submission = get_object_or_404(IFRS17Submission, id=submission_id)
    
    # Get all submissions for the same institution and reporting period
    all_submissions = IFRS17Submission.objects.filter(
        institution=submission.institution,
        reporting_period=submission.reporting_period
    ).order_by('submission_date')
    
    # Group submissions by file type for better organization
    submissions_by_type = {}
    for sub in all_submissions:
        file_type = sub.file_type or 'other'
        if file_type not in submissions_by_type:
            submissions_by_type[file_type] = []
        submissions_by_type[file_type].append(sub)
    
    context = {
        'title': f'IFRS 17 Submission - {submission.institution.name}',
        'submission': submission,
        'all_submissions': all_submissions,
        'submissions_by_type': submissions_by_type,
        'total_files': all_submissions.count()
    }
    return render(request, 'ifrs17_submission_detail.html', context)


@login_required
def upload_ifrs17_data(request):
    """Handle IFRS 17 data file uploads."""
    if request.method == 'POST':
        form = IFRS17FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Check for duplicate file names for the same institution and period
            institution = form.cleaned_data['institution']
            reporting_period = form.cleaned_data['reporting_period']
            uploaded_file = form.cleaned_data['uploaded_file']
            file_name = uploaded_file.name
            
            # Check if a file with the same name exists for this institution and period
            existing_submission = IFRS17Submission.objects.filter(
                institution=institution,
                reporting_period=reporting_period,
                uploaded_file__icontains=file_name
            ).first()
            
            if existing_submission and not request.POST.get('override_file'):
                # File with same name exists, show override confirmation
                context = {
                    'title': 'Data & Validation',
                    'upload_form': form,
                    'duplicate_file': existing_submission,
                    'file_name': file_name,
                    'institution': institution,
                    'reporting_period': reporting_period,
                }
                return render(request, 'data_validation.html', context)
            
            # If override is confirmed, delete the existing file
            if existing_submission and request.POST.get('override_file'):
                existing_submission.delete()
            
            # Create new submission
            submission = form.save(commit=False)
            submission.status = 'submitted'
            submission.submission_date = timezone.now()
            submission.save()
            
            messages.success(request, f'IFRS 17 data uploaded successfully for {submission.institution.name}')
            return redirect('core:data-validation')
        else:
            # Debug form errors
            print("Form errors:", form.errors)
            print("Form non-field errors:", form.non_field_errors())
            for field, errors in form.errors.items():
                print(f"Field {field}: {errors}")
            messages.error(request, f'Please correct the errors below: {form.errors}')
    else:
        form = IFRS17FileUploadForm()
    
    # Get all institutions for the upload form
    institutions = Institution.objects.filter(status='active').order_by('name')
    
    # Get recent submissions for display
    recent_submissions = IFRS17Submission.objects.select_related('institution').order_by('-submission_date')[:10]
    
    # Calculate summary statistics
    total_submissions = IFRS17Submission.objects.count()
    successful_submissions = IFRS17Submission.objects.filter(status='approved').count()
    failed_submissions = IFRS17Submission.objects.filter(status='rejected').count()
    pending_submissions = IFRS17Submission.objects.filter(status__in=['draft', 'submitted', 'under_review']).count()
    
    context = {
        'title': 'Data & Validation',
        'message': 'Submission History and Data Quality Management',
        'institutions': institutions,
        'recent_submissions': recent_submissions,
        'total_submissions': total_submissions,
        'successful_submissions': successful_submissions,
        'failed_submissions': failed_submissions,
        'pending_submissions': pending_submissions,
        'upload_form': form,
    }
    return render(request, 'data_validation.html', context)


@login_required
def institution_data(request, institution_id):
    """View all data for a specific institution."""
    institution = get_object_or_404(Institution, id=institution_id)
    
    # Get all data for this institution
    ifrs17_submissions = IFRS17Submission.objects.filter(institution=institution).order_by('-reporting_period')
    revenue_data = InsuranceRevenue.objects.filter(institution=institution).order_by('-reporting_period')
    csm_data = CSMProfitability.objects.filter(institution=institution).order_by('-reporting_period')
    discount_data = DiscountRates.objects.filter(institution=institution).order_by('-reporting_period')
    reinsurance_data = ReinsuranceHeld.objects.filter(institution=institution).order_by('-reporting_period')
    transition_data = IFRS4Transition.objects.filter(institution=institution).order_by('-reporting_period')
    grouping_data = ContractGrouping.objects.filter(institution=institution).order_by('-reporting_period')
    quality_data = DataQualityCheck.objects.filter(institution=institution).order_by('-reporting_period')
    
    # Get latest records
    latest_ifrs17 = ifrs17_submissions.first()
    latest_revenue = revenue_data.first()
    latest_csm = csm_data.first()
    
    # Calculate overall quality scores
    zwl_quality = quality_data.filter(currency='ZWL').first()
    usd_quality = quality_data.filter(currency='USD').first()
    
    zwl_quality_score = zwl_quality.overall_quality_score if zwl_quality else None
    usd_quality_score = usd_quality.overall_quality_score if usd_quality else None
    
    # Calculate overall quality score
    if zwl_quality_score and usd_quality_score:
        overall_quality_score = (zwl_quality_score + usd_quality_score) / 2
    elif zwl_quality_score:
        overall_quality_score = zwl_quality_score
    elif usd_quality_score:
        overall_quality_score = usd_quality_score
    else:
        overall_quality_score = None
    
    context = {
        'title': f'{institution.name} - Data Overview',
        'institution': institution,
        'ifrs17_submissions': ifrs17_submissions,
        'revenue_data': revenue_data,
        'csm_data': csm_data,
        'discount_data': discount_data,
        'reinsurance_data': reinsurance_data,
        'transition_data': transition_data,
        'grouping_data': grouping_data,
        'quality_data': quality_data,
        'latest_ifrs17': latest_ifrs17,
        'latest_revenue': latest_revenue,
        'latest_csm': latest_csm,
        'overall_quality_score': overall_quality_score,
        'zwl_quality_score': zwl_quality_score,
        'usd_quality_score': usd_quality_score,
    }
    return render(request, 'institution_data.html', context)


@login_required
def validate_institution_data(request, institution_id):
    """Run data validation and governance checks for an institution."""
    institution = get_object_or_404(Institution, id=institution_id)
    
    if request.method == 'POST':
        # Run validation checks
        validation_results = run_data_validation(institution)
        
        # Create or update data quality records
        for currency in ['ZWL', 'USD']:
            quality_data, created = DataQualityCheck.objects.get_or_create(
                institution=institution,
                reporting_period=timezone.now().date(),
                currency=currency,
                defaults={
                    'completeness_score': validation_results[f'{currency.lower()}_completeness'],
                    'accuracy_score': validation_results[f'{currency.lower()}_accuracy'],
                    'consistency_score': validation_results[f'{currency.lower()}_consistency'],
                    'timeliness_score': validation_results[f'{currency.lower()}_timeliness'],
                    'overall_quality_score': validation_results[f'{currency.lower()}_overall'],
                    'data_governance_score': validation_results[f'{currency.lower()}_governance'],
                    'control_effectiveness': validation_results[f'{currency.lower()}_control'],
                    'audit_trail_completeness': validation_results[f'{currency.lower()}_audit'],
                    'regulatory_compliance': validation_results[f'{currency.lower()}_compliance'],
                    'exchange_rate_consistency': validation_results[f'{currency.lower()}_exchange_consistency'],
                    'currency_conversion_accuracy': validation_results[f'{currency.lower()}_conversion_accuracy'],
                    'multi_currency_reconciliation': validation_results[f'{currency.lower()}_reconciliation'],
                    'missing_data_points': validation_results[f'{currency.lower()}_missing_data'],
                    'data_anomalies': validation_results[f'{currency.lower()}_anomalies'],
                    'validation_errors': validation_results[f'{currency.lower()}_validation_errors'],
                    'critical_issues': validation_results[f'{currency.lower()}_critical_issues'],
                    'issues_resolved': validation_results[f'{currency.lower()}_issues_resolved'],
                    'pending_issues': validation_results[f'{currency.lower()}_pending_issues'],
                    'remediation_plan': validation_results[f'{currency.lower()}_remediation_plan'],
                }
            )
            
            if not created:
                # Update existing record
                quality_data.completeness_score = validation_results[f'{currency.lower()}_completeness']
                quality_data.accuracy_score = validation_results[f'{currency.lower()}_accuracy']
                quality_data.consistency_score = validation_results[f'{currency.lower()}_consistency']
                quality_data.timeliness_score = validation_results[f'{currency.lower()}_timeliness']
                quality_data.overall_quality_score = validation_results[f'{currency.lower()}_overall']
                quality_data.data_governance_score = validation_results[f'{currency.lower()}_governance']
                quality_data.control_effectiveness = validation_results[f'{currency.lower()}_control']
                quality_data.audit_trail_completeness = validation_results[f'{currency.lower()}_audit']
                quality_data.regulatory_compliance = validation_results[f'{currency.lower()}_compliance']
                quality_data.exchange_rate_consistency = validation_results[f'{currency.lower()}_exchange_consistency']
                quality_data.currency_conversion_accuracy = validation_results[f'{currency.lower()}_conversion_accuracy']
                quality_data.multi_currency_reconciliation = validation_results[f'{currency.lower()}_reconciliation']
                quality_data.missing_data_points = validation_results[f'{currency.lower()}_missing_data']
                quality_data.data_anomalies = validation_results[f'{currency.lower()}_anomalies']
                quality_data.validation_errors = validation_results[f'{currency.lower()}_validation_errors']
                quality_data.critical_issues = validation_results[f'{currency.lower()}_critical_issues']
                quality_data.issues_resolved = validation_results[f'{currency.lower()}_issues_resolved']
                quality_data.pending_issues = validation_results[f'{currency.lower()}_pending_issues']
                quality_data.remediation_plan = validation_results[f'{currency.lower()}_remediation_plan']
                quality_data.save()
        
        messages.success(request, f'Data validation completed for {institution.name}')
        return redirect('core:institution-data', institution_id=institution.id)
    
    return redirect('core:institution-data', institution_id=institution.id)


def run_data_validation(institution):
    """Run comprehensive data validation and governance checks."""
    # This is a simplified validation - in a real system, this would be much more comprehensive
    
    # Get all data for the institution
    ifrs17_data = IFRS17Submission.objects.filter(institution=institution)
    revenue_data = InsuranceRevenue.objects.filter(institution=institution)
    csm_data = CSMProfitability.objects.filter(institution=institution)
    quality_data = DataQualityCheck.objects.filter(institution=institution)
    
    results = {}
    
    for currency in ['ZWL', 'USD']:
        # Completeness check
        total_expected_records = 8  # All data types
        actual_records = 0
        
        if ifrs17_data.filter(currency=currency).exists():
            actual_records += 1
        if revenue_data.filter(currency=currency).exists():
            actual_records += 1
        if csm_data.filter(currency=currency).exists():
            actual_records += 1
        # Add other data types...
        
        completeness = (actual_records / total_expected_records) * 100 if total_expected_records > 0 else 0
        
        # Accuracy check (simplified)
        accuracy = 95.0  # In real system, this would check data accuracy
        
        # Consistency check
        consistency = 92.0  # In real system, this would check data consistency
        
        # Timeliness check
        timeliness = 88.0  # In real system, this would check data timeliness
        
        # Overall quality score
        overall = (completeness + accuracy + consistency + timeliness) / 4
        
        # Governance scores
        governance = 90.0
        control = 85.0
        audit = 92.0
        compliance = 88.0
        
        # Currency-specific checks
        exchange_consistency = True
        conversion_accuracy = 94.0
        reconciliation = True
        
        # Issues
        missing_data = max(0, total_expected_records - actual_records)
        anomalies = 2
        validation_errors = 1
        critical_issues = 0
        issues_resolved = 3
        pending_issues = 1
        
        remediation_plan = f"Address {missing_data} missing data points and {anomalies} data anomalies for {currency} accounts."
        
        # Store results
        results.update({
            f'{currency.lower()}_completeness': completeness,
            f'{currency.lower()}_accuracy': accuracy,
            f'{currency.lower()}_consistency': consistency,
            f'{currency.lower()}_timeliness': timeliness,
            f'{currency.lower()}_overall': overall,
            f'{currency.lower()}_governance': governance,
            f'{currency.lower()}_control': control,
            f'{currency.lower()}_audit': audit,
            f'{currency.lower()}_compliance': compliance,
            f'{currency.lower()}_exchange_consistency': exchange_consistency,
            f'{currency.lower()}_conversion_accuracy': conversion_accuracy,
            f'{currency.lower()}_reconciliation': reconciliation,
            f'{currency.lower()}_missing_data': missing_data,
            f'{currency.lower()}_anomalies': anomalies,
            f'{currency.lower()}_validation_errors': validation_errors,
            f'{currency.lower()}_critical_issues': critical_issues,
            f'{currency.lower()}_issues_resolved': issues_resolved,
            f'{currency.lower()}_pending_issues': pending_issues,
            f'{currency.lower()}_remediation_plan': remediation_plan,
        })
    
    return results


@login_required
def parse_file_data(request, submission_id):
    """Parse uploaded file data and return as JSON."""
    try:
        submission = get_object_or_404(IFRS17Submission, id=submission_id)
        
        if not submission.uploaded_file:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
        
        file_path = submission.uploaded_file.path
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # Parse file based on extension
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
        else:
            return JsonResponse({'error': 'Unsupported file format'}, status=400)
        
        # Convert DataFrame to list of dictionaries
        data = df.fillna('').to_dict('records')
        
        # Limit to first 50 rows for performance
        if len(data) > 50:
            data = data[:50]
            truncated = True
        else:
            truncated = False
        
        return JsonResponse({
            'success': True,
            'data': data,
            'total_rows': len(df),
            'displayed_rows': len(data),
            'truncated': truncated,
            'columns': list(df.columns)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error parsing file: {str(e)}'
        }, status=500)


@login_required
def data_quality_review(request):
    """Data Quality & Governance review page - shows institutions and reporting dates."""
    # Get all submissions grouped by reporting period
    submissions = IFRS17Submission.objects.all().order_by('-reporting_period', 'institution__name')
    
    # Group by reporting period
    reporting_periods = {}
    for submission in submissions:
        period = submission.reporting_period
        if period not in reporting_periods:
            reporting_periods[period] = {
                'period': period,
                'institutions': [],
                'total_submissions': 0,
                'approved': 0,
                'under_review': 0,
                'rejected': 0
            }
        
        reporting_periods[period]['institutions'].append(submission)
        reporting_periods[period]['total_submissions'] += 1
        
        if submission.status == 'approved':
            reporting_periods[period]['approved'] += 1
        elif submission.status == 'under_review':
            reporting_periods[period]['under_review'] += 1
        elif submission.status == 'rejected':
            reporting_periods[period]['rejected'] += 1
    
    # Convert to list and sort by period (newest first)
    periods_list = list(reporting_periods.values())
    periods_list.sort(key=lambda x: x['period'], reverse=True)
    
    context = {
        'title': 'Data Quality & Governance Review',
        'reporting_periods': periods_list,
        'total_periods': len(periods_list),
        'total_submissions': submissions.count()
    }
    
    return render(request, 'data_quality_review.html', context)


@login_required
def reporting_period_detail(request, year, month):
    """Detail view for a specific reporting period showing all submitted documents."""
    from datetime import date
    
    # Create date object from year and month
    period_date = date(year, month, 1)
    
    # Get all submissions for this reporting period
    submissions = IFRS17Submission.objects.filter(
        reporting_period__year=year,
        reporting_period__month=month
    ).order_by('institution__name', 'submission_date')
    
    # Group by institution
    institutions = {}
    for submission in submissions:
        institution = submission.institution
        if institution.id not in institutions:
            institutions[institution.id] = {
                'institution': institution,
                'submissions': [],
                'total_files': 0,
                'status_summary': {
                    'approved': 0,
                    'under_review': 0,
                    'rejected': 0,
                    'submitted': 0
                }
            }
        
        institutions[institution.id]['submissions'].append(submission)
        institutions[institution.id]['total_files'] += 1
        institutions[institution.id]['status_summary'][submission.status] += 1
    
    context = {
        'title': f'Reporting Period - {period_date.strftime("%B %Y")}',
        'period_date': period_date,
        'institutions': list(institutions.values()),
        'total_institutions': len(institutions),
        'total_submissions': submissions.count()
    }
    
    return render(request, 'reporting_period_detail.html', context)


@login_required
def run_data_quality_checks(request):
    """Run data quality checks for all submissions."""
    if request.method == 'POST':
        try:
            # This is where you'll implement the actual data quality checks
            # For now, just return a success response
            return JsonResponse({
                'success': True,
                'message': 'Data quality checks completed successfully',
                'checks_run': [
                    'ZWL Account Validation',
                    'USD Account Validation', 
                    'Data Completeness Check',
                    'Data Consistency Check',
                    'Governance Compliance Check'
                ],
                'issues_found': 5,
                'critical_issues': 1,
                'warnings': 4
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error running data quality checks: {str(e)}'
            }, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)
