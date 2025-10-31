# Integración de BaseStation + ESL

## Fase 1 - Conexión de BaseStation y ESLs vía MQTT

Se usa mosquitto 1.6.9 como broker (recomendado en la documentación).
Dentro del **ESLStationManageTool.exe** se configuraron los siguientes campos:
- `api version`: 2.2.2
- `MQTT Server`: tcp://192.168.0.8:1883
- `MQTT Client ID`: BASESTATION
- `MQTT Username`: user0001
- `MQTT Password`: test0001
- `MQTT topic prefixs`: `{
    "TOPIC_REFRESH_LIST":"test/refresh/queue",
    "TOPIC_NOTIFY":"test/refresh/notify",
    "TOPIC_CONFIG":"test/device/config",
    "TOPIC_DEVICE_PROPERTY":"test/device/property"
}`
- `enable device search`: `1`

Conviene exportar la configuración. Luego hay que hacer un **Update** y reiniciar el BS.

### Iniciar broker

```bash
docker compose up --build
```

Registrar un nuevo usuario:

```bash
docker compose exec mqtt mosquitto_passwd -c /mosquitto/config/passwordfile user0001
```

Escuchar en los topicos:

```bash
docker compose exec mqtt mosquitto_sub -t "test/device/property" -u "user0001" -P "test0001" -v

docker compose exec mqtt mosquitto_sub -t "test/device/config" -u "user0001" -P "test0001" -v

docker compose exec mqtt mosquitto_sub -t "test/refresh/notify" -u "user0001" -P "test0001" -v

docker compose exec mqtt mosquitto_sub -t "test/refresh/queue" -u "user0001" -P "test0001" -v
```

Buscar etiquetas:

```bash
docker compose exec mqtt mosquitto_pub -t "test/device/config" -u "user0001" -P "test0001" -m '{"queueId":2001,"action":2,"deviceType":2,"content":{"enable_device_searching":true,"device_searching_id":123456,"device_searching_channel":0,"device_searching_limit":300,"device_searching_triggered_time":0,"is_esl_device_searching_triggered":true}}'
```

Consultar batería de una etiqueta:

```bash
docker compose exec mqtt mosquitto_pub -t "test/device/config" -u "user0001" -P "test0001" -m '{"queueId":3003,"action":1,"deviceType":1,"deviceMac":"0012383B268CE5B0","content":["online","power"]}'
```