import ettercap
import tshark
import tcpxtract
import driftnet
import tshark_stats

def get_parsers():
    parsers = []
    parsers.append(ettercap.Parser())
    parsers.append(driftnet.Parser())
    parsers.append(tcpxtract.Parser())
    parsers.append(tshark.Parser())
    parsers.append(tshark_stats.Parser())
    return parsers