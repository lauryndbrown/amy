from consents.models import Consent
from workshops.base_views import RedirectSupportMixin
from consents.forms import ConsentsForm
from workshops.base_views import AMYCreateView


class ConsentsUpdate(RedirectSupportMixin, AMYCreateView):
    model = Consent
    form_class = ConsentsForm
    success_url = "consents/edit"
    # queryset = Event.objects.select_related(
    #     "assigned_to",
    #     "administrator",
    #     "language",
    # ).prefetch_related("sponsorship_set")
    # slug_field = "slug"
    # template_name = "workshops/event_edit_form.html"

    def get_success_url(self):
        # default_url = super().get_success_url()
        next_url = self.request.GET.get("next", None)
        return next_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"prefix": "consents"})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # kwargs = {
        #     "initial": {"person": self.object},
        #     "widgets": {"person": HiddenInput()},
        # }
        return context

    def form_valid(self, form):
        res = super().form_valid(form)
        return res
