from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

class CustomPageNumberPagination(PageNumberPagination): # for pagination
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProjectView(APIView): 
    """
    ProjectView handles GET requests to retrieve a paginated list of projects.
    Only authenticated users with member permissions can access this view.

    """ 
    permission_classes=[IsAuthenticated,MemberPermission]
    
    @method_decorator(cache_page(60 * 15))  # Cache set for 15 minutes
    def get(self,request):
        try:
            projects = Project.objects.all()
            
            # Paginate the project objects
            paginator = CustomPageNumberPagination()
            result_page = paginator.paginate_queryset(projects, request)
            serializer = ProjectSerializer(result_page, many=True)
            response_data = {
                'data': serializer.data,
                'message': 'Success'
            }
            return paginator.get_paginated_response(response_data)
        except Exception as e:
            # Print the exception for debugging purposes
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectCreate(APIView):
    """
    ProjectCreate handles POST requests to create a new project.
    Only authenticated users with admin permissions can access this view.

    """
    permission_classes=[IsAuthenticated,AdminPermission]
        
    def post(self, request):
        try:
            serializer = ProjectSerializer(data=request.data)

            # Check if the provided data is valid
            if serializer.is_valid():
                serializer.save()
                return Response({'status':True,'message': 'Project created successfully'},
                                status=status.HTTP_201_CREATED)
            return Response({'status':False,'error': serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProjectUpdate(APIView):
    """
    ProjectUpdate handles PUT requests to update an existing project.
    Only authenticated users with manager permissions can access this view.

    """
    permission_classes=[IsAuthenticated,ManagerPermission]
    
    def put(self, request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({"Status":False,'message': 'ID is required'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                id = int(id)
            except ValueError:
                return Response({'message':'id should be an integer value'})
            project = Project.objects.get(id=id)

            # Initialize the serializer with the project object and the provided data
            serializer = ProjectSerializer(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Status":True,'Message':'Updated Successfull'},
                                status=status.HTTP_200_OK)
            return Response({"Status":False,"error":serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Return an error response if the project with the given ID does not exist
        except ObjectDoesNotExist:
            return Response({"Status":False,'Message':'Object doesnot exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProjectDelete(APIView):
    """
    ProjectDelete handles DELETE requests to delete an existing project.
    Only authenticated users with admin permissions can access this view.

    """

    permission_classes = [IsAuthenticated,AdminPermission]

    def delete(self, request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({"Status":False,'message': 'ID is required'},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Convert the project ID to an integer
            try:
                id = int(id)
            except ValueError:
                return Response({'message':'id should be an integer value'})
            project = Project.objects.get(id=id)

            # Delete the project
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            data = {"Status":False,'message':'Object doesnot exist'}
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TaskView(APIView):
    """
    TaskView handles GET requests to retrieve a paginated list of tasks.
    Only authenticated users with member permissions can access this view.

    """
    permission_classes = [IsAuthenticated, MemberPermission]

    @method_decorator(cache_page(60 * 15))  
    def get(self, request):
        try:

            # Initialize the paginator with a page size of 10
            paginator = PageNumberPagination()
            paginator.page_size = 10  
            tasks = Task.objects.all()
            result_page = paginator.paginate_queryset(tasks, request)
            serializer = TaskSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            print(e)
            # Return an error response in case of an exception
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskCreation(APIView):
    """
    TaskCreation handles POST requests to create a new task.
    Only authenticated users with admin permissions can access this view.

    """
    permission_classes = [IsAuthenticated,AdminPermission]

    def post(self, request):
        try:
            serializer = TaskSerializer(data=request.data)

            # Check if the provided data is valid
            if serializer.is_valid():
                task = serializer.save()
                return Response({"Status":True,'message':'Task created successfully',},
                                status=status.HTTP_201_CREATED)
            return Response({"Status":False,'error':serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class TaskDeletion(APIView):
    """
    TaskDeletion handles DELETE requests to delete an existing task.
    Only authenticated users with admin permissions can access this view.

    """
    permission_classes = [IsAuthenticated,AdminPermission]

    def delete(self,request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({'message': 'ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Convert the project ID to an integer
            try:
                id = int(id)
            except ValueError:
                return Response({'message':'id should be an integer value'})
            tasks = Task.objects.get(id=id)
            tasks.delete()
            return Response({'message':'Task deleted successfully'},
                            status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"Status":False,'message':'Object doesnot exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskUpdate(APIView):
    """
    TaskUpdate handles PUT requests to update an existing task.
    Only authenticated users with manager permissions can access this view.

    """
    permission_classes = [IsAuthenticated, ManagerPermission]

    def put(self, request):
        try:
            id = request.data.get('id')
            if id:
                try:
                    id = int(id)
                except ValueError:
                    return Response({'message':'id should be an integer value'})
                task = Task.objects.get(pk=id)
                serializer = TaskSerializer(task, data=request.data, partial=True)

                # Check if the provided data is valid
                if serializer.is_valid():
                    serializer.save()
                    return Response({"Status":True,'message': 'Task updated successfully'},
                                    status=status.HTTP_200_OK)
                return Response({"Status":False,'error': serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'message':'id not provided'},status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MilestoneView(APIView):
    """
    MilestoneView handles GET requests to retrieve a paginated list of milestones.
    Only authenticated users with member permissions can access this view.

    """
    permission_classes = [IsAuthenticated,MemberPermission]

    def get(self, request):
        try:
            paginator = PageNumberPagination()
            paginator.page_size = 10  
            milestones = Milestone.objects.all()
            result_page = paginator.paginate_queryset(milestones, request)
            serializer = MilestoneSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except ObjectDoesNotExist:
            return Response({"Status":False,'message': 'No milestones found'}, 
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class MilestoneCreate(APIView):
    """
    MilestoneCreate handles POST requests to create a new milestone.
    Only authenticated users with admin permissions can access this view.

    """
    permission_classes =[IsAuthenticated,AdminPermission]

    def post(self, request):
        try:
            serializer = MilestoneSerializer(data=request.data)
            if serializer.is_valid():
                milestone = serializer.save()
                return Response({"Status":True,'message': 'Milestone created successfully'}, 
                                status=status.HTTP_201_CREATED)
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class MilestoneUpdate(APIView):
    """
    MilestoneUpdate handles PUT requests to update an existing milestone.
    Only authenticated users with manager permissions can access this view.

    """
    permission_classes = [IsAuthenticated, ManagerPermission]  

    def put(self, request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({"Status":False,'message': 'ID is required'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                id = int(id)
            except ValueError:
                return Response({"Status":False,'Message':'Id should be a valid integer'},
                                status=status.HTTP_400_BAD_REQUEST)
            milestone = Milestone.objects.get(id=id)
            serializer = MilestoneSerializer(milestone, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'Status':True,'message':'milestone updated successfully'},
                                status=status.HTTP_200_OK)
            return Response({'Status':False,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({'message':'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class MilestoneDelete(APIView):
    """
    MilestoneDelete handles DELETE requests to delete an existing milestone.
    Only authenticated users with admin permissions can access this view.

    """
    permission_classes =[IsAuthenticated,AdminPermission]

    def delete(self, request):
        try:
            id = request.data.get('id')
            if id is None:
                return Response({'message': 'ID is required'},
                                status=status.HTTP_400_BAD_REQUEST)
            try:
                id = int(id)
            except ValueError:
                return Response({'message':'id should be an integer value'})
            milestone = Milestone.objects.get(id=id)
            milestone.delete()
            return Response({'message': 'Milestone deleted successfully'},
                            status=status.HTTP_204_NO_CONTENT)
        except Milestone.DoesNotExist:
            return Response({"Staus":False,'message': 'Milestone not found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'Status':False,'Message':'Something unexpected occured'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)