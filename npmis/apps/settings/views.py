from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView

from .models import Institution, Agenda, Tdv, Sdg, Costcentre, Vote, Sector, Subsector, SdgGoal, SdgTarget, \
    AgendaGoal, AgendaTarget, Fydp, FydpTarget, FydpGoal, TdvTarget, TdvGoal, AgendaAspiration, Programme, \
    ProjectNature, FundSource, FundCategory, FinancingModality, Financier, Currency
from .serializers import InstitutionSerializer, VoteSerializer, SectorSerializer, \
    SectorDetailSerializer, SubsectorSerializer, \
    SDGTargetSerializer, SDGListSerializer, SDGGoalListSerializer, SDGTargetListSerializer, \
    SDGGoalDetailSerializer, SDGGoalUpdateSerializer, SDGGoalCreateSerializer, SDGCreateSerializer, SDGUpdateSerializer, \
    SDGDetailSerializer, AgendaTargetSerializer, AgendaTargetListSerializer, AgendaGoalDetailSerializer, \
    AgendaGoalUpdateSerializer, AgendaGoalCreateSerializer, AgendaGoalListSerializer, AgendaDetailSerializer, \
    AgendaUpdateSerializer, AgendaListSerializer, AgendaCreateSerializer, FYDPTargetSerializer, \
    FYDPTargetListSerializer, FYDPGoalDetailSerializer, FYDPGoalUpdateSerializer, FYDPGoalCreateSerializer, \
    FYDPGoalListSerializer, FYDPDetailSerializer, FYDPUpdateSerializer, FYDPCreateSerializer, FYDPListSerializer, \
    TDVListSerializer, TDVCreateSerializer, TDVUpdateSerializer, TDVDetailSerializer, TDVGoalListSerializer, \
    TDVGoalCreateSerializer, TDVGoalUpdateSerializer, TDVGoalDetailSerializer, TDVTargetListSerializer, \
    TDVTargetSerializer, AgendaAspirationListSerializer, AgendaAspirationCreateSerializer, \
    AgendaAspirationUpdateSerializer, AgendaAspirationDetailSerializer, ProjectNatureSerializer, \
    SubsectorCreateSerializer, SectorListSerializer, ProgrammeListSerializer, ProgrammeUpdateSerializer, \
    ProgrammeDetailSerializer, ProgrammeCreateSerializer, CostcentreCreateSerializer, CostcentreListSerializer, \
    CostcentreUpdateSerializer, CostcentreDetailSerializer, FundSourceSerializer, FundCategorySerializer, \
    FinancingModalitySerializer, FinancierSerializer, CurrencySerializer
from ..common.classes import Response


class SDGListAPIView(ListAPIView):
    queryset = Sdg.objects.all()
    serializer_class = SDGListSerializer


class SDGCreateAPIView(CreateAPIView):
    queryset = Sdg.objects.all()
    serializer_class = SDGCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message='SDG created successfully')
        except Exception as e:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'{e}')


class SDGUpdateAPIView(UpdateAPIView):
    queryset = Sdg.objects.all()
    serializer_class = SDGUpdateSerializer


class SDGDetailAPIView(RetrieveAPIView):
    queryset = Sdg.objects.all()
    serializer_class = SDGDetailSerializer


class SDGGoalListAPIView(ListAPIView):
    serializer_class = SDGGoalListSerializer


class SDGGoalCreateAPIView(CreateAPIView):
    queryset = SdgGoal.objects.all()
    serializer_class = SDGGoalCreateSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='Goal(s) added successfully')


class SDGGoalUpdateAPIView(UpdateAPIView):
    queryset = SdgGoal.objects.all()
    serializer_class = SDGGoalUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no]

        # Lookup the object
        try:
            return SdgGoal.objects.get(pk=composite_pk)
        except SdgGoal.DoesNotExist:
            raise NotFound("SDG not found")
        except Exception as e:
            print(e)


