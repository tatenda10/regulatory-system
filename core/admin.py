from django.contrib import admin
from .models import (
    Institution, IFRS17Submission, ComplianceAlert, InsuranceRevenue, 
    CSMProfitability, DiscountRates, ReinsuranceHeld, IFRS4Transition, 
    ContractGrouping, DataQualityCheck
)


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'institution_type', 'status', 'contact_person', 'email']
    list_filter = ['institution_type', 'status', 'country']
    search_fields = ['name', 'registration_number', 'license_number', 'contact_person', 'email']
    ordering = ['name']


@admin.register(IFRS17Submission)
class IFRS17SubmissionAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'status', 'contractual_service_margin', 'total_liabilities', 'submission_date']
    list_filter = ['status', 'reporting_period', 'institution__institution_type']
    search_fields = ['institution__name', 'notes']
    ordering = ['-submission_date']
    date_hierarchy = 'submission_date'


@admin.register(ComplianceAlert)
class ComplianceAlertAdmin(admin.ModelAdmin):
    list_display = ['institution', 'title', 'alert_type', 'severity', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'created_at']
    search_fields = ['title', 'description', 'institution__name']
    ordering = ['-created_at']


@admin.register(InsuranceRevenue)
class InsuranceRevenueAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'total_revenue', 'service_performance_ratio', 'created_at']
    list_filter = ['currency', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes']
    ordering = ['-reporting_period']


@admin.register(CSMProfitability)
class CSMProfitabilityAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'closing_csm', 'csm_profit_margin', 'csm_roi', 'created_at']
    list_filter = ['currency', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes']
    ordering = ['-reporting_period']


@admin.register(DiscountRates)
class DiscountRatesAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'total_discount_rate', 'net_finance_result', 'created_at']
    list_filter = ['currency', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes']
    ordering = ['-reporting_period']


@admin.register(ReinsuranceHeld)
class ReinsuranceHeldAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'total_reinsurance_held', 'risk_transfer_ratio', 'created_at']
    list_filter = ['currency', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes']
    ordering = ['-reporting_period']


@admin.register(IFRS4Transition)
class IFRS4TransitionAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'implementation_status', 'equity_impact', 'created_at']
    list_filter = ['currency', 'implementation_status', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes']
    ordering = ['-reporting_period']


@admin.register(ContractGrouping)
class ContractGroupingAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'product_line', 'contract_type', 'number_of_contracts', 'created_at']
    list_filter = ['currency', 'product_line', 'contract_type', 'measurement_model', 'risk_profile', 'reporting_period', 'created_at']
    search_fields = ['institution__name', 'product_line', 'contract_type', 'notes']
    ordering = ['-reporting_period', 'product_line']


@admin.register(DataQualityCheck)
class DataQualityCheckAdmin(admin.ModelAdmin):
    list_display = ['institution', 'reporting_period', 'currency', 'overall_quality_score', 'data_governance_score', 'critical_issues', 'created_at']
    list_filter = ['currency', 'reporting_period', 'institution__institution_type', 'created_at']
    search_fields = ['institution__name', 'notes', 'remediation_plan']
    ordering = ['-reporting_period']
