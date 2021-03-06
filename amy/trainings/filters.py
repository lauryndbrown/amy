import re

import django_filters
from django.db.models import Q
from django.forms import widgets

from workshops.fields import ModelSelect2Widget
from workshops.filters import (
    AMYFilterSet,
    NamesOrderingFilter,
)
from workshops.forms import SELECT2_SIDEBAR
from workshops.models import (
    Event,
    Person,
)


def filter_all_persons(queryset, name, all_persons):
    """Filter only trainees when all_persons==False."""
    if all_persons:
        return queryset
    else:
        return queryset.filter(
            task__role__name="learner", task__event__tags__name="TTT"
        ).distinct()


def filter_trainees_by_trainee_name_or_email(queryset, name, value):
    if value:
        # 'Harry Potter' -> ['Harry', 'Potter']
        tokens = re.split(r"\s+", value)
        # Each token must match email address or github username or personal or
        # family name.
        for token in tokens:
            queryset = queryset.filter(
                Q(personal__icontains=token)
                | Q(family__icontains=token)
                | Q(email__icontains=token)
            )
        return queryset
    else:
        return queryset


def filter_trainees_by_unevaluated_homework_presence(queryset, name, flag):
    if flag:  # return only trainees with an unevaluated homework
        return queryset.filter(trainingprogress__state="n").distinct()
    else:
        return queryset


def filter_trainees_by_training_request_presence(queryset, name, flag):
    if flag is None:
        return queryset
    elif flag is True:  # return only trainees who submitted training request
        return queryset.filter(trainingrequest__isnull=False).distinct()
    else:  # return only trainees who did not submit training request
        return queryset.filter(trainingrequest__isnull=True)


def filter_trainees_by_instructor_status(queryset, name, choice):
    if choice == "all":
        return queryset.filter(
            is_swc_instructor=True,
            is_dc_instructor=True,
            is_lc_instructor=True,
        )
    elif choice == "any":
        return queryset.filter(
            Q(is_swc_instructor=True)
            | Q(is_dc_instructor=True)
            | Q(is_lc_instructor=True)
        )
    elif choice == "swc":
        return queryset.filter(is_swc_instructor=True)
    elif choice == "dc":
        return queryset.filter(is_dc_instructor=True)
    elif choice == "lc":
        return queryset.filter(is_lc_instructor=True)
    elif choice == "eligible":
        # Instructor eligible but without any badge.
        # This code is kept in Q()-expressions to allow for fast condition
        # change.
        return queryset.filter(Q(instructor_eligible__gte=1) & Q(is_instructor=False))
    elif choice == "no":
        return queryset.filter(
            is_instructor=False,
        )
    else:
        return queryset


def filter_trainees_by_training(queryset, name, training):
    if training is None:
        return queryset
    else:
        return queryset.filter(
            task__role__name="learner", task__event=training
        ).distinct()


class TraineeFilter(AMYFilterSet):
    search = django_filters.CharFilter(
        method=filter_trainees_by_trainee_name_or_email, label="Name or Email"
    )

    all_persons = django_filters.BooleanFilter(
        label="Include all people, not only trainees",
        method=filter_all_persons,
        widget=widgets.CheckboxInput,
    )

    homework = django_filters.BooleanFilter(
        label="Only trainees with unevaluated homework",
        widget=widgets.CheckboxInput,
        method=filter_trainees_by_unevaluated_homework_presence,
    )

    training_request = django_filters.BooleanFilter(
        label="Is training request present?",
        method=filter_trainees_by_training_request_presence,
    )

    is_instructor = django_filters.ChoiceFilter(
        label="Is Instructor?",
        method=filter_trainees_by_instructor_status,
        choices=[
            ("", "Unknown"),
            ("all", "All instructor badges"),
            ("any", "Any instructor badge "),
            ("swc", "SWC instructor"),
            ("dc", "DC instructor"),
            ("lc", "LC instructor"),
            ("eligible", "No, but eligible to be certified"),
            ("no", "No instructor badge"),
        ],
    )

    training = django_filters.ModelChoiceFilter(
        queryset=Event.objects.ttt(),
        method=filter_trainees_by_training,
        label="Training",
        widget=ModelSelect2Widget(
            data_view="ttt-event-lookup",
            attrs=SELECT2_SIDEBAR,
        ),
    )

    order_by = NamesOrderingFilter(
        fields=(
            "last_login",
            "email",
        ),
    )

    class Meta:
        model = Person
        fields = [
            "search",
            "all_persons",
            "homework",
            "is_instructor",
            "training",
        ]
