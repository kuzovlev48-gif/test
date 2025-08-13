# 🐳 Запуск игры из Docker

Эта инструкция поможет вам запустить игру "Смешивание цветов" в Docker контейнере.

## 📋 Предварительные требования

Убедитесь, что у вас установлен Docker:
- **macOS**: [Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: `sudo apt-get install docker.io` (Ubuntu/Debian)
- **Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop)

## 🚀 Быстрый запуск

### 1. Сборка Docker образа

Откройте терминал в папке с игрой и выполните:

```bash
docker build -t ball-game .
```

Эта команда создаст Docker образ с именем `ball-game`.

### 2. Запуск игры

```bash
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ball-game
```

## 🔧 Подробная инструкция

### Для macOS

1. **Установите XQuartz** (если не установлен):
   ```bash
   brew install --cask xquartz
   ```

2. **Запустите XQuartz**:
   ```bash
   open -a XQuartz
   ```

3. **Разрешите подключения** в XQuartz:
   - Перейдите в XQuartz → Preferences → Security
   - Отметьте "Allow connections from network clients"

4. **Соберите образ**:
   ```bash
   docker build -t ball-game .
   ```

5. **Запустите игру**:
   ```bash
   docker run -it --rm \
     -e DISPLAY=host.docker.internal:0 \
     ball-game
   ```

### Для Linux

1. **Разрешите X11 подключения**:
   ```bash
   xhost +local:docker
   ```

2. **Соберите образ**:
   ```bash
   docker build -t ball-game .
   ```

3. **Запустите игру**:
   ```bash
   docker run -it --rm \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     ball-game
   ```

### Для Windows

1. **Установите VcXsrv** (X11 сервер):
   - Скачайте с [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/)
   - Установите и запустите XLaunch
   - В настройках отметьте "Disable access control"

2. **Соберите образ**:
   ```bash
   docker build -t ball-game .
   ```

3. **Запустите игру**:
   ```bash
   docker run -it --rm \
     -e DISPLAY=host.docker.internal:0.0 \
     ball-game
   ```

## 🎮 Управление игрой

После запуска вы увидите окно игры с шариками:

- **ЛКМ (зажать и тянуть)** - всасывать шарики в инвентарь
- **ПКМ** - выплёвывать шарики из инвентаря обратно в игру
- **Перетащить в красную зону** - удалить шарик из инвентаря

## 🛠️ Устранение проблем

### Ошибка "Cannot connect to X server"

**macOS**:
```bash
# Перезапустите XQuartz и попробуйте снова
open -a XQuartz
docker run -it --rm -e DISPLAY=host.docker.internal:0 ball-game
```

**Linux**:
```bash
# Разрешите подключения к X11
xhost +local:docker
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix ball-game
```

### Игра не запускается

Проверьте, что все файлы на месте:
```bash
ls -la
# Должны быть: gui.py, logic.py, settings.py, requirements.txt, Dockerfile
```

### Пересборка образа

Если вы изменили код, пересоберите образ:
```bash
docker build --no-cache -t ball-game .
```

## 🐳 Docker команды

### Просмотр образов
```bash
docker images
```

### Удаление образа
```bash
docker rmi ball-game
```

### Запуск в фоновом режиме
```bash
docker run -d --name ball-game-container ball-game
```

### Остановка контейнера
```bash
docker stop ball-game-container
docker rm ball-game-container
```

## 📝 Структура Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "gui.py"]
```

## 🎯 Готово!

Теперь вы можете запускать игру в изолированной среде Docker. Это гарантирует, что игра будет работать одинаково на любой системе с установленным Docker.

**Приятной игры!** 🎨✨
