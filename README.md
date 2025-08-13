# 🎮 Игра про шарики - Смешивание цветов

Интерактивная игра, где вы можете управлять шариками, смешивать их цвета и экспериментировать с физикой!

## 🎯 Особенности игры

- **Анимированные шарики** с реалистичной физикой
- **Математическое смешивание цветов** по RGB-модели
- **Интерактивное управление** мышью
- **Система инвентаря** для хранения шариков
- **Зона удаления** для очистки инвентаря

## 🎮 Управление

- **ЛКМ (зажать и тянуть)** - всасывать шарики в инвентарь
- **ПКМ** - выплёвывать шарики из инвентаря обратно в игру
- **Перетащить в красную зону** - удалить шарик из инвентаря

## 🎨 Механика смешивания цветов

При касании шарики смешивают свои цвета по математическим принципам RGB:
- **Красный + Синий** = Фиолетовый `(127, 0, 127)`
- **Красный + Зелёный** = Жёлто-коричневый `(127, 127, 0)`
- **Зелёный + Синий** = Бирюзовый `(0, 127, 127)`

## 🚀 Запуск игры

### Обычный запуск

```bash
# Установка зависимостей
pip3 install pygame

# Запуск игры
python3 gui.py
```

### 🐳 Запуск из Docker

#### Быстрый запуск

1. **Сборка образа**:
   ```bash
   docker build -t ball-game .
   ```

2. **Запуск игры**:
   ```bash
   docker run -it --rm \
     -e DISPLAY=$DISPLAY \
     -v /tmp/.X11-unix:/tmp/.X11-unix \
     ball-game
   ```

#### Подробная инструкция по Docker

**Для macOS**:
```bash
# Установите XQuartz (если не установлен)
brew install --cask xquartz

# Запустите XQuartz
open -a XQuartz

# Разрешите подключения в XQuartz → Preferences → Security
# Отметьте "Allow connections from network clients"

# Соберите и запустите
docker build -t ball-game .
docker run -it --rm -e DISPLAY=host.docker.internal:0 ball-game
```

**Для Linux**:
```bash
# Разрешите X11 подключения
xhost +local:docker

# Соберите и запустите
docker build -t ball-game .
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ball-game
```

**Для Windows**:
```bash
# Установите VcXsrv с https://sourceforge.net/projects/vcxsrv/
# Запустите XLaunch и отметьте "Disable access control"

# Соберите и запустите
docker build -t ball-game .
docker run -it --rm -e DISPLAY=host.docker.internal:0.0 ball-game
```

## 📁 Структура проекта

- `gui.py` - основной файл игры с графическим интерфейсом
- `logic.py` - игровая логика (физика, смешивание цветов)
- `settings.py` - настройки игры
- `requirements.txt` - зависимости Python
- `Dockerfile` - конфигурация Docker
- `README.md` - документация

## 🛠️ Технические детали

- **Python 3.7+**
- **Pygame** для графики
- **Dataclasses** для структуры данных
- **Математическое смешивание RGB** цветов

## 🎯 Цель игры

Экспериментируйте с цветами! Создавайте новые оттенки, смешивая шарики разных цветов. Попробуйте создать все возможные комбинации!

## 🔧 Настройка

Отредактируйте `settings.py` для изменения:
- Размера окна
- Количества стартовых шариков
- Физических параметров
- Визуальных эффектов

## 🛠️ Устранение проблем

### Docker ошибки

**Ошибка "Cannot connect to X server"**:

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

**Игра не запускается**:
```bash
# Проверьте, что все файлы на месте
ls -la
# Должны быть: gui.py, logic.py, settings.py, requirements.txt, Dockerfile

# Пересоберите образ при изменении кода
docker build --no-cache -t ball-game .
```

---

**Приятной игры!** 🎨✨
