from django.http import JsonResponse
from django.views import View




from backend.model.bert import Bert
import pprint











class MessageView(View):
    bert_model = Bert("./backend/model/data")

    def post(self, request):
        message = request.POST.get('message')
        if not message:
            message = "Empty Message"

        response = self.process_message(message)

        return JsonResponse({'response': response})

    def process_message(self, message):
        response = self.bert_model.generate(message)
        pprint.pprint(response['answers'])
        return response['answers'][0].answer

message_view = MessageView.as_view()