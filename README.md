# notifyhub
Proyecto Final 2
1. Ejecutar Docker Desktop.

2. Ejecutar visual studio code.
    Verificar que la consola se encuentre en la ruta del proyecto.

3. Construir y levantar los contenedores
    En la raíz del proyecto, ejecuta:
    docker compose up --build -d
    Esto hará lo siguiente:
    •	Crear 3 instancias del API (api1, api2, api3)
    •	Levantar RabbitMQ con panel de control
    •	Iniciar MySQL con la tabla logs
    •	Crear el worker que procesará los mensajes
    •	Levantar NGINX como balanceador en el puerto 8080

4. Verificar que todos los servicios estén activos
    docker compose ps
    Debes ver algo como esto:
 

5. Acceder al panel de RabbitMQ
    Abre en tu navegador:
    http://localhost:15672
    Usuario: rmq_user
    Password: rmq_pass
    Aquí verás las colas:
    •	q.email
    •	q.sms

6. Probar los endpoints del API (a través del balanceador NGINX)
    Enviar Email:
    Invoke-RestMethod -Uri "http://localhost:8080/api/v1/notifications/email" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"to":"test@example.com","subject":"Hola","body":"Prueba de correo"}'

    Generador sms
    Invoke-RestMethod -Uri "http://localhost:8080/api/v1/notifications/sms" `
    -Method POST `
    -ContentType "application/json" `
    -Body '{"number":"+50255555555", "text":"Prueba de sms"}'

    La respuesta esperada será:
    {
    "status": "accepted"
    }

7. Ver los registros en MySQL
    Acceder al contenedor:
    docker exec -it notifyhub-mysql-1 mysql -u nh_user -p
    Contraseña: nh_pass
    Consultar los registros procesados por el worker:
    USE notifyhub;
    SELECT * FROM logs;

8. Apagar el proyecto
    docker compose down