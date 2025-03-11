from django.core.exceptions import ValidationError
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from npmis.apps.common.signals import signal_npmis_pre_save
from npmis.apps.events.decorators import method_event
from npmis.apps.events.managers import EventManagerSave
from npmis.apps.settings.events import event_sdg_created, event_sdg_edited
from npmis.apps.settings.literals import INSTITUTION_CATEGORY


class Sdg(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sdg'
        verbose_name = 'SDG'
        verbose_name_plural = 'SDGs'
        ordering = ['-start_date']

    def __str__(self):
        return f'{self.id}: {self.name}'

    def generate_id(self):
        sdg_id = f'SDG{self.end_date.year}'
        return sdg_id

    def clean(self):
        # Ensure that the start date is before the end date
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Start date must be before end date.")

        # Ensure that there is only one active SDG
        if self.is_active:
            active_sdgs = Sdg.objects.filter(is_active=True)
            if self.pk:  # Exclude the current instance if it's being updated
                active_sdgs = active_sdgs.exclude(pk=self.pk)
            if active_sdgs.exists():
                raise ValidationError("There can only be one active SDG at a time.")

    def save(self, *args, **kwargs):
        # Ensure only one active SDG at a time
        if self.is_active:
            # Deactivate all other active SDGs
            Sdg.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)

        # Generate ID for new instances
        if self._state.adding:
            self.id = self.generate_id()

        super().save(*args, **kwargs)


