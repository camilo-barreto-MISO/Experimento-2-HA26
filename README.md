# Experimento-2-HA26

Para correr el experimento siga los siguientes pasos:
1. Clone el repositorio en su máquina local
2. Teniendo docker desktop instalado y corriendo, digite en la raíz del proyecto: `docker compose up`
3. Cuando termine de subir los contenedores, abra postman y cargue la colección: [Experimento-2-HA26-setup.postman_collection.json](https://github.com/camilo-barreto-MISO/Experimento-2-HA26/blob/main/Experimento-2-HA26-setup.postman_collection.json)
4. Las peticiones de la carpeta usuarios (Crear usuarios y autententicar), las puede usar para crear usuarios diferentes a los que tenemos cargados en nuestros ejemplos y verificar que la lógica funciona con cualquier nuevo usuario.
5. Las peticiones de la carpeta deportistas son los servicios que están protegidos para dentro de nuestros microservicios, como se explica a continuación:
   - El servicio *obtener-eventos* puede ser consumido tanto por los usuarios básicos como premium
   - El servicio *agendar-entrenamientos* solo está disponible para los ususarios premium, por lo tanto la respuesta del consumo del usuario básico responde 403 forbidden
  
La base de datos viene precargada con 2 usuarios:
1. **BÁSICO** usuario: **runfast** | contraseña: **1234**
2. **PREMIUM** usuario: **sportacus** | contraseña: **5678**
