from pydantic import conlist

from ...base import Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class IdentificacionAdministrador(Resource):
    identificador_administrador: str
    tipo_movimiento: str
    nombre_administrador: str
    rfc_administrador: str
    personalidad_juridica_administrador: str
    modalidad_comercial_administrador: str
    nombre_comercial: str


class BajaAdministrador(Resource):
    causa_baja_administrador: str


class InformacionSolicitada(Resource):
    identificacion_administrador: IdentificacionAdministrador
    baja_administrador: BajaAdministrador


class Reporte2610(ReportIFPE, Sendable, Updateable, Resendable):
    """
    Este reporte recaba información referente a los movimientos
    de Altas y/o Bajas de los Administradores de Comisionistas,
    que sean contratados por la Institución de Fondos de Pago
    Electrónico para que sean intermediarios entre los comisionistas
    y la Institución.
    """

    _resource = '/IFPE/R26/2610'

    informacion_solicitada: conlist(  # type: ignore[valid-type]
        InformacionSolicitada, min_items=1
    )
