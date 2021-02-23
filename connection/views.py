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

def Receive_apply(request):
    if request.POST:
        myCate = request.POST['cate']
        if myCate != 'null':
            myCate = Category.objects.get(c_id = myCate)
        partnerName = User.objects.get(username=request.POST['p_user'])
        yourCate = request.POST['p_cate']
        if yourCate != 'None':
            yourCate = Category.objects.get(c_user = partnerName, c_cate = yourCate)


        # Friends가 없을 경우에 추가
        if yourCate != 'None':
            try:
                Friends.objects.get(f_user=request.user, f_partner=partnerName, f_cate=yourCate)
                msg = '이미 친구 상태입니다.'
            except Friends.DoesNotExist:
                Friends.objects.create(f_user=request.user, f_partner=partnerName, f_cate=yourCate)
                msg = '친구 수락되었습니다.'
        else:
            try:
                friend = Friends.objects.filter(f_user=request.user, f_partner=partnerName)
                msg = '이미 친구 상태입니다.'

                have = False
                for f in friend:
                    if f.f_cate is None:
                        have = True

                if have == False:
                    Friends.objects.create(f_user=request.user, f_partner=partnerName)
                    msg = '친구 수락되었습니다.'

            except Friends.DoesNotExist:
                Friends.objects.create(f_user=request.user, f_partner=partnerName)
                msg = '친구 수락되었습니다.'

        if myCate != 'null':
            try:
                Friends.objects.get(f_user=partnerName, f_partner=request.user, f_cate=myCate)
                msg = '이미 친구 상태입니다.'

            except Friends.DoesNotExist:
                Friends.objects.create(f_user=partnerName, f_partner=request.user, f_cate=myCate)
                msg = '친구 수락되었습니다.'

        else:
            try:
                friend = Friends.objects.filter(f_user=partnerName, f_partner=request.user)
                msg = '이미 친구 상태입니다.'

                have = False
                for f in friend:
                    if f.f_cate is None:
                        have = True

                if have == False:
                    Friends.objects.create(f_user=partnerName, f_partner=request.user)
                    msg = '친구 수락되었습니다.'

            except Friends.DoesNotExist:
                Friends.objects.create(f_user=partnerName, f_partner=request.user)
                msg = '친구 수락되었습니다.'



        # Proposal 삭제
        if yourCate == 'None':
            proposal = Proposal.objects.filter(p_user=partnerName, p_partner=request.user)
            for p in proposal:
                if p.p_cate is None:
                    p.delete()
        else:
            proposal = Proposal.objects.get(p_user=partnerName, p_partner=request.user, p_cate=yourCate)
            proposal.delete()


        # context data
        try:
            proposal = Proposal.objects.filter(p_partner = request.user, p_reject = False)
        except Proposal.DoesNotExist:
            proposal = ''

        context = {
                'object_list' : Friends.objects.filter(f_user = request.user),
                'getProposal' : proposal,
                'msg' : msg
            }


        return render(request, 'connection/friends_list.html', context=context) # msg로 인해 redirect 에서 render로





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


def Friends_apply(request):
    if request.POST:
        user = User.objects.get(username=request.POST['user_name'])
        if request.POST['cate'] == 'null':
            try:
                proposal = Proposal.objects.filter(p_user=request.user, p_partner=user.pk)
                have = False
                for p in proposal:
                    if p.p_cate is None:
                        have = True
                if have == True:
                    msg = str(user) + ' 님은 이미 친구 신청되어 있습니다.'
                else:
                    Proposal.objects.create(p_user=request.user, p_partner=user)
                    msg = str(user) + ' 님에게 친구 신청하였습니다.'

            except Proposal.DoesNotExist:
                Proposal.objects.create(p_user=request.user, p_partner=user)
                msg = str(user) + ' 님에게 친구 신청하였습니다.'

        else:
            cate = Category.objects.get(c_id = request.POST['cate'])
            try:
                Proposal.objects.get(p_user=request.user, p_partner=user.pk, p_cate=cate)
                msg = str(user) + ' 님은 이미 친구 신청되어 있습니다.'

            except Proposal.DoesNotExist:
                Proposal.objects.create(p_user=request.user, p_partner=user, p_cate=cate)
                msg = str(user) + ' 님에게 친구 신청하였습니다.'

        # 내가 신청한 목록 추가
        apply_list = Proposal.objects.filter(p_user=request.user)
        return render(request, 'connection/friends_proposal.html', {'apply_list': apply_list, 'msg': msg})


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