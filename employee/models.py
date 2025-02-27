import datetime
from employee.utility import code_format
from django.db import models
from employee.managers import EmployeeManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from leave.models import Leave
from django.utils.timezone import now

class Role(models.Model):

    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    class Meta:
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')
        ordering = ['name','created']

    def __str__(self):
        return self.name

class Department(models.Model):

    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    
    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name','created']
    
    def __str__(self):
        return self.name

class Nationality(models.Model):
    name = models.CharField(max_length=125)
    flag = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = _('Nationality')
        verbose_name_plural = _('Nationality')
        ordering = ['name','created']

    def __str__(self):
        return self.name

class Religion(models.Model):
    name = models.CharField(max_length=125)
    description = models.CharField(max_length=125,null=True,blank=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)
    
    class Meta:
        verbose_name = _('Religion')
        verbose_name_plural = _('Religions')
        ordering = ['name','created']

    def __str__(self):
        return self.name

class Bank(models.Model):

    employee = models.ForeignKey('Employee',help_text='select employee(s) to add bank account',on_delete=models.CASCADE,null=True,blank=False)
    name = models.CharField(_('Name of Bank'),max_length=125,blank=False,null=True,help_text='')
    account = models.CharField(_('Account Number'),help_text='employee account number',max_length=30,blank=False,null=True)
    branch = models.CharField(_('Branch'),help_text='which branch was the account issue',max_length=125,blank=True,null=True)
    salary = models.DecimalField(_('Starting Salary'),help_text='This is the initial salary of employee',max_digits=16, decimal_places=2,null=True,blank=False)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    class Meta:
        verbose_name = _('Bank')
        verbose_name_plural = _('Banks')
        ordering = ['-name','-account']

    def __str__(self):
        return ('{0}'.format(self.name))

