from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Vote

def vote(request):
    if request.method == "POST":
        selected = request.POST.get("choice")
        if selected:
            Vote.objects.create(choice=selected)

    total_votes = Vote.objects.count()

    count_a = Vote.objects.filter(choice="Option A").count()
    count_b = Vote.objects.filter(choice="Option B").count()
    count_c = Vote.objects.filter(choice="Option C").count()

    def percent(count):
        return int((count / total_votes) * 100) if total_votes > 0 else 0

    context = {
        "count_a": count_a,
        "count_b": count_b,
        "count_c": count_c,
        "percent_a": percent(count_a),
        "percent_b": percent(count_b),
        "percent_c": percent(count_c),
        "total": total_votes,
    }

    return render(request, "poll/vote.html", context)

