# Controle Financeiro (Django)

Aplicação web em Django para controle financeiro pessoal: cadastro de categorias e transações (entradas e saídas), com dashboard que exibe saldo total, saldo do mês e resumo por categoria.

## O que o projeto faz

- **Categorias**: cadastro de categorias de movimentação (Entrada ou Saída).
- **Transações**: registro de transações com descrição, valor, data, tipo (Entrada/Saída) e categoria.
- **Dashboard** (`/dashboard/`): página que mostra:
  - **Saldo total**: soma de todas as entradas menos todas as saídas.
  - **Saldo do mês**: mesmo cálculo apenas para o mês atual.
  - **Por categoria**: total por categoria no mês atual (entradas positivas, saídas negativas).

Os cálculos são feitos no serviço `financeiro_service` (saldo total, saldo mensal e saldo por categoria) e reutilizam um `TransacaoQuerySet` customizado no app `core` para agregações.

### Regras de validação (Transação)

- **Valor**: sempre positivo (constraint no banco `valor_positivo`: `valor > 0`).
- **Tipo**: apenas `'E'` (Entrada) ou `'S'` (Saída) (constraint no banco `tipo_valido`).
- **Tipo vs categoria**: o tipo da transação deve ser igual ao tipo da categoria (validado em `clean()`).
- **Data**: não pode ser futura (validado em `clean()`).
- O método `save()` chama `full_clean()` para garantir que essas regras sejam aplicadas ao salvar (incluindo pelo admin).

### Migrações

A migração `0002` adiciona as constraints `valor_positivo` e `tipo_valido`. Antes de criá-las, um passo de dados (`corrigir_dados_invalidos`) ajusta registros já existentes: transações com valor ≤ 0 têm o valor corrigido; transações com tipo fora de `['E','S']` passam a ter tipo `'E'`, para que a migração não falhe por dados antigos.

## Tecnologias

- **Django** 6.x
- **PostgreSQL** (driver `psycopg2-binary`)
- **python-dotenv** para variáveis de ambiente (ex.: `.env` na raiz)

## Estrutura principal

```
financeiro/
├── manage.py
├── financeiro/          # projeto Django (settings, urls raiz)
└── core/                 # app principal
    ├── models.py         # Categoria, Transacao (constraints e clean/save)
    ├── managers.py       # TransacaoQuerySet (saldo, do_mes)
    ├── migrations/       # 0001_initial, 0002 constraints + correção de dados
    ├── services/
    │   └── financeiro_service.py   # saldo_total, saldo_mensal, saldo_por_categoria
    ├── views/
    │   └── dashboard.py  # view do dashboard
    └── urls.py           # rota /dashboard/
```

## Como rodar

1. **Ambiente virtual e dependências** (na raiz do repositório):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Variáveis de ambiente**: crie um arquivo `.env` na raiz (mesmo nível de `financeiro/`) com as configurações do banco, por exemplo:

   ```
   DB_NAME=seu_banco
   DB_USER=usuario
   DB_PASSWORD=senha
   DB_HOST=localhost
   DB_PORT=5432
   ```

   Ajuste em `financeiro/settings.py` para usar essas variáveis em `DATABASES` se ainda não estiver configurado.

3. **Migrações e servidor** (dentro da pasta `financeiro`):

   ```bash
   cd financeiro
   python manage.py migrate
   python manage.py runserver
   ```

4. Acesse:
   - **Dashboard**: http://127.0.0.1:8000/dashboard/
   - **Admin** (categorias e transações): http://127.0.0.1:8000/admin/ (crie um superusuário com `python manage.py createsuperuser` se necessário).

## Resumo

Este projeto é um **controle financeiro** em Django: gerencia **categorias** e **transações** com validações e constraints no modelo (valor positivo, tipo válido, tipo igual ao da categoria, data não futura), e oferece um **dashboard** com saldo total, saldo do mês e totais por categoria no mês atual.
