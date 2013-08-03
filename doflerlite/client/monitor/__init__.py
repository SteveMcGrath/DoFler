import ettercap
import driftnet

def get_parsers():
    return {
        'ettercap': ettercap.Parser,
        'driftnet': driftnet.Parser,
    }