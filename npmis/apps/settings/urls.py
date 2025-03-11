from django.urls import path

from .views import InstitutionCreateAPIView, InstitutionUpdateAPIView, InstitutionListAPIView, InstitutionDetailAPIView, \
    AgendaListAPIView, \
    AgendaCreateAPIView, AgendaUpdateAPIView, AgendaDetailAPIView, FYDPListAPIView, FYDPCreateAPIView, \
    FYDPUpdateAPIView, FYDPDetailAPIView, TDVListAPIView, TDVCreateAPIView, TDVUpdateAPIView, TDVDetailAPIView, \
    SDGListAPIView, SDGCreateAPIView, SDGUpdateAPIView, SDGDetailAPIView, CostcentreListAPIView, \
    CostcentreCreateAPIView, CostcentreUpdateAPIView, CostcentreDetailAPIView, VoteListAPIView, VoteCreateAPIView, \
    VoteUpdateAPIView, VoteDetailAPIView, SectorListAPIView, SectorCreateAPIView, SectorUpdateAPIView, \
    SectorDetailAPIView, SubsectorListAPIView, SubsectorCreateAPIView, SubsectorUpdateAPIView, SubsectorDetailAPIView, \
    SDGGoalCreateAPIView, SDGGoalUpdateAPIView, SDGGoalDetailAPIView, SDGGoalListAPIView, SDGTargetCreateAPIView, \
    SDGTargetListAPIView, SDGTargetUpdateAPIView, SDGTargetDetailAPIView, AgendaGoalListAPIView, \
    AgendaGoalCreateAPIView, AgendaGoalUpdateAPIView, AgendaGoalDetailAPIView, AgendaTargetListAPIView, \
    AgendaTargetCreateAPIView, AgendaTargetUpdateAPIView, AgendaTargetDetailAPIView, FYDPGoalListAPIView, \
    FYDPGoalCreateAPIView, FYDPGoalUpdateAPIView, FYDPGoalDetailAPIView, FYDPTargetListAPIView, FYDPTargetCreateAPIView, \
    FYDPTargetUpdateAPIView, FYDPTargetDetailAPIView, TDVGoalListAPIView, TDVGoalCreateAPIView, TDVGoalUpdateAPIView, \
    TDVGoalDetailAPIView, TDVTargetListAPIView, TDVTargetCreateAPIView, TDVTargetUpdateAPIView, TDVTargetDetailAPIView, \
    AgendaAspirationListAPIView, AgendaAspirationCreateAPIView, AgendaAspirationUpdateAPIView, \
    AgendaAspirationDetailAPIView, ProgrammeListAPIView, ProgrammeCreateAPIView, ProgrammeUpdateAPIView, \
    ProgrammeDetailAPIView, ProjectNatureListAPIView, ProjectNatureCreateAPIView, ProjectNatureUpdateAPIView, \
    ProjectNatureDetailAPIView, CurrencyListAPIView, CurrencyCreateAPIView, CurrencyUpdateAPIView, \
    CurrencyDetailAPIView, FundSourceListAPIView, FundSourceCreateAPIView, FundSourceUpdateAPIView, \
    FundSourceDetailAPIView, FundCategoryListAPIView, FundCategoryCreateAPIView, FundCategoryUpdateAPIView, \
    FundCategoryDetailAPIView, FinancingModalityListAPIView, FinancingModalityCreateAPIView, \
    FinancingModalityUpdateAPIView, FinancingModalityDetailAPIView, FinancierListAPIView, FinancierCreateAPIView, \
    FinancierUpdateAPIView, FinancierDetailAPIView

