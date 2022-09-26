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
            message="Voy genial! He entendido todo hasta ahora"
         elif str(materia)=="Investigacion Operativa":
            message="Voy re bien! Estoy al dia con los practicos"
         elif str(materia)=="Lenguajes de Programacion":
            message="Estoy un poco atrasada :c"
         elif str(materia)=="Bases de Datos":
            message="Me falta hacer el tp2 y terminar el tp3"
         elif str(materia)=="Sistemas Operativos":
            message="Me queda por ver la ultima clase subida"
         dispatcher.utter_message(text=str(message))
         return [SlotSet("materia",materia)]

#class ActionHorariosMateria(Action):

#     def name(self) -> Text:
#         return "action_horarios_materia"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         materia= tracker.get_slot("materia")
#         message="Los horarios de " + materia + " son: "
#         if str(materia)=="Programacion Exploratoria":
#            message=message+"miercoles de 13hs a 16hs"
#         elif str(materia)=="Investigacion Operativa":
#            message=message+"lunes de 15hs a 17hs y martes de 16hs a 18hs"
#         elif str(materia)=="Lenguajes de Programacion":
#            message=message+"martes de 13hs a 16hs y jueves de 14hs a 17hs"
#         elif str(materia)=="Bases de Datos":
#            message=message+"lunes de 9hs a 13hs y miercoles de 9hs a 12hs"
#         elif str(materia)=="Sistemas Operativos":
#            message=message+"martes de 10hs a 12hs y jueves de 9hs a 12hs"
#         dispatcher.utter_message(text=str(message))
#         return []

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
            mensaje="Los dias en que se cursa son: "+horarios[materia]['dia']+" de "+horarios[materia]['horario']
            dispatcher.utter_message(text=str(mensaje))
        else:
            mensaje= "no es una materia que reconozca"
            dispatcher.utter_message(text=str(mensaje))
        return []