class SDGGoalDetailAPIView(RetrieveAPIView):
    queryset = SdgGoal.objects.all()
    serializer_class = SDGGoalDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no]

        # Lookup the object
        try:
            return SdgGoal.objects.get(pk=composite_pk)
        except SdgGoal.DoesNotExist:
            raise NotFound("SDG not found")
        except Exception as e:
            print(e)


class SDGTargetListAPIView(ListAPIView):
    queryset = SdgTarget.objects.all()
    serializer_class = SDGTargetListSerializer


class SDGTargetCreateAPIView(CreateAPIView):
    queryset = SdgTarget.objects.all()
    serializer_class = SDGTargetSerializer

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='SDG targets added successfully')

    def perform_create(self, serializer):
        serializer.save()


class SDGTargetUpdateAPIView(UpdateAPIView):
    queryset = SdgTarget.objects.all()
    serializer_class = SDGTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no, target_no]

        # Lookup the object
        try:
            return SdgTarget.objects.get(pk=composite_pk)
        except SdgTarget.DoesNotExist:
            raise NotFound("SDG target not found")
        except Exception as e:
            print(e)


class SDGTargetDetailAPIView(RetrieveAPIView):
    queryset = SdgTarget.objects.all()
    serializer_class = SDGTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no, target_no]

        # Lookup the object
        try:
            return SdgTarget.objects.get(pk=composite_pk)
        except SdgTarget.DoesNotExist:
            raise NotFound("SDG not found")
        except Exception as e:
            print(e)


class AgendaListAPIView(ListAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaListSerializer


class AgendaCreateAPIView(CreateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaCreateSerializer


class AgendaUpdateAPIView(UpdateAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaUpdateSerializer


class AgendaDetailAPIView(RetrieveAPIView):
    queryset = Agenda.objects.all()
    serializer_class = AgendaDetailSerializer


class AgendaAspirationListAPIView(ListAPIView):
    queryset = AgendaAspiration.objects.all()
    serializer_class = AgendaAspirationListSerializer


class AgendaAspirationCreateAPIView(CreateAPIView):
    queryset = AgendaAspiration.objects.all()
    serializer_class = AgendaAspirationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='Aspirations added successfully')

    def perform_create(self, serializer):
        serializer.save()


class AgendaAspirationUpdateAPIView(UpdateAPIView):
    queryset = AgendaAspiration.objects.all()
    serializer_class = AgendaAspirationUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no]

        # Lookup the object
        try:
            return AgendaAspiration.objects.get(pk=composite_pk)
        except AgendaAspiration.DoesNotExist:
            raise NotFound("Agenda aspiration not found")
        except Exception as e:
            print(e)


class AgendaAspirationDetailAPIView(RetrieveAPIView):
    queryset = AgendaAspiration.objects.all()
    serializer_class = AgendaAspirationDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no]

        # Lookup the object
        try:
            return AgendaAspiration.objects.get(pk=composite_pk)
        except AgendaAspiration.DoesNotExist:
            raise NotFound("Agenda aspiration not found")
        except Exception as e:
            print(e)


class AgendaGoalListAPIView(ListAPIView):
    queryset = AgendaGoal.objects.all()
    serializer_class = AgendaGoalListSerializer


class AgendaGoalCreateAPIView(CreateAPIView):
    queryset = AgendaGoal.objects.all()
    serializer_class = AgendaGoalCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='Agenda Goals added successfully')

    def perform_create(self, serializer):
        serializer.save()


class AgendaGoalUpdateAPIView(UpdateAPIView):
    queryset = AgendaGoal.objects.all()
    serializer_class = AgendaGoalUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no, goal_no]

        # Lookup the object
        try:
            return AgendaGoal.objects.get(pk=composite_pk)
        except AgendaGoal.DoesNotExist:
            raise NotFound("Agenda not found")
        except Exception as e:
            print(e)


