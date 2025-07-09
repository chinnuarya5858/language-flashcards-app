from rest_framework import generics,status
from .models import Flashcard
from .serializers import FlashcardSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view,renderer_classes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect,get_object_or_404



# Create your views here.
@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def register_user(request):
    if request.method=='GET':
        return Response(template_name='register.html')
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=User.objects.create_user(username=username,password=password)
    token,_=Token.objects.get_or_create(user=user)
    login(request,user,backend='django.contrib.auth.backends.ModelBackend')
    return redirect('flashcard-html')

@api_view(['GET','POST'])
@renderer_classes([TemplateHTMLRenderer])
def login_user(request):
    if request.method=='GET':
        return Response(template_name='login.html')
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(username=username,password=password)
    if user is not None:
        login(request,user)
        return redirect('flashcard-html')
    return Response({'error':'Invalid Credentials'},status=400)



class FlashcardFormAPIView(APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='add_flashcard.html'

    def get(self,request):
        return Response({"flashcards":Flashcard.objects.filter(user=request.user)})
    def post(self,request):
       serializer=FlashcardSerializer(data=request.data)
       if serializer.is_valid():
            serializer.save(user=request.user)
            return redirect('flashcard-html')
       return Response({'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    

class FlashcardHTMLView(APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='home.html'

    def get(self,request):
        return Response({"flashcards":Flashcard.objects.filter(user=request.user)})


class FlashcardReviewAPIView(APIView):
    renderer_classes=[TemplateHTMLRenderer]
    template_name='review.html'

    def get(self,request,pk):
        flashcard=get_object_or_404(Flashcard,pk=pk,user=request.user)
        return Response({'flashcard':flashcard})
    
    def post(self,request,pk):
        flashcard=get_object_or_404(Flashcard,pk=pk)

        if 'delete' in request.POST:
            flashcard.delete()
            return redirect('flashcard-html')

    

        word=request.POST.get('word')
        meaning=request.POST.get('meaning')
        example_sentences=request.POST.get('example_sentences')
        language=request.POST.get('language')
        difficulty=request.POST.get('difficulty')

        if word and meaning and example_sentences and language and difficulty:
            flashcard.word=word
            flashcard.meaning=meaning
            flashcard.example_sentences=example_sentences
            flashcard.language=language
            flashcard.difficulty=difficulty
            flashcard.save()
        return redirect('flashcard-html')
    
        


    