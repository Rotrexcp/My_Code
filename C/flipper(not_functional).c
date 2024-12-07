#include <stdio.h>
#include <time.h>

#define HORAS_RESTANTES_CRITICAS 5  // Horas antes de la expiración que activan la renovación

// Estructura que simula la tarjeta de estudiante
typedef struct {
    int mes_validacion;    // Mes de validez (1-12)
    int anio_validacion;   // Año de validez
    struct tm fecha_vencimiento; // Fecha de vencimiento de la tarjeta
} TarjetaEstudiante;

// Función que verifica si la tarjeta sigue siendo válida
int es_tarjeta_valida(TarjetaEstudiante *tarjeta) {
    time_t ahora = time(NULL);  // Obtiene el tiempo actual
    struct tm fecha_actual = *localtime(&ahora);

    // Compara el mes y año de vencimiento con la fecha actual
    if (tarjeta->anio_validacion < fecha_actual.tm_year + 1900 ||
        (tarjeta->anio_validacion == fecha_actual.tm_year + 1900 && tarjeta->mes_validacion < fecha_actual.tm_mon + 1)) {
        return 0;  // Tarjeta vencida
    }
    return 1;  // Tarjeta válida
}

// Función que renueva la tarjeta
void renovar_tarjeta(TarjetaEstudiante *tarjeta) {
    time_t ahora = time(NULL);
    struct tm fecha_actual = *localtime(&ahora);

    // Asignar el próximo mes como el mes de vencimiento
    tarjeta->mes_validacion = fecha_actual.tm_mon + 2;  // Proximo mes
    if (tarjeta->mes_validacion > 12) {
        tarjeta->mes_validacion = 1;   // Si es diciembre, va al enero del siguiente año
        tarjeta->anio_validacion++;    // Aumenta el año
    }
    tarjeta->fecha_vencimiento = fecha_actual;
    tarjeta->fecha_vencimiento.tm_mon = tarjeta->mes_validacion - 1; // Establecer el mes en la estructura tm

    // Actualiza la fecha de vencimiento según la nueva fecha
    mktime(&tarjeta->fecha_vencimiento);

    printf("Tarjeta renovada! Nueva fecha de vencimiento: %d/%d\n", tarjeta->mes_validacion, tarjeta->anio_validacion);
}

// Función que chequea si la tarjeta debe ser renovada
void verificar_y_renovar(TarjetaEstudiante *tarjeta) {
    time_t ahora = time(NULL);
    struct tm fecha_actual = *localtime(&ahora);

    // Si quedan menos de 5 horas de validez, se renueva la tarjeta
    double diferencia = difftime(mktime(&tarjeta->fecha_vencimiento), ahora); // Calcula la diferencia entre la fecha de vencimiento y la actual

    // Si quedan menos de 5 horas, renovar la tarjeta
    if (diferencia < 5 * 60 * 60) {
        printf("¡La tarjeta está por caducar! Renovando...\n");
        renovar_tarjeta(tarjeta);
    } else {
        printf("La tarjeta sigue siendo válida. Fecha de vencimiento: %d/%d\n", tarjeta->mes_validacion, tarjeta->anio_validacion);
    }
}

int main() {
    TarjetaEstudiante tarjeta = {12, 2024, {0}}; // Inicializa con un mes y año predeterminado de vencimiento

    // Establecer la fecha de vencimiento inicial de la tarjeta
    time_t ahora = time(NULL);
    struct tm fecha_actual = *localtime(&ahora);
    tarjeta.fecha_vencimiento = fecha_actual;
    tarjeta.fecha_vencimiento.tm_mon = tarjeta.mes_validacion - 1;  // Asegura que el mes coincida
    tarjeta.fecha_vencimiento.tm_year = tarjeta.anio_validacion - 1900;

    // Verificamos si la tarjeta está válida y si necesita ser renovada
    verificar_y_renovar(&tarjeta);

    return 0;
}
