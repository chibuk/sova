# from rest_framework.renderers import JSONRenderer
# from rest_framework.viewsets import ModelViewSet

# from event.models import EventPage
# from event.serialisers import EventPageSerialiser
# from django.db.models import Q
# from datetime import datetime
# from wagtail.api.v2.views import PagesAPIViewSet


# class EventPageAPIListView(ModelViewSet):
#     serializer_class = EventPageSerialiser
#     queryset = EventPage.objects.all()
#     renderer_classes = [JSONRenderer]

#     def get_queryset(self):
#         param = self.request.query_params.get('dates', None)
#         if param is not None: 
#             dates_list = param.split(',')
#             date_on = datetime.strptime(dates_list[0], "%Y-%m-%d")
#             if len(dates_list) == 1:
#                 date_end = date_on
#             else:
#                 date_end = datetime.strptime(dates_list[1], "%Y-%m-%d")
#             queryset = EventPage.objects.live().filter((Q(date_on__gte=date_on) & Q(date_on__lte=date_end)) | 
#                                                        (Q(date_on__lt=date_end) & Q(date_end__gte=date_on)))
#         else:
#             queryset = []
#         return queryset
    

# class EventPagesAPIViewSet(PagesAPIViewSet):
#     model = EventPage
    
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         param = self.request.query_params.get('dates', None)    # Формат такой: ?dates=2025-01-01,2025-01-31
#         if param is not None: 
#             dates_list = param.split(',')
#             date_on = datetime.strptime(dates_list[0], "%Y-%m-%d")
#             if len(dates_list) == 1:                            # имеем только начальную дату ?dates=2025-01-01
#                 date_end = date_on
#             else:                                               # значит есть коечная дата ?dates=2025-01-01,2025-01-31
#                 date_end = datetime.strptime(dates_list[1], "%Y-%m-%d")
#             return queryset.filter((Q(date_on__gte=date_on) & Q(date_on__lte=date_end)) | 
#                                    (Q(date_on__lt=date_end) & Q(date_end__gte=date_on)))
#         else:                                                   # даты не указаны
#             return queryset.none()
    