class AgendaGoalDetailAPIView(RetrieveAPIView):
    queryset = AgendaGoal.objects.all()
    serializer_class = AgendaGoalDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no, goal_no]

        # Lookup the object
        try:
            return AgendaGoal.objects.get(pk=composite_pk)
        except AgendaGoal.DoesNotExist:
            raise NotFound("Agenda goal not found")
        except Exception as e:
            print(e)


class AgendaTargetListAPIView(ListAPIView):
    queryset = AgendaTarget.objects.all()
    serializer_class = AgendaTargetListSerializer


class AgendaTargetCreateAPIView(CreateAPIView):
    queryset = AgendaTarget.objects.all()
    serializer_class = AgendaTargetSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message='Agenda targets added successfully')
        except Exception as e:
            print(f"{e}")

    def perform_create(self, serializer):
        serializer.save()


class AgendaTargetUpdateAPIView(UpdateAPIView):
    queryset = AgendaTarget.objects.all()
    serializer_class = AgendaTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no, goal_no, target_no]

        # Lookup the object
        try:
            return AgendaTarget.objects.get(pk=composite_pk)
        except AgendaTarget.DoesNotExist:
            raise NotFound("Agenda target not found")
        except Exception as e:
            print(e)


class AgendaTargetDetailAPIView(RetrieveAPIView):
    queryset = AgendaTarget.objects.all()
    serializer_class = AgendaTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('agenda')
        aspiration_no = self.kwargs.get('aspiration_no')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, aspiration_no, goal_no, target_no]

        # Lookup the object
        try:
            return AgendaTarget.objects.get(pk=composite_pk)
        except AgendaTarget.DoesNotExist:
            raise NotFound("Agenda target not found")
        except Exception as e:
            print(e)


class FYDPListAPIView(ListAPIView):
    queryset = Fydp.objects.all()
    serializer_class = FYDPListSerializer


class FYDPCreateAPIView(CreateAPIView):
    queryset = Fydp.objects.all()
    serializer_class = FYDPCreateSerializer


class FYDPUpdateAPIView(UpdateAPIView):
    queryset = Fydp.objects.all()
    serializer_class = FYDPUpdateSerializer


class FYDPDetailAPIView(RetrieveAPIView):
    queryset = Fydp.objects.all()
    serializer_class = FYDPDetailSerializer


class FYDPGoalListAPIView(ListAPIView):
    queryset = FydpGoal.objects.all()
    serializer_class = FYDPGoalListSerializer


class FYDPGoalCreateAPIView(CreateAPIView):
    queryset = FydpGoal.objects.all()
    serializer_class = FYDPGoalCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='Goals added successfully')

    def perform_create(self, serializer):
        serializer.save()


class FYDPGoalUpdateAPIView(UpdateAPIView):
    queryset = FydpGoal.objects.all()
    serializer_class = FYDPGoalUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no]

        # Lookup the object
        try:
            return FydpGoal.objects.get(pk=composite_pk)
        except FydpGoal.DoesNotExist:
            raise NotFound("FYDP goal not found")
        except Exception as e:
            print(e)


class FYDPGoalDetailAPIView(RetrieveAPIView):
    queryset = FydpGoal.objects.all()
    serializer_class = FYDPGoalDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('sdg')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no]

        # Lookup the object
        try:
            return FydpGoal.objects.get(pk=composite_pk)
        except FydpGoal.DoesNotExist:
            raise NotFound("FYDP goal not found")
        except Exception as e:
            print(e)


class FYDPTargetListAPIView(ListAPIView):
    queryset = FydpTarget.objects.all()
    serializer_class = FYDPTargetListSerializer


class FYDPTargetCreateAPIView(CreateAPIView):
    queryset = FydpTarget.objects.all()
    serializer_class = FYDPTargetSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message='FYDP targets added successfully')
        except Exception as e:
            print(f"{e}")

    def perform_create(self, serializer):
        serializer.save()


