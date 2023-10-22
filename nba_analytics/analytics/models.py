from django.db import models

# Create your models here.
# analytics/models.py

class NBAPlayer(models.Model):
    name = models.CharField(max_length=255)
    gp = models.PositiveIntegerField()
    min = models.DecimalField(max_digits=5, decimal_places=2)
    pts = models.DecimalField(max_digits=5, decimal_places=2)
    fgm = models.DecimalField(max_digits=5, decimal_places=2)
    fga = models.DecimalField(max_digits=5, decimal_places=2)
    fg = models.DecimalField(max_digits=5, decimal_places=2)
    three_p_made = models.DecimalField(max_digits=5, decimal_places=2)
    three_p_a = models.DecimalField(max_digits=5, decimal_places=2)
    three_p = models.DecimalField(max_digits=5, decimal_places=2)
    ftm = models.DecimalField(max_digits=5, decimal_places=2)
    fta = models.DecimalField(max_digits=5, decimal_places=2)
    ft = models.DecimalField(max_digits=5, decimal_places=2)
    oreb = models.DecimalField(max_digits=5, decimal_places=2)
    dreb = models.DecimalField(max_digits=5, decimal_places=2)
    reb = models.DecimalField(max_digits=5, decimal_places=2)
    ast = models.DecimalField(max_digits=5, decimal_places=2)
    stl = models.DecimalField(max_digits=5, decimal_places=2)
    blk = models.DecimalField(max_digits=5, decimal_places=2, default = 0)
    tov = models.DecimalField(max_digits=5, decimal_places=2)
    target_5yrs = models.BooleanField()

    def __str__(self):
        return self.name

    #name = models.CharField(max_length=100)
    #team = models.CharField(max_length=50)
    #points_per_game = models.DecimalField(max_digits=5, decimal_places=2)
    # Add more fields for other player attributes
