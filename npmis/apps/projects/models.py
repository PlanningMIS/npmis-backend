import datetime
import os
import uuid

from django.db import models
from django.utils.text import slugify

from npmis.apps.settings.models import Subsector, Sector, Vote, Programme, TdvGoal, SdgGoal, AgendaGoal, FydpGoal, \
    ProjectNature, Currency, FundSource, FundCategory, FinancingModality, Financier


class Project(models.Model):
    COUNTERPART = "CounterPart"
    SINGLE = "Single"
    MULTIFINANCING = "MultiFinancing"
    FINANCING_STRUCTURE_CHOICES = {
        COUNTERPART: "Counter Part",
        SINGLE: "Single",
        MULTIFINANCING: "Multi-Financing",
    }

    DRAFT = "DRAFT"
    PENDING = "PENDING"
    RECOMMENDED = "RECOMMENDED"
    APPROVED = "APPROVED"

    PROJECT_STATUS_CHOICES = {
        DRAFT: 'Draft',
        PENDING: 'Pending',
        RECOMMENDED: 'Recommended',
        APPROVED: 'Approved',
    }

    def upload_to(instance, filename):
        """Generate a new unique filename for the uploaded concept note."""
        ext = os.path.splitext(filename)[1]  # Extract file extension
        project_id = slugify(instance.project_id)
        new_filename = f"{project_id}_{uuid.uuid4().hex}{ext}"  # Generate unique filename
        return os.path.join("concept_notes/", new_filename)  # Store in 'concept_notes/' folder

    project_id = models.CharField(primary_key=True, max_length=15)
    project_no = models.CharField(max_length=15, blank=True, null=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField()
    project_nature = models.ForeignKey(ProjectNature, models.DO_NOTHING, blank=True, null=True)
    project_objective = models.CharField(max_length=1000)
    programme = models.ForeignKey(Programme, models.DO_NOTHING, blank=True, null=True)
    project_background = models.TextField()
    exp_start_date = models.DateField()
    exp_completion_date = models.DateField()
    sector = models.ForeignKey(Sector, models.DO_NOTHING)
    subsector = models.ForeignKey(Subsector, models.DO_NOTHING)
    vote = models.ForeignKey(Vote, models.DO_NOTHING, blank=True, null=True)
    costcentre = models.CharField(max_length=15, blank=True, null=True)
    estimated_cost = models.FloatField()
    lifespan = models.SmallIntegerField()
    concept_note = models.FileField(upload_to=upload_to, blank=True, null=True)
    financing_structure = models.CharField(max_length=255, choices=FINANCING_STRUCTURE_CHOICES, default='Single')
    prioritization = models.CharField(max_length=50, blank=True, null=True)
    tdv_goal = models.ForeignKey(TdvGoal, models.DO_NOTHING, blank=True, null=True, to_field='code')
    tdv_alignment = models.TextField(blank=True, null=True)
    fydp = models.ForeignKey(FydpGoal, models.DO_NOTHING, blank=True, null=True, to_field='code')
    fydp_alignment = models.TextField(blank=True, null=True)
    sdg = models.ForeignKey(SdgGoal, models.DO_NOTHING, blank=True, null=True, to_field='code')
    sdg_alignment = models.TextField(blank=True, null=True)
    agenda = models.ForeignKey(AgendaGoal, models.DO_NOTHING, blank=True, null=True, to_field='code')
    agenda_alignment = models.TextField(blank=True, null=True)
    project_scope = models.TextField(blank=True, null=True)
    goal = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    action_plan = models.CharField(max_length=255, blank=True, null=True)
    compensation_pap = models.CharField(max_length=100, blank=True, null=True)
    occupancy_certificate = models.CharField(max_length=255, blank=True, null=True)
    institution_setup = models.CharField(max_length=255, blank=True, null=True)
    implementation_team = models.CharField(max_length=255, blank=True, null=True)
    compensation_pap_doc = models.CharField(max_length=255, blank=True, null=True)
    financial_discount_rate = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    economic_discount_rate = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=PROJECT_STATUS_CHOICES, default='DRAFT')
    step = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'project'
        ordering = ['project_id']

    def generate_project_id(self):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        projects = Project.objects.filter(sector=self.sector).count()
        project_id = '{}-{}{}{:02d}'.format(self.sector.id, year, month, int(projects) + 1)
        return project_id

    def save(self, *args, **kwargs, ):
        if self._state.adding:
            self.project_id = self.generate_project_id()
        return super().save(*args, **kwargs)


class ProjectFunding(models.Model):
    project = models.ForeignKey(Project, models.DO_NOTHING)
    fund_source = models.ForeignKey(FundSource, models.DO_NOTHING, to_field='code'),
    fund_category = models.ForeignKey(FundCategory, models.DO_NOTHING, to_field='code'),
    financing_modality = models.ForeignKey(FinancingModality, models.DO_NOTHING, to_field='code'),
    financier = models.ForeignKey(Financier, models.DO_NOTHING, to_field='code'),
    committed_amount = models.CharField(max_length=25),
    currency = models.ForeignKey(Currency, models.DO_NOTHING),
    exchange_rate = models.DecimalField(max_digits=4, decimal_places=2)


class ProjectActivity(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    activity_description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'project_activity'
        ordering = ['id']


class ProjectCashflow(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    cashflow_type = models.CharField(max_length=15)
    year_ref = models.IntegerField()
    inflow = models.DecimalField(max_digits=4, decimal_places=0)
    outflow = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        db_table = 'project_cashflow'
        ordering = ['id']


class ProjectIndicator(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    indicator_description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'project_indicator'


class ProjectInput(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'project_input'


class ProjectOutput(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, models.DO_NOTHING)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'project_output'


class ProjectTechnicalFeasibility(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Project', models.DO_NOTHING)
    doctype = models.CharField(max_length=255)
    feasibility_description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'project_technical_feasibility'
