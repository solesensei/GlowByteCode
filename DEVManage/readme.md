# DEV Manage
**Bash**-скрипты написанные для dev-серверов **RTDM** Росбанка, предназначенные для быстрой одновременной отправки команд (перезагрузка, остановка, статус, запуск) следующим серверам:
- SAS Servers
- Active MQ
- Mule
- FED Servers

## Использование
```bash
# ---------------------------------------------------------- #
Usage: ./DEV_MANAGE/dev_manage.sh [system] [action]
# ---------------------------------------------------------- #
$: ./DEV_MANAGE/dev_manage.sh mule restart 
# Перезагрузка mule
$: ./DEV_MANAGE/dev_manage.sh mq stop
# Остановка ActiveMQ
$: ./DEV_MANAGE/dev_manage.sh sas status
# Статус SAS Servers
$: ./DEV_MANAGE/dev_manage.sh fed stop
# Запуск Fed Servers
$: ./DEV_MANAGE/dev_manage.sh [dev] restart
# Перезагрузка всех серверов на DEV
# ---------------------------------------------------------- #
Usage: ./DEV_MANAGE/dfs_manage.sh [stop|start|status|restart]
# ---------------------------------------------------------- #
# Управление fed серверами
```
