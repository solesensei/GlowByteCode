# RemotePIP
Скрипт предназначен для отправки `.whl` пакетов скачанных с помощью `pip` на удаленный сервер, через GBC

Необходим, когда на удаленном сервере невозможно воспользоваться командой `pip install` из-за строгого брандмауэра.


## Требования
- Требуется Python3 одной версии локальном и удаленном ПК
- **UNIX** или **WSL**
- **[GlowDrop](../GlowDrop)** - средство для отправки файлов через GBC

## Использование
```bash
./pip_remote %pip_package_name%
# %pip_package_name% - just name of package that you use for pip install
```