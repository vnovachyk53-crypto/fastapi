-- Запустіть цей файл у MySQL під користувачем, який має право CREATE DATABASE.
CREATE DATABASE IF NOT EXISTS workout_tracker
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- Облікові дані застосунку задаються у файлі .env.
-- За потреби створіть окремого користувача MySQL вручну та надайте йому
-- права SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX на workout_tracker.*.
