from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Agenda, Institution, Fydp, Tdv, Sdg, Sector, Subsector, Costcentre, Vote, SdgGoal, SdgTarget, \
    AgendaTarget, AgendaGoal, FydpGoal, FydpTarget, TdvGoal, TdvTarget, AgendaAspiration, Programme, ProjectNature, \
    FundSource, FundCategory, FinancingModality, Financier, Currency


class SDGListSerializer(ModelSerializer):
    class Meta:
        model = Sdg
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class SDGCreateSerializer(ModelSerializer):
    class Meta:
        model = Sdg
        fields = ['name', 'description', 'start_date', 'end_date']


class SDGUpdateSerializer(ModelSerializer):
    class Meta:
        model = Sdg
        fields = ['pk', 'name', 'description', 'start_date', 'end_date']


class SDGGoalListSerializer(ModelSerializer):
    class Meta:
        model = SdgGoal
        fields = ['pk', 'sdg', 'goal_no', 'code', 'name', 'description']


class SDGGoalDetailSerializer(ModelSerializer):
    targets = serializers.SerializerMethodField()

    class Meta:
        model = SdgGoal
        fields = ['pk', 'sdg', 'goal_no', 'code', 'name', 'description', 'targets']

    def get_targets(self, obj):
        # Get the specific fields to include (e.g., from a query parameter)
        fields = self.context.get('request').query_params.get('target_fields', '').split(',')
        if not fields or fields == ['']:
            fields = ['target_no', 'code', 'description']  # Default fields

        # Serialize the related targets with only the specified fields
        targets = SdgTarget.objects.filter(sdg=obj.sdg, goal_no=obj.goal_no)
        return [
            {field: getattr(target, field) for field in fields}
            for target in targets
        ]


class SDGDetailSerializer(ModelSerializer):
    goals = SDGGoalDetailSerializer(source='sdggoal_set', many=True, read_only=True)

    class Meta:
        model = Sdg
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'goals']


class SDGGoalCreateSerializer(ModelSerializer):
    class Meta:
        model = SdgGoal
        fields = ['sdg', 'name', 'description']


class SDGGoalUpdateSerializer(ModelSerializer):
    class Meta:
        model = SdgGoal
        fields = ['name', 'description']


class SDGTargetListSerializer(ModelSerializer):
    class Meta:
        model = SdgTarget
        fields = ['pk', 'sdg', 'goal_no', 'target_no', 'code', 'description']


class SDGTargetSerializer(ModelSerializer):
    class Meta:
        model = SdgTarget
        fields = ['sdg', 'goal_no', 'description']


class AgendaListSerializer(ModelSerializer):
    class Meta:
        model = Agenda
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class AgendaCreateSerializer(ModelSerializer):
    class Meta:
        model = Agenda
        fields = ['name', 'description', 'start_date', 'end_date']


class AgendaUpdateSerializer(ModelSerializer):
    class Meta:
        model = Agenda
        fields = ['pk', 'name', 'description', 'start_date', 'end_date']


class AgendaAspirationListSerializer(ModelSerializer):
    class Meta:
        model = AgendaAspiration
        fields = ['pk', 'agenda', 'aspiration_no', 'code', 'name', 'description']


class AgendaAspirationDetailSerializer(ModelSerializer):
    targets = serializers.SerializerMethodField()

    class Meta:
        model = AgendaAspiration
        fields = ['pk', 'agenda', 'aspiration_no', 'code', 'name', 'description', 'targets']

    def get_targets(self, obj):
        # Get the specific fields to include (e.g., from a query parameter)
        fields = self.context.get('request').query_params.get('target_fields', '').split(',')
        if not fields or fields == ['']:
            fields = ['target_no', 'code', 'description']  # Default fields

        # Serialize the related targets with only the specified fields
        targets = AgendaTarget.objects.filter(agenda=obj.agenda, goal_no=obj.goal_no)
        return [
            {field: getattr(target, field) for field in fields}
            for target in targets
        ]


class AgendaDetailSerializer(ModelSerializer):
    goals = AgendaAspirationDetailSerializer(source='agendagoal_set', many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'goals']


class AgendaAspirationCreateSerializer(ModelSerializer):
    class Meta:
        model = AgendaAspiration
        fields = ['agenda', 'name', 'description']


class AgendaAspirationUpdateSerializer(ModelSerializer):
    class Meta:
        model = AgendaAspiration
        fields = ['name', 'description']


class AgendaGoalListSerializer(ModelSerializer):
    class Meta:
        model = AgendaGoal
        fields = ['pk', 'agenda', 'goal_no', 'code', 'name', 'description']


