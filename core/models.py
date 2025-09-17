from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """Base model with common fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Institution(BaseModel):
    """Insurance institution/company model."""
    name = models.CharField(max_length=200, unique=True)
    registration_number = models.CharField(max_length=50, unique=True)
    license_number = models.CharField(max_length=50, unique=True)
    institution_type = models.CharField(
        max_length=20,
        choices=[
            ('life', 'Life Insurance'),
            ('general', 'General Insurance'),
            ('composite', 'Composite'),
            ('reinsurance', 'Reinsurance'),
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('inactive', 'Inactive'),
        ],
        default='active'
    )
    contact_person = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Zimbabwe')
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class IFRS17Submission(BaseModel):
    """IFRS 17 data submission from institutions."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='ifrs17_submissions')
    reporting_period = models.DateField()
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='draft'
    )
    
    # IFRS 17 Key Metrics
    contractual_service_margin = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    risk_adjustment = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    loss_component = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    total_liabilities = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Additional metrics
    equity_impact = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    solvency_ratio = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # File upload
    uploaded_file = models.FileField(upload_to='ifrs17_submissions/%Y/%m/', null=True, blank=True)
    file_type = models.CharField(max_length=10, choices=[('csv', 'CSV'), ('xlsx', 'Excel'), ('xbrl', 'XBRL')], null=True, blank=True)
    
    notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    review_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-submission_date']
        # Removed unique_together to allow multiple files per institution/period
    
    def __str__(self):
        return f"{self.institution.name} - {self.reporting_period}"


class ComplianceAlert(BaseModel):
    """Compliance alerts and warnings."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('overdue', 'Overdue Submission'),
            ('non_compliant', 'Non-Compliant'),
            ('warning', 'Warning'),
            ('info', 'Information'),
        ]
    )
    severity = models.CharField(
        max_length=10,
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ]
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_resolved = models.BooleanField(default=False)
    resolved_date = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.institution.name} - {self.title}"


class InsuranceRevenue(BaseModel):
    """Insurance Revenue and Service Performance data."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='revenue_data')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # Revenue Recognition
    insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    service_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Service Performance
    contracts_fulfilled = models.IntegerField()
    contracts_ongoing = models.IntegerField()
    service_performance_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Revenue by Product Line
    life_insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    health_insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    general_insurance_revenue = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - Revenue {self.reporting_period} ({self.currency})"


class CSMProfitability(BaseModel):
    """CSM Profitability tracking and analysis."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='csm_profitability')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # CSM Performance Metrics
    opening_csm = models.DecimalField(max_digits=15, decimal_places=2)
    new_contracts_csm = models.DecimalField(max_digits=15, decimal_places=2)
    interest_accretion = models.DecimalField(max_digits=15, decimal_places=2)
    experience_adjustments = models.DecimalField(max_digits=15, decimal_places=2)
    csm_release = models.DecimalField(max_digits=15, decimal_places=2)
    closing_csm = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Profitability Analysis
    csm_profit_margin = models.DecimalField(max_digits=5, decimal_places=2)
    csm_roi = models.DecimalField(max_digits=5, decimal_places=2)
    expected_profit = models.DecimalField(max_digits=15, decimal_places=2)
    actual_profit = models.DecimalField(max_digits=15, decimal_places=2)
    profit_variance = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Contract Group Performance
    profitable_contracts = models.IntegerField()
    loss_making_contracts = models.IntegerField()
    break_even_contracts = models.IntegerField()
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - CSM Profitability {self.reporting_period} ({self.currency})"


class DiscountRates(BaseModel):
    """Discount Rates and Insurance Finance Result data."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='discount_rates')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # Discount Rate Components
    risk_free_rate = models.DecimalField(max_digits=5, decimal_places=2)
    liquidity_premium = models.DecimalField(max_digits=5, decimal_places=2)
    credit_spread = models.DecimalField(max_digits=5, decimal_places=2)
    total_discount_rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Insurance Finance Result
    finance_income = models.DecimalField(max_digits=15, decimal_places=2)
    finance_expense = models.DecimalField(max_digits=15, decimal_places=2)
    net_finance_result = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Rate Sensitivity Analysis
    rate_sensitivity_1bp = models.DecimalField(max_digits=15, decimal_places=2)
    rate_sensitivity_10bp = models.DecimalField(max_digits=15, decimal_places=2)
    rate_sensitivity_100bp = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Currency-specific rates
    usd_discount_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    zwl_discount_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - Discount Rates {self.reporting_period} ({self.currency})"


