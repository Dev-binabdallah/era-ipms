"""
ERA-IPMS Django model foundation.

The MariaDB/MySQL schema in database/schema.sql is the authoritative
database baseline. These models map the Django ORM to that schema.

The tables are intentionally unmanaged for this baseline because the
database schema is maintained separately and the existing MariaDB
database requires a deliberate migration plan before Django is allowed
to create/alter/drop application tables.
"""

from django.db import models


class Titles(models.Model):
    title_id = models.BigAutoField(primary_key=True)
    title_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "titles"


class Permissions(models.Model):
    permission_id = models.BigAutoField(primary_key=True)
    permission_code = models.CharField(max_length=100, unique=True)
    permission_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "permissions"


class Responsibilities(models.Model):
    responsibility_id = models.BigAutoField(primary_key=True)
    responsibility_code = models.CharField(max_length=100, unique=True)
    responsibility_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "responsibilities"


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    title = models.ForeignKey(
        Titles,
        on_delete=models.RESTRICT,
        db_column="title_id",
        related_name="users",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=150, unique=True, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_username(self):
        return self.username

    def get_session_auth_hash(self):
        return self.password_hash

    class Meta:
        managed = False
        db_table = "users"


class TitlePermissions(models.Model):
    title_permission_id = models.BigAutoField(primary_key=True)
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        db_column="title_id",
        related_name="title_permissions",
    )
    permission = models.ForeignKey(
        Permissions,
        on_delete=models.CASCADE,
        db_column="permission_id",
        related_name="title_permissions",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "title_permissions"


class UserResponsibilities(models.Model):
    user_responsibility_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="responsibility_assignments",
    )
    responsibility = models.ForeignKey(
        Responsibilities,
        on_delete=models.RESTRICT,
        db_column="responsibility_id",
        related_name="user_assignments",
    )
    assigned_at = models.DateTimeField()
    assigned_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="assigned_by",
        related_name="responsibilities_assigned",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "user_responsibilities"


class StaffMembers(models.Model):
    staff_member_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(
        Users,
        on_delete=models.RESTRICT,
        db_column="user_id",
        related_name="staff_profile",
    )
    full_name = models.CharField(max_length=200)
    person_type = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "staff_members"


class Projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="created_by",
        related_name="projects_created",
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "projects"


class UserProjectAssignments(models.Model):
    assignment_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        db_column="user_id",
        related_name="project_assignments",
    )
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        db_column="project_id",
        related_name="user_assignments",
    )
    assigned_at = models.DateTimeField()
    assigned_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="assigned_by",
        related_name="project_assignments_created",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = "user_project_assignments"


class Beneficiaries(models.Model):
    beneficiary_id = models.BigAutoField(primary_key=True)
    beneficiary_code = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="active")
    created_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="created_by",
        related_name="beneficiaries_created",
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "beneficiaries"


class DisabilityAssessments(models.Model):
    assessment_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(
        Beneficiaries,
        on_delete=models.RESTRICT,
        db_column="beneficiary_id",
        related_name="disability_assessments",
    )
    assessment_date = models.DateField()
    assessment_type = models.CharField(max_length=100, blank=True, null=True)
    disability_type = models.CharField(max_length=100, blank=True, null=True)
    needs = models.TextField(blank=True, null=True)
    assessment_notes = models.TextField(blank=True, null=True)
    assessed_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="assessed_by",
        related_name="disability_assessments_conducted",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "disability_assessments"


class HomeVisits(models.Model):
    home_visit_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(
        Beneficiaries,
        on_delete=models.RESTRICT,
        db_column="beneficiary_id",
        related_name="home_visits",
    )
    visit_date = models.DateField()
    conducted_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="conducted_by",
        related_name="home_visits_conducted",
    )
    purpose = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    support_provided = models.TextField(blank=True, null=True)
    follow_up_required = models.BooleanField(default=False)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "home_visits"


class Referrals(models.Model):
    referral_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(
        Beneficiaries,
        on_delete=models.RESTRICT,
        db_column="beneficiary_id",
        related_name="referrals",
    )
    referral_date = models.DateField()
    destination = models.CharField(max_length=255)
    reason = models.TextField(blank=True, null=True)
    referred_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="referred_by",
        related_name="referrals_created",
    )
    status = models.CharField(max_length=50, default="submitted")
    approved_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="approved_by",
        related_name="referrals_approved",
        blank=True,
        null=True,
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "referrals"


class ReferralFollowUps(models.Model):
    follow_up_id = models.BigAutoField(primary_key=True)
    referral = models.ForeignKey(
        Referrals,
        on_delete=models.CASCADE,
        db_column="referral_id",
        related_name="follow_ups",
    )
    follow_up_date = models.DateField()
    conducted_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="conducted_by",
        related_name="referral_follow_ups_conducted",
    )
    outcome = models.TextField(blank=True, null=True)
    service_received = models.BooleanField(default=False)
    remaining_needs = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "referral_follow_ups"


class Activities(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        db_column="project_id",
        related_name="activities",
    )
    activity_name = models.CharField(max_length=200)
    activity_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    responsible_user = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="responsible_user_id",
        related_name="activities_responsible",
    )
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "activities"


class ActivityAssignments(models.Model):
    activity_assignment_id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(
        Activities,
        on_delete=models.CASCADE,
        db_column="activity_id",
        related_name="assignments",
    )
    user = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="user_id",
        related_name="activity_assignments",
    )
    assigned_at = models.DateTimeField()
    assigned_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="assigned_by",
        related_name="activity_assignments_created",
        blank=True,
        null=True,
    )
    status = models.CharField(max_length=50, default="assigned")

    class Meta:
        managed = False
        db_table = "activity_assignments"


