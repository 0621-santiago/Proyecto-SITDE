# Matriz de reglas de negocio · SITDE

Tarea SITDE-24 (WBS 2.3.1). Cada regla tiene una condición sobre los datos, la acción que recomienda el sistema y su prioridad. El sistema **recomienda**; la decisión final es del administrador de la planta.

Las reglas se evalúan sobre los lotes de producción, el inventario y las recepciones de materia prima. El motor de reglas (SITDE-29) las recorre y genera las alertas que se muestran en el dashboard.

| Código | Regla | Condición | Acción recomendada | Prioridad | Datos que usa |
|---|---|---|---|---|---|
| RN-01 | Lote vencido | `fecha_vencimiento < hoy` y cantidad disponible > 0 | No usar ni vender el lote. Registrarlo como merma y retirarlo del inventario. | Alta | Lote de producción |
| RN-02 | Lote próximo a vencer | `0 ≤ fecha_vencimiento − hoy ≤ 3 días` y cantidad disponible > 0 | Priorizar la venta de ese lote (primero en vencer, primero en salir). | Alta | Lote de producción |
| RN-03 | Stock bajo el mínimo | `stock_actual < stock_minimo` | Programar producción o pedido del producto. | Media | Inventario |
| RN-04 | Stock sobre el máximo | `stock_actual > stock_maximo` | Detener la producción de ese producto hasta reducir existencias. | Media | Inventario |
| RN-05 | Trazabilidad del lote | Un lote sin ninguna recepción de leche asociada | Rechazar el registro: todo lote debe originarse en recepciones registradas. | Alta | Lote, consumo de materia prima |
| RN-06 | Merma alta | `(cantidad_esperada − cantidad_real) / cantidad_esperada > 5 %` | Revisar el proceso de producción o el almacenamiento de ese producto. | Media | Lote, inventario |

## Notas

- **Umbrales.** Los 3 días de RN-02 y el 5 % de RN-06 son valores iniciales. Se ajustarán con los administradores de las plantas en las visitas de noviembre.
- **Configuración.** Cada regla se guarda en el modelo `NormaNegocio` (condición, acción y prioridad), para que se pueda activar, desactivar o ajustar sin cambiar el código.
- **Relación con las historias de usuario.** RN-03 cubre la HU-06 (alertas de inventario). Todas las reglas alimentan la HU-10 (recomendaciones automáticas).
