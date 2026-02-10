# Proyecto Dronify - Desarrollo

## Resumen Diario

### Día 1

Implementación inicial del módulo **Dron_vic** para la gestión de drones.

**Tareas completadas:**
- Creación de la estructura del módulo con directorios models, views, controllers y security
- Desarrollo del modelo de usuarios con los campos necesarios
- Configuración de las vistas de Clientes y Pilotos

### Día 2

**Primer commit:**  
Ampliación del módulo con todos los modelos necesarios para la gestión de drones, paquetes y vuelos, sin relaciones entre ellos.

**Tareas completadas:**
- Creación de modelos adicionales (Dron, Paquete, Vuelo)
- Definición de campos y atributos para cada modelo
- Configuración de vista por defecto para cada modelo nuevo

**Segundo commit:**  
Se han creado las relaciones entre los modelos.

**Tareas completadas:**
- Establecimiento de relaciones entre Vuelo y Dron, Piloto, Paquete
- Creación de campos computados para calcular los datos necesarios
- Creación de campos relacionados

### Día 3
Se han completado todas las vistas falta implementar la logica de funcionamiento y procesos.

**Tareas completadas:**
- Vistas completadas para todos los modelos: Usuarios (Clientes y Pilotos), Drones, Paquetes y Vuelos