class FYDPTargetUpdateAPIView(UpdateAPIView):
    queryset = FydpTarget.objects.all()
    serializer_class = FYDPTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        sdg = self.kwargs.get('fydp')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [sdg, goal_no, target_no]

        # Lookup the object
        try:
            return FydpTarget.objects.get(pk=composite_pk)
        except FydpTarget.DoesNotExist:
            raise NotFound("FYDP target not found")
        except Exception as e:
            print(e)


class FYDPTargetDetailAPIView(RetrieveAPIView):
    queryset = FydpTarget.objects.all()
    serializer_class = FYDPTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        agenda = self.kwargs.get('fydp')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [agenda, goal_no, target_no]

        # Lookup the object
        try:
            return FydpTarget.objects.get(pk=composite_pk)
        except FydpTarget.DoesNotExist:
            raise NotFound("FYDP target not found")
        except Exception as e:
            print(e)


class TDVListAPIView(ListAPIView):
    queryset = Tdv.objects.all()
    serializer_class = TDVListSerializer


class TDVCreateAPIView(CreateAPIView):
    queryset = Tdv.objects.all()
    serializer_class = TDVCreateSerializer


class TDVUpdateAPIView(UpdateAPIView):
    queryset = Tdv.objects.all()
    serializer_class = TDVUpdateSerializer


class TDVDetailAPIView(RetrieveAPIView):
    queryset = Tdv.objects.all()
    serializer_class = TDVDetailSerializer


class TDVGoalListAPIView(ListAPIView):
    queryset = TdvGoal.objects.all()
    serializer_class = TDVGoalListSerializer


class TDVGoalCreateAPIView(CreateAPIView):
    queryset = TdvGoal.objects.all()
    serializer_class = TDVGoalCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status_code=status.HTTP_201_CREATED, message='Goals added successfully')

    def perform_create(self, serializer):
        serializer.save()


class TDVGoalUpdateAPIView(UpdateAPIView):
    queryset = TdvGoal.objects.all()
    serializer_class = TDVGoalUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        tdv = self.kwargs.get('tdv')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [tdv, goal_no]

        # Lookup the object
        try:
            return TdvGoal.objects.get(pk=composite_pk)
        except TdvGoal.DoesNotExist:
            raise NotFound("TDV not found")
        except Exception as e:
            print(e)


class TDVGoalDetailAPIView(RetrieveAPIView):
    queryset = TdvGoal.objects.all()
    serializer_class = TDVGoalDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        tdv = self.kwargs.get('tdv')
        goal_no = self.kwargs.get('goal_no')

        # Combine the composite key into a single string
        composite_pk = [tdv, goal_no]

        # Lookup the object
        try:
            return TdvGoal.objects.get(pk=composite_pk)
        except TdvGoal.DoesNotExist:
            raise NotFound("TDV not found")
        except Exception as e:
            print(e)


class TDVTargetListAPIView(ListAPIView):
    queryset = TdvTarget.objects.all()
    serializer_class = TDVTargetListSerializer


class TDVTargetCreateAPIView(CreateAPIView):
    queryset = TdvTarget.objects.all()
    serializer_class = TDVTargetSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message='TDV targets added successfully')
        except Exception as e:
            print(f"{e}")

    def perform_create(self, serializer):
        serializer.save()


class TDVTargetUpdateAPIView(UpdateAPIView):
    queryset = TdvTarget.objects.all()
    serializer_class = TDVTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        tdv = self.kwargs.get('tdv')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [tdv, goal_no, target_no]

        # Lookup the object
        try:
            return TdvTarget.objects.get(pk=composite_pk)
        except TdvTarget.DoesNotExist:
            raise NotFound("TDV target not found")
        except Exception as e:
            print(e)