class ReinsuranceHeld(BaseModel):
    """Reinsurance Held data and analysis."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='reinsurance_data')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # Reinsurance Assets
    reinsurance_assets = models.DecimalField(max_digits=15, decimal_places=2)
    recoverable_amounts = models.DecimalField(max_digits=15, decimal_places=2)
    expected_recoveries = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Reinsurance Types
    proportional_reinsurance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    non_proportional_reinsurance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    facultative_reinsurance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    treaty_reinsurance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Reinsurance Counterparties
    domestic_reinsurers = models.DecimalField(max_digits=15, decimal_places=2)
    international_reinsurers = models.DecimalField(max_digits=15, decimal_places=2)
    total_reinsurance_held = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Risk Transfer Analysis
    risk_transfer_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    concentration_risk = models.DecimalField(max_digits=5, decimal_places=2)
    counterparty_credit_risk = models.DecimalField(max_digits=5, decimal_places=2)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - Reinsurance {self.reporting_period} ({self.currency})"


class IFRS4Transition(BaseModel):
    """IFRS4 to IFRS17 transition tracking."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='ifrs4_transitions')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # IFRS4 Baseline
    ifrs4_liabilities = models.DecimalField(max_digits=15, decimal_places=2)
    ifrs4_premiums = models.DecimalField(max_digits=15, decimal_places=2)
    ifrs4_claims = models.DecimalField(max_digits=15, decimal_places=2)
    
    # IFRS17 Implementation
    ifrs17_liabilities = models.DecimalField(max_digits=15, decimal_places=2)
    ifrs17_csm = models.DecimalField(max_digits=15, decimal_places=2)
    ifrs17_risk_adjustment = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Transition Impact
    liability_adjustment = models.DecimalField(max_digits=15, decimal_places=2)
    equity_impact = models.DecimalField(max_digits=15, decimal_places=2)
    pnl_impact = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Implementation Status
    implementation_status = models.CharField(
        max_length=20,
        choices=[
            ('planning', 'Planning Phase'),
            ('pilot', 'Pilot Testing'),
            ('implementation', 'Implementation'),
            ('completed', 'Completed'),
            ('monitoring', 'Monitoring'),
        ]
    )
    
    # Compliance Metrics
    data_quality_score = models.DecimalField(max_digits=5, decimal_places=2)
    process_maturity_score = models.DecimalField(max_digits=5, decimal_places=2)
    system_readiness_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - IFRS4 Transition {self.reporting_period} ({self.currency})"


class ContractGrouping(BaseModel):
    """Contract Grouping and Aggregation data."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='contract_groupings')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # Grouping Criteria
    product_line = models.CharField(max_length=50)
    contract_type = models.CharField(max_length=50)
    measurement_model = models.CharField(
        max_length=10,
        choices=[
            ('GMM', 'General Measurement Model'),
            ('PAA', 'Premium Allocation Approach'),
            ('VFA', 'Variable Fee Approach'),
        ]
    )
    
    # Group Statistics
    number_of_contracts = models.IntegerField()
    total_contract_value = models.DecimalField(max_digits=15, decimal_places=2)
    average_contract_value = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Aggregation Metrics
    contracts_per_group = models.IntegerField()
    materiality_threshold = models.DecimalField(max_digits=15, decimal_places=2)
    grouping_efficiency = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Risk Characteristics
    risk_profile = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ])
    volatility_score = models.DecimalField(max_digits=5, decimal_places=2)
    correlation_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period', 'product_line']
        unique_together = ['institution', 'reporting_period', 'currency', 'product_line', 'contract_type']
    
    def __str__(self):
        return f"{self.institution.name} - {self.product_line} Grouping {self.reporting_period} ({self.currency})"


class DataQualityCheck(BaseModel):
    """Data Quality and Governance checks for ZWL and USD accounts."""
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='data_quality_checks')
    reporting_period = models.DateField()
    currency = models.CharField(max_length=3, choices=[('ZWL', 'Zimbabwe Dollar'), ('USD', 'US Dollar')])
    
    # Data Quality Metrics
    completeness_score = models.DecimalField(max_digits=5, decimal_places=2)
    accuracy_score = models.DecimalField(max_digits=5, decimal_places=2)
    consistency_score = models.DecimalField(max_digits=5, decimal_places=2)
    timeliness_score = models.DecimalField(max_digits=5, decimal_places=2)
    overall_quality_score = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Governance Checks
    data_governance_score = models.DecimalField(max_digits=5, decimal_places=2)
    control_effectiveness = models.DecimalField(max_digits=5, decimal_places=2)
    audit_trail_completeness = models.DecimalField(max_digits=5, decimal_places=2)
    regulatory_compliance = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Currency-specific Issues
    exchange_rate_consistency = models.BooleanField(default=True)
    currency_conversion_accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    multi_currency_reconciliation = models.BooleanField(default=True)
    
    # Data Issues
    missing_data_points = models.IntegerField(default=0)
    data_anomalies = models.IntegerField(default=0)
    validation_errors = models.IntegerField(default=0)
    critical_issues = models.IntegerField(default=0)
    
    # Remediation
    issues_resolved = models.IntegerField(default=0)
    pending_issues = models.IntegerField(default=0)
    remediation_plan = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-reporting_period']
        unique_together = ['institution', 'reporting_period', 'currency']
    
    def __str__(self):
        return f"{self.institution.name} - Data Quality {self.reporting_period} ({self.currency})"
