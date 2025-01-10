from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet

from event.models import EventPage
from datetime import datetime
from django.db.models import Q

api_router = WagtailAPIRouter('wagtailapi')

api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)



class EventPagesAPIViewSet(PagesAPIViewSet):
    """
    Своя точка входа для получения из диапазона дат страниц EventPage
    При этом сохраняется вся функциональность wagtail.api.v2
    Пример запроса: /events/?dates=2025-01-11,2025-02-02&fields=date_on,date_end,h1,h2&order=date_on
    """
    model = EventPage
    
    def check_query_parameters(self, queryset):
        """
        Ensure that only valid query parameters are included in the URL.
        Перегружаю этот метод для разрешения своего параметра - 'dates=YYYY-mm-dd,YYYY-mm-dd'
        Это позволит переопределить get_queryset
        """
        query_parameters = set(self.request.GET.keys())

        # All query parameters must be either a database field or an operation
        allowed_query_parameters = set(
            self.get_available_fields(queryset.model, db_fields_only=True)
        ).union(self.known_query_parameters).union(['dates'])   # Чтобы разрешить свой параметр ?dates=025-01-01,2025-01-31
        unknown_parameters = query_parameters - allowed_query_parameters
        if unknown_parameters:
            raise BadRequestError(
                "query parameter is not an operation or a recognised field: %s"
                % ", ".join(sorted(unknown_parameters))
            )
    
    def get_queryset(self):
        """
        Переопределение для фильтрации по дате начала события и дате его окончания
        Вернёт только события из запрошенного диапазона дат date_on и date_end
        """
        queryset = super().get_queryset()
        param = self.request.query_params.get('dates', None)    # Формат такой: ?dates=2025-01-01,2025-01-31
        if param is not None: 
            dates_list = param.split(',')
            date_on = datetime.strptime(dates_list[0], "%Y-%m-%d")
            if len(dates_list) == 1:                            # имеем только начальную дату ?dates=2025-01-01
                date_end = date_on
            else:                                               # значит есть коечная дата ?dates=2025-01-01,2025-01-31
                date_end = datetime.strptime(dates_list[1], "%Y-%m-%d")
            return queryset.filter((Q(date_on__gte=date_on) & Q(date_on__lte=date_end)) | 
                                   (Q(date_on__lt=date_end) & Q(date_end__gte=date_on)))
        else:                                                   # даты не указаны
            return queryset.none()
    

api_router.register_endpoint("events", EventPagesAPIViewSet)
