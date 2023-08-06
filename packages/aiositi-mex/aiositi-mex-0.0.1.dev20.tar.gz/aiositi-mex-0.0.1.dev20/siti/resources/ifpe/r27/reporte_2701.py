from typing import List, Optional

from ....http import Session, session as global_session
from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionReclamacion(Resource):
    # _date_format = '%Y-%m-%d'

    folio_reclamacion: str
    estatus_reclamacion: str
    fecha_actualizacion_estatus: str


class IdentificadorClienteCuentaMovimiento(Resource):
    identificador_cliente: str
    identificador_cuenta: str
    identificador_movimiento: str


class DetalleReclamacion(Resource):
    # _date_format = '%Y-%m-%d'

    fecha_reclamacion: str
    canal_recepcion_reclamacion: str
    tipo_reclamacion: str
    motivo_reclamacion: str
    descripcion_reclamacion: str


class DetalleEventoOriginaReclamacion(Resource):
    fecha_evento: str
    objeto_evento: str
    canal_operacion: str
    importe_valorizado_moneda_nacional: str


class EventosSubsecuentes(Resource):
    detalle_evento_origina_reclamacion: DetalleEventoOriginaReclamacion


class DetalleResoucion(Resource):
    # _date_format = '%Y-%m-%d'

    fecha_resolucion: str
    sentio_resolucon: str
    importe_abonado_cuenta_cliente: str
    fecha_abono_cuenta_cliente: str
    identificador_cuenta_fideicomiso_institucion: str
    importe_recuperado: str
    fecha_recuperacion_recursos: str
    identificador_cuenta_recibe_importe_recuperado: str
    quebranto_institucion: str
    # cambiar formato de fecha a '%Y-%m-%d


class InformacionSolicitada(Resource):
    identificacion_reclamacion: IdentificacionReclamacion
    identificador_cliente_cuenta_movimiento: IdentificadorClienteCuentaMovimiento  # noqa: E501
    detalle_reclamacion: DetalleReclamacion
    detalle_evento_origina_reclamacion: DetalleEventoOriginaReclamacion
    eventos_subsecuentes: List[EventosSubsecuentes]
    detalle_resolucion: DetalleResoucion


class Reporte2701(ReportIFPE, Sendable, Resendable, Updateable):
    """
    En este reporte se recaba información referente a las reclamaciones
    relativas a operaciones con fondos de pago electrónico realizadas
    por los Clientes, agrupadas por productos y canales transaccionales
    de las Instituciones de Fondos de Pago Electrónico. Adicionalmente,
    este reporte considera información respecto de los datos de la
    gestión de dichas reclamaciones.
    """

    _resource = '/IFPE/R27/2701'

    informacion_solicitada: Optional[List[InformacionSolicitada]]

    async def send(self, *, session: Session = global_session, **data):
        url = f'{self._endpoint}{self._resource}'
        if not self.informacion_solicitada:
            url = f'{url}/envio-vacio'
        return await super().send(url=url, session=session, **data)
