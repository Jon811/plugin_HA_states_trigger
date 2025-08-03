import requests
import json
import os
import random

from vacore import VACore

modname = os.path.basename(__file__)[:-3]  # calculating modname


# функция на старте
def start(core: VACore):
    manifest = {
        "name": "Триггер состояний объектов Home Assistant",
        "version": "1.0",
        "default_options": {
            "hassio_url": "http://hassio.lan:8123/",
            "hassio_key": "",   # получить в /profile, "Долгосрочные токены доступа"
            "switches": {         # всё, чему можно установить state on и off
                "кухню": "light.kitchen",
                "люстру": "switch.living_room",
                "телевизор": "media_player.lg_webos_smart_tv"
            },
            "temperature": {
                "в зале": "sensor.living_room",
                "на балконе": "sensor.balcony"
            }
        },

        "commands": {
            "включи": HA_set_state_on,
            "выключи": HA_set_state_off,
            "какая температура": HA_say_temperature
        }
    }

    return manifest


def start_with_options(core: VACore, manifest: dict):
    print(manifest['commands'])
    return manifest

def HA_set_state_on(core: VACore, phrase: str=None):
    if phrase == None:
        phrase = core.get_last_phrase()
    if phrase == "":
        core.play_voice_assistant_speech("Не могу понять, что нужно сделать")
        return
    options = core.plugin_options(modname)
    plugin_commands = core.plugin_manifest(modname)['commands']
    if options["hassio_url"] == "" or options["hassio_key"] == "":
        core.play_voice_assistant_speech("Нужен ключ или ссылка для Хоум Ассистента")
        return

    try:
        headers = {
            "Authorization": f"Bearer " + options["hassio_key"],
            "content-type": "application/json",
        }
        matched_event = False
        for com, entity in options["switches"].items():
            if phrase == com:
                data = {"entity_id": entity}
                domain= entity.split('.')[0]
                response = requests.post(options["hassio_url"] + 'api/services/' + domain + '/turn_on', headers=headers, json=data)
                print(response.text)
                reply = f"включено"
                core.play_voice_assistant_speech(reply)
                matched_event = True
                break
        if not matched_event:
            core.play_voice_assistant_speech("Не шмогла")
            print('Не могу найти нужный объект')

    except:
        import traceback
        traceback.print_exc()
        reply = "Не получилось"
        core.play_voice_assistant_speech(reply)
        print(reply)
    return

def HA_set_state_off(core: VACore, phrase: str=None):
    if phrase == None:
        phrase = core.get_last_phrase()
    if phrase == "":
        core.play_voice_assistant_speech("Не могу понять, что нужно сделать")
        return
    options = core.plugin_options(modname)
    plugin_commands = core.plugin_manifest(modname)['commands']
    if options["hassio_url"] == "" or options["hassio_key"] == "":
        core.play_voice_assistant_speech("Нужен ключ или ссылка для Хоум Ассистента")
        return
    try:
        headers = {
            "Authorization": f"Bearer " + options["hassio_key"],
            "content-type": "application/json",
        }
        matched_event = False
        for com, entity in options["switches"].items():
            if phrase == com:
                data = {"entity_id": entity}
                domain= entity.split('.')[0]
                response = requests.post(options["hassio_url"] + 'api/services/' + domain + '/turn_off', headers=headers, json=data)
                print(response.text)
                reply = f"выключено"
                core.play_voice_assistant_speech(reply)
                matched_event = True
                break
        if not matched_event:
            core.play_voice_assistant_speech("Не шмогла")
            print('Не могу найти нужный объект')

    except:
        import traceback
        traceback.print_exc()
        reply = "Не получилось"
        core.play_voice_assistant_speech(reply)
        print(reply)
    return


def HA_say_temperature(core: VACore, phrase: str):
    
    options = core.plugin_options(modname)
    plugin_commands = core.plugin_manifest(modname)['commands']

    if options["hassio_url"] == "" or options["hassio_key"] == "":
        core.play_voice_assistant_speech("Нужен ключ или ссылка для Хоум Ассистента")
        return

    try:
        headers = {
            "Authorization": f"Bearer " + options["hassio_key"],
            "content-type": "application/json",
        }
        matched_event = False
        for com, entity in options["temperature"].items():
            if phrase == com:
                response = requests.get(options["hassio_url"] + 'api/states/' + entity, headers=headers).json()
                print(response)
                temperature = round(float(response['state']), 0)
                reply = f"Температура {com} {temperature} градусов"
                core.play_voice_assistant_speech(reply)
    except:
        import traceback
        traceback.print_exc()
        reply = "Не получилось"
        core.play_voice_assistant_speech(reply)
        print(reply)
    return
