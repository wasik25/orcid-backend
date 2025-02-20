from django.urls import path, include

from .views import *

urlpatterns = [

path('login/', UserLoginView.as_view(), name='user-login'),
path('register/', UserRegistrationView.as_view(), name='user-register'),
path('user/profile/', UserProfileView.as_view(), name='user-profile'),
path('attendancelist/', AttendanceList.as_view(), name='attendencelist'),
path('attendancecreate/', AttendanceCreate.as_view(), name='attendencecreate'),
path('attendancedetail/<int:id>/', AttendanceDetail.as_view(), name='attendencedetail'),
path('attendanceupdate/update/<int:id>', AttendanceUpdate.as_view(), name='attendenceupdate'),

path('leaveAll/', AllLeaveList.as_view(), name='allleavelist'),
path('leaveAll//count/', AllLeaveCountView.as_view(), name='AllLeave-count'),
path('leaveAll/<int:id>/', leaveAllDetail.as_view(), name='leaveAllDetail'),
path('leaveCreate/create', LeaveCreate.as_view(), name='leaveCreate'),

path('employeelist/', EmployeeList.as_view(), name='employeelist'),
path('employeelist/count/', EmployeeCountView.as_view(), name='employee-count'),
path('employeecreate/', EmployeeCreate.as_view(), name='employeecreate'),
path('employeelist/<int:id>/', EmployeeDetail.as_view(), name='EmployeeDetail'),
path('employeelist/update/<int:id>/', EmployeeUpdate.as_view(), name='EmployeeUpdate'),
      
path('EmergencyCreate/create', EmergencyCreate.as_view(), name='EmergencyCreate'),
path('FamilyCreate/create', FamilyCreate.as_view(), name='FamilyCreate'),
path('BankAccountCreate/create', BankAccountCreate.as_view(), name='BankAccountCreate'),

path('birthdays/', EmployeeBirthdayView.as_view(), name='employee-birthdays'),
path('payments/', PaymentsList.as_view(), name='payments'),
path('allusers/', UserView.as_view(), name='UserView'),
path('initiate-salary-payment/', InitiateSalaryPayment.as_view(), name='initiate-salary-payment'),
path('sslcommerz-ipn/', sslcommerz_ipn, name='sslcommerz-ipn'),
]