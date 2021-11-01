from django.db import models

class Doctor(models.Model):
   name = models.CharField(max_length=200)
   def __str__(self):
       return f'{self.pk}번 의사 {self.name}'


# patient.doctors.all()
# doctor.patients_set.all() 가능하게하려면  -> doctor.patients.all()로 바뀜 -> ManyToManyField가 알아서 해줌
class Patient(models.Model):
   name = models.CharField(max_length=200)
   doctors = models.ManyToManyField(Doctor, related_name='patients')  # 한 환자에 의사 여러명 가능!
    # ManyToManyField는 Patient에서만 가능! -> 두번째로 만든 class에서 사용가능!

   def __str__(self):
       return f'{self.pk}번 환자 {self.name}'


# 보통 중계모델(Reservation) 사용하지만, ManyToManyField 사용하면 알아서 다 해줌
# class Reservation(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#
#     def __str__(self):  # db건드리는 것이 아니기때문에 다시 migration 할필요 없음
#         return f'{self.doctor.id}번 의사의 {self.patient.id}번 환자'
