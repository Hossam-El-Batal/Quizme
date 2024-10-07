from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from attempts.models import Attempt
from attempts.serializers import AttemptSerializer
from authentication.permissions import AUTH_SWAGGER_PARAM
from exam.models import Exam


# TODO (Suggestion) Can make this follow the same convention as exam v2
#  (make the answers coupled to the attempt, remove answer crud)
class AttemptViewSet(viewsets.ModelViewSet):
    serializer_class = AttemptSerializer
    queryset = Attempt.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Attempt.objects.none()

        if hasattr(self.request.user, "role") and self.request.user.role == 'student':
            return Attempt.objects.filter(student_id=self.request.user)
        else:
            exam_id = self.request.query_params.get('exam_id')
            if exam_id:
                try:
                    exam = Exam.objects.get(id=exam_id)
                    if exam.user_id != self.request.user:
                        raise NotFound()
                    return Attempt.objects.filter(exam_id=exam_id)
                except Exam.DoesNotExist:
                    raise NotFound("Exam does not exist")
            # instructor_exams = Exam.objects.values_list('id', flat=True)
            return Attempt.objects.filter(exam_id__user_id=self.request.user)

    @swagger_auto_schema(
        operation_summary="Create an attempt",
        operation_description="Allows authenticated users to create an attempt. Requires authentication.",
        request_body=AttemptSerializer,
        responses={201: AttemptSerializer, 400: "Bad Request"},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update an attempt",
        operation_description="Allows authenticated users to update an attempt. Requires authentication.",
        request_body=AttemptSerializer,
        responses={200: AttemptSerializer, 400: "Bad Request"},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete an attempt",
        operation_description="Allows authenticated users to delete an attempt. Requires authentication.",
        responses={204: "No Content"},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve an attempt",
        operation_description="Allows authenticated users to retrieve an attempt. Requires authentication.",
        responses={200: AttemptSerializer()},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def retrieve(self, request, *args, **kwargs):

        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partially update an attempt",
        operation_description="Allows authenticated users to partially update an attempt. Requires authentication.",
        request_body=AttemptSerializer,
        responses={200: AttemptSerializer(), 400: "Bad Request"},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="List attempts",
        operation_description="Allows authenticated users to list attempts. Requires authentication.",
        responses={200: AttemptSerializer(many=True)},
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get student's attempt by exam code",
        operation_description="Retrieves the authenticated student's attempt for a specific exam using exam code",
        responses={
            200: AttemptSerializer,
            404: "Not Found - Exam doesn't exist or no attempt found",
            403: "Forbidden - User is not authorized to view this attempt"
        },
        manual_parameters=[AUTH_SWAGGER_PARAM],
        tags=['attempts']
    )
    @action(detail=False, methods=['get'], url_path='exam/(?P<exam_code>[^/.]+)')
    def get_attempt_by_exam(self, request, exam_code=None):
        # Check if user is authenticated and is a student
        if not hasattr(request.user, "role"):
            raise PermissionDenied("User role is not defined")

        try:
            # First verify the exam exists and get its ID
            exam = Exam.objects.get(exam_code=exam_code)
            serializer = None
            if request.user.role == "instructor" and request.user == exam.user_id:
                # Get the attempt for this exam
                attempts = Attempt.objects.filter(
                    exam_id=exam.id  # Use the exam.id directly
                )
                serializer = self.get_serializer(attempts, many=True)
            elif request.user.role == "student":
                # Get the attempt for this student and exam
                attempt = Attempt.objects.filter(
                    student_id=request.user,  # Assuming student_id is the correct field
                    exam_id=exam.id  # Use the exam.id directly
                ).first()

                if not attempt:
                    raise NotFound("No attempt found for this exam")

                serializer = self.get_serializer(attempt)
            return Response(serializer.data)

        except Exam.DoesNotExist:
            raise NotFound("Exam does not exist")


class EvaluateAttemptView(APIView):
    # ! Unused for now
    def post(self, request, *args, **kwargs):
        attempt_id = kwargs.get('attempt_id')
        # TODO: Implement evaluation logic within celery tasks
        return Response()