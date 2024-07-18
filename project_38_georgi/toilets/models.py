# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.core.validators import MinValueValidator, MaxValueValidator
# from django.utils import timezone
#
#
# class SoftDeleteManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(is_active=True)
#
#     def all_with_deleted(self):
#         return super().get_queryset()
#
#     def deleted(self):
#         return super().get_queryset().filter(is_active=False)
#
#
# class SoftDeleteModel(models.Model):
#     is_active = models.BooleanField(default=True)
#     deleted_at = models.DateTimeField(null=True, blank=True)
#
#     objects = SoftDeleteManager()
#
#     class Meta:
#         abstract = True
#
#     def soft_delete(self):
#         self.is_active = False
#         self.deleted_at = timezone.now()
#         self.save()
#
#     def restore(self):
#         self.is_active = True
#         self.deleted_at = None
#         self.save()
#
#
# class Region(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.name
#
#
# class User(AbstractUser, SoftDeleteModel):
#     ROLE_CHOICES = (
#         ('ADMIN', 'Admin'),
#         ('MANAGER', 'Manager'),
#         ('STAFF', 'Staff'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STAFF')
#     phone = models.CharField(max_length=20, blank=True)
#     regions = models.ManyToManyField(Region, blank=True, related_name='users')
#
#     def __str__(self):
#         return f"{self.username} - {self.role}"
#
#
# class Client(models.Model):
#     name = models.CharField(max_length=100)
#     vat = models.CharField(max_length=20, unique=True)
#     address = models.TextField()
#     phone = models.CharField(max_length=20)
#     email = models.EmailField()
#     NOTIFICATION_CHOICES = (
#         ('EMAIL', 'Email'),
#         ('SMS', 'SMS'),
#         ('BOTH', 'Both'),
#         ('NONE', 'None'),
#     )
#     notification_preference = models.CharField(max_length=5, choices=NOTIFICATION_CHOICES, default='NONE')
#
#     def __str__(self):
#         return self.name
#
#
# class Toilet(SoftDeleteModel):
#     client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name='toilets')
#     nfc_tag = models.CharField(max_length=50, unique=True)
#     address = models.TextField()
#     inventory_number = models.CharField(max_length=50, unique=True)
#     article_number = models.CharField(max_length=50)
#     STATE_CHOICES = (
#         ('INVENTORY', 'In Inventory'),
#         ('CLIENT', 'At Client'),
#         ('TRANSPORT', 'In Transport'),
#         ('REPAIR', 'Under Repair'),
#     )
#     state = models.CharField(max_length=10, choices=STATE_CHOICES, default='INVENTORY')
#     monthly_cleanings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
#     market_name = models.CharField(max_length=100)
#     region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='toilets')
#
#     def __str__(self):
#         return f"Toilet {self.inventory_number} - {self.client.name if self.client else 'No Client'}"
#
#
# class Contract(models.Model):
#     client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='contracts')
#     toilets = models.ManyToManyField(Toilet, related_name='contracts')
#     contract_number = models.CharField(max_length=50, unique=True)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     document = models.FileField(upload_to='contracts/', null=True, blank=True)
#
#     def __str__(self):
#         return f"Contract {self.contract_number} - {self.client.name}"
#
#
# class WeeklySchedule(models.Model):
#     toilet = models.ForeignKey(Toilet, on_delete=models.CASCADE, related_name='schedules')
#     staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='assigned_schedules')
#     creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_schedules')
#     region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name='schedules')
#     DAY_CHOICES = (
#         ('MON', 'Monday'),
#         ('TUE', 'Tuesday'),
#         ('WED', 'Wednesday'),
#         ('THU', 'Thursday'),
#         ('FRI', 'Friday'),
#         ('SAT', 'Saturday'),
#         ('SUN', 'Sunday'),
#     )
#     day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)
#     STATUS_CHOICES = (
#         ('SCHEDULED', 'Scheduled'),
#         ('COMPLETED', 'Completed'),
#         ('MISSED', 'Missed'),
#         ('DELIVERY', 'Delivery'),
#         ('RECOVERY', 'Recovery'),
#     )
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='SCHEDULED')
#     notes = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return f"{self.get_status_display()} for {self.toilet} on {self.get_day_of_week_display()}"
#
#
# class HistoricalData(models.Model):
#     toilet = models.ForeignKey(Toilet, on_delete=models.SET_NULL, null=True, related_name='history')
#     toilet_inventory_number = models.CharField(max_length=50)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='historical_data')
#     user_name = models.CharField(max_length=150, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     EVENT_CHOICES = (
#         ('CLEANING', 'Cleaning'),
#         ('ISSUE', 'Issue Reported'),
#         ('NFC_CHANGE', 'NFC Tag Changed'),
#         ('STATE_CHANGE', 'State Changed'),
#         ('ADDRESS_CHANGE', 'Address Changed'),
#     )
#     event_type = models.CharField(max_length=20, choices=EVENT_CHOICES)
#     toilet_address = models.TextField()
#     gps_location = models.CharField(max_length=100, blank=True)
#     message = models.TextField(blank=True)
#     photo = models.ImageField(upload_to='event_photos/', null=True, blank=True)
#
#     def save(self, *args, **kwargs):
#         if self.user:
#             self.user_name = self.user.get_full_name() or self.user.username
#         if self.toilet:
#             self.toilet_inventory_number = self.toilet.inventory_number
#             self.toilet_address = self.toilet.address
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"{self.event_type} for Toilet {self.toilet_inventory_number} by {self.user_name} at {self.timestamp}"
