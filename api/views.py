import json

from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
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
