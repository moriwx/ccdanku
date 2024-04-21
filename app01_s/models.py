from django.db import models

# Create your models here.


class long_and_lati(models.Model):
    code = models.DecimalField(max_digits=32, decimal_places=0,primary_key=True)
    county = models.CharField(max_length=32)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    latitude = models.DecimalField(max_digits=6, decimal_places=4)
    #longitude = models.FloatField()
    #latitude = models.FloatField()
    


class location(models.Model):
    id_label = models.DecimalField(max_digits=32, decimal_places=0,primary_key=True)
    numbers = models.ForeignKey(long_and_lati, on_delete=models.CASCADE, blank=True, null=True)
    province = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
    county = models.CharField(max_length=32)


class reference(models.Model):
    id_label = models.DecimalField(max_digits=32, decimal_places=0,primary_key=True)
    ref = models.CharField(max_length=200)


class words(models.Model):
    id_label = models.DecimalField(max_digits=32, decimal_places=0, primary_key=True)
    words = models.CharField(max_length=32)
    meaning = models.CharField(max_length=150)
    pronunciation = models.CharField(max_length=100)
    sample_sentence = models.CharField(max_length=100)
    remarks = models.CharField(max_length=100)
    ref_source = models.ForeignKey(reference, on_delete=models.CASCADE, blank=True, null=True)
    county_number = models.ForeignKey(location, on_delete=models.CASCADE, blank=True, null=True)
    dialect_area = models.CharField(max_length=32)
    sub_dialect_area = models.CharField(max_length=32)
    dialect_field = models.CharField(max_length=32)
    sub_dialect_field = models.CharField(max_length=32)
    lenwords = models.DecimalField(max_digits=32, decimal_places=0)