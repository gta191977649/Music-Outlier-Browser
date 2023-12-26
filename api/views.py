import json

from django.shortcuts import render
from django.views.generic import View
from .utils import calculate_file_hash
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
    try:
        req = json.loads(request.body)

        # Build WHERE clause using list comprehension
        where_clauses = [
            "`{}` {} %s".format(query["feature"], getCriteriaSign(query["criteria"]))
            for query in req["query"]
        ]
        where_statement = " AND ".join(where_clauses)

        # Parameters for the query
        params = [
            "%{}%".format(query["value"]) if query["criteria"] == "contain" else query["value"]
            for query in req["query"]
        ]

        SQL = "SELECT * FROM `song_v2` WHERE {} LIMIT %s".format(where_statement)

        with connection.cursor() as cursor:
            cursor.execute(SQL, params + [req["limit"]])
            row = dictfetchall(cursor)

        out = Outlier()
        res = out.cluster(method="mean_shift", data=row)

        return JsonResponse(res, safe=False)

    except Exception as e:
        # Handle exceptions
        return JsonResponse({"error": str(e)}, safe=False, status=500)

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

    def post(self, request, *args, **kwargs):
        midi_serializer = MidiFileSerializer(data=request.data)
        if midi_serializer.is_valid():
            uploaded_file = request.FILES.get('file')
            file_hash = calculate_file_hash(uploaded_file)

            existing_file = MidiFile.objects.filter(file_hash=file_hash).first()
            if existing_file:
                print("File already exists, use existing file for analysis")
                chords = self.analyze_midi(existing_file.file.path)
            else:
                # Save new file and analyze
                midi_file = midi_serializer.save(file_hash=file_hash)
                chords = self.analyze_midi(midi_file.file.path)

            return Response({'chords': chords}, status=200)
        else:
            return Response(midi_serializer.errors, status=400)
    def analyze_midi(self, file_path):
        # anlysis
        model = Contrast(file_path)
        return model.anlysis()