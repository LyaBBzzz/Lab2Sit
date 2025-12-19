from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name


class Territory(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="territories")
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.region})"


class Precinct(models.Model):
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE, related_name="precincts")
    precinct_number = models.CharField(max_length=16)
    registered_voters = models.IntegerField()
    ballots_issued = models.IntegerField()
    ballots_valid = models.IntegerField()
    ballots_invalid = models.IntegerField()

    def __str__(self):
        return f"УИК {self.precinct_number} ({self.territory})"


class Candidate(models.Model):
    name = models.CharField(max_length=128)
    party = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name


class VoteResult(models.Model):
    precinct = models.ForeignKey(Precinct, on_delete=models.CASCADE, related_name="results")
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="results")
    votes = models.IntegerField()

    class Meta:
        unique_together = ("precinct", "candidate")
