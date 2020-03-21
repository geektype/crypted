from django.shortcuts import render
from django.http import HttpResponse
from Crypto.PublicKey import RSA





def index(request):
    key = RSA.generate(1024)
    private_key = key.export_key()
    private_key = private_key.decode("utf-8")
    public_key = key.publickey().export_key()
    public_key = public_key.decode("utf-8")

    request.session['public'] = public_key
    request.session['private'] = private_key

    request.session.set_expiry(30)

    context = {}
    return render(request, 'genKeyPair/index.html', context)

 

def downloadPublic(request):
    if request.session.get('public', False):
        filename = "public-key.pem"
        content = request.session['public']

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

        return response
    return HttpResponse("no key exists")

def downloadPrivate(request):
    if request.session.get('private', False):
        filename = "private-key.pem"
        content = request.session['private']

        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)

        return response
    return HttpResponse("no key exists")


