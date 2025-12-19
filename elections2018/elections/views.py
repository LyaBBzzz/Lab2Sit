from django.shortcuts import render
from django.db.models import Sum
from .models import Region, Territory, Precinct, Candidate, VoteResult


def index(request):
    regions = Region.objects.all().order_by("name")
    territories = Territory.objects.select_related("region").all()
    precincts = Precinct.objects.select_related("territory", "territory__region").all()
    candidates = Candidate.objects.all()

    total_by_candidate = (
        VoteResult.objects
        .values("candidate__name")
        .annotate(total_votes=Sum("votes"))
        .order_by("-total_votes")
    )

    total_by_region = (
        VoteResult.objects
        .values("precinct__territory__region__name")
        .annotate(total_votes=Sum("votes"))
        .order_by("precinct__territory__region__name")
    )

    context = {
        "regions": regions,
        "territories": territories,
        "precincts": precincts[:200],
        "candidates": candidates,
        "total_by_candidate": total_by_candidate,
        "total_by_region": total_by_region,
    }
    return render(request, "index.html", context)
