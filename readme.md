# Pyro

## Для запуска проекта необходимо установить [Pyenv](https://github.com/pyenv/pyenv?tab=readme-ov-file#installation)

### Установка для Linux
```sh
# Обновить систему: sudo apt update, upgrade...
# Установить пакеты для сборки https://stackoverflow.com/a/74314165
# Перезагрузиться
# Скачать и установить pyenv командой
curl -fsSL https://pyenv.run | bash
# Зарегистрировать pyenv в bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
source ~/.bashrc
# Проверить установку. Может понадобиться перезапуск консоли или перезагрузка
pyenv --version
# Для сборки исполняемых файлов версий Python необхоимо установить пакеты
sudo apt install build-essential curl libbz2-dev libffi-dev liblzma-dev libncursesw5-dev libreadline-dev libsqlite3-dev libssl-dev libxml2-dev libxmlsec1-dev llvm make tk-dev wget xz-utils zlib1g-dev
```

### Установка [для Windows](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#installation):

Выполнить в терминале powershell команду для скачивания программы и её регистрации в Windows:
```PowerShell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1"
```
При возникновении ошибки прав доступа запустить PowerShell от имени администратора и выполнить команду, после чего повторить попытку установки:
```PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine

# Добавление PYENV, PYENV_HOME и PYENV_ROOT в ваши переменные среды

[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_ROOT',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

[System.Environment]::SetEnvironmentVariable('PYENV_HOME',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")

# Теперь добавьте следующие пути к вашей переменной ПАТХ ПОЛЬЗОВАТЕЛЬСКОГО, чтобы получить доступ к команде pyenv

[System.Environment]::SetEnvironmentVariable('path', $env:USERPROFILE + "\.pyenv\pyenv-win\bin;" + $env:USERPROFILE + "\.pyenv\pyenv-win\shims;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```
### Использование

```sh
# В проекте используется версия Python 3.12.10, для установки выполнить команду
pyenv install 3.12.10
# Если версия не найдена, обновить список доступных версий Python командой
pyenv update
```

## Для управления версиями установленных библиотек использутся [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

### Установка для Windowss
Выполнить в терминале PowerShell команды для скачивания программы и её регистрации в Windows:
```PowerShell
# скачивание
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
# регистрация в PATH windows
[System.Environment]::SetEnvironmentVariable("PATH", [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::User) + ";$env:APPDATA\Python\Scripts", [System.EnvironmentVariableTarget]::User)
# перезапустить PowerShell, проверить правильность установки:
poetry --version
```

### Установка для Linux
```sh
curl -sSL https://install.python-poetry.org | python -
```
## Настройка окружения
В корне проекта создать файл .env, скопировать в него содержимое файла .env.example и заполнить его.

## Работа с проектом

```sh
# установка зависимостей
poetry install
# подготовка локальной базы данных
poetry run python src/manage.py migrate
# добавление суперпользователя
poetry run python src/manage.py createsuperuser
# запуск сервера для локальной разработки
poetry run python src/manage.py runserver
```
После запуска в [панели администратора](http://localhost:8000/admin)
добавить несколько участков и камер.
