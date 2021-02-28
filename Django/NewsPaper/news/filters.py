from django_filters import FilterSet,DateFilter,CharFilter
from .models import Post,Author

class PostFilter(FilterSet):
    insertdt = DateFilter( field_name='insertdt',lookup_expr=('gt'),label='Позже',)
    caption = CharFilter( field_name='caption', lookup_expr='icontain', label='Заголовок')

    class Meta:
        model = Post
        fields = {'author_id':['exact'],}
