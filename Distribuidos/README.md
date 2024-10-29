
## 🦁🔎 Microservicios - NestJS x ElasticSearch x Kafka

Breve proyecto para demostrar el uso de ElasticSearch y Kafka junto a NestJS. Tiene como propósito acercar a los estudiantes a la indexación de documentos, junto a su posterior análisis a través de Kibana utilizando microservicios comunicados a través de Kafka.

### Vídeo tutorial

<a href = 'https://www.youtube.com/watch?v=jwIzxIU8_aE'
target='_blank'>
<img src='https://img.shields.io/badge/Video-0F0F0F?style=for-the-badge&logo=youtube&logoColor=%23FF0000'>
</a>


### Cómo correr el proyecto

Clona el repositorio

```bash
git clone https://github.com/cesarmunozr/SD-2024-2.git
```

Utiliza la branch de kafka-microservices
```
git checkout kafka-microservices
```

Instala las dependencias
```
npm i 
```

Inicia los contenedores
```
docker compose up
```

Inicia el el microservicio rest
```
npm run start rest
```

Inicia el el microservicio elastic
```
npm run start elastic
```

Eso es todo, happy coding. ✨ 

