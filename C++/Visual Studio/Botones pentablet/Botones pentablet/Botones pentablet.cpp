#include <iostream>
#include <windows.h>
#include <string>
#include <libSign.h> // Asegúrate de que este archivo está correctamente configurado en tu proyecto.

using namespace std;

// Definiciones de los identificadores
struct SIGNDATAPACKET {
    int eventtype;
    int physical_key;
    int keystatus;
};

const int EventType_Key = 1;
const int KeyStatus_Down = 1;
const int KeyStatus_Up = 0;

const int ERR_OK = 0;  // Define este valor como "0" para indicar que la inicialización fue exitosa
const int DeviceStatus_Connected = 1;  // Define este valor para indicar que la tableta está conectada

// Variables globales
bool estado_modificador = false;

// Funciones para manejar eventos de los botones
void ejecutar_funcion(const string& funcion) {
    if (funcion == "B1") {
        std::cout << "Ejecutando Ctrl+Tab\n";
    }
    else if (funcion == "B2") {
        std::cout << "Ejecutando tecla E\n";
    }
    else if (funcion == "B3") {
        std::cout << "Ejecutando Win+Ctrl+S\n";
    }
    else if (funcion == "B5") {
        std::cout << "Ejecutando Ctrl+Z\n";
    }
    else if (funcion == "B6") {
        std::cout << "Ejecutando Ctrl+Shift+Z\n";
    }
}

// Callback para procesar eventos de la tableta
int CALLBACK procesar_evento(SIGNDATAPACKET pktObj) {
    // Verificar si se reciben eventos
    cout << "Evento recibido: Key " << pktObj.physical_key << ", Estado " << pktObj.keystatus << endl;

    if (pktObj.eventtype == EventType_Key) {
        string boton = "B" + to_string(pktObj.physical_key);  // Mapear el botón
        if (pktObj.keystatus == KeyStatus_Down) {
            if (boton == "B4") {  // Botón modificador (B4)
                estado_modificador = true;
                cout << "Modificador activado\n";
            }
            else {
                if (estado_modificador) {
                    cout << "Ejecutando función combinada para " << boton << endl;
                }
                else {
                    ejecutar_funcion(boton);  // Ejecutar función para el botón
                }
            }
        }
        else if (pktObj.keystatus == KeyStatus_Up) {
            if (boton == "B4") {  // Botón modificador (B4)
                estado_modificador = false;
                cout << "Modificador desactivado\n";
            }
        }
    }
    return 0;
}

int main() {
    // Inicializar SDK
    if (signInitialize() != ERR_OK) {
        cout << "Error al inicializar el SDK." << endl;
        return -1;
    }
    else {
        cout << "SDK inicializado correctamente." << endl;
    }

    // Verificar si la tableta está conectada
    int device_status = signGetDeviceStatus();
    if (device_status != DeviceStatus_Connected) {
        cout << "Error: La tableta no está conectada o está en un estado incorrecto." << endl;
        signClean();  // Limpiar el SDK
        return -1;
    }

    cout << "Tableta conectada correctamente." << endl;

    // Registrar el callback para manejar los eventos
    if (signRegisterDataCallBack(procesar_evento) == 0) {
        cout << "Error al registrar el callback." << endl;
        signClean();
        return -1;
    }
    cout << "Callback registrado." << endl;

    // Mantener el programa activo
    cout << "Esperando eventos de la tableta..." << endl;
    while (true) {
        Sleep(1000);  // Esperar 1 segundo entre eventos
    }

    // Limpiar y cerrar el SDK antes de salir
    signUnregisterDataCallBack(0);
    signClean();
    cout << "SDK cerrado." << endl;
    return 0;
}
