import os
import json
import urllib.request
import numpy as np

from flask_restful import Resource, reqparse
from flask import request, jsonify
from Resources.calculateList import CalculateList


class GenerateGrade(Resource):
    def centroid(self, musics):
        n = len(musics)  # numero de musicas
        m = len(musics[0])  # numero de caracteristicas
        center = np.zeros(m)  # vetor centro das caracteristicas
        for music in musics:
            for i in range(m):
                center[i] = music[i] + center[i]
        center = center/n
        return center

    def sigmoid(self, x):
        return 1/(1+np.exp(-x))

    def post(self):
        try:
            # recebe como parametro de entrada o codigo da sala (code)
            parser = reqparse.RequestParser()
            args = parser.parse_args()
            data = request.data
            dataDict = json.loads(data)
            roomCode = dataDict['code']

            # busca na API as informacoes (antigo fetch do banco) recebendo
            # a resposta em json
            url = os.environ.get(
                "MAINAPI", "http://localhost:3001/v1")+"/rooms/"+roomCode+"/ia"
            body = {}
            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json; charset=utf-8')

            # jsondata = json.dumps(body)
            # jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
            # req.add_header('Content-Length', len(jsondataasbytes))
            response = urllib.request.urlopen(req)
            string = response.read().decode('utf-8')
            json_obj = json.loads(string)

            # guarda features das musicas em um dicionario e salva lista de ids das musicas
            tracks = dict()
            # guarda tracks de cada usuario em um dicionario
            userTracks = dict()
            trackList = []
            for track in json_obj:
                if track['user_id'] in userTracks:
                    userTracks[track['user_id']] = np.append(
                        userTracks[track['user_id']], track['track_id'])
                else:
                    userTracks[track['user_id']] = np.array(track['track_id'])
                trackList.append(track['track_id'])
                t = [track['feature']['danceability'],
                     track['feature']['energy'],
                     track['feature']['instrumentalness'],
                     track['feature']['liveness'],
                     track['feature']['speechiness'],
                     track['feature']['valence'],
                     track['feature']['acousticness'],
                     track['feature']['mode'],
                     self.sigmoid(track['feature']['duration_ms']),
                     self.sigmoid(track['feature']['key']),
                     self.sigmoid(track['feature']['time_signature']),
                     self.sigmoid(track['feature']['tempo']),
                     self.sigmoid(track['feature']['loudness'])]
                tracks[track['track_id']] = np.array(t)

            # calcula centroide e variancia do usuario, baseado em suas musicas, e cria uma lista com ids dos usuarios
            userList = []
            users = dict()
            for i in userTracks:
                userTracksFeatures = []
                for track in userTracks[i]:
                    userTracksFeatures.append(tracks[track])
                users[i] = [self.centroid(userTracksFeatures),
                            np.var(userTracksFeatures)]
                userList.append(i)

            # monta matriz com notas, cada linha representa um usuario e
            # cada coluna representa uma musica, a nota eh definida para todas
            # as musicas de todos os usuarios da sala a nota eh dada com base
            # na variancia das musicas de um usuario sobre a distancia entre o
            # centroide do usuario e as features da musica

            i = 0
            matrix = [[0 for x in range(3)]
                      for y in range(len(users) * len(tracks))]
            for user in users:
                for track in tracks:
                    matrix[i][0] = user
                    matrix[i][1] = track
                    # nota_maxima*var/dist
                    matrix[i][2] = 5*users[user][1] / \
                        np.linalg.norm(users[user][0]-tracks[track])
                    i = i+1
            # print(matrix)
            M, S = CalculateList().refined_pre_processing(matrix)
            songs = CalculateList().diversify_group_recommendation_the_algorithm(matrix, M, S, 5)
            # print(songs)
            return jsonify(songs)

        except Exception as e:
            return {'error': str(e)}
