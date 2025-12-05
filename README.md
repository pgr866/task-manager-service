# Practica8-ITSI

## Trabajo Guiado

```powershell
docker run -it --rm --name n8n -p 5678:5678 -v n8n:/home/node/.n8n -e N8N_USER_ENV_VARS=true -e SHEET_ID_CHISTES="1Was0oMuPtx8V5PZ5oUMRCwfIt5idw9GvX2Pi7wpSt9U" -e SHEET_NAME_PROG="Programming" -e SHEET_NAME_MISC="Misc" -e SHEET_NAME_DARK="Dark" n8nio/n8n
```

```bash
# Instala ultima version de Node
curl -o- https://fnm.vercel.app/install | bash
source ~/.bashrc
fnm install 24
node -v
npm -v
```

```bash
npm install n8n-cli -g
```

- Generar Clave de API en n8n (Settings > n8n API).

```bash
export N8N_HOST="http://localhost:5678"
export N8N_API_KEY="<PEGUE_SU_CLAVE_DE_API_AQUÍ>"
```

- Eliminar flujo de trabajo refactorizado.

```bash
n8n-cli workflows import workflows/workflow.json --skip-validation
```

## Ejercicio 1

- Crear credenciales de PostgreSQL y RabbitMQ mediante expresiones {{ $env.DB_HOST }}...

```powershell
docker run -it --rm --name n8n -p 5678:5678 -v n8n:/home/node/.n8n -e N8N_USER_ENV_VARS=true -e DB_HOST="db" -e DB_NAME="taskdb" -e DB_USER="user" -e DB_PASS="password" -e MQ_HOST="mq" -e MQ_USER="guest" -e MQ_PASS="guest" n8nio/n8n
```

- Disparar Webhook con siguiente curl:
```powershell
curl -X POST -H "Content-Type: application/json" -d '{"title": "Tarea enviada por webhook n8n", "description": "A cola RabbitMQ"}' http://localhost:5678/webhook-test/5aab41db-6d3e-4b06-83f7-6c46367acac4
```

## Ejercicio 2

- Incorporar contenedor de n8n en [docker-compose.yml](docker-compose.yml).

- Copiar [.env.example](.env.example) en .env.

- Iniciar proyecto completo con:
```powershell
docker-compose up -d
```

## Ejercicio 3

- Configurado despliegue automático con GitHub Actions en [.github/workflows/deploy.yml](.github/workflows/deploy.yml).

```powershell
ngrok http 5678
```
