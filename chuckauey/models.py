from __future__ import unicode_literals

from django.db import models

class OnstreetParkingBaySensors(models.Model):
    bay_id = models.FloatField(db_column='Bay_id', blank=True, null=True)  # Field name made lowercase.
    st_marker_id = models.CharField(db_column='St_marker_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=255, blank=True, null=True)  # Field name made lowercase.
    location = models.CharField(db_column='Location', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lat = models.FloatField(db_column='Lat', blank=True, null=True)  # Field name made lowercase.
    lon = models.FloatField(db_column='Lon', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'onstreet_parking_bay_sensors'


class OnstreetParkingBays(models.Model):
    the_geom = models.CharField(db_column='The_geom', max_length=255, blank=True, null=True)  # Field name made lowercase.
    meter_id = models.CharField(db_column='Meter_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    bay_id = models.FloatField(db_column='Bay_id', blank=True, null=True)  # Field name made lowercase.
    marker_id = models.CharField(db_column='Marker_id', max_length=255, blank=True, null=True)  # Field name made lowercase.
    last_edit = models.FloatField(db_column='Last_edit', blank=True, null=True)  # Field name made lowercase.
    rd_seg_id = models.FloatField(db_column='Rd_seg_id', blank=True, null=True)  # Field name made lowercase.
    rd_seg_dsc = models.CharField(db_column='Rd_seg_dsc', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'onstreet_parking_bays'