from schema import Schema, And, Optional

import json

class PedidoSchema:
    def __init__(self):
        self.schema = Schema({'id': And(str),
                                'destinatario': And(str),
                                'direccion': And(str),
                                Optional('estado'): And(str),
                                'productos': [{
                                                    'id': And(str),
                                                    'unidades': And(int)
                                            }]
                                })

    def validate (self, p_json):
        return self.schema.validate(p_json)

    def is_valid(self, p_json):
        return self.schema.is_valid(p_json)

    