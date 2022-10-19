import logging


def initiate_logger():
    logging.basicConfig(
        filename="KonverterXML.log",
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.INFO
    )

    logging.info("Kører KonverterXML\n")

    logging.getLogger()