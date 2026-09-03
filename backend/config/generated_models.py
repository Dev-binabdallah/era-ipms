# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activities(models.Model):
    activity_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    activity_name = models.CharField(max_length=200)
    activity_date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    responsible_user = models.ForeignKey('Users', models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activities'


class ActivityParticipants(models.Model):
    participant_id = models.BigAutoField(primary_key=True)
    activity = models.ForeignKey(Activities, models.DO_NOTHING)
    beneficiary = models.ForeignKey('Beneficiaries', models.DO_NOTHING)
    participant_name = models.CharField(max_length=200, blank=True, null=True)
    participant_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'activity_participants'


class Beneficiaries(models.Model):
    beneficiary_id = models.BigAutoField(primary_key=True)
    beneficiary_code = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'beneficiaries'


class DisabilityAssessments(models.Model):
    assessment_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(Beneficiaries, models.DO_NOTHING)
    assessment_date = models.DateField()
    assessment_type = models.CharField(max_length=100, blank=True, null=True)
    disability_type = models.CharField(max_length=100, blank=True, null=True)
    needs = models.TextField(blank=True, null=True)
    assessment_notes = models.TextField(blank=True, null=True)
    assessed_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='assessed_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disability_assessments'


class EggProduction(models.Model):
    egg_production_id = models.BigAutoField(primary_key=True)
    production_date = models.DateField()
    eggs_produced = models.IntegerField()
    eggs_used = models.IntegerField(blank=True, null=True)
    eggs_sold = models.IntegerField(blank=True, null=True)
    eggs_remaining = models.IntegerField(blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'egg_production'


class Expenses(models.Model):
    expense_id = models.BigAutoField(primary_key=True)
    expense_date = models.DateField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING, blank=True, null=True)
    expense_area = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'expenses'


class FarmActivities(models.Model):
    farm_activity_id = models.BigAutoField(primary_key=True)
    crop = models.ForeignKey('FarmCrops', models.DO_NOTHING)
    activity_date = models.DateField()
    activity_type = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    conducted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='conducted_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'farm_activities'


class FarmCrops(models.Model):
    crop_id = models.BigAutoField(primary_key=True)
    crop_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    planting_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'farm_crops'


class FeedRecords(models.Model):
    feed_record_id = models.BigAutoField(primary_key=True)
    record_date = models.DateField()
    feed_source = models.CharField(max_length=200, blank=True, null=True)
    feed_description = models.TextField(blank=True, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    cost = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feed_records'


class Harvests(models.Model):
    harvest_id = models.BigAutoField(primary_key=True)
    crop = models.ForeignKey(FarmCrops, models.DO_NOTHING)
    harvest_date = models.DateField()
    quantity = models.DecimalField(max_digits=12, decimal_places=2)
    unit = models.CharField(max_length=50, blank=True, null=True)
    usage_type = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'harvests'


class HomeVisits(models.Model):
    home_visit_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(Beneficiaries, models.DO_NOTHING)
    visit_date = models.DateField()
    conducted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='conducted_by')
    purpose = models.CharField(max_length=255, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)
    support_provided = models.TextField(blank=True, null=True)
    follow_up_required = models.IntegerField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'home_visits'


class MeIndicators(models.Model):
    indicator_id = models.BigAutoField(primary_key=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    indicator_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    target_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    current_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    unit = models.CharField(max_length=50, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'me_indicators'


class PoultryHealthRecords(models.Model):
    health_record_id = models.BigAutoField(primary_key=True)
    record_date = models.DateField()
    condition_type = models.CharField(max_length=100)
    number_affected = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    action_taken = models.TextField(blank=True, null=True)
    outcome = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poultry_health_records'


class PoultryTransactions(models.Model):
    poultry_transaction_id = models.BigAutoField(primary_key=True)
    transaction_date = models.DateField()
    transaction_type = models.CharField(max_length=100)
    quantity = models.IntegerField()
    chicken_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    recorded_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='recorded_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'poultry_transactions'


class Projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    objectives = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    responsible_user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'projects'


class ReferralFollowUps(models.Model):
    follow_up_id = models.BigAutoField(primary_key=True)
    referral = models.ForeignKey('Referrals', models.DO_NOTHING)
    follow_up_date = models.DateField()
    conducted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='conducted_by')
    outcome = models.TextField(blank=True, null=True)
    service_received = models.IntegerField(blank=True, null=True)
    remaining_needs = models.TextField(blank=True, null=True)
    next_action = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referral_follow_ups'


class Referrals(models.Model):
    referral_id = models.BigAutoField(primary_key=True)
    beneficiary = models.ForeignKey(Beneficiaries, models.DO_NOTHING)
    referral_date = models.DateField()
    referral_destination = models.CharField(max_length=255)
    reason = models.TextField(blank=True, null=True)
    referred_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='referred_by')
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'referrals'


class Roles(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(unique=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class StaffVolunteers(models.Model):
    staff_volunteer_id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField('Users', models.DO_NOTHING)
    full_name = models.CharField(max_length=200)
    person_type = models.CharField(max_length=100)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=150, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'staff_volunteers'


class Users(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    role = models.ForeignKey(Roles, models.DO_NOTHING)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=150, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=30, blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
