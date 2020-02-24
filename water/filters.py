from rest_framework import filters


class DatetimeRangeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        timestamp_from = request.GET.get("from", None)
        timestamp_to = request.GET.get("to", None)

        if timestamp_from is not None:
            # date_from = datetime.fromisoformat(timestamp_from)
            date_from = timestamp_from
        if timestamp_to is not None:
            # date_to = datetime.fromisoformat(timestamp_to)
            date_to = timestamp_to

        if timestamp_from is not None and timestamp_to is not None:
            qs = queryset.filter(station_state__timestamp__range=[date_from, date_to])
            print(qs.query)
            return qs
        elif timestamp_from is not None:
            qs = queryset.filter(station_state__timestamp__gte=date_from)
            print(qs.query)
            return qs
        elif timestamp_to is not None:
            qs = queryset.filter(station_state__timestamp__lte=date_to)
            print(qs.query)
            return qs

        return queryset