class SdgGoal(models.Model):
    pk = models.CompositePrimaryKey('sdg', 'goal_no')
    sdg = models.ForeignKey(Sdg, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'sdg_goal'
        verbose_name = 'SDG Goals'
        verbose_name_plural = 'SDG Goals'
        ordering = ['sdg', 'goal_no']

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        goal_no = SdgGoal.objects.filter(sdg=self.sdg).count() + 1
        goal_code = f'{self.sdg.id}-{goal_no:02d}'
        return goal_no, goal_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.goal_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class SdgTarget(models.Model):
    pk = models.CompositePrimaryKey('sdg', 'goal_no', 'target_no')
    sdg = models.ForeignKey(Sdg, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    target_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=20)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'sdg_target'
        verbose_name = 'SDG Target'
        verbose_name_plural = 'SDG Targets'
        ordering = ['sdg', 'goal_no', 'target_no']

    def __str__(self):
        return f'{self.code}: {self.description}'


    def generate_code(self):
        target_no = SdgTarget.objects.filter(sdg=self.sdg, goal_no=self.goal_no).count() + 1
        goal_code = f'{self.sdg.id}-{self.goal_no:02d}-{target_no:02d}'
        return target_no, goal_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.target_no, self.code = self.generate_code()
        super().save(*args, **kwargs)


class Agenda(models.Model):
    id = models.CharField(primary_key=True, max_length=10),
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'agenda'
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agenda'

    def __str__(self):
        return f'{self.id}: {self.name}'

    def generate_id(self):
        agenda_id = f'AG{self.end_date.year}'
        return agenda_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.id = self.generate_id()
        super().save(*args, **kwargs)


class AgendaAspiration(models.Model):
    """
    Represents an Agenda Aspiration.
    """
    pk = models.CompositePrimaryKey('agenda', 'aspiration_no')
    agenda = models.ForeignKey(Agenda, models.CASCADE)
    aspiration_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        aspiration_no = AgendaAspiration.objects.filter(agenda=self.agenda).count() + 1
        aspiration_code = f'{self.agenda.id}-{aspiration_no:02d}'
        return aspiration_no, aspiration_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.aspiration_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class AgendaGoal(models.Model):
    pk = models.CompositePrimaryKey('agenda', 'aspiration_no', 'goal_no')
    agenda = models.ForeignKey(Agenda, models.CASCADE)
    aspiration_no = models.PositiveIntegerField()
    goal_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'agenda_goal'
        verbose_name = 'Agenda Goal'
        verbose_name_plural = 'Agenda Goals'

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        goal_no = AgendaGoal.objects.filter(agenda=self.agenda, aspiration_no=self.aspiration_no).count() + 1
        goal_code = f'{self.agenda.id}-{self.aspiration_no:02d}{goal_no:02d}'
        return goal_no, goal_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.goal_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class AgendaTarget(models.Model):
    pk = models.CompositePrimaryKey('agenda', 'aspiration_no', 'goal_no', 'target_no')
    agenda = models.ForeignKey(Agenda, models.CASCADE)
    aspiration_no = models.PositiveIntegerField()
    goal_no = models.PositiveIntegerField()
    target_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'agenda_target'
        verbose_name = 'Agenda Target'
        verbose_name_plural = 'Agenda Targets'

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        target_no = AgendaGoal.objects.filter(agenda=self.agenda, aspiration_no=self.aspiration_no,
                                              goal_no=self.goal_no).count() + 1
        target_code = f'{self.agenda.id}-{self.aspiration_no:02d}{self.goal_no:02d}{target_no:02d}'
        return target_no, target_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.target_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class Fydp(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'fydp'
        verbose_name = 'FYDP'
        verbose_name_plural = 'FYDPs'

    def __str__(self):
        return f'{self.id}: {self.name}'

    def generate_id(self):
        tdv_id = f'FYDP{self.end_date.year}'
        return tdv_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.id = self.generate_id()
        super().save(*args, **kwargs)


class FydpGoal(models.Model):
    pk = models.CompositePrimaryKey('fydp', 'goal_no')
    fydp = models.ForeignKey(Fydp, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'fydp_goal'
        verbose_name = 'FYDP Goal'
        verbose_name_plural = 'FYDP Goals'

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        goal_no = FydpGoal.objects.filter(fyd=self.fydp).count() + 1
        goal_code = f'{self.fydp.id}-{goal_no:02d}'
        return goal_no, goal_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.goal_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class FydpTarget(models.Model):
    pk = models.CompositePrimaryKey('fydp', 'goal_no', 'target_no')
    fydp = models.ForeignKey(Fydp, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    target_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'fydp_target'
        verbose_name = 'FYDP Target'
        verbose_name_plural = 'FYDP Targets'

    def __str__(self):
        return f'{self.code}: {self.description}'

    def generate_id(self):
        target_no = TdvTarget.objects.filter(fydp=self.fydp, goal_no=self.goal_no).count() + 1
        target_code = f'{self.fydp.id}-{self.goal_no:02d}{target_no:02d}'
        return target_no, target_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.target_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class Tdv(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        db_table = 'tdv'
        verbose_name = 'Tanzania Development Vision'
        verbose_name_plural = 'Tanzania Development Visions'

    def __str__(self):
        return f'{self.id}: {self.name}'

    def generate_id(self):
        tdv_id = f'TDV{self.end_date.year}'
        return tdv_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.id = self.generate_id()
        super().save(*args, **kwargs)


class TdvGoal(models.Model):
    pk = models.CompositePrimaryKey('tdv', 'goal_no')
    tdv = models.ForeignKey(Tdv, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=1000)

    class Meta:
        db_table = 'tdv_goal'
        verbose_name = 'Tanzania Development Vision Goal'
        verbose_name_plural = 'Tanzania Development Vision Goals'

    def __str__(self):
        return f'{self.code}: {self.name}'

    def generate_id(self):
        goal_no = TdvGoal.objects.filter(tdv=self.tdv).count() + 1
        goal_code = f'{self.tdv.id}-{goal_no:02d}'
        return goal_no, goal_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.goal_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class TdvTarget(models.Model):
    pk = models.CompositePrimaryKey('tdv', 'goal_no', 'target_no')
    tdv = models.ForeignKey(Tdv, models.DO_NOTHING)
    goal_no = models.PositiveIntegerField()
    target_no = models.PositiveIntegerField()
    code = models.CharField(unique=True, max_length=10)
    description = models.CharField(max_length=500)

    class Meta:
        db_table = 'tdv_target'
        verbose_name = 'Tanzania Development Vision Target'
        verbose_name_plural = 'Tanzania Development Vision Targets'

    def __str__(self):
        return f'{self.code}: {self.description}'

    def generate_id(self):
        target_no = TdvTarget.objects.filter(tdv=self.tdv, goal_no=self.goal_no).count() + 1
        target_code = f'{self.tdv.id}-{self.goal_no:02d}{target_no:02d}'
        return target_no, target_code

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.target_no, self.code = self.generate_id()
        super().save(*args, **kwargs)


class Sector(models.Model):
    id = models.CharField(db_column='sector_id', primary_key=True, max_length=20)
    name = models.CharField(db_column='sector_description', max_length=255)

    class Meta:
        db_table = 'sector'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}: {self.name}'


class Subsector(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    sector = models.ForeignKey(Sector, models.DO_NOTHING, db_column='sector_id')
    name = models.CharField(db_column='subsector_description', max_length=1000, unique=True)

    class Meta:
        db_table = 'subsector'
        unique_together = (('id', 'sector'),)
        ordering = ['id']

    def __str__(self):
        return f'{self.sector.id}: {self.name}'

    def generate_id(self):
        subsectors = Subsector.objects.filter(sector=self.sector).count() + 1
        subsector_id = f'{self.sector.id}-{subsectors:02d}'
        return subsector_id

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.id = self.generate_id()
        super().save(*args, **kwargs)


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    vote_no = models.CharField(db_column='vote_no', max_length=4, unique=True)
    name = models.CharField(db_column='vote_name', max_length=255)
    category = models.CharField(max_length=100, choices=[
        ('Executive', 'Executive'),
        ('Legislature', 'Legislature'),
        ('Judiciary', 'Judiciary'),
        ('MDA', 'MDA'),
        ('LGA', 'LGA'),
        ('Other', 'Other')
    ], default='Other')

    class Meta:
        db_table = 'vote'
        ordering = ['vote_no']

    def __str__(self):
        return f'{self.vote_no}: {self.name}'


class Costcentre(models.Model):
    pk = models.CompositePrimaryKey('costcentre_no', 'vote_no')
    costcentre_no = models.CharField(max_length=15)
    vote_no = models.CharField(db_column='vote_no', max_length=4)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'costcentre'
        ordering = ['vote_no','costcentre_no']


class Institution(models.Model):
    id = models.CharField(db_column='institution_id', primary_key=True, max_length=10)
    name = models.CharField(db_column='institution_name', max_length=255)
    description = models.TextField(blank=True, null=True)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE, to_field='vote_no', max_length=22, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'institution'


class ProjectNature(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'project_nature'


class Programme(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, blank=True, null=True)
    sector = models.ForeignKey(Sector, models.DO_NOTHING)

    class Meta:
        db_table = 'programme'


class Currency(models.Model):
    id = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        db_table = 'currency'
        ordering = ['id']


class FundSource(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'fund_source'
        ordering = ['id']


class FundCategory(models.Model):
    fund_source = models.ForeignKey(FundSource, models.DO_NOTHING, to_field='code')
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'fund_category'
        ordering = ['fund_source', 'code']


class FinancingModality(models.Model):
    fund_category = models.ForeignKey(FundCategory, models.DO_NOTHING, to_field='code')
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'financing_modality'
        ordering = ['code']


class Financier(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'financier'
        ordering = ['code']
