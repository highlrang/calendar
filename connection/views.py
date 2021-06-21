from django.shortcuts import render, redirect, reverse
from django.views.generic import *
from connection.models import *
from schedule.models import Category

# Create your views here.
class Friends_list(ListView):
    template_name='connection/friends_list.html'

    def get_queryset(self):
        return Friends.objects.filter(f_user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            proposal = Proposal.objects.filter(p_partner = self.request.user, p_reject = False)
            context['getProposal'] = proposal
        except Proposal.DoesNotExist:
            context['getProposal'] = ''
        return context


def Friends_revoke(request, pk):
    friend = Friends.objects.get(f_id = pk)
    friend.delete()
    return redirect(reverse('connection:friendsList'))



class Friends_proposal(TemplateView):
    template_name = 'connection/friends_proposal.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apply_list'] = Proposal.objects.filter(p_user=self.request.user)
        return context




def Final_category(request):
    if request.POST:
        partner_name = request.POST['partner_name']
        partner_cate = request.POST['partner_cate']
        category_list = Category.objects.filter(c_user=request.user)
        return render(request, 'connection/final_category.html', {'cate_list': category_list, 'p_user':partner_name, 'p_cate': partner_cate})



class ReceiveApplyView(View):
    template_name = 'connection/friends_list.html'

    def insert_friend(self, user, partner, cate):
        already = Friends.objects.filter(f_user=user, f_partner=partner, f_cate=cate).exists()
        if already is False:
            Friends.objects.create(f_user=user, f_partner=partner, f_cate=cate)

    def remove_proposal(self, id):
        Proposal.objects.get(p_id=id).delete()

    def post(self, request, *args, **kwargs):
        proposalId = kwargs['p_id'] # 추가하기
        partnerName = User.objects.get(username=kwargs['p_user'])
        partnerCate = Category.objects.get(c_user=partnerName, c_cate=kwargs['p_cate'])

        # Friends가 없을 경우에만 추가
        self.insert_friend(request.user, partnerName, partnerCate)

        # Proposal 삭제
        self.remove_proposal(proposalId)

        # context data
        context = {
            'object_list': Friends.objects.filter(f_user=request.user),
            'getProposal': Proposal.objects.filter(p_partner=request.user, p_reject=False),
        }

        return render(request, self.template_name, context=context)





def User_search(request):
    if request.POST:
        try:
            User.objects.get(username = request.POST['user_name'])
            search_result = request.POST['user_name']
        except User.DoesNotExist:
            search_result = 'False'

        return render(request, 'connection/friends_proposal.html', {'search_result':search_result})


def Select_category(request):
    if request.POST:
        user_name = request.POST['user_name']
        cate_list = Category.objects.filter(c_user=request.user)
    return render(request, 'connection/select_category.html', {'user_name': user_name, 'cate_list':cate_list})


class FriendsApplyView(View):
    template_name = 'connection/friends_proposal.html'

    def post(self, request, *args, **kwargs):
        user = User.objects.get(username= kwargs['user_name'])
        cate = Category.objects.get(c_id = kwargs['cate'])
        # category null 없게하기 (null은 p_cate__isnull=True)

        already_friend = Proposal.objects.filter(p_user=request.user, p_partner=user.pk, p_cate=cate).exists()
        if already_friend:
            msg = str(user) + ' 님은 이미 친구 신청되어 있습니다.'

        else:
            Proposal.objects.create(p_user=request.user, p_partner=user, p_cate=cate)
            msg = str(user) + ' 님에게 친구 신청하였습니다.'

        # 내가 신청한 목록 추가
        apply_list = Proposal.objects.filter(p_user=request.user)
        context = {'apply_list': apply_list, 'msg': msg}
        return render(request, self.template_name, context)


# 거절
def Apply_reject(request, pk):
    proposal = Proposal.objects.get(p_id=pk)
    proposal.p_reject = True
    proposal.save()
    return redirect(reverse('connection:friendsList'))

# 신청 취소
def Proposal_revoke(request, pk):
    proposal = Proposal.objects.get(p_id=pk)
    proposal.delete()
    return redirect(reverse('connection:friendsProposal'))

