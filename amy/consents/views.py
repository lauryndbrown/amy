from consents.models import Consent
from workshops.base_views import RedirectSupportMixin
from consents.forms import ConsentsForm
from workshops.base_views import AMYCreateView


class ConsentsUpdate(RedirectSupportMixin, AMYCreateView):
    model = Consent
    form_class = ConsentsForm
    # queryset = Event.objects.select_related(
    #     "assigned_to",
    #     "administrator",
    #     "language",
    # ).prefetch_related("sponsorship_set")
    # slug_field = "slug"
    # template_name = "workshops/event_edit_form.html"

    def get_context_data(self, **kwargs):
        breakpoint()
        context = super().get_context_data(**kwargs)
        # kwargs = {
        #     "initial": {"person": self.object},
        #     "widgets": {"person": HiddenInput()},
        # }
        return context

    def form_valid(self, form):
        breakpoint()
        res = super().form_valid(form)
        return res
