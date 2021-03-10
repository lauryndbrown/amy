from django.db import models
from workshops.mixins import CreatedUpdatedMixin
from workshops.models import Person, STR_MED
from django.db.models import Prefetch
from django.urls import reverse


class CreatedUpdatedArchivedMixin(CreatedUpdatedMixin):
    """This mixin adds an archived timestamp to the CreatedUpdatedMixin."""

    archived_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class TermQuerySet(models.query.QuerySet):
    def active(self, person: Person):
        return self.filter(person=person, archived_at=None)

    def prefetch_options(self, person: Person):
        return self.filter(archived_at=None).prefetch_related(
            Prefetch(
                "termoption_set",
                queryset=TermOption.objects.filter(archived_at=None),
                to_attr="options",
            )
        )


class Term(CreatedUpdatedArchivedMixin, models.Model):
    TERM_REQUIRE_TYPE = (
        ("profile", "Required to create a Profile"),
        ("optional", "Optional"),
    )

    slug = models.SlugField(unique=True)
    content = models.TextField(verbose_name="Content")
    required_type = models.CharField(
        max_length=STR_MED, choices=TERM_REQUIRE_TYPE, default="optional"
    )
    objects = TermQuerySet.as_manager()


class TermOption(CreatedUpdatedArchivedMixin, models.Model):
    OPTION_TYPE = (("agree", "Agree"), ("decline", "Decline"), ("unset", "Unset"))

    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    option_type = models.CharField(max_length=STR_MED, choices=OPTION_TYPE)
    content = models.TextField(verbose_name="Content", blank=True)


class Consent(CreatedUpdatedArchivedMixin, models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    term_option = models.ForeignKey(TermOption, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return reverse("consent_details", kwargs={"consent_id": self.id})

    # TODO: add constraint term.id == term_option.term.id
    # or remove term and just reach into term_option
    # TODO: add constraint unique person, term, archived_at=None


# class Question():
#     content = models.TextField(verbose_name="Content")

#     def answers():
#         QuestionOption.objects.filter(

# class QuestionOption():
#     OPTION_TYPE = (
#         ("agree", "Agree"),
#         ("decline", "Decline"),
#         ("unset", "Unset")
#     )

#     option_type = models.CharField(max_length=STR_MED, choices=OPTION_TYPE)
#     content = models.TextField(verbose_name="Content")
# class Consent(CreatedUpdatedArchivedMixin, models.Model):
#     question = models.ForeignKey(Question, on_delete=models.PROTECT)
#     answer  = models.ForeignKey(Person, on_delete=models.PROTECT)
#     user = models.ForeignKey(Person, on_delete=models.PROTECT)
