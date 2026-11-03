from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Lesson, PhrasePair, Section, Tag
from .repetition_service import mark_incorrect, schedule_next_review


class PhrasePairSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhrasePair
        fields = ["id", "phrase_one", "phrase_two", "is_learned"]


class LessonSerializer(serializers.ModelSerializer):
    phrase_pairs = PhrasePairSerializer(many=True)
    progress = serializers.SerializerMethodField()
    section = serializers.PrimaryKeyRelatedField(
        queryset=Section.objects.all(), required=False, allow_null=True
    )
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Lesson
        fields = [
            "id",
            "section",
            "title",
            "description",
            "created_at",
            "phrase_pairs",
            "progress",
            "tags",
        ]
        read_only_fields = ["id", "created_at", "progress"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request", None)
        if request and hasattr(request, "user") and request.user.is_authenticated:
            self.fields["section"].queryset = Section.objects.filter(user_id=request.user.id)
        else:
            self.fields["section"].queryset = Section.objects.none()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = list(instance.tags.values_list("name", flat=True))
        return data

    def get_progress(self, obj) -> float:
        return obj.calculate_progress()

    def _get_or_create_tags(self, tag_names):
        User = get_user_model()
        request_user = self.context["request"].user
        user = User.objects.get(pk=request_user.pk)

        tags = []
        seen_tags = set()

        for tag_name in tag_names:
            tag_name = tag_name.strip().casefold()

            if not tag_name or tag_name in seen_tags:
                continue

            seen_tags.add(tag_name)

            tag, _ = Tag.objects.get_or_create(
                user=user,
                name=tag_name,
            )
            tags.append(tag)

        return tags

    def create(self, validated_data):
        phrase_pairs_data = validated_data.pop("phrase_pairs", [])
        tag_names = validated_data.pop("tags", [])
        lesson = Lesson.objects.create(**validated_data)
        tags = self._get_or_create_tags(tag_names)
        lesson.tags.set(tags)
        for phrase_pair_data in phrase_pairs_data:
            PhrasePair.objects.create(lesson=lesson, **phrase_pair_data)
        return lesson

    def update(self, instance, validated_data):
        phrase_pairs_data = validated_data.pop("phrase_pairs", None)
        tag_names = validated_data.pop("tags", None)

        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.section = validated_data.get("section", instance.section)
        instance.save()

        if tag_names is not None:
            tags = self._get_or_create_tags(tag_names)
            instance.tags.add(*tags)

        if phrase_pairs_data is not None:
            for phrase_pair_data in phrase_pairs_data:
                if "id" in phrase_pair_data:
                    try:
                        phrase_pair = PhrasePair.objects.get(
                            id=phrase_pair_data["id"], lesson=instance
                        )
                        was_previously_learned = phrase_pair.is_learned

                        phrase_pair.phrase_one = phrase_pair_data.get(
                            "phrase_one", phrase_pair.phrase_one
                        )
                        phrase_pair.phrase_two = phrase_pair_data.get(
                            "phrase_two", phrase_pair.phrase_two
                        )
                        phrase_pair.is_learned = phrase_pair_data.get(
                            "is_learned", phrase_pair.is_learned
                        )

                        phrase_pair.save()

                        if not was_previously_learned and phrase_pair.is_learned:
                            schedule_next_review(phrase_pair)

                        elif was_previously_learned and not phrase_pair.is_learned:
                            mark_incorrect(phrase_pair)
                    except PhrasePair.DoesNotExist:
                        PhrasePair.objects.create(lesson=instance, **phrase_pair_data)
                else:
                    PhrasePair.objects.create(lesson=instance, **phrase_pair_data)

        return instance


class SectionSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ["id", "title", "description", "color", "progress", "review_count", "lessons"]

    def get_progress(self, obj) -> float:
        return obj.calculate_progress()

    def get_review_count(self, obj) -> int:
        return obj.review_count()
