# Como Executar

## Instale as dependencias do projeto

```bash
pip install -r requirements.txt
```

## Realize as migrações da base de dados

```bash
python manage.py migrate
```

## Realize a carga dos dados nos XMLs

```bash
python manage.py extract
```

## Execute o servidor

```bash
python manage.py runserver 0.0.0.0:8000
```
