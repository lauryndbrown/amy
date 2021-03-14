from consents.models import Consent
from workshops.base_views import RedirectSupportMixin
from consents.forms import ConsentForm
from workshops.base_views import AMYCreateView, AMYDeleteView


class ConsentUpdate(RedirectSupportMixin, AMYCreateView):
    model = Consent
    form_class = ConsentForm
    success_url = "consents/edit"

    def get_success_url(self):
        # Currently can only be called via redirect.
        # There is no direct view for Consents.
        next_url = self.request.GET["next"]
        return next_url

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        person = kwargs["data"]["consents-person"]
        kwargs.update({"prefix": "consents", "person": person})
        return kwargs

    def get_success_message(self, *args, **kwargs):
        return "Consents were successfully updated."


class ConsentDelete(RedirectSupportMixin, AMYDeleteView):
    pass
