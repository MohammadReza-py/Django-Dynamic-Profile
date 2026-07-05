# Profile Serializer
from django.apps import apps
from django.db import models
from django.forms import model_to_dict

class Serializer:
    denyFields = ['password', 'code', 'otp', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
    def __init__(self, model, userID):
        self.userID = userID
        self.MyModel: models.Model = apps.get_model(model.model_app, model.model_name)

    def getFields(self):
        fields = self.MyModel._meta.get_fields()
        return fields

    def recordObj(self):
        return self.MyModel.objects.filter(user=self.userID)

    def recordsValues(self):
        return self.MyModel.objects.values().filter(user=self.userID)

    def getModel(self, app, name):
        model = apps.get_model(app, name)
        return model

    def addDenyField(self, field_name):
        self.denyFields.append(field_name)

    def removeDenyField(self, field_name):
        self.denyFields.remove(field_name)

    def safeDecode(self, obj):
        object = {}
        for k, v in model_to_dict(obj).items():
            if k not in self.denyFields:
                v = str(v)
                object.update({k: v})
        return object

    def setSlugToLink(self, obj: dict):
        for k, v in obj.items():
            pass

    def getRecord(self, id):
        return self.recordObj.objects.filter(id=id)

    def serializedData(self):
        serializedRecords = {}
        for i in range(len(self.recordObj())):
            record = self.recordObj()[i]
            recordValue = self.recordsValues()[i]
            serializedRecord = {}
            for key, value in recordValue.items():
                if key[-2:] != 'id' or key == 'id':
                    serializedRecord[key] = value
                else:
                    object = getattr(record, key[:-3])
                    serializedRecord[key[:-3]] = self.safeDecode(object)

            serializedRecords.update({i: serializedRecord})
        return serializedRecords


# create a model as Profile with following fields
#    title = models.CharField(max_length=100, null=True, blank=True)
#    fa_title = models.CharField(max_length=100, null=True, blank=True)
#    model_app = models.CharField(max_length=100, null=True, blank=True)
#    model_name = models.CharField(max_length=100, null=True, blank=True)

# Use it in view by following codes;
# field = Profile.objects.filter(title=title).first()
# serializer = profile_serializer.Serializer(field, request.user.id)
