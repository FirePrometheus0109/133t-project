from django.contrib.postgres import aggregates
from django.contrib.postgres import search


SEARCH_VECTOR = (
    # single values which dont duplicate output results
    search.SearchVector(
        'title',
        weight='A'
    )
    +
    search.SearchVector(
        'description',
        weight='B'
    )
    +
    search.SearchVector(
        'industry__name',
        weight='D'
    )
    +
    search.SearchVector(
        'location__city__name',
        weight='D'
    )
    +
    search.SearchVector(
        'location__city__state__name',
        weight='D'
    )
    +
    search.SearchVector(
        'location__zip__code',
        weight='D'
    )
    +
    search.SearchVector(
        'company__name',
        weight='D'
    )
    +
    # skills can multiply ouput results
    search.SearchVector(
        aggregates.StringAgg(
            'job_skill_set__skill__name',
            delimiter=' '
        ),
        weight='C'
    )
)


LOCATION_SEARCH_VECTOR = (
    search.SearchVector(
        'location__zip__code',
        weight='A'
    )
    +
    search.SearchVector(
        'location__city__name',
        weight='B'
    )
    +
    search.SearchVector(
        'location__city__state__abbreviation',
        weight='C'
    )
)
