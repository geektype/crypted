from django.shortcuts import render
from .forms import EncryptForm
from django.http import HttpResponse
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


def encryptData(pub_key, data):
    """
        Function that encrypts data using key and returns HTTP download response

        Parameters:
        pub_key : request.FILE
        data : string

        return:
        HttpResponse
    """
    data = data.encode("utf-8")
    filename = "encrypted.bin"
    # content = []
    # for chunk in pub_key.chunks():
    #     content.append(chunk)
    public_key = RSA.import_key(pub_key.read())

    session_key = get_random_bytes(16)

    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_session_key = rsa_cipher.encrypt(session_key)

    AES_cipher = AES.new(session_key, AES.MODE_EAX)
    encrypted_data, tag = AES_cipher.encrypt_and_digest(data)

    encrypted_payload = []
    [encrypted_payload.append(x) for x in (encrypted_session_key, AES_cipher.nonce, tag, encrypted_data)]

    response = HttpResponse(encrypted_payload, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response


def index(request):
    """
        View to show form to upload key and type in data
        User gets an encrypted .bin file when successful
    """
    if request.method == "POST":
        form = EncryptForm(request.POST, request.FILES)
        if form.is_valid():
            return encryptData(request.FILES['public_key'], form.cleaned_data['data'])
    else:
        form = EncryptForm()
    context = {'form' : form}
    return render(request, 'encrypt/index.html', context)