urlpatterns = [
    path('sdg/', SDGListAPIView.as_view(), name='list_sdg'),
    path('sdg/create', SDGCreateAPIView.as_view(), name='create_sdg'),
    path('sdg/update/<str:pk>', SDGUpdateAPIView.as_view(), name='update_sdg'),
    path('sdg/detail/<str:pk>', SDGDetailAPIView.as_view(), name='detail_sdg'),
    path('sdg/goal/', SDGGoalListAPIView.as_view(), name='list_sdg_goal'),
    path('sdg/goal/create', SDGGoalCreateAPIView.as_view(), name='create_sdg_goal'),
    path('sdg/goal/update/<str:sdg>/<str:goal_no>', SDGGoalUpdateAPIView.as_view(), name='update_sdg_goal'),
    path('sdg/goal/detail/<str:sdg>/<int:goal_no>', SDGGoalDetailAPIView.as_view(), name='detail_sdg_goal'),
    path('sdg/target/', SDGTargetListAPIView.as_view(), name='list_sdg_target'),
    path('sdg/target/create', SDGTargetCreateAPIView.as_view(), name='create_sdg_target'),
    path('sdg/target/update/<str:sdg>/<str:goal_no>/<str:target_no>', SDGTargetUpdateAPIView.as_view(), name='update_sdg_target'),
    path('sdg/target/detail/<str:sdg>/<str:goal_no>/<str:target_no>', SDGTargetDetailAPIView.as_view(), name='detail_sdg_target'),

    path('agenda/', AgendaListAPIView.as_view(), name='list_agenda'),
    path('agenda/create', AgendaCreateAPIView.as_view(), name='create_agenda'),
    path('agenda/update/<str:pk>', AgendaUpdateAPIView.as_view(), name='update_agenda'),
    path('agenda/detail/<str:pk>', AgendaDetailAPIView.as_view(), name='detail_agenda'),
    path('agenda/aspiration/', AgendaAspirationListAPIView.as_view(), name='list_agenda_aspiration'),
    path('agenda/aspiration/create', AgendaAspirationCreateAPIView.as_view(), name='create_agenda_aspiration'),
    path('agenda/aspiration/update/<str:agenda>/<str:aspiration_no>', AgendaAspirationUpdateAPIView.as_view(), name='update_agenda_aspiration'),
    path('agenda/aspiration/detail/<str:agenda>/<int:aspiration_no>', AgendaAspirationDetailAPIView.as_view(), name='detail_agenda_aspiration'),
    path('agenda/goal/', AgendaGoalListAPIView.as_view(), name='list_agenda_goal'),
    path('agenda/goal/create', AgendaGoalCreateAPIView.as_view(), name='create_agenda_goal'),
    path('agenda/goal/update/<str:agenda>/<str:aspiration_no>/<str:goal_no>', AgendaGoalUpdateAPIView.as_view(), name='update_agenda_goal'),
    path('agenda/goal/detail/<str:agenda>/<str:aspiration_no>/<str:goal_no>', AgendaGoalDetailAPIView.as_view(), name='detail_agenda_goal'),
    path('agenda/target/', AgendaTargetListAPIView.as_view(), name='list_agenda_target'),
    path('agenda/target/create', AgendaTargetCreateAPIView.as_view(), name='create_agenda_target'),
    path('agenda/target/update/<str:agenda>/<str:aspiration_no>/<str:goal_no>/<str:target_no>', AgendaTargetUpdateAPIView.as_view(), name='update_agenda_target'),
    path('agenda/target/detail/<str:agenda>/<str:aspiration_no>/<str:goal_no>/<str:target_no>', AgendaTargetDetailAPIView.as_view(), name='detail_agenda_target'),

    path('fydp/', FYDPListAPIView.as_view(), name='list_fydp'),
    path('fydp/create', FYDPCreateAPIView.as_view(), name='create_fydp'),
    path('fydp/update/<str:pk>', FYDPUpdateAPIView.as_view(), name='update_fydp'),
    path('fydp/detail/<str:pk>', FYDPDetailAPIView.as_view(), name='detail_fydp'),
    path('fydp/goal/', FYDPGoalListAPIView.as_view(), name='list_fydp_goal'),
    path('fydp/goal/create', FYDPGoalCreateAPIView.as_view(), name='create_fydp_goal'),
    path('fydp/goal/update/<str:fydp>/<str:goal_no>', FYDPGoalUpdateAPIView.as_view(), name='update_fydp_goal'),
    path('fydp/goal/detail/<str:fydp>/<int:goal_no>', FYDPGoalDetailAPIView.as_view(), name='detail_fydp_goal'),
    path('fydp/target/', FYDPTargetListAPIView.as_view(), name='list_fydp_target'),
    path('fydp/target/create', FYDPTargetCreateAPIView.as_view(), name='create_fydp_target'),
    path('fydp/target/update/<str:fydp>/<str:goal_no>/<str:target_no>', FYDPTargetUpdateAPIView.as_view(), name='update_fydp_target'),
    path('fydp/target/detail/<str:fydp>/<str:goal_no>/<str:target_no>', FYDPTargetDetailAPIView.as_view(), name='detail_tdv_target'),

    path('tdv/', TDVListAPIView.as_view(), name='list_tdv'),
    path('tdv/create', TDVCreateAPIView.as_view(), name='create_tdv'),
    path('tdv/update/<str:pk>', TDVUpdateAPIView.as_view(), name='update_tdv'),
    path('tdv/detail/<str:pk>', TDVDetailAPIView.as_view(), name='detail_tdv'),
    path('tdv/goal/', TDVGoalListAPIView.as_view(), name='list_tdv_goal'),
    path('tdv/goal/create', TDVGoalCreateAPIView.as_view(), name='create_tdv_goal'),
    path('tdv/goal/update/<str:sdg>/<str:goal_no>', TDVGoalUpdateAPIView.as_view(), name='update_tdv_goal'),
    path('tdv/goal/detail/<str:sdg>/<int:goal_no>', TDVGoalDetailAPIView.as_view(), name='detail_tdv_goal'),
    path('tdv/target/', TDVTargetListAPIView.as_view(), name='list_tdv_target'),
    path('tdv/target/create', TDVTargetCreateAPIView.as_view(), name='create_tdv_target'),
    path('tdv/target/update/<str:sdg>/<str:goal_no>/<str:target_no>', TDVTargetUpdateAPIView.as_view(), name='update_tdv_target'),
    path('tdv/target/detail/<str:goal_no>/<str:target_no>', TDVTargetDetailAPIView.as_view(), name='detail_tdv_target'),

    path('programme/', ProgrammeListAPIView.as_view(), name='list_programme'),
    path('programme/create', ProgrammeCreateAPIView.as_view(), name='create_programme'),
    path('programme/update/<str:pk>', ProgrammeUpdateAPIView.as_view(), name='update_programme'),
    path('programme/detail/<str:pk>', ProgrammeDetailAPIView.as_view(), name='detail_programme'),

    path('projectnature/', ProjectNatureListAPIView.as_view(), name='list_projectnature'),
    path('projectnature/create', ProjectNatureCreateAPIView.as_view(), name='create_projectnature'),
    path('projectnature/update/<str:pk>', ProjectNatureUpdateAPIView.as_view(), name='update_projectnature'),
    path('projectnature/detail/<str:pk>', ProjectNatureDetailAPIView.as_view(), name='detail_projectnature'),

    path('costcentre/', CostcentreListAPIView.as_view(), name='list_costcentre'),
    path('costcentre/create', CostcentreCreateAPIView.as_view(), name='create_costcentre'),
    path('costcentre/update/<str:vote_no>/<str:costcentre_no>', CostcentreUpdateAPIView.as_view(), name='update_costcentre'),
    path('costcentre/detail/<str:vote_no>/<str:costcentre_no>', CostcentreDetailAPIView.as_view(), name='detail_costcentre'),

    path('vote/', VoteListAPIView.as_view(), name='list_vote'),
    path('vote/create', VoteCreateAPIView.as_view(), name='create_vote'),
    path('vote/update/<str:pk>', VoteUpdateAPIView.as_view(), name='update_vote'),
    path('vote/detail/<str:pk>', VoteDetailAPIView.as_view(), name='detail_vote'),

    path('sector/', SectorListAPIView.as_view(), name='list_sectors'),
    path('sector/create', SectorCreateAPIView.as_view(), name='create_sector'),
    path('sector/update/<str:pk>', SectorUpdateAPIView.as_view(), name='update_sector'),
    path('sector/detail/<str:pk>', SectorDetailAPIView.as_view(), name='detail_sector'),

    path('subsector/', SubsectorListAPIView.as_view(), name='list_subsectors'),
    path('subsector/create', SubsectorCreateAPIView.as_view(), name='create_subsector'),
    path('subsector/update/<str:pk>', SubsectorUpdateAPIView.as_view(), name='update_subsector'),
    path('subsector/detail/<str:pk>', SubsectorDetailAPIView.as_view(), name='detail_subsector'),

    path('institution/', InstitutionListAPIView.as_view(), name='list_institutions'),
    path('institution/create', InstitutionCreateAPIView.as_view(), name='create_institution'),
    path('institution/update/<str:pk>', InstitutionUpdateAPIView.as_view(), name='update_institution'),
    path('institution/detail/<str:pk>', InstitutionDetailAPIView.as_view(), name='detail_institution'),

    path('institution/', InstitutionListAPIView.as_view(), name='list_institutions'),
    path('institution/create', InstitutionCreateAPIView.as_view(), name='create_institution'),
    path('institution/update/<str:pk>', InstitutionUpdateAPIView.as_view(), name='update_institution'),
    path('institution/detail/<str:pk>', InstitutionDetailAPIView.as_view(), name='detail_institution'),

    path('currency/', CurrencyListAPIView.as_view(), name='list_currency'),
    path('currency/create', CurrencyCreateAPIView.as_view(), name='create_currency'),
    path('currency/update/<str:pk>', CurrencyUpdateAPIView.as_view(), name='update_currency'),
    path('currency/detail/<str:pk>', CurrencyDetailAPIView.as_view(), name='detail_currency'),

    path('fundsource/', FundSourceListAPIView.as_view(), name='list_fundsource'),
    path('fundsource/create', FundSourceCreateAPIView.as_view(), name='create_fundsource'),
    path('fundsource/update/<str:pk>', FundSourceUpdateAPIView.as_view(), name='update_fundsource'),
    path('fundsource/detail/<str:pk>', FundSourceDetailAPIView.as_view(), name='detail_fundsource'),

    path('fundcategory/', FundCategoryListAPIView.as_view(), name='list_fundcategory'),
    path('fundcategory/create', FundCategoryCreateAPIView.as_view(), name='create_fundcategory'),
    path('fundcategory/update/<str:pk>', FundCategoryUpdateAPIView.as_view(), name='update_fundcategory'),
    path('fundcategory/detail/<str:pk>', FundCategoryDetailAPIView.as_view(), name='detail_fundcategory'),

    path('financingmodality/', FinancingModalityListAPIView.as_view(), name='list_financingmodality'),
    path('financingmodality/create', FinancingModalityCreateAPIView.as_view(), name='create_financingmodality'),
    path('financingmodality/update/<str:pk>', FinancingModalityUpdateAPIView.as_view(), name='update_financingmodality'),
    path('financingmodality/detail/<str:pk>', FinancingModalityDetailAPIView.as_view(), name='detail_financingmodality'),

    path('financier/', FinancierListAPIView.as_view(), name='list_financier'),
    path('financier/create', FinancierCreateAPIView.as_view(), name='create_financier'),
    path('financier/update/<str:pk>', FinancierUpdateAPIView.as_view(), name='update_financier'),
    path('financier/detail/<str:pk>', FinancierDetailAPIView.as_view(), name='detail_financier'),
]