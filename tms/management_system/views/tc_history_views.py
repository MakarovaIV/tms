from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from ..models import CustomUser, Project, TC, TCHistory, Suit


class TCHistoryView(ListView):
    model = TCHistory
    template_name = 'management_system/tc_history/tc_history_list.html'
    context_object_name = 'tc_history'

    def get_queryset(self):
        self.proj_id = get_object_or_404(Project, id=self.kwargs['proj_id'])
        self.suit_id = get_object_or_404(Suit, id=self.kwargs['suit_id'])
        self.pk = get_object_or_404(TC, id=self.kwargs['pk'])
        return TCHistory.objects.filter(tc_id=self.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        tc = get_object_or_404(TC, id=self.kwargs['pk'])
        modified_by_id = get_object_or_404(CustomUser, id=tc.modified_by)
        context["tc"] = tc
        context["name"] = tc.name
        context["desc"] = tc.desc
        context["steps"] = tc.steps
        context["status"] = tc.status
        context["modified_by"] = modified_by_id
        return context


class TCHistoryDetailView(DetailView):
    model = TCHistory
    template_name = 'management_system/tc_history/tc_history_detail.html'
    context_object_name = 'tc_history_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["proj_id"] = get_object_or_404(Project, id=self.kwargs['proj_id']).id
        context["suit_id"] = get_object_or_404(Suit, id=self.kwargs['suit_id']).id
        context["tc"] = get_object_or_404(TC, id=self.object.tc_id)
        return context

    def get_success_url(self):
        return reverse_lazy('tc_history_detail', kwargs={'proj_id': self.kwargs['proj_id'],
                                                         'suit_id': self.kwargs['suit_id'],
                                                         'tc': self.object.tc_id})


def recover_tc(request, proj_id, suit_id, tc_id, pk):
    data = request.POST.copy()
    if request.user.is_authenticated:
        tc = TCHistory.objects.filter(pk=pk).get()
        name = tc.name
        desc = tc.desc
        modified_by = tc.modified_by
        status = tc.status
        steps = tc.steps
        creation_date = tc.creation_date
        modification_date = tc.modification_date
        proj_id = tc.proj_id
        suit_id = tc.suit_id
        user_id = tc.user_id
        TC.objects.filter(pk=tc.tc_id).update(name=name,
                                              desc=desc,
                                              modified_by=modified_by,
                                              status=status,
                                              steps=steps,
                                              creation_date=creation_date,
                                              modification_date=modification_date,
                                              proj_id=proj_id,
                                              suit_id=suit_id,
                                              user_id=user_id)
        # updated_tc.save()
        return redirect('tc_update', proj_id=proj_id, suit_id=suit_id, pk=tc.tc_id)
