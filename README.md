# Projeto Museu

Sistema de gerenciamento para museu desenvolvido em Django.

## 📋 Pré-requisitos

- Python 3.11+
- pip
- Git

## 🚀 Instalação e Configuração

1. **Clone o repositório:**
   ```bash
   git clone <url-do-repositorio>
   cd muzeu_2
   ```

2. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # ou
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas configurações
   ```

5. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

6. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Colete os arquivos estáticos (produção):**
   ```bash
   python manage.py collectstatic
   ```

8. **Execute o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

## 📁 Estrutura do Projeto

```
muzeu_2/
├── apps/                   # Apps customizados do projeto
├── config/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                  # Arquivos de upload
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/              # Templates HTML
│   └── base/
├── .env                    # Variáveis de ambiente
├── .env.example           # Exemplo de configuração
├── .gitignore             # Arquivos ignorados pelo Git
├── manage.py              # Comando principal do Django
└── requirements.txt       # Dependências do projeto
```

## 🛠️ Comandos Úteis

- **Criar nova aplicação:**
  ```bash
  python manage.py startapp nome_app apps/nome_app
  ```

- **Fazer migrações:**
  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- **Executar testes:**
  ```bash
  python manage.py test
  ```

- **Shell do Django:**
  ```bash
  python manage.py shell
  ```

## 📝 Configuração de Desenvolvimento

1. Certifique-se de que `DEBUG=True` no arquivo `.env`
2. Configure o banco de dados SQLite para desenvolvimento
3. Use `python manage.py runserver` para testar localmente

## 🚀 Deploy em Produção

1. Configure `DEBUG=False` no arquivo `.env`
2. Configure um banco de dados robusto (PostgreSQL/MySQL)
3. Configure servidor web (Nginx + Gunicorn)
4. Execute `python manage.py collectstatic`

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Contato

Seu Nome - seu-email@example.com

Link do Projeto: [https://github.com/usuario/muzeu_2](https://github.com/usuario/muzeu_2)