class AgendaGoalDetailSerializer(ModelSerializer):
    targets = serializers.SerializerMethodField()

    class Meta:
        model = AgendaGoal
        fields = ['pk', 'agenda', 'goal_no', 'code', 'name', 'description', 'targets']

    def get_targets(self, obj):
        # Get the specific fields to include (e.g., from a query parameter)
        fields = self.context.get('request').query_params.get('target_fields', '').split(',')
        if not fields or fields == ['']:
            fields = ['target_no', 'code', 'description']  # Default fields

        # Serialize the related targets with only the specified fields
        targets = AgendaTarget.objects.filter(agenda=obj.agenda, goal_no=obj.goal_no)
        return [
            {field: getattr(target, field) for field in fields}
            for target in targets
        ]


class AgendaDetailSerializer(ModelSerializer):
    goals = AgendaGoalDetailSerializer(source='agendagoal_set', many=True, read_only=True)

    class Meta:
        model = Agenda
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'goals']


class AgendaGoalCreateSerializer(ModelSerializer):
    class Meta:
        model = AgendaGoal
        fields = ['agenda', 'name', 'description']


class AgendaGoalUpdateSerializer(ModelSerializer):
    class Meta:
        model = AgendaGoal
        fields = ['name', 'description']


class AgendaTargetListSerializer(ModelSerializer):
    class Meta:
        model = AgendaTarget
        fields = ['pk', 'agenda', 'goal_no', 'target_no', 'code', 'description']


class AgendaTargetSerializer(ModelSerializer):
    class Meta:
        model = AgendaTarget
        fields = ['agenda', 'goal_no', 'description']


class FYDPListSerializer(ModelSerializer):
    class Meta:
        model = Fydp
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class FYDPCreateSerializer(ModelSerializer):
    class Meta:
        model = Fydp
        fields = ['name', 'description', 'start_date', 'end_date']


class FYDPUpdateSerializer(ModelSerializer):
    class Meta:
        model = Fydp
        fields = ['pk', 'name', 'description', 'start_date', 'end_date']


class FYDPGoalListSerializer(ModelSerializer):
    class Meta:
        model = FydpGoal
        fields = ['pk', 'fydp', 'goal_no', 'code', 'name', 'description']


class FYDPGoalDetailSerializer(ModelSerializer):
    targets = serializers.SerializerMethodField()

    class Meta:
        model = FydpGoal
        fields = ['pk', 'fydp', 'goal_no', 'code', 'name', 'description', 'targets']

    def get_targets(self, obj):
        # Get the specific fields to include (e.g., from a query parameter)
        fields = self.context.get('request').query_params.get('target_fields', '').split(',')
        if not fields or fields == ['']:
            fields = ['target_no', 'code', 'description']  # Default fields

        # Serialize the related targets with only the specified fields
        targets = FydpTarget.objects.filter(fydp=obj.fydp, goal_no=obj.goal_no)
        return [
            {field: getattr(target, field) for field in fields}
            for target in targets
        ]


class FYDPDetailSerializer(ModelSerializer):
    goals = FYDPGoalDetailSerializer(source='fydpgoal_set', many=True, read_only=True)

    class Meta:
        model = Fydp
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'goals']


class FYDPGoalCreateSerializer(ModelSerializer):
    class Meta:
        model = FydpGoal
        fields = ['fydp', 'name', 'description']


class FYDPGoalUpdateSerializer(ModelSerializer):
    class Meta:
        model = FydpGoal
        fields = ['name', 'description']


class FYDPTargetListSerializer(ModelSerializer):
    class Meta:
        model = FydpTarget
        fields = ['pk', 'fydp', 'goal_no', 'target_no', 'code', 'description']


class FYDPTargetSerializer(ModelSerializer):
    class Meta:
        model = FydpTarget
        fields = ['fydp', 'goal_no', 'description']


class TDVListSerializer(ModelSerializer):
    class Meta:
        model = Tdv
        fields = ['id', 'name', 'description', 'start_date', 'end_date']


class TDVCreateSerializer(ModelSerializer):
    class Meta:
        model = Tdv
        fields = ['name', 'description', 'start_date', 'end_date']


class TDVUpdateSerializer(ModelSerializer):
    class Meta:
        model = Tdv
        fields = ['pk', 'name', 'description', 'start_date', 'end_date']


class TDVGoalListSerializer(ModelSerializer):
    class Meta:
        model = TdvGoal
        fields = ['pk', 'tdv', 'goal_no', 'code', 'name', 'description']


