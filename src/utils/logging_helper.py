import logging
from datetime import datetime as dt


def initiate_logger():
    logging.basicConfig(
        filename=f"KonverterXML_{dt.now().strftime('%Hh%Mm%Ss')}.log",
        filemode='a',
        format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    logging.info("Kører KonverterXML\n")

    logging.getLogger()
