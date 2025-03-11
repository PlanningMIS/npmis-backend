from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from django.conf import settings


class CustomUserDetailsSerializer(UserDetailsSerializer):
    vote = serializers.SerializerMethodField()
    institution = serializers.SerializerMethodField()

    def get_vote(self, user):
        if hasattr(user, "vote") and user.vote:
            return {
                "id": user.vote.vote_no,
                "name": user.vote.name,
            }
        return None

    def get_institution(self, user):
        if hasattr(user, "institution") and user.institution:
            return {
                "id": user.institution.id,
                "name": user.institution.name,
            }
        return None

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ("vote", "institution")
