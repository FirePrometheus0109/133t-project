from django.contrib.postgres import aggregates
from django.contrib.postgres import search
from django.db import models as orm

SEARCH_VECTOR = (
    # single values which dont duplicate output results
    search.SearchVector(
        'user__first_name',
        weight='D'
    )
    +
    search.SearchVector(
        'user__last_name',
        weight='D'
    )
    +
    search.SearchVector(
        'about',
        weight='B'
    )
    +
    search.SearchVector(
        'address__city__name',
        weight='D'
    )
    +
    search.SearchVector(
        'address__city__state__name',
        weight='D'
    )
    +
    search.SearchVector(
        'address__zip__code',
        weight='D'
    )
    # Multiple values for one job_seeker which can multiply ouput results
    +
    search.SearchVector(
        aggregates.StringAgg(
            'skills__name',
            delimiter=' '
        ),
        weight='C'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'job_experience__company',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'job_experience__description',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'educations__institution',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'educations__field_of_study',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'educations__description',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'certifications__description',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'certifications__institution',
            delimiter=' '
        ),
        weight='D'
    )
    +
    search.SearchVector(
        aggregates.StringAgg(
            'certifications__field_of_study',
            delimiter=' '
        ),
        weight='D'
    )
    # search only by titles of current jobs, most relevant value
    +
    search.SearchVector(
        aggregates.StringAgg(
            orm.Case(
                orm.When(
                    job_experience__is_current=True,
                    then='job_experience__job_title'),
                default=orm.Value(''),
                output_field=orm.CharField()),
            delimiter=' '
        ),
        weight='A'
    )
)

LOCATION_SEARCH_VECTOR = (
    search.SearchVector(
        'address__city__name',
        weight='A'
    )
    +
    search.SearchVector(
        'address__city__state__abbreviation',
        weight='B'
    )
    +
    search.SearchVector(
        'address__zip__code',
        weight='C'
    )
)