class TDVGoalDetailSerializer(ModelSerializer):
    targets = serializers.SerializerMethodField()

    class Meta:
        model = TdvGoal
        fields = ['pk', 'tdv', 'goal_no', 'code', 'name', 'description', 'targets']

    def get_targets(self, obj):
        # Get the specific fields to include (e.g., from a query parameter)
        fields = self.context.get('request').query_params.get('target_fields', '').split(',')
        if not fields or fields == ['']:
            fields = ['target_no', 'code', 'description']  # Default fields

        # Serialize the related targets with only the specified fields
        targets = TdvTarget.objects.filter(tdv=obj.tdv, goal_no=obj.goal_no)
        return [
            {field: getattr(target, field) for field in fields}
            for target in targets
        ]


class TDVDetailSerializer(ModelSerializer):
    goals = TDVGoalDetailSerializer(source='tdvgoal_set', many=True, read_only=True)

    class Meta:
        model = Tdv
        fields = ['id', 'name', 'description', 'start_date', 'end_date', 'goals']


class TDVGoalCreateSerializer(ModelSerializer):
    class Meta:
        model = TdvGoal
        fields = ['tdv', 'name', 'description']


class TDVGoalUpdateSerializer(ModelSerializer):
    class Meta:
        model = TdvGoal
        fields = ['name', 'description']


class TDVTargetListSerializer(ModelSerializer):
    class Meta:
        model = TdvTarget
        fields = ['pk', 'tdv', 'goal_no', 'target_no', 'code', 'description']


class TDVTargetSerializer(ModelSerializer):
    class Meta:
        model = TdvTarget
        fields = ['tdv', 'goal_no', 'description']


class SectorSerializer(ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


class SubsectorListSerializer(ModelSerializer):
    class Meta:
        model = Subsector
        fields = ['id', 'name']


class SectorListSerializer(ModelSerializer):
    subsectors = SubsectorListSerializer(source='subsector_set', many=True, read_only=True)

    class Meta:
        model = Sector
        fields = ['id', 'name', 'subsectors']


class SectorDetailSerializer(ModelSerializer):
    subsectors = SubsectorListSerializer(source='subsector_set', many=True, read_only=True)

    class Meta:
        model = Sector
        fields = ['id', 'name', 'subsectors']


class SubsectorCreateSerializer(ModelSerializer):
    class Meta:
        model = Subsector
        fields = ['sector', 'name']


class SubsectorSerializer(ModelSerializer):
    sector = SectorSerializer()

    class Meta:
        model = Subsector
        fields = ['id', 'name', 'sector']


class CostcentreListSerializer(ModelSerializer):
    class Meta:
        model = Costcentre
        fields = '__all__'


class CostcentreCreateSerializer(ModelSerializer):
    class Meta:
        model = Costcentre
        fields = ['costcentre_no', 'vote_no', 'name']


class CostcentreUpdateSerializer(ModelSerializer):
    class Meta:
        model = Costcentre
        fields = '__all__'


class VoteSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'


class CostcentreDetailSerializer(ModelSerializer):
    vote = VoteSerializer()

    class Meta:
        model = Costcentre
        fields = '__all__'


class InstitutionSerializer(ModelSerializer):
    subsector = SubsectorSerializer()

    class Meta:
        model = Institution
        fields = ['id', 'name', 'subsector']


class ProgrammeListSerializer(ModelSerializer):
    sector = SectorSerializer()

    class Meta:
        model = Programme
        fields = ['id', 'name', 'sector']


class ProgrammeCreateSerializer(ModelSerializer):
    class Meta:
        model = Programme
        fields = ['id', 'name', 'sector']


class ProgrammeUpdateSerializer(ModelSerializer):
    class Meta:
        model = Programme
        fields = ['name']


class ProgrammeDetailSerializer(ModelSerializer):
    class Meta:
        model = Programme
        fields = ['id', 'name', 'sector']


class ProjectNatureSerializer(ModelSerializer):
    class Meta:
        model = ProjectNature
        fields = ['id', 'name']


class FundSourceSerializer(ModelSerializer):
    class Meta:
        model = FundSource
        fields = ['code', 'name']


class FundCategorySerializer(ModelSerializer):
    class Meta:
        model = FundCategory
        fields = ['fund_source', 'code', 'name']


class FinancingModalitySerializer(ModelSerializer):
    class Meta:
        model = FinancingModality
        fields = ['fund_category', 'code', 'name']


class FinancierSerializer(ModelSerializer):
    class Meta:
        model = Financier
        fields = ['code', 'name']


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'name']