class Emergency(models.Model):
    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'
    
    EMERGENCY_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )

    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    fullname = models.CharField(_('Fullname'),help_text='who should we contact ?',max_length=255,null=True,blank=False)
    tel = PhoneNumberField(default='+8801712345678', null = False, blank=False, verbose_name='Phone Number (Example +8801712345678)', help_text= 'Enter number with Country Code Eg. +8801712345678')
    location = models.CharField(_('Place of Residence'),max_length= 125,null=True,blank=False)
    relationship = models.CharField(_('Relationship with Person'),help_text='Who is this person to you ?',max_length=8,default=FATHER,choices=EMERGENCY_RELATIONSHIP,blank=False,null=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergency'
        ordering = ['-created']

    def __str__(self):
        return self.fullname

    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

class Relationship(models.Model):
    MARRIED = 'Married'
    SINGLE = 'Single'
    DIVORCED = 'Divorced'
    WIDOW = 'Widow'
    WIDOWER = 'Widower'

    STATUS = (
    (MARRIED,'Married'),
    (SINGLE,'Single'),
    (DIVORCED,'Divorced'),
    (WIDOW,'Widow'),
    (WIDOWER,'Widower'),
    )

    FATHER = 'Father'
    MOTHER = 'Mother'
    SIS = 'Sister'
    BRO = 'Brother'
    UNCLE = 'Uncle'
    AUNTY = 'Aunty'
    HUSBAND = 'Husband'
    WIFE = 'Wife'
    FIANCE = 'Fiance'
    FIANCEE = 'Fiancee'
    COUSIN = 'Cousin'
    NIECE = 'Niece'
    NEPHEW = 'Nephew'
    SON = 'Son'
    DAUGHTER = 'Daughter'

    NEXTOFKIN_RELATIONSHIP = (
    (FATHER,'Father'),
    (MOTHER,'Mother'),
    (SIS,'Sister'),
    (BRO,'Brother'),
    (UNCLE,'Uncle'),
    (AUNTY,'Aunty'),
    (HUSBAND,'Husband'),
    (WIFE,'Wife'),
    (FIANCE,'Fiance'),
    (COUSIN,'Cousin'),
    (FIANCEE,'Fiancee'),
    (NIECE,'Niece'),
    (NEPHEW,'Nephew'),
    (SON,'Son'),
    (DAUGHTER,'Daughter'),
    )

    employee = models.ForeignKey('Employee',on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(_('Marital Status'),max_length=10,default=SINGLE,choices=STATUS,blank=False,null=True)
    spouse = models.CharField(_('Spouse (Fullname)'),max_length=255,blank=True,null=True)
    occupation = models.CharField(_('Occupation'),max_length=125,help_text='spouse occupation',blank=True,null=True)
    tel = PhoneNumberField(default=None, null = True, blank=True, verbose_name='Spouse Phone Number (Example +8801712345678)', help_text= 'Enter number with Country Code Eg. +8801712345678')
    children = models.PositiveIntegerField(_('Number of Children'),null=True,blank=True,default=0)
    nextofkin = models.CharField(_('Next of Kin'),max_length=255,blank=False,null=True,help_text='fullname of next of kin')
    contact = PhoneNumberField(verbose_name='Next of Kin Phone Number (Example +8801712345678)',null=True,blank=True,help_text='Phone Number of Next of Kin')
    relationship = models.CharField(_('Relationship with Next of Person'),help_text='Who is this person to you ?',max_length=15,choices=NEXTOFKIN_RELATIONSHIP,blank=False,null=True)
    father = models.CharField(_('Father\'s Name'),max_length=255,blank=True,null=True)
    foccupation = models.CharField(_('Father\'s Occupation'),max_length=125,help_text='',blank=True,null=True)
    mother = models.CharField(_('Mother\'s Name'),max_length=255,blank=True,null=True)
    moccupation = models.CharField(_('Mother\'s Occupation'),max_length=125,help_text='',blank=True,null=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)

    class Meta:
        verbose_name = 'Relationship'
        verbose_name_plural = 'Relationships'
        ordering = ['created']

    def __str__(self):
        if self.status == 'Married':
            return self.spouse
        return self.status

class Employee(models.Model):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'
    NOT_KNOWN = 'Not Known'

    GENDER = (
    (MALE,'Male'),
    (FEMALE,'Female'),
    (OTHER,'Other'),
    (NOT_KNOWN,'Not Known'),
    )

    MR = 'Mr'
    MRS = 'Mrs'
    MSS = 'Mss'
    DR = 'Dr'
    SIR = 'Sir'
    MADAM = 'Madam'

    TITLE = (
    (MR,'Mr'),
    (MRS,'Mrs'),
    (MSS,'Mss'),
    (DR,'Dr'),
    (SIR,'Sir'),
    (MADAM,'Madam'),
    )

    FULL_TIME = 'Full-Time'
    PART_TIME = 'Part-Time'
    CONTRACT = 'Contract'
    INTERN = 'Intern'

    EMPLOYEETYPE = (
    (FULL_TIME,'Full-Time'),
    (PART_TIME,'Part-Time'),
    (CONTRACT,'Contract'),
    (INTERN,'Intern'),
    )

    OLEVEL = 'O-LEVEL'
    SENIORHIGH = 'Senior High'
    JUNIORHIGH = 'Junior High'
    BACHELORS = 'Bachelors'
    PRIMARY = 'Primary Level'
    OTHER = 'Other'

    EDUCATIONAL_LEVEL = (
    (SENIORHIGH,'Senior High School'),
    (JUNIORHIGH,'Junior High School'),
    (PRIMARY,'Primary School'),
    (BACHELORS,'Bachelors/University/Polytechnic'),
    (OLEVEL,'OLevel'),
    (OTHER,'Other'),
    )

    EAST = 'East'
    WEST = 'West'
    NORTH = 'North'
    SOUTH = 'South'
    
    GREATER = 'Greater'
    
    REGIONS = (
    (EAST,'East'),
    (WEST,'West'),
    (NORTH,'North'),
    (SOUTH,'South'),
    )
    
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=10, choices=TITLE, default='Mr')
    image = models.FileField(_('Profile Image'),upload_to='profiles',default='default.png',blank=True,null=True,help_text='upload image size less than 2.0MB')
    firstname = models.CharField(_('Firstname'),max_length=125,null=False,blank=False)
    lastname = models.CharField(_('Lastname'),max_length=125,null=False,blank=False)
    othername = models.CharField(_('Othername (optional)'),max_length=125,null=True,blank=True)
    sex = models.CharField(max_length=10, choices=GENDER)
    email = models.CharField(_('Email (optional)'),max_length=255,default=None,blank=True,null=True)
    tel = PhoneNumberField(default='+8801712345678', null = False, blank=False, verbose_name='Phone Number (Example +8801712345678)', help_text= 'Enter number with Country Code Eg. +8801712345678')
    bio = models.CharField(_('Bio'),help_text='your biography,tell me something about yourself eg. i love working ...',max_length=255,default='',null=True,blank=True)
    birthday = models.DateField(_('Birthday'),blank=False,null=False)
    religion = models.ForeignKey(Religion,verbose_name =_('Religion'),on_delete=models.SET_NULL,null=True,default=None)
    nationality = models.ForeignKey(Nationality,verbose_name =_('Nationality'),on_delete=models.SET_NULL,null=True,default=None)
    hometown = models.CharField(_('Hometown'),max_length=125,null=True,blank=True)
    region = models.CharField(_('Region'), help_text='what region of the country are you from ?', max_length=20, choices=REGIONS, blank=False, null=True)
    residence = models.CharField(_('Current Residence'),max_length=125,null=False,blank=False)
    address = models.CharField(_('Address'),help_text='address of current residence',max_length=125,null=True,blank=True)
    education = models.CharField(_('Education'),help_text='highest educational standard ie. your last level of schooling',max_length=20,default=SENIORHIGH,choices=EDUCATIONAL_LEVEL,blank=False,null=True)
    lastwork = models.CharField(_('Last Place of Work'),help_text='where was the last place you worked ?',max_length=125,null=True,blank=True)
    position = models.CharField(_('Position Held'),help_text='what position where you in your last place of work ?',max_length=255,null=True,blank=True)
    nidnumber = models.CharField(_('National ID Number'),max_length=50,null=True,blank=True)
    tinnumber = models.CharField(_('TIN'),max_length=15,null=True,blank=True)
    department =  models.ForeignKey(Department,verbose_name =_('Department'),on_delete=models.SET_NULL,null=True,default=None)
    role =  models.ForeignKey(Role,verbose_name =_('Role'),on_delete=models.SET_NULL,null=True,default=None)
    startdate = models.DateField(_('Employement Date'),help_text='date of employement',blank=False,null=True)
    employeetype = models.CharField(_('Employee Type'),max_length=15,default=FULL_TIME,choices=EMPLOYEETYPE,blank=False,null=True)
    employeeid = models.CharField(_('Employee ID Number'),max_length=10,null=True,blank=True)
    dateissued = models.DateField(_('Date Issued'),help_text='date staff id was issued',blank=False,null=True)
    is_blocked = models.BooleanField(_('Is Blocked'),help_text='button to toggle employee block and unblock',default=False)
    is_deleted = models.BooleanField(_('Is Deleted'),help_text='button to toggle employee deleted and undelete',default=False)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,blank=False,null=True)
    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['-created']

    def __str__(self):
        return self.get_full_name

    @property
    def get_full_name(self):
        fullname = ''
        firstname = self.firstname
        lastname = self.lastname
        othername = self.othername

        if (firstname and lastname) or othername is None:
            fullname = firstname +' '+ lastname
            return fullname
        elif othername:
            fullname = firstname + ' '+ lastname +' '+othername
            return fullname
        return

    @property
    def get_age(self):
        current_year = datetime.date.today().year
        dateofbirth_year = self.birthday.year
        if dateofbirth_year:
            return current_year - dateofbirth_year
        return

    @property
    def can_apply_leave(self):
        pass

    @property
    def get_pretty_birthday(self):
        if self.birthday:
            return self.birthday.strftime('%A,%d %B') 
        return

    @property
    def birthday_today(self):

        return self.birthday.day == datetime.date.today().day

    @property
    def days_check_date_fade(self):

        return self.birthday.day < datetime.date.today().day 

    def birthday_counter(self):

        today = datetime.date.today()
        current_year = today.year

        birthday = self.birthday 

        future_date_of_birth = datetime.date(current_year,birthday.month,birthday.day)

        if birthday:
            if (future_date_of_birth - today).days > 1:

                return str((future_date_of_birth - today).days) + ' day\'s'

            else:

                return ' tomorrow'
        return

    def save(self,*args,**kwargs):

        get_id = self.employeeid 
        data = code_format(get_id)
        self.employeeid = data 
        super().save(*args,**kwargs) 

class Payment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='PENDING')
    tran_id = models.CharField(max_length=100)
    val_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(verbose_name=_('Created'),auto_now_add=True,null=True)
    updated = models.DateTimeField(verbose_name=_('Updated'),auto_now=True,null=True)