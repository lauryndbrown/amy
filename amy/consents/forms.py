from django import forms
from workshops.forms import BootstrapHelper
from workshops.models import Person
from consents.models import Term


class TrainingRequestForm(forms.Form):
    helper = BootstrapHelper(wider_labels=True, add_cancel_button=False)

    def __init__(self, *args, **kwargs):
        person = kwargs["person"]
        self._build_terms_form(person)
        super().__init__(*args, **kwargs)
        # set up a layout object for the helper
        self.helper.layout = self.helper.build_default_layout(self)

    # def single_option(term: Term) -> bool:
    #     return len(term.options) == 1

    # def two_options(term: Term) -> bool:
    #     return len(term.options) == 1
    def _build_terms_form(self, person: Person) -> None:
        terms = Term.objects.options_with_answers()
        for term in terms:
            options = [(opt.id, opt.content) for opt in term.options]
            self.fields[term.slug] = forms.ChoiceField(
                widget=forms.RadioSelect, choices=options
            )
