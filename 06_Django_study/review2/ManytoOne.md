# ManytoOne

```python
# model
from django.db import models

class Doctor(models.Model):
   name = models.CharField(max_length=200)
   def __str__(self):
       return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
   name = models.CharField(max_length=200)
#    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
   def __str__(self):
       return f'{self.pk}번 환자 {self.name}'


class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):  # db건드리는 것이 아니기때문에 다시 migration 할필요 없음
        return f'{self.doctor.id}번 의사의 {self.patient.id}번 환자'
```



```bash
# migrate 후 $ python manage.py shell_plus
In [2]: Doctor.objects.create(name='Justin')
Out[2]: <Doctor: 1번 의사 Justin>

In [3]: Patient.objects.create(name='Gayoung')
Out[3]: <Patient: 1번 환자 Gayoung>

In [4]: doctor1 = Doctor.objects.get(pk=1)

In [5]: patient1 = Patient.objects.get(pk=1)

In [6]: Reservation.objects.create(doctor=doctor1, patient=patient1)
Out[6]: <Reservation: 1번 의사의 1번 환자>

In [7]: # 의사가 예약한 환자찾기

In [8]: doctor1.reservation_set.all()
Out[8]: <QuerySet [<Reservation: 1번 의사의 1번 환자>]>

In [9]: patient1.reservation_set.all()
Out[9]: <QuerySet [<Reservation: 1번 의사의 1번 환자>]>

In [10]: doctor1
Out[10]: <Doctor: 1번 의사 Justin>

In [11]: patient2 = Patient.objects.create(name='Harry')

In [12]: Reservation.objects.create(doctor=doctor1, patient=patient2)
Out[12]: <Reservation: 1번 의사의 2번 환자>

In [13]: doctor1.reservation_set.all()
Out[13]: <QuerySet [<Reservation: 1번 의사의 1번 환자>, <Reservation: 1번 의사의 2번 환자>]>

In [14]: for reservation in doctor1.reservation_set.all():
    ...:     print(reservation.patient.name)
    ...: 
Gayoung
Harry
```



- 위와 동일!!

```python
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
```

```bash
In [1]: doctor1 = Doctor.objects.create(name='쑤')

In [2]: patient1 = Patient.objects.create(name='성워니')

In [3]: doctor1
Out[3]: <Doctor: 1번 의사 쑤>

In [4]: patient1
Out[4]: <Patient: 1번 환자 성워니>

In [5]: doctor1.patients.add(patient1)

In [6]: doctor1.patients.all()
Out[6]: <QuerySet [<Patient: 1번 환자 성워니>]>

# 예약 취소 - 환자입장
In [7]: patient1.doctors.remove(doctor1)

In [8]: patient1.doctors.all()
Out[8]:<QuerySet []>

# 예약 취소 - 의사입장
In [8]: doctor1.patients.all()
Out[8]:<QuerySet []>
```

