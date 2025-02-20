from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from attendance.models import *
from employee.models import *
from leave.models import Leave

from django.contrib.auth.hashers import make_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields =  "__all__"




class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["name"]

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class EmployeeSerializer(serializers.ModelSerializer):
    department= DepartmentSerializer()
    role= RoleSerializer()
    class Meta:
        model = Employee
        fields = ["id",
        "title",
        "image",
        "firstname",
        "lastname",
        "othername",
        "sex",
        "email",
        "tel",
        "bio",
        "birthday",
        "hometown",
        "region",
        "residence",
        "address",
        "education",
        "lastwork",
        "position",
        "nidnumber",
        "tinnumber",
        "startdate",
        "employeetype",
        "employeeid",
        "dateissued",
        "is_blocked",
        "is_deleted",
        "created",
        "updated",
        "salary",
        "user",
        "religion",
        "nationality",
        "department",
        "role"]

class EmployeeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
class EmployeeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"
class AttendanceSerializer(serializers.ModelSerializer):
    
    employee = EmployeeSerializer()

    class Meta:
        model = Attendance
        fields = ['id', 'date','check_in', 'check_out', 'employee']

class AttendanceCreateSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Attendance
        fields = "__all__"
class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"


class EmergencySerializer(serializers.ModelSerializer):

	class Meta:
		model = Emergency
		fields = ['employee','fullname','tel','location','relationship']

class FamilySerializer(serializers.ModelSerializer):

	class Meta:
		model = Relationship
		fields = ['employee','status','spouse','occupation','tel','children','nextofkin','contact','relationship','father','foccupation','mother','moccupation']

class BankAccountSerializer(serializers.ModelSerializer):

	class Meta:
		model = Bank
		fields = ['employee','name','branch','account','salary']
            

class PaymentSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = Payment
        fields = ['employee','amount','payment_date','status','tran_id','val_id','id']