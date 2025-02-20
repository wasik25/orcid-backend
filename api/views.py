# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import *
from attendance.models import *
from employee.models import *
from leave.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
import uuid
import requests
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful.",
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AttendanceList(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer


class PaymentsList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class AttendanceCreate(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceCreateSerializer


class AttendanceDetail(generics.RetrieveAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound("Product not found.")
        
class AttendanceUpdate(generics.UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound("Product not found.")       
        
class AllLeaveList(generics.ListAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    def get_queryset(self):
        queryset = Leave.objects.all()
        status= self.request.query_params.get('status', None)
        

        if status:
            queryset = queryset.filter(status__icontains=status)
        

        return queryset
    

class AllLeaveCountView(APIView):
    def get(self, request):
        AllLeave_count =  Leave.objects.count()
        return Response({'AllLeave_count': AllLeave_count})
        return queryset
    


        
class leaveAllDetail(generics.RetrieveAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound("Product not found.")
class LeaveCreate(generics.CreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

class UserProfileView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        return Employee.objects.filter(user=self.request.user)
    def get(self, request):
        user = request.user
        user = User.objects.get(id=user.id)
        print(user)
        profile = Employee.objects.filter(user=user)
        user_profile = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        user_data = Employee.objects.filter(user=request.user)
        serializer = EmployeeSerializer(user_data, many=True)
        return Response(user_profile)

class EmployeeList(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    def get_queryset(self):
        queryset = Employee.objects.all()
        is_deleted = self.request.query_params.get('is_deleted', None)
        if is_deleted is not None:
            is_deleted = is_deleted .lower() == 'true'
            queryset = queryset.filter(is_deleted = is_deleted )
        return queryset
        
class EmployeeCountView(APIView):
    def get(self, request):
        employee_count =  Employee.objects.count()
        return Response({'employee_count': employee_count})
        return queryset

class EmployeeCreate(generics.CreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeCreateSerializer


class EmployeeDetail(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'id'

    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound("Product not found.")
        

class EmployeeUpdate(generics.UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeUpdateSerializer
    lookup_field = 'id'
    
    def get_object(self):
        try:
            return super().get_object()
        except:
            raise NotFound("Product not found.")   
        

class EmergencyCreate(generics.CreateAPIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer



class FamilyCreate(generics.CreateAPIView):
    queryset = Relationship.objects.all()
    serializer_class = FamilySerializer

class BankAccountCreate(generics.CreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankAccountSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    @action(detail=False, methods=['post'])
    def initiate(self, request):
        employee_id = request.data.get('employee_id')
        amount = request.data.get('amount')
        
        try:
            employee = Employee.objects.get(id=employee_id)
            tran_id = uuid.uuid4().hex
            
            sslcommerz_data = {
                'total_amount': amount,
                'currency': 'BDT',
                'tran_id': tran_id,
                'success_url': 'http://localhost:8000/api/payment/success/',
                'fail_url': 'http://localhost:8000/api/payment/fail/',
                'cus_email': employee.email,
                'cus_name': employee.firstname,
            }
            
            Payment.objects.create(
                employee=employee,
                amount=amount,
                tran_id=tran_id
            )
            
            response = requests.post(
                'https://sandbox.sslcommerz.com/gwprocess/v4/api.php' if settings.SSLCOMMERZ_CONFIG['sandbox'] 
                else 'https://securepay.sslcommerz.com/gwprocess/v4/api.php',
                data=sslcommerz_data,
                auth=(settings.SSLCOMMERZ_CONFIG['store_id'], settings.SSLCOMMERZ_CONFIG['store_pass'])
            )
            
            return Response({'gateway_url': response.json().get('GatewayPageURL')})
        
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'])
    def success(self, request):
        response = requests.post(
            'https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php' if settings.SSLCOMMERZ_CONFIG['sandbox']
            else 'https://securepay.sslcommerz.com/validator/api/validationserverAPI.php',
            data={'val_id': request.data.get('val_id')},
            auth=(settings.SSLCOMMERZ_CONFIG['store_id'], settings.SSLCOMMERZ_CONFIG['store_pass'])
        )
        
        data = response.json()
        payment = Payment.objects.get(tran_id=data['tran_id'])
        payment.status = 'SUCCESS'
        payment.val_id = data['val_id']
        payment.save()
        
        return Response({'status': 'Payment Successful'})

    @action(detail=False, methods=['post'])
    def fail(self, request):
        payment = Payment.objects.get(tran_id=request.data.get('tran_id'))
        payment.status = 'FAILED'
        payment.save()
        return Response({'status': 'Payment Failed'})
    

class EmployeeBirthdayView(APIView):
    def get(self, request):
        today = timezone.now().date()
        employees = Employee.objects.filter(birthday__month=today.month)
        employeescount= employees.count()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(employeescount)
    

class InitiateSalaryPayment(APIView):
    def post(self, request):
        employee_id = request.data.get('employee_id')
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

        amount = employee.salary
        tran_id = f"SALARY_{employee.id}_{employee.firstname}" 
        payment = Payment.objects.create(
            employee=employee,
            amount=amount,
            tran_id=tran_id
        )

        sslcz_url = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

        payload = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_passwd': settings.SSLCOMMERZ_STORE_PASSWORD,
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': tran_id,
            'success_url': 'http://your-frontend-url/success',  # Redirect after success
            'fail_url': 'http://your-frontend-url/fail',        # Redirect after failure
            'cancel_url': 'http://your-frontend-url/cancel',    # Redirect after cancel
            'emi_option': 0,
            'cus_name': employee.firstname,
            'cus_email': employee.email,
            'cus_phone': '017XXXXXXXX',  
            'cus_add1': 'Dhaka',
            'cus_city': 'Dhaka',
            'cus_country': 'Bangladesh',
            'shipping_method': 'NO',
            'product_name': 'Salary Payment',
            'product_category': 'Salary',
            'product_profile': 'general',
        }

        response = requests.post(sslcz_url, data=payload)
        if response.status_code == 200:
            payment_url = response.json().get('GatewayPageURL')
            return Response({'payment_url': payment_url}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Payment initiation failed'}, status=status.HTTP_400_BAD_REQUEST)
        

@csrf_exempt
def sslcommerz_ipn(request):
    if request.method == 'POST':
        tran_id = request.POST.get('tran_id')
        status = request.POST.get('status')

        try:
            payment = Payment.objects.get(tran_id=tran_id)
            payment.status = status
            payment.save()
            return HttpResponse("IPN received and updated", status=200)
        except Payment.DoesNotExist:
            return HttpResponse("Transaction not found", status=404)
    return HttpResponse("Invalid request", status=400)