import ettercap
import tshark
import tcpxtract
import driftnet
import tshark_stats

def get_parsers():
    parsers = {
        'driftnet': driftnet.Parser,
        'ettercap': ettercap.Parser,
        'tcpxtract': tcpxtract.Parser,
        'driftnet': driftnet.Parser,
        'tshark': tshark.Parser,
        'tshark-stats': tshark-stats.Parser,
    }
    return parsers