class ActivityParticipants(models.Model):
    participant_id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(
        Activities,
        on_delete=models.CASCADE,
        db_column="activity_id",
        related_name="participants",
    )
    beneficiary = models.ForeignKey(
        Beneficiaries,
        on_delete=models.RESTRICT,
        db_column="beneficiary_id",
        related_name="activity_participations",
    )
    participant_name = models.CharField(max_length=200, blank=True, null=True)
    participant_type = models.CharField(max_length=100, default="beneficiary")
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "activity_participants"


class PoultryGroups(models.Model):
    poultry_group_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        db_column="project_id",
        related_name="poultry_groups",
    )
    group_name = models.CharField(max_length=150)
    poultry_category = models.CharField(max_length=100, blank=True, null=True)
    breed_or_type = models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="active")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "poultry_groups"


class PoultryStockMovements(models.Model):
    movement_id = models.BigAutoField(primary_key=True)
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.CASCADE,
        db_column="poultry_group_id",
        related_name="stock_movements",
    )
    movement_date = models.DateField()
    movement_type = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="poultry_stock_movements",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "poultry_stock_movements"


class EggProduction(models.Model):
    egg_production_id = models.BigAutoField(primary_key=True)
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.CASCADE,
        db_column="poultry_group_id",
        related_name="egg_production_records",
    )
    production_date = models.DateField()
    eggs_produced = models.PositiveIntegerField(default=0)
    eggs_used = models.PositiveIntegerField(default=0)
    eggs_sold = models.PositiveIntegerField(default=0)
    eggs_remaining = models.PositiveIntegerField(default=0)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="egg_production_records",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "egg_production"


class FeedRecords(models.Model):
    feed_record_id = models.BigAutoField(primary_key=True)
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.CASCADE,
        db_column="poultry_group_id",
        related_name="feed_records",
    )
    record_date = models.DateField()
    feed_source = models.CharField(max_length=200, blank=True, null=True)
    feed_description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="feed_records",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "feed_records"


class PoultryHealthRecords(models.Model):
    health_record_id = models.BigAutoField(primary_key=True)
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.CASCADE,
        db_column="poultry_group_id",
        related_name="health_records",
    )
    record_date = models.DateField()
    condition_type = models.CharField(max_length=100)
    number_affected = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="poultry_health_records",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "poultry_health_records"


class PoultrySales(models.Model):
    poultry_sale_id = models.BigAutoField(primary_key=True)
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.CASCADE,
        db_column="poultry_group_id",
        related_name="sales",
    )
    sale_date = models.DateField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    buyer_description = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="poultry_sales",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "poultry_sales"


class FarmCrops(models.Model):
    crop_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,
        db_column="project_id",
        related_name="farm_crops",
    )
    crop_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    planting_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="active")
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="farm_crops_recorded",
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "farm_crops"


class FarmActivities(models.Model):
    farm_activity_id = models.BigAutoField(primary_key=True)
    crop = models.ForeignKey(
        FarmCrops,
        on_delete=models.CASCADE,
        db_column="crop_id",
        related_name="farm_activities",
    )
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="farm_activities_recorded",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "farm_activities"


class Harvests(models.Model):
    harvest_id = models.BigAutoField(primary_key=True)
    crop = models.ForeignKey(
        FarmCrops,
        on_delete=models.CASCADE,
        db_column="crop_id",
        related_name="harvests",
    )
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    usage_type = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="harvests_recorded",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "harvests"


class FarmPoultryTransfers(models.Model):
    transfer_id = models.BigAutoField(primary_key=True)
    harvest = models.ForeignKey(
        Harvests,
        on_delete=models.RESTRICT,
        db_column="harvest_id",
        related_name="poultry_transfers",
    )
    poultry_group = models.ForeignKey(
        PoultryGroups,
        on_delete=models.RESTRICT,
        db_column="poultry_group_id",
        related_name="farm_transfers",
    )
    transfer_date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="farm_poultry_transfers_recorded",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "farm_poultry_transfers"


class FinancialTransactions(models.Model):
    transaction_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.SET_NULL,
        db_column="project_id",
        related_name="financial_transactions",
        blank=True,
        null=True,
    )
    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=30)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="financial_transactions_recorded",
    )
    approved_by = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="approved_by",
        related_name="financial_transactions_approved",
        blank=True,
        null=True,
    )
    approved_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, default="recorded")
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "financial_transactions"


class MeIndicators(models.Model):
    indicator_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.SET_NULL,
        db_column="project_id",
        related_name="me_indicators",
        blank=True,
        null=True,
    )
    indicator_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    target_value = models.DecimalField(
        max_digits=14, decimal_places=2, blank=True, null=True
    )
    unit = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, default="active")
    created_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="created_by",
        related_name="me_indicators_created",
    )
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "me_indicators"


class MeIndicatorRecords(models.Model):
    indicator_record_id = models.BigAutoField(primary_key=True)
    indicator = models.ForeignKey(
        MeIndicators,
        on_delete=models.CASCADE,
        db_column="indicator_id",
        related_name="records",
    )
    record_date = models.DateField()
    recorded_value = models.DecimalField(max_digits=14, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey(
        Users,
        on_delete=models.RESTRICT,
        db_column="recorded_by",
        related_name="me_indicator_records",
    )
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "me_indicator_records"


class AuditEvents(models.Model):
    audit_event_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        Users,
        on_delete=models.SET_NULL,
        db_column="user_id",
        related_name="audit_events",
        blank=True,
        null=True,
    )
    event_type = models.CharField(max_length=50)
    entity_name = models.CharField(max_length=100, blank=True, null=True)
    entity_id = models.PositiveBigIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "audit_events"
