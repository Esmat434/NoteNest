from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import TokenAuthenticationPermission
from .permission import IsOwner
from .serializer import NoteSerializer
from .models import Note

# this class for create and show the list of note data
class NoteCreateListView(APIView):
    permission_classes = [TokenAuthenticationPermission,IsOwner]

    def get(self,request):
        notes = Note.objects.filter(user = request.user,is_enable = True,is_deleted = False)
        serializer = NoteSerializer(notes,many = True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer = NoteSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response({"error":"Enter valid data."},status=status.HTTP_400_BAD_REQUEST)

# this class for show detail and update and also delete the note data
class NoteDetailUpdateDeleteView(APIView):
    permission_classes = [TokenAuthenticationPermission,IsOwner]

    def get_note(self,request,pk): # this function create to get note data
        try:
            note = Note.objects.get(id = pk, user = request.user, is_deleted = False)
            return note
        except Note.DoesNotExist:
            return None

    def get(self,request,pk):
        note = self.get_note(request,pk) # use this function to get note data
        if not note:
            return Response({"error":'Data does not exists.'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = NoteSerializer(note)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        note = self.get_note(request,pk) # use this function to get note data
        if not note:
            return Response({"error":'Data does not exists.'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = NoteSerializer(note, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response({"error":"Enter valid data."},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        note = self.get_note(request,pk)
        if not note:
            return Response({"error":'Data does not exists.'},status=status.HTTP_404_NOT_FOUND)
        
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NoteIsNotEnableListView(APIView):
    permission_classes = [TokenAuthenticationPermission,IsOwner]

    def get(self,request):
        note = Note.objects.filter(user = request.user,is_enable=False, is_deleted=False)
        serializer = NoteSerializer(note,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)