# from amy.consents.models import PersonConsent, TermOption
# from rest_framework import serializers
# from django.db.models import Prefetch, query


# class ConsentSerializer(serializers.Serializer):
#     question = serializers.TextField()
#     answer = serializers.TextField()
#     person_id = serializers.Integer()

#     @classmethod
#     def from_person(person: Person):
#         terms = Term.objects.filter(archived_at=None).prefetch_related(
#             Prefetch(
#                 "termoption_set",
#                 queryset=TermOption.objects.filter(archived_at=None).prefetch_related(
#                     Prefetch(
#                         "personconsent_set",
#                         queryset=PersonConsent.objects.filter(
#                             archived_at=None, person=person
#                         ),
#                         to_attr="answers",
#                     )
#                 ),
#                 to_attr="options",
#             )
#         )
#         # consents = PersonConsent.objects.filter(archived_at=None)
# .select_related("term_option").select_related("term_option__term")
#         # for consent in consents:
#         #     consent.term
