from django.urls import reverse

from workshops.tests.base import TestBase
from workshops.models import (
    Membership,
)

from fiscal.models import MembershipPersonRole, MembershipTask


class TestMembershipTasks(TestBase):
    def setUp(self):
        super().setUp()
        self._setUpUsersAndLogin()

        self.membership = Membership.objects.create(
            public_status="public",
            variant="partner",
            agreement_start="2021-02-14",
            agreement_end="2022-02-14",
            contribution_type="financial",
            seats_instructor_training=0,
            additional_instructor_training_seats=0,
        )
        self.membership_person_role = MembershipPersonRole.objects.first()

    def test_adding_new_tasks(self):
        self.assertEqual(self.membership.membershiptask_set.count(), 0)
        data = {
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 0,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 1000,
            "form-0-person": self.hermione.pk,
            "form-0-role": self.membership_person_role.pk,
            "form-0-id": "",
            "form-1-person": self.harry.pk,
            "form-1-role": self.membership_person_role.pk,
            "form-1-id": "",
        }
        response = self.client.post(
            reverse("membership_tasks", args=[self.membership.pk]),
            data=data,
            follow=True,
        )

        self.assertRedirects(
            response, reverse("membership_details", args=[self.membership.pk])
        )
        self.assertEqual(self.membership.membershiptask_set.count(), 2)
        self.assertEqual(
            list(self.membership.persons.all()), [self.hermione, self.harry]
        )

    def test_removing_tasks(self):
        mt1 = MembershipTask.objects.create(
            person=self.hermione,
            membership=self.membership,
            role=self.membership_person_role,
        )
        mt2 = MembershipTask.objects.create(
            person=self.harry,
            membership=self.membership,
            role=self.membership_person_role,
        )

        data = {
            "form-TOTAL_FORMS": 2,
            "form-INITIAL_FORMS": 2,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 1000,
            "form-0-person": mt1.person.pk,
            "form-0-role": mt1.role.pk,
            "form-0-id": mt1.pk,
            "form-0-DELETE": "on",
            "form-1-person": mt2.person.pk,
            "form-1-role": mt2.role.pk,
            "form-1-id": mt2.pk,
            "form-1-DELETE": "on",
        }
        response = self.client.post(
            reverse("membership_tasks", args=[self.membership.pk]),
            data=data,
            follow=True,
        )

        self.assertRedirects(
            response, reverse("membership_details", args=[self.membership.pk])
        )

        self.assertEqual(list(self.membership.persons.all()), [])

    def test_mix_adding_removing_tasks(self):
        mt1 = MembershipTask.objects.create(
            person=self.hermione,
            membership=self.membership,
            role=self.membership_person_role,
        )
        mt2 = MembershipTask.objects.create(
            person=self.harry,
            membership=self.membership,
            role=self.membership_person_role,
        )

        data = {
            "form-TOTAL_FORMS": 3,
            "form-INITIAL_FORMS": 2,
            "form-MIN_NUM_FORMS": 0,
            "form-MAX_NUM_FORMS": 1000,
            "form-0-person": mt1.person.pk,
            "form-0-role": mt1.role.pk,
            "form-0-id": mt1.pk,
            "form-0-DELETE": "on",
            "form-1-person": mt2.person.pk,
            "form-1-role": mt2.role.pk,
            "form-1-id": mt2.pk,
            "form-1-DELETE": "on",
            "form-2-person": self.ron.pk,
            "form-2-role": self.membership_person_role.pk,
            "form-2-id": "",
        }
        response = self.client.post(
            reverse("membership_tasks", args=[self.membership.pk]),
            data=data,
            follow=True,
        )

        self.assertRedirects(
            response, reverse("membership_details", args=[self.membership.pk])
        )

        self.assertEqual(list(self.membership.persons.all()), [self.ron])