class TDVTargetDetailAPIView(RetrieveAPIView):
    queryset = TdvTarget.objects.all()
    serializer_class = TDVTargetSerializer

    def get_object(self):
        # Extract the composite key from the URL
        tdv = self.kwargs.get('tdv')
        goal_no = self.kwargs.get('goal_no')
        target_no = self.kwargs.get('target_no')

        # Combine the composite key into a single string
        composite_pk = [tdv, goal_no, target_no]

        # Lookup the object
        try:
            return TdvTarget.objects.get(pk=composite_pk)
        except TdvTarget.DoesNotExist:
            raise NotFound("TDV not found")
        except Exception as e:
            print(e)


class CostcentreListAPIView(ListAPIView):
    serializer_class = CostcentreListSerializer

    def get_queryset(self):
        # Get the queryset of all Costcentre objects
        queryset = Costcentre.objects.all()

        # Check if the user is authenticated and has a vote associated
        if self.request.user.is_authenticated and hasattr(self.request.user, 'vote'):
            # Filter the queryset based on the vote_no of the user's vote
            queryset = queryset.filter(vote_no=self.request.user.vote.vote_no)

        return queryset


class CostcentreCreateAPIView(CreateAPIView):
    queryset = Costcentre.objects.all()
    serializer_class = CostcentreCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Check if the request data is a list (multiple objects) or a dict (single object)
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Costcentre(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class CostcentreUpdateAPIView(UpdateAPIView):
    queryset = Costcentre.objects.all()
    serializer_class = CostcentreUpdateSerializer

    def get_object(self):
        # Extract the composite key from the URL
        vote_no = self.kwargs.get('vote_no')
        costcentre_no = self.kwargs.get('costcentre_no')

        # Combine the composite key into a single string
        composite_pk = [costcentre_no, vote_no]

        # Lookup the object
        try:
            return TdvTarget.objects.get(pk=composite_pk)
        except TdvTarget.DoesNotExist:
            raise NotFound("Costcentre not found")
        except Exception as e:
            print(e)


class CostcentreDetailAPIView(RetrieveAPIView):
    queryset = Costcentre.objects.all()
    serializer_class = CostcentreDetailSerializer

    def get_object(self):
        # Extract the composite key from the URL
        vote_no = self.kwargs.get('vote_no')
        costcentre_no = self.kwargs.get('costcentre_no')

        # Combine the composite key into a single string
        composite_pk = [costcentre_no, vote_no]

        # Lookup the object
        try:
            return TdvTarget.objects.get(pk=composite_pk)
        except TdvTarget.DoesNotExist:
            raise NotFound("Costcentre not found")
        except Exception as e:
            print(e)


class VoteListAPIView(ListAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteCreateAPIView(CreateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Check if the request data is a list (multiple objects) or a dict (single object)
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Vote(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class VoteUpdateAPIView(UpdateAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteDetailAPIView(RetrieveAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class SectorListAPIView(ListAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorListSerializer


class SectorCreateAPIView(CreateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Check if the request data is a list (multiple objects) or a dict (single object)
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message='Sector(s) added successfully')
        except Exception as e:
            print(f"{e}")


class SectorUpdateAPIView(UpdateAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class SectorDetailAPIView(RetrieveAPIView):
    queryset = Sector.objects.all()
    serializer_class = SectorDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            status_code=status.HTTP_200_OK,
            data=serializer.data
        )


class SubsectorListAPIView(ListAPIView):
    queryset = Subsector.objects.all()
    serializer_class = SubsectorSerializer


class SubsectorCreateAPIView(CreateAPIView):
    queryset = Subsector.objects.all()
    serializer_class = SubsectorCreateSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Check if the request data is a list (multiple objects) or a dict (single object)
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Subsector(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class SubsectorUpdateAPIView(UpdateAPIView):
    queryset = Subsector.objects.all()
    serializer_class = SubsectorSerializer


class SubsectorDetailAPIView(RetrieveAPIView):
    queryset = Subsector.objects.all()
    serializer_class = SubsectorSerializer


class InstitutionListAPIView(ListAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionCreateAPIView(CreateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionUpdateAPIView(UpdateAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class InstitutionDetailAPIView(RetrieveAPIView):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer


class ProgrammeListAPIView(ListAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeListSerializer


class ProgrammeCreateAPIView(CreateAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeCreateSerializer


class ProgrammeUpdateAPIView(UpdateAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeUpdateSerializer


class ProgrammeDetailAPIView(RetrieveAPIView):
    queryset = Programme.objects.all()
    serializer_class = ProgrammeDetailSerializer


class ProjectNatureListAPIView(ListAPIView):
    queryset = ProjectNature.objects.all()
    serializer_class = ProjectNatureSerializer


class ProjectNatureCreateAPIView(CreateAPIView):
    queryset = ProjectNature.objects.all()
    serializer_class = ProjectNatureSerializer


class ProjectNatureUpdateAPIView(UpdateAPIView):
    queryset = ProjectNature.objects.all()
    serializer_class = ProjectNatureSerializer


class ProjectNatureDetailAPIView(RetrieveAPIView):
    queryset = ProjectNature.objects.all()
    serializer_class = ProjectNatureSerializer


class FundSourceListAPIView(ListAPIView):
    queryset = FundSource.objects.all()
    serializer_class = FundSourceSerializer


class FundSourceCreateAPIView(CreateAPIView):
    queryset = FundSource.objects.all()
    serializer_class = FundSourceSerializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Fund source(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class FundSourceUpdateAPIView(UpdateAPIView):
    queryset = FundSource.objects.all()
    serializer_class = FundSourceSerializer


class FundSourceDetailAPIView(RetrieveAPIView):
    queryset = FundSource.objects.all()
    serializer_class = FundSourceSerializer


class FundCategoryListAPIView(ListAPIView):
    queryset = FundCategory.objects.all()
    serializer_class = FundCategorySerializer
    filterset_fields = ['fund_source', 'code']


class FundCategoryCreateAPIView(CreateAPIView):
    queryset = FundCategory.objects.all()
    serializer_class = FundCategorySerializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Fund category(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class FundCategoryUpdateAPIView(UpdateAPIView):
    queryset = FundCategory.objects.all()
    serializer_class = FundCategorySerializer


class FundCategoryDetailAPIView(RetrieveAPIView):
    queryset = FundCategory.objects.all()
    serializer_class = FundCategorySerializer


class FinancingModalityListAPIView(ListAPIView):
    queryset = FinancingModality.objects.all()
    serializer_class = FinancingModalitySerializer
    filterset_fields = ['fund_category', 'code']


class FinancingModalityCreateAPIView(CreateAPIView):
    queryset = FinancingModality.objects.all()
    serializer_class = FinancingModalitySerializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Financing modality(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class FinancingModalityUpdateAPIView(UpdateAPIView):
    queryset = FinancingModality.objects.all()
    serializer_class = FinancingModalitySerializer


class FinancingModalityDetailAPIView(RetrieveAPIView):
    queryset = FinancingModality.objects.all()
    serializer_class = FinancingModalitySerializer


class FinancierListAPIView(ListAPIView):
    queryset = Financier.objects.all()
    serializer_class = FinancierSerializer


class FinancierCreateAPIView(CreateAPIView):
    queryset = Financier.objects.all()
    serializer_class = FinancierSerializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Financier(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class FinancierUpdateAPIView(UpdateAPIView):
    queryset = Financier.objects.all()
    serializer_class = FinancierSerializer


class FinancierDetailAPIView(RetrieveAPIView):
    queryset = Financier.objects.all()
    serializer_class = FinancierSerializer


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyCreateAPIView(CreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    def create(self, request, *args, **kwargs):
        try:
            many = isinstance(request.data, list)
            serializer = self.get_serializer(data=request.data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(status_code=status.HTTP_201_CREATED, message="Currency(s) added successfully")
        except Exception as e:
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            )


class CurrencyUpdateAPIView(UpdateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyDetailAPIView(RetrieveAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
