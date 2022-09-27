# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from swiplserver import PrologMQI, PrologThread

import random
import os.path
import json

class ActionEstadoMateria(Action):

     def name(self) -> Text:
         return "action_estado_materia"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         materia= tracker.latest_message['entities'][0]['value']
         if str(materia)=="Programacion Exploratoria":
            message="Voy genial! Al dia!"
         elif str(materia)=="Investigacion Operativa":
            message="Voy re bien! Estoy al dia con los practicos"
         elif str(materia)=="Lenguajes de Programacion":
            message="Estoy un poco atrasada :c"
         elif str(materia)=="Bases de Datos":
            message="Me falta terminar tp2, tp3 y hacer tp4"
         elif str(materia)=="Sistemas Operativos":
            message="Estoy al dia!"
         dispatcher.utter_message(text=str(message))
         return [SlotSet("materia",materia)]

class ActionOpinionMateria(Action):

     def name(self) -> Text:
         return "action_opinion_materia"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         materia= tracker.get_slot("materia")
         if str(materia)=="Programacion Exploratoria" or str(materia)=="Bases de Datos":
            message="Me encanta! me parece super util y necesaria"
         elif str(materia)=="Investigacion Operativa":
            message="Me gusta! creo que tiene contenidos aplicables en el futuro"
         elif str(materia)=="Lenguajes de Programacion" or str(materia)=="Sistemas Operativos":
            message="Se me hace un poco larga y tediosa"
         dispatcher.utter_message(text=str(message))
         return []

class OperarArchivo():

    @staticmethod
    def guardar(AGuardar):
        with open(".\\actions\\datos","w") as archivo_descarga:
            json.dump(AGuardar, archivo_descarga, indent=4)
        archivo_descarga.close()

    @staticmethod
    def cargarArchivo(): 
        if os.path.isfile(".\\actions\\datos"):
            with open(".\\actions\\datos","r") as archivo_carga:
                retorno=json.load(archivo_carga)
                archivo_carga.close()
        else:
            retorno={}
        return retorno

class ActionExtraerDatosHorarios(Action):
    def name(self) -> Text:
       return "action_horarios_materia"

    def run(self, dispatcher: CollectingDispatcher,tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        materia= tracker.get_slot("materia")
        horarios= OperarArchivo.cargarArchivo()
        if materia in horarios:
            mensaje=f"{materia} se cursa los "+horarios[materia]['dia']+" de "+horarios[materia]['horario']
            dispatcher.utter_message(text=str(mensaje))
        else:
            mensaje= "No es una materia que reconozca"
            dispatcher.utter_message(text=str(mensaje))
        return []

class ActionPROLOGMateriasCursando(Action):

    def name(self) -> Text:
        return "action_materias_cursando"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                        prolog_thread.query_async(r"consult('C:\\RASA Personal\\data\\PE.pl')", find_all=False)
                        prolog_thread.query_async(f"materias_cursando(Lista)", find_all=False)
                        result = prolog_thread.query_async_result()[0]['Lista']
                        dispatcher.utter_message(f"Estoy cursando las 5 del 2do cuatri de 3er año de Sistemas: \n")
                        for materia in result:
                            dispatcher.utter_message(text= f"- {materia}")
            return[]

class ActionPROLOGMateriasAnio(Action):

    def name(self) -> Text:
        return "action_materias_de_anio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            with PrologMQI(port=8000) as mqi:
                with mqi.create_thread() as prolog_thread:
                        prolog_thread.query_async(r"consult('C:\\RASA Personal\\data\\PE.pl')", find_all=False)
                        anio= next(tracker.get_latest_entity_values("anio"),None)
                        if (int(anio) < 6):
                            prolog_thread.query_async(f"materias_de({anio},Lista)", find_all=False)
                            result = prolog_thread.query_async_result()[0]['Lista']
                            dispatcher.utter_message(f"Materias de {anio} : \n")
                            for materia in result:
                                dispatcher.utter_message(text= f"- {materia}")
                        else:
                            dispatcher.utter_message(text= "La duracion de la carrera es de 5 años!")
            return[]