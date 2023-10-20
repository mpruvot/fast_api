# FastAPI
Créer une application avec FastApi et Pydantic.

L'objectif sera de faire une application comme user_management.
Les user defront etre represente par un modele Pydantic contenant:
- nom
- type (admin/visitor)
- un uuid4 généré automatiquement a la creation d'un user (see https://docs.python.org/3/library/uuid.html)


L'application aura une route:


`GET /users/` qui retournera tous les users.

Elle pourra prendre un query params type "admin" ou "visitor" pour filtrer la reponse:
`GET /users/?type=admin`


On pourra recuperer un user specifique en faisant
`GET /users/{user_uuid}/`

On pourra créer un user en faisant un
`POST /users/`
qui prendra en body un nom et un type et retournera l'uuid du user créé.

Les codes de retours HTTP devront etre coherent !!

Pas de stockage en db, utilise un json ou juste sotcké en RAM !