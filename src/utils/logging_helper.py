import logging
from datetime import datetime as dt


def initiate_logger(folder_path=""):
    logging.basicConfig(
        filename=f"{folder_path}/KonverterXML_{dt.now().strftime('%Hh%Mm%Ss')}.log",
        filemode='a',
        format='%(asctime)s.%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    logging.info("Kører KonverterXML\n")

    logging.getLogger()
