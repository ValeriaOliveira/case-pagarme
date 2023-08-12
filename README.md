![](https://imgur.com/RIOFthI.png)

# Desafio Técnico Pagar.me

## 1. API

#### Passo 1: [Instalar Docker](https://docs.docker.com/get-docker/)

#### Passo 2: [Instalar Docker Compose](https://docs.docker.com/compose/install/)

#### Passo 3: Clonar o Repositório
```bash 
git clone https://github.com/ValeriaOliveira/case-pagarme.git && cd case-pagarme
```
#### Passo 4: Construir a imagem do docker
```bash 
docker-compose build
```

#### Passo 5: Subir o docker-compose.yml
```bash
docker-compose up -d
```

## 2. Raciocínio 

O arquivo generate.py roda em loop infinito criando arquivos CSVs dentro da pasta input_data, pelo que compreendi do case o objetivo era conseguir tratar os dados como se fossem de streaming.


### Solução (Visão Geral)

  Para desenvolver o raciocínio acima optei por orquestrar em docker-compose o arquivo da resolução do problema resolution.py em conjunto com o generate.py para ter dois processos rodando de forma que um não fique esperando o outro para executar, porém dentro de um container.<br><br>
  Uma vez executado o docker-compose as consultas são criadas em arquivos CSVs no diretório ./ que são atualizados em tempo real com sleep de 5 segundos, por escolha pessoal, apenas para dar tempo do generate.py gerar mais arquivos sendo este ponto irrelevante pro funcionamento e a diário, simulando a ideia de fazer a ingestão dos dados por tempo.<br><br>
  Mantenho um arquivo CSV só para o histórico dos dados onde adiciono todas as leituras na ordem de criação dos CSVs e uma para o banco de dados atualizado, utilizo esses arquivos de base para fazer as consultas com pandas.
  

### Solução (Tecnologia)


* **Pandas (Python)**: Escolhi pandas por ser mais simples e acessível para fazer as consultas.

* **Docker Compose**: Escolhi usar por querer adicionar mais tecnologia ao case.


### Possíveis Melhorias 

* Documentar tudo em português ou inglês
* Usar um crontab ao invês de desenvolver o arquivo em looping infinito
* Usar Beam ou Spark para manipulação dos dados
