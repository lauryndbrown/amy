from django.test import TestCase
from consents.forms import ConsentForm
from consents.models import Term, TermOption, Consent
from workshops.models import Person


class TestTermForm(TestCase):
    # def setUp(self) -> None:

    def test_with_initial(self) -> None:
        term = Term.objects.create(content="term1", slug="term1")
        option1 = TermOption.objects.create(
            term=term,
            option_type="agree",
            content="option1",
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="option1",
        )
        person = Person.objects.create(
            personal="Harry", family="Potter", email="hp@magic.uk"
        )
        consent = Consent.objects.create(
            person=person,
            term=term,
            term_option=option1,
        )
        ConsentForm(term, initial={"options": consent.term_option})

    def test_no_term(self):
        pass
