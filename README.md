# notifyhub
Proyecto Final 2

Construir y levantar los contenedores
En la raíz del proyecto, ejecuta:
docker compose up --build -d
Esto hará lo siguiente:
•	Crear 3 instancias del API (api1, api2, api3)
•	Levantar RabbitMQ con panel de control
•	Iniciar MySQL con la tabla logs
•	Crear el worker que procesará los mensajes
•	Levantar NGINX como balanceador en el puerto 8080

