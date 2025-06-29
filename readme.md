# Pyro

Для запуска проекта необходимо установить [Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)
```
pip install pyenv-win --target %USERPROFILE%\\.pyenv
```

Установка [для Windows](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#installation):

Выполнить в терминале powershell команду для скачивания программы и её регистрации в Windows:
```PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
При возникновении ошибки прав доступа запустить PowerShell от имени администратора и выполнить команду, после чего повторить попытку установки:
```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
```
Может понадобиться обновить список доступных версий Python командой
```
pyenv update
```

В проекте используется версия Python 3.12.10, для установки выполнить в терминале команду
```
pyenv install 3.12.10
```
Задаем локальную версию Python 3.12.10 в папке проекта для синхронизации версии Python на разных машинах
```
pyenv local 3.12.10
```

Для управления версиями установленных библиотек необходимо установить [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
Выполнить в терминале PowerShell команды для скачивания программы и её регистрации в Windows:
```PowerShell
# скачивание
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
# регистрация в PATH windows
[System.Environment]::SetEnvironmentVariable("PATH", [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User) + ";$env:APPDATA\Python\Scripts", [System.EnvironmentVariableTarget]::User)
```

перезапустить PowerShell, проверить правильность установки:
```
poetry --version
```

Запустить локальный сервер для разработки:
```sh
poetry run python src/manage.py runserver
```