from workshops.base_views import (
    AMYDeleteView,
    AMYDetailView,
    AMYListView,
    AMYUpdateView,
)
from consents.models import Term
from consents.forms import TermForm
from consents.models import Consent
from workshops.base_views import RedirectSupportMixin
from consents.forms import ConsentsForm
from workshops.base_views import AMYCreateView
from workshops.util import OnlyForAdminsMixin
from consents.filters import TermFilter

# TODO:
# - Add PermissionRequiredMixin to Create, Update, And Delete views


class AllTerms(OnlyForAdminsMixin, AMYListView):
    context_object_name = "all_terms"
    queryset = Term.objects.all().prefetch_all_options()
    template_name = "consents/all_terms.html"
    filter_class = TermFilter
    title = "All Terms"


class TermDetails(OnlyForAdminsMixin, AMYDetailView):
    context_object_name = "term"
    template_name = "terms/term.html"
    pk_url_kwarg = "term_id"
    queryset = Term.objects.prefetch_all_options()


class TermCreate(OnlyForAdminsMixin, AMYCreateView):
    model = Term
    pk_url_kwarg = "term_id"
    form_class = TermForm


class TermUpdate(OnlyForAdminsMixin, AMYUpdateView):
    pass


class TermDelete(OnlyForAdminsMixin, AMYDeleteView):
    pass


class ConsentUpdate(RedirectSupportMixin, AMYCreateView):
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
