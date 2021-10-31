from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from attendance.models import AttendanceBlock
from attendance.serializers import AttendanceBlockSerializer


class AttendanceBlockAdminAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = (
        TokenAuthentication,
        SessionAuthentication,
    )
    serializer_class = AttendanceBlockSerializer

    def get_queryset(self):
        roll_number = self.request.GET.get("roll_number")
        semester = self.request.GET.get("semester")
        return AttendanceBlock.objects.filter(semester__student__roll_number=roll_number, semester__semester=semester)

    # def get(self, request):
    #     roll_number = request.GET.get('roll_number')
    #     semester = request.GET.get('semester')
    #     attendance_block = AttendanceBlock.objects.filter(
    #         semester__student__roll_number=roll_number,
    #         semester__semester=semester
    #     )
    #     if attendance_block.exists():
    #         attendance_block = attendance_block.first()
    #         sessions = Session.objects.filter(attendance_block=attendance_block)
    #
    #         response = {}
    #         for session in sessions:
    #             date = session.date.strftime('%d-%m-%Y')
    #             sessions_of_day = response.get(date, [])
    #             sessions_of_day.append({
    #                 'date': date,
    #                 'subject': session.subject.name,
    #                 'did_attend': session.did_attend,
    #                 'start': session.start,
    #                 'end': session.end,
    #             })
    #             response[date] = sessions_of_day
    #
    #         return Response(response, status=HTTP_200_OK)
    #
    #     return Response({"error": "Attendance doesn't exist"}, status=HTTP_404_NOT_FOUND)
