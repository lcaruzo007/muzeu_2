from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from .models import ItemAcervo
from apps.usuarios.elasticsearch_service import elasticsearch_service

@receiver(post_save, sender=ItemAcervo)
def index_item_acervo(sender, instance, created, **kwargs):
    if instance.ativo:
        elasticsearch_service.index_item(
            obj_type='acervo',
            obj_id=instance.id,
            title=instance.titulo,
            description=instance.descricao,
            content=f"{instance.origem} {instance.material} {instance.observacoes}",
            category=instance.categoria.nome,
            tags=[instance.tipo_item, instance.estado_conservacao],
            url=reverse('acervo:detalhe', args=[instance.pk]),
            image_url=instance.imagem.url if instance.imagem else ""
        )

@receiver(post_delete, sender=ItemAcervo)
def delete_item_acervo_from_index(sender, instance, **kwargs):
    elasticsearch_service.delete_item('acervo', instance.id)
