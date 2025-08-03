from django.core.management.base import BaseCommand
from apps.acervo.models import ItemAcervo
from apps.usuarios.elasticsearch_service import elasticsearch_service
from django.urls import reverse

class Command(BaseCommand):
    help = 'Indexar todos os itens do acervo no Elasticsearch'

    def handle(self, *args, **options):
        if not elasticsearch_service.is_available():
            self.stdout.write(
                self.style.ERROR('Elasticsearch não está disponível!')
            )
            return

        # Criar índice
        elasticsearch_service.create_index()
        
        # Indexar todos os itens ativos
        itens = ItemAcervo.objects.filter(ativo=True).select_related('categoria')
        total = itens.count()
        
        self.stdout.write(f'Indexando {total} itens...')
        
        for i, item in enumerate(itens, 1):
            success = elasticsearch_service.index_item(
                obj_type='acervo',
                obj_id=item.id,
                title=item.titulo,
                description=item.descricao,
                content=f"{item.origem} {item.material} {item.observacoes}",
                category=item.categoria.nome,
                tags=[item.tipo_item, item.estado_conservacao],
                url=reverse('acervo:detalhe', args=[item.pk]),
                image_url=item.imagem.url if item.imagem else ""
            )
            
            if success:
                self.stdout.write(f'  {i}/{total} - {item.titulo}')
            else:
                self.stdout.write(
                    self.style.ERROR(f'  ERRO ao indexar: {item.titulo}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'Indexação concluída! {total} itens processados.')
        )
