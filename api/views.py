import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MidiFile
from .serializers import MidiFileSerializer
import outlier.outlier
from outlier.outlier import Outlier
from contrast_model.Contrast import *
import numpy as np
import music21


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def getCriteriaSign(s):
    sign = {
        "eq" : "=",
        "ls": "<",
        "gt": ">",
        "contain": "LIKE",
    }
    return sign[s]
def convert(o):
    if isinstance(o, np.generic): return o.item()
    raise TypeError
@csrf_exempt
def cluster(request):
    print(request.body)
    # Build query from request filter
    req = json.loads(request.body)
    SQL = "SELECT * from `song_v2` WHERE "
    for idx, query in enumerate(req["query"]):
        if idx > 0:
            SQL = SQL + " AND "
        value = query["value"]
        if query["criteria"] == "contain":
            value = "%" + value + "%"
        SQL = SQL + "`{}` {} '{}'".format(query["feature"], getCriteriaSign(query["criteria"]), value)
    SQL = SQL + " LIMIT {}".format(req["limit"])


    with connection.cursor() as cursor:
        cursor.execute(SQL)
        row = dictfetchall(cursor)

        out = Outlier()

        res=out.cluster(method="mean_shift",data=row)
        #res = json.dumps(res,default=convert)

        return JsonResponse(res, safe=False)

    return JsonResponse("Error", safe=False)

@csrf_exempt
def search(request):
    print(request.body)
    # Build query from request filter
    req = json.loads(request.body)
    SQL = "SELECT * from `song_v2` WHERE "
    for idx,query in enumerate(req["query"]):
        if idx > 0:
            SQL = SQL + " AND "
        value = query["value"]
        if query["criteria"] == "contain":
            value = "%" + value + "%"
        SQL = SQL + "`{}` {} '{}'".format(query["feature"],getCriteriaSign(query["criteria"]),value)
    SQL = SQL + " LIMIT {}".format(req["limit"])
    print(SQL)

    with connection.cursor() as cursor:
        #cursor.execute("SELECT * from `song_v2` LIMIT 100")
        cursor.execute(SQL)
        # row = cursor.fetchone()
        row = dictfetchall(cursor)
    return JsonResponse(row, safe=False)
    # data = {
    #     "1":1,
    # }
    # return JsonResponse(data)


class MidiFileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        midi_serializer = MidiFileSerializer(data=request.data)
        if midi_serializer.is_valid():
            midi_serializer.save()
            midi_file = midi_serializer.instance.file.path
            chords = self.analyze_midi(midi_file)
            return Response({'chords': chords}, status=200)
        else:
            return Response(midi_serializer.errors, status=400)

    def analyze_midi(self, file_path):
        # anlysis
        model = Contrast(file_path)
        return model.anlysis()