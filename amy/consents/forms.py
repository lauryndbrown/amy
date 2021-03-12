from consents.models import Consent
from django import forms
from workshops.forms import BootstrapHelper
from consents.models import Term, TermOption
from datetime import datetime
from workshops.forms import WidgetOverrideMixin

OPTION_DISPLAY = {"agree": "Yes", "disagree": "No", "unset": "unset"}


def option_display_value(option: TermOption) -> str:
    return option.content or OPTION_DISPLAY[option.option_type]


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ["content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["options"] = self.create_options_field()

    def create_options_field(self):
        if not self.instance:
            return []
        options = self.instance.prefetch_active_options().options
        options = [(opt.id, option_display_value(opt)) for opt in self.instance.options]

        required = False if self.instance.required_type == "optional" else True
        field = forms.ChoiceField(
            widget=forms.RadioSelect,
            choices=options,
            label=self.instance.content,
            required=required,
        )
        return field


class ConsentsForm(WidgetOverrideMixin, forms.ModelForm):
    class Meta:
        model = Consent
        fields = ["person"]

    def __init__(self, *args, **kwargs):
        form_tag = kwargs.pop("form_tag", True)
        # TODO how to get the person value out of the person field
        if "data" in kwargs:
            if "person" in kwargs["data"]:
                person = kwargs["data"]["person"]
            else:
                person = kwargs["data"]["consents-person"]
        else:
            person = kwargs["initial"]["person"]
        super().__init__(*args, **kwargs)

        self._build_terms_form(person)
        self.helper = BootstrapHelper(add_cancel_button=False, form_tag=form_tag)

    def _build_terms_form(self, person) -> None:
        """
        Construct a Form of all nonarchived Terms with the
        consent answers added as initial.
        """

        def option_display_value(option: TermOption) -> str:
            return option.content or self.OPTION_DISPLAY[option.option_type]

        # person = self.initial.get("person"
        self.terms = Term.objects.prefetch_options(person=person)
        term_id_by_option_id = {
            consent.term_id: consent.term_option_id
            for consent in Consent.objects.filter(
                archived_at=None, term__in=self.terms, person=person
            )
        }
        for term in self.terms:
            options = [(opt.id, option_display_value(opt)) for opt in term.options]
            required = False if term.required_type == "optional" else True
            initial = term_id_by_option_id.get(term.id, None)

            self.fields[term.slug] = forms.ChoiceField(
                widget=forms.RadioSelect,
                choices=options,
                label=term.content,
                required=required,
                initial=initial,
            )

    def save(self, *args, **kwargs):
        person = self.cleaned_data["person"]
        # super().save(*args, **kwargs)
        for term in self.terms:
            option_id = self.cleaned_data.get(term.slug)
            if not option_id:
                continue
            try:
                consent = Consent.objects.get(
                    person=person, term=term, archived_at=None
                )
            except Consent.DoesNotExist:
                pass
            else:
                consent.archived_at = datetime.now()
                consent.save()
            Consent.objects.create(
                person=person, term_option_id=option_id, term_id=term.id
            )

    def _yes_only(self, term) -> bool:
        return len(term.options) == 1

    def _yes_and_no(self, term) -> bool:
        return len(term.options) == 2
