# Generate expiring token

- https://developers.facebook.com/apps/1155313532906262/whatsapp-business/wa-dev-console/?business_id=1591481458457121

- Paste it in `config.py`

# Build & run Dockerized environment

```bash
docker build -t whatsapp-bot .
docker run -it -v ${PWD}/:/app whatsapp-bot 
```
