from django.db import models
from workshops.mixins import CreatedUpdatedMixin
from workshops.models import Person, STR_MED
from django.db.models import Prefetch


class CreatedUpdatedArchivedMixin(CreatedUpdatedMixin):
    """This mixin adds an archived timestamp to the CreatedUpdatedMixin."""

    archived_at = models.DateTimeField(null=True)

    class Meta:
        abstract = True


class TermQuerySet(models.query.QuerySet):
    def active(self, person: Person):
        return self.filter(person=person, archived_at=None)

    def options_with_answers(self, person: Person):
        return self.filter(archived_at=None).prefetch_related(
            Prefetch(
                "termoption_set",
                queryset=TermOption.objects.filter(archived_at=None).prefetch_related(
                    Prefetch(
                        "personconsent_set",
                        queryset=PersonConsent.objects.filter(
                            archived_at=None, person=person
                        ),
                        to_attr="answers",
                    )
                ),
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

    @classmethod
    def options_for_term(cls, term):
        return cls.objects.filter(term=term, archived_at=None)


class PersonConsent(CreatedUpdatedArchivedMixin, models.Model):
    person = models.ForeignKey(Person, on_delete=models.PROTECT)
    term_option = models.ForeignKey(TermOption, on_delete=models.PROTECT)


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
