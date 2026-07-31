## Микросервис для обработки сообщений (RabbitMQ - PostgreSQL)
Сервис принимает сообщение из очереди и отправляет в базу данных.

### Примеры выполнения программы
#### 1. Получение и отправка сообщения

Отправляем сообщение:

![RabbitMQ](https://github.com/rlapgit/test-project/blob/main/photos/rabbitmq.png)

Обрабатываем и отправляем в бд:

![App](https://github.com/rlapgit/test-project/blob/main/photos/app.png)

Сообщение в бд:

![Adminer](https://github.com/rlapgit/test-project/blob/main/photos/adminer.png)

#### 2. Получение некорректного сообщения

![RabbitMQ](https://github.com/rlapgit/test-project/blob/main/photos/rabbitmq_incorrect.png)

![App](https://github.com/rlapgit/test-project/blob/main/photos/app_incorrect.png)

#### 3. Повторные попытки (например, бд упала)

![App](https://github.com/rlapgit/test-project/blob/main/photos/db_down.png)
