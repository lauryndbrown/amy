from consents.models import Consent
from django import forms
from workshops.forms import BootstrapHelper
from consents.models import Term, TermOption
from datetime import datetime
from workshops.forms import WidgetOverrideMixin

# class TermsForm(forms.Form):
#     helper = BootstrapHelper(wider_labels=True, add_cancel_button=False)

#     def __init__(self, *args, **kwargs):
#         person = kwargs["person"]
#         self._build_terms_form(person)
#         super().__init__(*args, **kwargs)
#         # set up a layout object for the helper
#         self.helper.layout = self.helper.build_default_layout(self)

#     # def single_option(term: Term) -> bool:
#     #     return len(term.options) == 1

#     # def two_options(term: Term) -> bool:
#     #     return len(term.options) == 1
#     def _build_terms_form(self, person: Person) -> None:
#         terms = Term.objects.options_with_answers()
#         for term in terms:
#             options = [(opt.id, opt.content) for opt in term.options]
#             self.fields[term.slug] = forms.ChoiceField(
#                 widget=forms.RadioSelect, choices=options
#             )


class ConsentsForm(WidgetOverrideMixin, forms.ModelForm):
    OPTION_DISPLAY = {"agree": "Yes", "disagree": "No", "unset": "unset"}

    class Meta:
        model = Consent
        fields = ["person"]

    def __init__(self, *args, **kwargs):
        form_tag = kwargs.pop("form_tag", True)
        super().__init__(*args, **kwargs)

        self._build_terms_form()
        self.helper = BootstrapHelper(add_cancel_button=False, form_tag=form_tag)

    def _build_terms_form(self) -> None:
        """
        Construct a Form of all nonarchived Terms with the
        consent answers added as initial.
        """

        def option_display_value(option: TermOption) -> str:
            return option.content or self.OPTION_DISPLAY[option.option_type]

        person = self.initial["person"]
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
        person = kwargs.pop("person")
        super().save(*args, **kwargs)
        for term in self.terms:
            option_id = self.cleaned_data.get(term.slug)
            consent, created = Consent.objects.get_or_create(person=person, term=term)
            if not created:
                consent.archived_at = datetime.now()
                consent.save()
                Consent.objects.create(
                    person=person, term_option_id=option_id, term_id=term.id
                )

    def _yes_only(self, term) -> bool:
        return len(term.options) == 1

    def _yes_and_no(self, term) -> bool:
        return len(term.options) == 2
