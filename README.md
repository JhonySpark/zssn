# Sobre o projeto

O teste foi desenvolvido utilizando a linguagem Python com framework Flask API, testes com Pytest e banco de dados MySQl. 
A estrutura do projeto é simples, poderia ter utilizado uma arquitetura mais robusta com DTO mas por questão de tempo, decidi fazer na estrutura simples funcional, para tornar o build da aplicação mais prático utlizei containerização com docker utilizando docker-composer para criar os containers de forma mais prática. 

O banco de dados foi feito um dump da base essencial e durante o processo de build do docker, eu subo o dump para o container criando toda estrutura de tabelas e dados essenciais como os items.

(Bonus)
Foi criado um exemplo de um possível front-end do projeto, que poderia ficar bem legal consumindo a api, mas 
por questão de tempo não foi possível realizar estas possíbilidades.

## Como rodar o projeto
1 - Através do docker-compose para instanciar os containers do front, backend e mysql. 
> `$ docker-compose up -d --build` 

2 - Executar o projeto em modo de dev`
> Após o docker compose desligue o container do app no docker
> `$ docker stop zssn_app` 

> Executar api em modo dev
`Flask run` 

> Executando testes
`$ pytest`  ( simple like that! :D )

## REST API
Lista dos endpoints disponíveis na API com exemplo de payloads. 
Também foi criado um arquivo **api_request.http** na raiz do projeto que pode ser utilizado juntamente com o 
pluguin **REST Client** do vs code para fazer os testes dos endpoints de forma mais prática.


## Endpoints

##### `POST /add_user`

content-type: application/json

`Dados do sobrevivente com os items iniciais`

    {
    "name": "John Doe",
    "age": "25",
    "gender": "M",
    "latitude": "40.7128",
    "longitude": "-74.0060",
    "items": 
        [{
            "id": 1,
            "amount": 0
        },{
            "id": 2,
            "amount": 0
        },{
            "id": 3,
            "amount": 0
        },{
            "id": 4,
            "amount": 0
        }]
    }


##### `PUT /update_user_location/:survivor_id`

content-type: application/json

`Coordenadas de geolocalização`

`( inclusive a estrutura da localização está em formato Point com indexação geoespacial)`

    {
        "latitude": "-19.922400",
        "longitude": "-43.947120"
    }



##### `PUT /report_infected/:survivor_id`

content-type: application/json

`Payload não é necessário`



##### `PUT /update_user_inventory/:survivor_id`

content-type: application/json

`Id do item e quantidade`
    
    {
        "id": 2,
        "amount": 1
    }



##### `POST /trade`

content-type: application/json

`Id do sobrevivente, id do item e quantidade`
    
    {
        "survivor1_id": 22,
        "survivor1_item":{
            "id": 4,
            "amount": 3
        },
        "survivor2_id": 23,
        "survivor2_item":{
            "id": 2,
            "amount": 1
        }
    }   
    
##### `GET /report`

content-type: application/json

`Payload não é necessário`
