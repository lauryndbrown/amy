from django.test import TestCase
from consents.models import Term, TermOption, Consent
from workshops.tests.base import SuperuserMixin
from datetime import datetime


# Create your tests here.
class TermTest(SuperuserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self._setUpSuperuser()  # creates self.admin

    def test_yes_only_term(self) -> None:
        # TODO add a manual migration to add basic cases
        term = Term.objects.create(
            content="Are you 18 or older?", slug="18-or-older", required_type="profile"
        )
        option_agree = TermOption.objects.create(term=term, option_type="agree")
        Consent.objects.create(person=self.admin, term_option=option_agree)

    def test_yes_and_no_term(self) -> None:
        # TODO add a manual migration to add basic cases
        term = Term.objects.create(
            content="May contact: Allow to contact from The Carpentries according to"
            " the Privacy Policy.",
            slug="may-contact",
        )
        option_agree = TermOption.objects.create(term=term, option_type="agree")
        option_agree = TermOption.objects.create(term=term, option_type="disagree")
        Consent.objects.create(person=self.admin, term_option=option_agree)

    def test_custom_choices_term(self) -> None:
        # TODO add a manual migration to add basic cases
        term = Term.objects.create(
            content="Do you consent to have your name or identity"
            " associated with lesson publications?",
            slug="may-publish-name",
        )
        TermOption.objects.create(
            term=term, option_type="agree", content="Yes, and only use my GitHub Handle"
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my ORCID profile",
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my profile.",
        )
        option_disagree = TermOption.objects.create(term=term, option_type="disagree")
        Consent.objects.create(person=self.admin, term_option=option_disagree)

    def test_unset_term(self) -> None:
        # Unsetting term will simply be archiving the option
        term = Term.objects.create(
            content="Do you consent to have your name or identity associated with"
            " lesson publications?",
            slug="may-publish-name",
        )
        TermOption.objects.create(
            term=term, option_type="agree", content="Yes, and only use my GitHub Handle"
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my ORCID profile",
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my profile.",
        )
        option_disagree = TermOption.objects.create(term=term, option_type="disagree")
        Consent.objects.create(person=self.admin, term_option=option_disagree)

        consent = Consent.objects.get(person=self.admin, term_option__term=term)
        consent.archived_at = datetime.now()
        consent.save()

    def test_changing_an_option(self) -> None:
        # Unsetting term will simply be archiving the option
        term = Term.objects.create(
            content="Do you consent to have your name or identity associated with"
            " lesson publications?",
            slug="may-publish-name",
        )
        TermOption.objects.create(
            term=term, option_type="agree", content="Yes, and only use my GitHub Handle"
        )
        TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my ORCID profile",
        )
        option_agree = TermOption.objects.create(
            term=term,
            option_type="agree",
            content="Yes, and use the name associated with my profile.",
        )
        option_disagree = TermOption.objects.create(term=term, option_type="disagree")
        Consent.objects.create(person=self.admin, term_option=option_disagree)

        consent = Consent.objects.get(person=self.admin, term_option__term=term)
        consent.archived_at = datetime.now()
        consent.save()

        consent = Consent.objects.create(person=self.admin, term_option=option_agree)
