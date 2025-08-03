# plugin_HA_states_trigger
Плагин переключения состояния объектов для Ирины. Должен быть включен REST API в Home Assistant.
За основу взят https://github.com/Ivan-Firefly/Irene-Voice-Assistant-Docker/blob/master/docker_plugins/plugin_HA_automation_trigger.py
Но теперь не нужно создавать автоматизации для управления объектами.
Для запуска сначала копируем файл в папку plugins, запускаем Ирину.
Затем необходимо получить долговременный токен в hassip:port/profile/security, внести его и адрес:порт в options/plugin_HA_states_trigger.json
Там уже будут примеры для пар слово : объект в секции switches.
Слово - это то, что говорится после "включи" и "выключи". То есть говорим "Ирина включи люстру", значит пишем "люстру". Объект - entity_id из Home Assistant
Также можно запрашивать температуру через "Ирина какая температура .....". Пары прописаны соответственно в temperature.
