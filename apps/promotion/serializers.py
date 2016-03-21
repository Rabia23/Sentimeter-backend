from rest_framework import serializers
from apps.promotion.models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('id', 'title', 'isActive', 'objectId', 'toggle_colors', 'color_selected', 'color_unselected',
                  'banner_image', 'background_image')
