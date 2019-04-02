# DEV Manage

**Bash**-скрипты написанные для dev-серверов **RTDM** Росбанка, предназначенные для быстрой одновременной отправки команд (перезагрузка, остановка, статус, запуск) следующим серверам:

- SAS Servers
- Active MQ
- Mule
- FED Servers

## Использование

Для пользователя **sas** на серверах созданы **alias**: `dev` и `fed`

```bash
$: dev [system] [action]
```

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
$: fed [stop|start|status|restart]
# Управление fed серверами
```

## Alias

### DEV Middle

```bash
# User specific aliases and functions
alias dev="/home/sas/DEV_MANAGE/dev_manage.sh"
alias to-test="cd /sas/test"
alias to-mule="cd /sas/mule-standalone"
alias to-pack="cd /sas/package"
alias log-mule="bash /home/sas/DEV_MANAGE/mule"
alias log-mq="bash /home/sas/DEV_MANAGE/mq"
alias log-sas="bash /home/sas/DEV_MANAGE/sas"
```

### DEV Compute

```bash
# User specific aliases and functions
alias fed="/home/sas/DEV_MANAGE/dfs_manage.sh"
```

## Logs usage

### ActiveMQ

```bash
$: log-mq head log
----------------------- INFO -----------------------
Look ActiveMQ Logs v1.0
----------------------------------------------------
Usage ./mq [cmd] log [cmd]
cmd       - commands before or after log file
log       - ActiveMQ log file
----------------------------------------------------
```

### Mule

```bash
$: log-mule out
----------------------- INFO -----------------------
Look Mule Logs v1.0
----------------------------------------------------
Usage ./mule [cmd] out|disp [cmd]
out       - look backward RSBOuterServices log
disp      - look backward RSBDispatcher log
cmd       - commands before or after log file
----------------------------------------------------
```