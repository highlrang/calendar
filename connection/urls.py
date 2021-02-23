from django.urls import path
from connection.views import *

app_name = 'connection'
urlpatterns = [
    path('list/', Friends_list.as_view(), name='friendsList'),
    # 친구인 상태에서 취소
    path('list/revoke/<int:pk>/', Friends_revoke, name='friendsRevoke'),

    path('proposal/', Friends_proposal.as_view(), name='friendsProposal'), # 신청하기
    path('proposal/revoke/<int:pk>', Proposal_revoke, name='proposalRevoke'), # 신청 철회
    path('proposal/search/', User_search, name='userSearch'),

    # 친구 수락할 때 카테고리와 수락하기
    path('proposal/final/category/', Final_category, name='finalCategory'),
    path('proposal/final/apply/', Receive_apply, name='receiveApply'),

    # 내가 신청할 때 카테고리와 신청하기
    path('proposal/category/', Select_category, name='selectCategory'),
    path('proposal/apply/', Friends_apply, name='friendsApply'),

    # 신청 거절
    path('proposal/reject/<int:pk>/', Apply_reject, name='applyReject'),

]