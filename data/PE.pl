materias(6111,"Introduccion a la Programacion I",1,1).
materias(6112,"Analisis Matematico I",1,1).
materias(6113,"Algebra I",1,1).
materias(6114,"Quimica",1,1).
materias(6121,"Ciencias de la Computacion I",1,2).
materias(6122,"Introduccion a la Programacion II",1,2).
materias(6123,"Algebra Lineal",1,2).
materias(6124,"Fisica General",1,2).
materias(6125,"Matematica Discreta",1,2).
materias(6211,"Ciencias de la Computacion II",2,1).
materias(6212,"Analisis y Dise�o de Algoritmos I",2,1).
materias(6213,"Introduccion a la Arquitectura de Sistemas",2,1).
materias(6214,"Analisis Matematico II",2,1).
materias(6215,"Electricidad y Magnetismo",2,1).
materias(6221,"Analisis y Dise�o de Algoritmos II",2,2).
materias(6222,"Comunicacion de Datos I",2,2).
materias(6223,"Probabilidades y Estadistica",2,2).
materias(6224,"Electronica Digital",2,2).
materias(6311,"Programacion Orientada a Objetos",3,1).
materias(6312,"Estructuras de Almacenamiento de Datos",3,1).
materias(6313,"Metodologias de Desarrollo de Software",3,1).
materias(6314,"Arquitectura de Computadoras I",3,1).
materias(6321,"Programacion Exploratoria",3,2).
materias(6322,"Base de Datos I",3,2).
materias(6323,"Lenguajes de Programacion I",3,2).
materias(6324,"Sistemas Operativos I",3,2).
materias(6325,"Investigacion Operativa I",3,2).
materias(6411,"Arquitectura de Computadoras y Tecnicas Digitales",4,1).
materias(6412,"Teoria de la Informacion",4,1).
materias(6413,"Comunicacion de Datos II",4,1).
materias(6414,"Introduccion al Calculo Diferencial e Integral",4,1).
materias(6421,"Dise�o de Sistemas de Software",4,2).
materias(6422,"Dise�o de Compiladores I",4,2).
materias(6511,"Ingenieria de Software",5,1).

%materias que no tienen correlativas
correlativa(6111,[]).
correlativa(6112,[]).
correlativa(6113,[]).
correlativa(6114,[]).
correlativa(6121,[]).
%materias que tienen una sola correlativa
correlativa(6122,[6111]).
correlativa(6123,[6113]).
correlativa(6124,[6112]).
correlativa(6125,[6113]).
correlativa(6213,[6122]).
correlativa(6214,[6112]).
correlativa(6215,[6124]).
correlativa(6222,[6213]).
correlativa(6224,[6215]).
correlativa(6311,[6221]).
correlativa(6313,[6221]).
correlativa(6321,[6221]).
correlativa(6323,[6311]).
correlativa(6411,[6314]).
correlativa(6414,[6214]).
correlativa(6422,[6323]).
correlativa(6511,[6421]).
%materias que tienen dos correlativas
correlativa(6221,[6211,6212]).
correlativa(6312,[6221,6223]).
correlativa(6314,[6213,6224]).
correlativa(6322,[6312,6313]).
correlativa(6324,[6312,6314]).
correlativa(6325,[6214,6223]).
correlativa(6413,[6222,6324]).
%materias que tienen tres correlativas
correlativa(6211,[6121,6122,6125]).
correlativa(6212,[6121,6122,6125]).
correlativa(6223,[6214,6123,6125]).
correlativa(6412,[6212,6222,6223]).
correlativa(6421,[6311,6322,6324]).

mostrar_correlativas([]).
mostrar_correlativas([Primera|Resto]) :-
	materias(Primera,Nombre,_,_),
	((length(Resto,0),
		write(Nombre),
		write('.'));
	(not(length(Resto,0)),
		write(Nombre),
		write(', '))),
	mostrar_correlativas(Resto).

correlativas_plan(X) :-
	materias(X,_,_,_),
	correlativa(X,Y),
	((length(Y,0), write(' ---- Sin correlativas.'));
	(not(length(Y,0)), write(' ---- Correlativas: '), mostrar_correlativas(Y))).

materias_de(X):- 
	write('Materias de: '),
	writeln(X),
	materias(_,Nombre,X,_),
	write(-Nombre),
	nl,fail;nl.

primer_elemento([X|_],X).

materias_con_una_correlativa :- 
	correlativa(Y,X),
	length(X,1),
	primer_elemento(X,A),
	materias(Y,Z,_,_),materias(A,T,_,_),
	write('Para hacer '),write(Z),write(' solo necesitas '),write(T),
	nl,fail;nl.

plan_is :-
	writeln('Las materias de Ingenieria en Sistemas son: '),
	materias(Cod,Nombre,Anio,Cuatrimestre),
	nl,
	write('Anio:'),write(Anio),
	write(' Cuatrimestre:'),write(Cuatrimestre),
	write(' Nombre:'),write(Nombre),
	correlativas_plan(Cod),
	nl,fail;nl.

materias_cursando(L):- findall(Nombre,(materias(_,Nombre,3,2)),L).

materias_de(X,L):- findall(Nombre,(materias(_,Nombre,X,_)),L).