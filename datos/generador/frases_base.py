"""Frases base del dataset de FinanzIA, con las 11 categorías del agente.

Formato:  texto ; monto mínimo ; monto máximo   (miles de pesos, 2026)
Las líneas en minúscula imitan cómo escribe la gente de afán (jerga, sin tildes).
Etiquetadas con la guía: lo que se compra para vender o producir es Mercancía e insumos.
"""

FRASES = {
"Alimentación en casa": """
Mercado quincenal en el D1;120;260
Mercado del mes en el Éxito;250;520
Arroz, aceite y granos en Ara;40;110
Frutas y verduras en la plaza de mercado;20;60
Pan y huevos para el desayuno;6;15
Leche, queso y jamón en la tienda;12;30
Carne y pollo en la carnicería;30;90
Pollo asado para almorzar en casa;25;40
Mercado en Olímpica el fin de semana;80;200
Cubeta de huevos;14;22
Verduras en el fruver;15;45
Granola y yogur en Carulla;15;30
Salchichas y pan para la comida;12;25
Mercado pequeño en la tienda del barrio;20;60
Botellón de agua para la casa;8;15
Enlatados y atún en Ara;25;60
Panela, sal y azúcar;8;18
Café molido para la casa;15;30
Pechuga para la semana;20;45
Pescado en la plaza;25;60
Mercado grande en Makro;150;400
Aceite y mantequilla;15;35
Tomate, cebolla y papa;10;25
Pan tajado y arequipe;8;14
Queso campesino en la plaza;10;20
Mercado por Rappi Turbo;40;120
Leche deslactosada y cereal;12;25
Arepas para la semana;6;12
remesa del mes;200;450
Mercado semanal en el Ara del barrio;60;150
Libra de arroz y frijol;8;15
Plátano y yuca para el sancocho;8;18
Costilla para el caldo;12;25
Carne molida para la casa;15;30
Cebolla larga y tomate para el hogao;5;12
Leche para los niños;10;25
Bolsa de leche y pan de la mañana;6;12
Arroz, lentejas y garbanzos;12;25
Mercado para la olla de la semana;50;120
Huevos y arepas para el desayuno de la casa;10;20
Frutas para los jugos de la casa;10;25
Chocolate en pastilla y panela;8;15
Pasta y salsa de tomate;8;18
Pollo despresado para la semana;20;45
Cilantro, ajo y cebolla;3;8
Mantequilla y queso para las arepas;10;20
Avena en hojuelas y leche;8;16
Galletas para la lonchera de los niños;5;12
Papa criolla y arveja;6;15
Sardinas y atún para la casa;10;25
Café y azúcar para la casa;12;25
mercado en el D1 pa la semana;60;150
verduras pa la casa;10;30
""",
"Comidas fuera de casa": """
Almuerzo corrientazo cerca a la U;14;20
Almuerzo ejecutivo en el centro;16;25
Tinto en Juan Valdez;4;8
Café con leche en Tostao;3;7
Empanada y gaseosa en la esquina;4;8
Arepa con queso en la calle;3;7
Buñuelo y avena en la panadería;4;9
Pandebono y tinto a media mañana;4;8
Desayuno caldo de costilla;10;16
Almuerzo en el casino de la universidad;10;16
Galletas y jugo en Oxxo;5;12
Botella de agua en la calle;2;4
Paquete de papas y gaseosa;4;8
Chocolatina y chicles en la tienda;2;6
Bananos y manzanas en el carrito de frutas;4;10
Almuerzo de menú del día en restaurante;15;22
Tamal y chocolate el domingo;8;16
Sopa y seco en el restaurante del barrio;13;18
Calentado y jugo en la panadería;12;20
Fruta picada en la calle;3;6
Pony Malta y Chocoramo;4;7
Gaseosa personal Postobón;3;5
Almuerzo en la cafetería del trabajo;12;18
Croissant y café en panadería;8;15
Jugo natural en la cafetería;4;8
Tinto y aromática en la esquina;2;4
Ensalada de frutas en la universidad;6;10
un tintico;2;3
mecato pa la tarde;3;8
algo de comer en la U;5;12
Pizza por Rappi;35;60
Hamburguesa en El Corral con amigos;30;55
Helado en Popsy el domingo;10;20
Domicilio de sushi el sábado;60;120
Comida en Crepes & Waffles;45;90
Salchipapa en el parque con amigos;15;30
Domicilio de alitas por Rappi;40;70
Almuerzo de negocios con un cliente;40;90
Bandeja paisa en restaurante;25;40
Perro caliente en la calle;6;12
Chorizo con arepa en el puesto;5;10
Caldo de pescado en el restaurante;15;30
Pastel de pollo y gaseosa;5;10
Almuerzo en el centro comercial;20;40
Desayuno en la cafetería de la estación;8;15
Obleas en el parque;4;8
Mazorca asada en la calle;5;10
Jugo de mango en la plaza;4;8
Lechona en la esquina;8;15
Sándwich y jugo en la cafetería;10;18
Hamburguesa de la calle;10;20
Pollo broaster con papas;15;30
Arepa de huevo en la esquina;4;8
algo pa la sed;2;5
""",
"Transporte": """
Pasaje de TransMilenio;3;4
Recarga tarjeta TuLlave;10;50
Recarga tarjeta SITP;10;30
Uber a la universidad;9;25
DiDi de regreso a la casa;8;22
Taxi carrera mínima;7;12
Picap para llegar a clase;5;10
inDrive al aeropuerto;35;60
Gasolina para la moto;20;40
Tanqueada del carro en Terpel;100;220
Parqueadero del centro comercial;5;15
Parqueadero mensual del edificio;120;250
Peaje vía a Girardot;14;20
Cambio de aceite de la moto;35;70
Revisión técnico-mecánica;220;320
SOAT de la moto;250;550
Lavada del carro;20;40
Bus intermunicipal a Zipaquirá;8;15
Pasaje de bus a Medellín;80;140
Bicicleta compartida Tembici;5;15
Patineta eléctrica por minutos;4;12
Despinchada de la bicicleta;10;25
Repuesto de frenos de la moto;40;120
Colectivo hasta la casa;3;4
Mototaxi en el barrio;3;6
Cabify al trabajo;10;25
Uber Moto al centro;6;12
Taxi de madrugada después del turno;15;30
Recarga de la Cívica en Medellín;10;40
Pasaje del Metro de Medellín;3;4
Pasaje del MIO en Cali;3;4
Gasolina corriente para el carro;80;180
ACPM para la camioneta;100;250
Montallantas;8;20
Batería nueva para la moto;150;300
Lavado de la moto;10;18
Renovación de la licencia de conducción;150;250
Peaje de regreso a Bogotá;12;20
Parqueo en la calle con el cuidandero;2;5
Propina al cuidador de carros;1;3
Bus intermunicipal a Tunja;25;40
Taxi desde la terminal;15;30
Uber compartido con amigos;5;12
DiDi Moto para no llegar tarde;5;10
Recarga TuLlave en la estación;20;50
TransMilenio ida y vuelta;6;8
Mantenimiento de la bicicleta;30;70
Casco nuevo para la moto;120;300
Gasolina para ir a la finca;60;150
Taxi a la cita médica;12;25
Parqueadero de la universidad;4;10
Peaje y gasolina del paseo;80;200
el bus;3;4
transmi pa la U;3;4
carrera en taxi;8;20
tanquear la moto;20;40
Taxi para la reunión con un cliente;15;30
Cuota mensual del seguro del carro;150;350
""",
"Vivienda y servicios": """
Arriendo del apartamento;900;1800
Arriendo de la habitación;450;800
Factura de energía Enel;60;180
Recibo del agua del acueducto;40;120
Factura de gas natural Vanti;20;60
Internet hogar Claro fibra;70;120
Plan de celular Tigo;35;70
Plan pospago Movistar;40;90
Recarga de datos WOM;10;25
Administración del conjunto;150;400
Recibo de la luz;50;150
Internet de ETB;60;110
Recarga de minutos Claro;5;20
Plan de datos para el celular;20;50
Pipeta de gas;60;95
Depósito del arriendo nuevo;500;1500
Tasa de aseo en el recibo;15;40
Impuesto predial del apartamento;300;900
Administración del edificio;120;300
Paquete de datos semanal;10;20
Factura del celular;40;80
Internet del apartamento;60;100
Agua y alcantarillado;40;110
Servicios públicos del mes;200;400
Luz de la casa;50;140
Gas de la cocina;20;50
Arriendo compartido con mi roomie;400;700
Cuota de vigilancia del barrio;15;40
Plan Claro hogar internet y telefonía;90;150
Recibo de Codensa;60;170
Mudanza en camión;250;600
Factura del agua EAAB;40;120
Recarga Tigo prepago;5;20
Wifi del apartamento;60;100
Recibo de gas de Gases de Occidente;20;60
Factura de EPM;80;250
Arriendo del cuarto en Chapinero;500;900
Reconexión del servicio de luz;40;90
Plan ilimitado de Movistar;50;90
Fibra óptica de Movistar;70;120
Recibo de energía de Air-e;70;220
Arriendo de la casa;800;1600
Cuota extraordinaria de administración;100;400
Recarga de datos en el Éxito;10;30
Instalación de internet;50;120
Cuarto amoblado;600;1000
Servicio de agua de la finca;20;60
el arriendo;500;1500
la luz;50;150
recibo del gas;20;60
pague el internet;60;100
plan del cel;30;70
admin del conjunto;150;350
recarga del celu;10;30
""",
"Salud": """
Medicamentos en Droguería La Rebaja;15;80
Acetaminofén y antigripal en Cruz Verde;8;25
Cuota moderadora de la EPS;4;10
Consulta de odontología particular;60;150
Examen de sangre en el laboratorio;25;90
Gafas formuladas en la óptica;150;600
Vitaminas en la farmacia;20;60
Sesión de terapia física;40;90
Consulta con el dermatólogo;100;250
Limpieza dental;60;140
Ecografía particular;80;200
Mensualidad de la medicina prepagada;250;600
Copago de la cirugía;100;500
Vacuna contra la influenza;40;90
Ibuprofeno en la droguería;5;15
Lentes de contacto;80;200
Consulta con el psicólogo;80;180
Cita particular con médico general;50;120
Suero y pañitos para el resfriado;10;25
Crema formulada por el dermatólogo;40;120
Radiografía de la muñeca;50;120
Cuota mensual de ortodoncia;100;200
Urgencias en clínica particular;150;400
Exámenes de laboratorio de rutina;40;120
Inhalador recetado;30;70
Antialérgico en Farmatodo;10;35
Curitas y alcohol;5;15
Termómetro digital;20;45
Tapabocas en la droguería;3;10
Gotas para los ojos;15;40
Consulta de nutricionista;70;150
Fisioterapia de la rodilla;45;90
Pastillas para el dolor de cabeza;5;15
Antibiótico recetado;20;60
Cita de control en la EPS;4;10
Montura nueva en la óptica;100;350
Plan complementario de salud;100;250
Domicilio de la droguería;15;50
Botiquín de primeros auxilios;25;60
Audiometría;40;90
Terapia de lenguaje;50;100
Electrocardiograma particular;50;120
Copago de medicamentos de la EPS;5;20
Jarabe para la tos;12;30
Nebulizador para la casa;80;180
Examen de la vista;30;80
Resonancia magnética copago;100;400
Sesión de acupuntura;60;120
Consulta de urgencias odontológicas;80;200
Prueba de covid;40;90
la drogueria;10;50
remedios pa la gripa;10;30
cita medica;30;100
el odontologo;60;150
pastillas;5;30
""",
"Educación": """
Pago parcial del semestre;1500;4500
Matrícula de la universidad;2000;6000
Curso online en Platzi;40;100
Curso de inglés en Udemy;30;80
Fotocopias e impresiones para la U;2;10
Cuadernos y esferos en Panamericana;15;50
Libro para la clase de cálculo;60;180
Inscripción al diplomado;300;1200
Impresión y anillado del trabajo final;10;30
Calculadora científica;60;140
Mensualidad del instituto de inglés;250;500
Derechos de grado;300;900
Certificado de notas;10;30
Duplicado del carné estudiantil;15;30
Materiales para el laboratorio;20;80
Curso de Excel avanzado;80;250
Inscripción al seminario de investigación;50;200
Tutoría de matemáticas;30;60
Clases particulares de física;35;70
Inscripción a las pruebas Saber Pro;100;160
Examen TOEFL;800;1000
Útiles escolares de mi hermanito;50;150
Pensión del colegio del niño;250;800
Mensualidad de Coursera;150;200
Diccionario de inglés;30;70
Planos impresos para la clase de arquitectura;15;50
USB para guardar los trabajos de la U;20;45
Marcadores y cartulina para la exposición;10;30
Inscripción a congreso académico;100;400
Póster académico impreso;30;80
Fotocopias de las guías;3;10
Duolingo Super;30;50
Bata de laboratorio;40;90
Kit de dibujo técnico;50;120
Curso de programación en Domestika;40;100
Taller de escritura;100;250
Materias del intersemestral;400;1200
Libro de texto usado;20;60
Multa de la biblioteca;2;10
Formulario de inscripción a la universidad;80;150
Curso preparatorio para el ICFES;150;400
Clases de nivelación de química;40;80
Licencia de estudiante de un software de diseño;30;80
Excursión académica de la carrera;80;300
Impresión a color de la presentación;5;20
Lápices y borrador para el parcial;3;10
Módulos del curso de contabilidad;100;300
Guía de estudio para el examen de admisión;30;70
la matricula;2000;5000
fotocopias;1;8
curso de ingles;100;400
impresiones de la U;2;10
el semestre;2000;5000
libro de la U;40;150
""",
"Personal, hogar y ocio": """
Mensualidad de Netflix;27;45
Spotify Duo;17;25
Boletas de cine y crispetas;40;80
Cervezas con amigos el viernes;30;80
Rumba y cover en Chapinero;40;120
Bolos con los compañeros;30;70
Concierto en el Movistar Arena;150;450
Boleta para el partido en El Campín;50;200
Juego en oferta en Steam;20;90
Xbox Game Pass;40;55
Suscripción de Disney+;25;45
Amazon Prime Video;15;25
Vaca para el paseo a la finca;60;200
Vaca para el asado;20;50
Alitas y pola con los de la U;40;70
Cóctel en un bar de la 85;40;90
Boletas de teatro;50;150
Salitre Mágico;80;150
Entrada al museo;10;30
Karaoke con amigos;30;80
Hotel en vacaciones;200;600
Fin de semana en Villa de Leyva;200;600
Billar y cerveza;20;50
Entrada a la discoteca;20;60
Disfraz para la fiesta de Halloween;50;150
Videojuego nuevo para la Play;200;350
Novela para leer en vacaciones;40;90
Pola en la tienda con los parceros;10;30
YouTube Premium;20;30
Suscripción de HBO Max;20;35
Crunchyroll;15;25
Tour de cerveza artesanal;60;120
Paintball con amigos;40;80
Escape room;50;90
Entrada a la Feria del Libro;10;20
Piscina el fin de semana;15;35
Chicharrón y cerveza en el estadero;30;70
Tejo con los amigos;20;50
Diamantes de Free Fire;10;40
Andrés Carne de Res;80;250
Alquiler de película en plataforma;10;20
Fin de semana en Melgar;300;800
Clase de baile de salsa;20;50
Mirador y chocolate en Monserrate;20;60
unas polas;10;40
salida con los parceros;40;120
rumba;40;150
el netflix;27;45
cine;20;60
Desodorante, crema dental y shampoo;25;60
Jabón en polvo y límpido;15;35
Corte de cabello en la peluquería;15;40
Mensualidad del gimnasio Smart Fit;80;110
Bombillos y arreglo de enchufe;15;50
Sábanas y toallas en Homecenter;60;200
Ollas y utensilios de cocina;40;150
Ropa en Koaj;50;150
Zapatos en el centro comercial;100;300
Escoba, trapero y bolsas de basura;15;40
Paca de papel higiénico;20;45
Detergente y suavizante;20;45
Manicure y pedicure;25;50
Crema hidratante en Farmatodo;20;50
Toallas higiénicas;8;20
Máquina de afeitar y espuma;15;40
Plomero para arreglar la tubería;60;180
Pintura para el cuarto;60;150
Cortina para la ducha;25;60
Tenis para correr;150;400
Chaqueta para el frío;100;250
Jeans en Studio F;80;200
Ropa interior;30;80
Cepillo de dientes;5;15
Perfume;80;250
Maquillaje en la droguería;20;80
Corte y barba en la barbería;20;40
Lavada del edredón en la lavandería;20;45
Ganchos y organizadores;15;40
Licuadora nueva;120;250
Microondas;250;450
Bloqueador solar;30;70
Tinte para el cabello;20;50
Uñas acrílicas;50;120
Masaje relajante;60;150
Productos de aseo en el D1;20;60
Desinfectante y bolsas de basura;10;25
Cerrajero por las llaves;40;90
Técnico para arreglar la nevera;80;200
Colchón nuevo;500;1200
Almohadas;40;100
Plancha para el pelo;80;200
Tapete para la sala;60;150
Vajilla;60;180
Mensualidad de clases de yoga;100;200
Ropa deportiva;60;150
Medias y pijama;30;70
Arreglo de zapatos en el zapatero;10;30
Bombillo LED;8;20
Pilas para el control;8;20
aseo de la casa;20;60
la peluqueria;15;40
ropa;50;200
el gym;80;110
shampoo y jabon;15;35
""",
"Mercancía e insumos": """
Surtido de mercancía para vender;150;800
Ingredientes para las tortas que vendo;50;200
Empanadas para vender en la feria;30;100
Material de bisutería para vender;50;200
Insumos de uñas para mis clientas;60;200
Tela para las prendas que confecciono;80;300
Hilos y botones para el taller;15;40
mercancia;100;600
insumos del negocio;50;300
Bulto de papa para las papas rellenas que vendo;80;150
Harina de maíz para las arepas que vendo;30;80
Aceite para la freidora del puesto;40;100
Queso para las arepas del negocio;30;90
Gaseosas para vender en la tienda;80;300
Cerveza para surtir la tienda;150;500
Dulces y chocolatinas para el puesto;40;120
Cigarrillos y chicles para revender;50;150
Frutas para los jugos que vendo;30;80
Carne para las hamburguesas del negocio;80;250
Pan para los perros calientes del puesto;20;60
Salchichas para el carrito de perros;40;120
Maíz para las mazorcas que vendo;30;70
Leche y fruta para las ensaladas que vendo;30;80
Arepas al por mayor para el puesto;30;80
Productos de aseo para revender por catálogo;50;200
Pedido de Yanbal para revender;100;400
Pedido de Esika para revender;100;400
Ropa al por mayor en San Victorino para vender;200;800
Medias y ropa interior para vender en la calle;80;250
Accesorios de celular para revender;80;300
Saldo de recargas para vender;50;200
Flores al por mayor para vender;50;150
Harina, huevos y azúcar para las tortas del negocio;40;120
Chocolate y leche condensada para los postres que vendo;30;90
Pollo para el negocio de asados;100;300
Café en grano para la tienda de tintos;30;80
Mango y piña al por mayor para las frutas picadas;40;100
Verduras al por mayor para el restaurante;80;250
Arroz por bulto para el restaurante;100;200
Pescado para vender en el puesto;100;300
Materiales para las manillas que vendo;30;100
Madera para los muebles que fabrico;150;500
Pintura para las artesanías que vendo;30;90
Cuero para los bolsos que hago;100;300
Repuestos para revender en el taller;100;400
Llantas usadas para revender;100;300
Paquetes de papas para surtir la tienda;60;200
Licores para el estanco;200;800
Huevos al por mayor para el negocio;60;150
Shampoo y cremas para el salón de belleza;80;200
Tintes para el salón de belleza;60;150
surtir la tienda;100;500
mercancia pa vender;80;400
insumos del puesto;30;150
""",
"Otros gastos del negocio": """
Suscripción Canva Pro;30;35
Licencia de Adobe Creative Cloud;120;250
Hosting y dominio para la página de un cliente;80;250
Día de coworking;25;50
Mouse y teclado para trabajar;60;180
Publicidad en Instagram para mis servicios;30;200
Envío de mercancía por Servientrega;10;30
Empaques y bolsas para los pedidos;20;80
ChatGPT Plus para el trabajo;80;100
Tarjetas de presentación;30;80
Repuesto del computador de trabajo;80;300
Plan de Google Workspace;25;60
Renovación del dominio .com;50;80
Cámara para las sesiones de fotos;800;2500
Domicilio para entregar un pedido;8;20
Microsoft 365 para el trabajo;30;50
Cuenta de Figma;50;70
Impresión del catálogo;50;150
Stand en la feria de emprendimiento;100;400
Honorarios del contador;100;300
Plataforma de facturación electrónica;30;70
Envío de un pedido por Rappi Favor;10;25
Disco duro para los backups de clientes;200;400
Micrófono para grabar el podcast;150;400
Freelancer que me ayudó con un logo;100;400
Comisión de Workana;20;150
Comisión de Upwork;20;150
Tinta para la impresora del negocio;40;100
LinkedIn Premium;100;150
Etiquetas adhesivas con mi logo;30;80
Lámpara para fotografiar productos;80;200
Fondo para fotos de producto;60;150
Mantenimiento de la máquina de coser;50;120
Arriendo del local;800;2000
Bolsas kraft con mi logo;40;100
Registro en la Cámara de Comercio;100;250
Suscripción de Shopify;100;160
Comisión de la pasarela de pagos;5;50
Software de edición de video;40;100
Vinilos para la vitrina del local;60;150
canva;30;35
envio del pedido;10;25
publicidad en face;30;150
Hielo para los jugos del puesto;5;15
Vasos y pitillos desechables;15;40
Servilletas y palillos para el negocio;8;20
Alquiler del carrito de ventas;10;30
Permiso de la alcaldía para el puesto;30;100
Pipeta de gas para el puesto de fritos;60;95
Flete para traer la mercancía;30;100
Arriendo del puesto en la plaza;150;400
Sombrilla para el puesto;60;150
Carpa para la feria;100;300
Mensualidad del datáfono;30;60
Balanza para el negocio;80;200
Vigilancia del local;20;60
hielo pa los jugos;5;15
bolsitas del negocio;10;30
""",
"Deudas y créditos": """
Cuota de la tarjeta de crédito;150;800
Cuota del crédito de libre inversión;200;900
Cuota del crédito del ICETEX;150;600
Intereses de la tarjeta;20;150
Cuota de manejo de la tarjeta;15;40
Cuota del préstamo del carro;500;1500
Cuota de la hipoteca;800;2500
Pago mínimo de la tarjeta Falabella;80;300
Abono a la deuda con mi hermano;50;300
Cuota de Addi;60;300
Cuota de Sistecrédito;50;250
Seguro de vida del crédito;15;50
Pago de deuda reportada en centrales;100;500
Intereses de mora;10;100
Descuento del crédito de libranza;200;600
Comisión por avance en efectivo;10;30
Cuota de la moto a crédito;200;500
Celular a cuotas;50;150
Nevera a crédito en Alkosto;80;300
Cuota del crédito educativo con el banco;200;700
Abono a capital de la tarjeta;100;800
Le pagué lo que le debía a un amigo;30;200
Seguro de desempleo de la tarjeta;10;30
Recargo por pago tardío;20;60
Cuota de Rapicredit;100;400
Cuota de Lineru;100;400
Cuota del préstamo en Bancolombia;200;900
Pago de la tarjeta Nu;100;600
Cuota de la tarjeta Éxito;80;300
Refinanciación de la deuda;100;500
Cuota del crédito de vivienda;700;2000
Pago de la tarjeta Davivienda;100;700
Cuota del préstamo con la natillera;30;150
Pago a plazos del computador personal;100;300
Intereses del sobregiro;20;100
Cuota del crédito rotativo;100;400
la tarjeta;100;600
cuota del credito;150;800
intereses;20;150
pague a la tarjeta;100;600
Pago del gota a gota;20;100
Cuota diaria del préstamo gota a gota;10;50
Pagué lo que debía fiado en la tienda;20;100
Abono al préstamo del proveedor;50;300
Cuota del microcrédito de Bancamía;100;400
Cuota del crédito de Banco Mundo Mujer;100;400
Abono a la deuda con la vecina;20;100
Cuota del crédito para el negocio;150;600
Abono al crédito de la nevera del negocio;80;250
el gota a gota;20;80
abono al credito;50;300
""",
"Otros": """
Cuatro por mil del mes;2;20
Comisión por retirar en cajero de otro banco;5;8
Comisión por transferencia a otro banco;3;8
Cuota de manejo de la cuenta de ahorros;8;15
Comisión de Servibanca;5;9
Costo del giro internacional;20;80
Comisión de Western Union;15;50
Comisión de la consulta en cajero;2;5
4x1000;2;20
Regalo para mi mamá;50;200
Regalo de cumpleaños para un amigo;30;120
Torta para el cumpleaños de mi papá;40;100
Flores para el día de la madre;40;120
Regalo del amigo secreto;30;80
Donación a una fundación;20;100
Colecta de la oficina;10;30
Regalo de grado para mi prima;50;200
Detalle de aniversario;50;200
Decoración para la fiesta de cumpleaños;30;100
Bombas y velas para la celebración;15;40
Regalo de Navidad para mi sobrino;40;150
Ancheta de Navidad;60;200
Regalo para el baby shower;50;150
Regalo de matrimonio;100;400
Tarjeta y chocolates para mi novia;20;60
Ramo de rosas;30;80
Peluche de regalo;25;70
Aporte para la novena de aguinaldos;10;30
Cuota para el regalo de la profesora;5;20
Donación por Nequi a una causa;10;50
Regalo del día del padre;50;200
Regalo de quince años;60;250
Torta y pasabocas para la fiesta de la oficina;30;80
Recordatorios para la primera comunión;40;150
Papel de regalo y tarjeta;5;15
Bono de regalo de Falabella;50;200
Gift card de Amazon;50;200
Regalo de amor y amistad;30;100
Detalle para el día de la mujer;20;60
Regalo para el bebé de mi amiga;40;120
Globos y pancarta para la sorpresa;20;60
Piñata para el cumpleaños del niño;30;80
Donación de mercado al hogar de ancianos;50;150
Regalo para mi hermana;40;150
Vino para regalar;40;100
Chocolates para regalar;15;50
Camisa de regalo para mi papá;60;180
Libro de regalo para un amigo;40;90
Propina de Navidad al portero;20;50
Vaca para el regalo grupal;10;40
Mariachis para la serenata;200;500
Torta de grado;50;120
Regalo de despedida para un compañero;20;60
Ofrenda en la misa;5;30
Regalo de cumpleaños para mi abuela;40;150
Detalle para la profesora en su día;15;40
Donación a la Cruz Roja;20;100
Regalo de bienvenida para el bebé;40;120
regalo;30;150
detalle pa mi novia;20;80
regalo cumple de mi amigo;30;100
donacion;10;100
flores;30;80
Comparendo por mal parqueo;200;650
Multa de tránsito;400;650
Ayuda para mis papás;100;400
Plata que le mandé a mi abuela;50;300
Lotería y chance;2;20
Notaría para autenticar un documento;10;30
Duplicado de la cédula;40;60
Trámite del pasaporte;300;400
""",
}
