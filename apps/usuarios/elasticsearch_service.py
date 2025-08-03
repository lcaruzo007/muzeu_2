from elasticsearch import Elasticsearch
from django.conf import settings
from django.apps import apps
import json

class ElasticsearchService:
    def __init__(self):
        try:
            if hasattr(settings, 'ELASTICSEARCH_HOST') and settings.ELASTICSEARCH_HOST:
                self.es = Elasticsearch([settings.ELASTICSEARCH_HOST], request_timeout=10)
            else:
                self.es = None
        except Exception as e:
            print(f"Erro ao conectar com Elasticsearch: {e}")
            self.es = None
        self.index_name = 'muzeu_search'
    
    def is_available(self):
        try:
            if not self.es:
                return False
            return self.es.ping()
        except Exception as e:
            print(f"Elasticsearch não disponível: {e}")
            return False
    
    def create_index(self):
        if not self.is_available():
            return False
            
        mapping = {
            "mappings": {
                "properties": {
                    "title": {"type": "text", "analyzer": "portuguese"},
                    "description": {"type": "text", "analyzer": "portuguese"},
                    "content": {"type": "text", "analyzer": "portuguese"},
                    "category": {"type": "keyword"},
                    "type": {"type": "keyword"},
                    "tags": {"type": "keyword"},
                    "date_created": {"type": "date"},
                    "url": {"type": "keyword"},
                    "image_url": {"type": "keyword"}
                }
            }
        }
        
        try:
            self.es.indices.create(index=self.index_name, body=mapping, ignore=400)
            return True
        except:
            return False
    
    def index_item(self, obj_type, obj_id, title, description, content="", category="", tags=[], url="", image_url=""):
        if not self.is_available():
            return False
            
        doc = {
            "title": title,
            "description": description,
            "content": content,
            "category": category,
            "type": obj_type,
            "tags": tags,
            "date_created": getattr(obj_id, 'criado_em', None),
            "url": url,
            "image_url": image_url
        }
        
        try:
            self.es.index(index=self.index_name, id=f"{obj_type}_{obj_id}", body=doc)
            return True
        except:
            return False
    
    def search(self, query, filters=None, size=20, from_=0):
        if not self.is_available():
            return {"hits": {"total": {"value": 0}, "hits": []}}
            
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {
                            "multi_match": {
                                "query": query,
                                "fields": ["title^2", "description", "content"],
                                "type": "best_fields",
                                "fuzziness": "AUTO"
                            }
                        }
                    ]
                }
            },
            "highlight": {
                "fields": {
                    "title": {},
                    "description": {},
                    "content": {}
                }
            },
            "size": size,
            "from": from_
        }
        
        # Aplicar filtros
        if filters:
            filter_terms = []
            if filters.get('type'):
                filter_terms.append({"term": {"type": filters['type']}})
            if filters.get('category'):
                filter_terms.append({"term": {"category": filters['category']}})
            
            if filter_terms:
                search_body["query"]["bool"]["filter"] = filter_terms
        
        try:
            return self.es.search(index=self.index_name, body=search_body)
        except:
            return {"hits": {"total": {"value": 0}, "hits": []}}
    
    def delete_item(self, obj_type, obj_id):
        if not self.is_available():
            return False
            
        try:
            self.es.delete(index=self.index_name, id=f"{obj_type}_{obj_id}", ignore=404)
            return True
        except:
            return False

# Instância global
elasticsearch_service = ElasticsearchService()
