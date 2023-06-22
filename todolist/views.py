from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import (
    ToDo,
)
from django.db.models import Q

from .serializers import (
    ToDoSerializer,
)

# Todo list CRUD API 
@api_view(['POST','GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def task(request,task_id=0):

    # Add new task to the todo list
    if request.method == 'POST':
        try:
            request_data = request.data
            request_data['user'] = request.user.id
            serializer = ToDoSerializer(data =request_data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'app_data': 'Something went wrong', 'dev_data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'app_data': 'Something went wrong', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)
    
    # Returns a list of all tasks created by the user.
    if request.method == 'GET':
        try:
            todos = ToDo.objects.filter(user__id=request.user.id).order_by('-created_at')
            todo_list = ToDoSerializer(todos,many=True).data
            return Response(todo_list)
        except Exception as E:
            return Response({'app_data':'Error while fetching posts', 'dev_data':str(E)},status=status.HTTP_400_BAD_REQUEST)    

    # Update a specific task 
    if request.method == 'PUT':
        try:
            request_data = request.data
            task = ToDo.objects.get(id=task_id)
            if task.user.id == request.user.id:
                serializer = ToDoSerializer(task,data =request_data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({'app_data': 'Something went wrong ', 'dev_data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'app_data': 'Something went wrong ', 'dev_data': 'Invalid task id'}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as E:
            return Response({'app_data': 'Something went wrong ', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)

    # Deleting a task
    if request.method == 'DELETE':
        try:
            ToDo.objects.filter(id=task_id,user__id=request.user.id).delete()
            return Response({'app_data': 'Deleted ', 'dev_data': 'Deleted'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as E:
            return Response({'app_data': 'Something went wrong ', 'dev_data': str(E)}, status=status.HTTP_400_BAD_REQUEST)



