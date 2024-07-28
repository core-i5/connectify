# post_service/documents.py

from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from .models import Discussion

discussion_index = Index('discussions')

discussion_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@registry.register_document
@discussion_index.document
class DiscussionDocument(Document):
    user = fields.ObjectField(properties={
        'id': fields.IntegerField(),
        'username': fields.TextField(),
    })

    class Index:
        name = 'discussions'

    class Django:
        model = Discussion
        fields = [
            'text',
            'created_on',
        ]
