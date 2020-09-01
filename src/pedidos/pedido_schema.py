from schema import Schema, And, Optional

class PedidoSchema:
    def __init__(self):
        self.schema = Schema({'pedido_id': And(str),
                                'destinatario': And(str),
                                'direccion': And(str),
                                Optional('estado'): And(str),
                                'productos': [{
                                                    'producto_id': And(str),
                                                    'unidades': And(int)
                                            }]
                                })

    def validate (self, p_json):
        return self.schema.validate(p_json)

    def is_valid(self, p_json):
        return self.schema.is_valid(p_json)

    