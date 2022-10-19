import os
import xml.etree.cElementTree as ET
import logging

from datetime import datetime
from xml.dom import minidom

from utils import xml_helper
from utils.logging_helper import initiate_logger


def convert_xml_files():
    output_file_name = "export-ORDERS.xml"
    all_files = os.listdir("./")
    xml_files = list(filter(lambda f: f.endswith('.xml') and not f == output_file_name, all_files))

    # Create output XML tree structure
    order_export = ET.Element('ORDER_EXPORT')
    order_export.set("type", "ORDERS")
    elements = ET.SubElement(order_export, "ELEMENTS")

    for file in xml_files:
        logging.info(f"Konverterer '{file}'")
        # Read input XML:
        input_xml = minidom.parse(file)
        order = ET.SubElement(elements, "ORDER")

        # Create "GENERAL"-element
        general = ET.SubElement(order, "GENERAL")
        try:
            ET.SubElement(general, "ORDER_ID").text = input_xml.getElementsByTagName('order-number')[0].firstChild.data
            ET.SubElement(general, "LANGUAGE_ID").text = "26"

            created_at = datetime.fromisoformat(input_xml.getElementsByTagName('created-at')[0].firstChild.data)
            ET.SubElement(general, "DATE").text = created_at.strftime("%d-%m-%Y %H:%M:%S")

            ET.SubElement(general, "CURRENCY_CODE").text = "DKK"
            ET.SubElement(general, "ORDER_TOTAL_PRICE").text = ""  # input_xml.getElementsByTagName('total-price')[0].firstChild.data
            ET.SubElement(general, "ORDER_VAT").text = "25"
            ET.SubElement(general, "TOTAL_WEIGHT").text = f"{float(input_xml.getElementsByTagName('total-weight')[0].firstChild.data) / 1000}".replace(".", ",")
            ET.SubElement(general, "STATE_ID").text = "1"
            ET.SubElement(general, "REFERRER").text = "https://www.papirladen.dk/admin/Modules/Login/Login"
            [note] = [note for note in input_xml.getElementsByTagName('note') if note.parentNode.tagName != "customer"]
            ET.SubElement(general, "CUST_COMMENTS").text = note.firstChild.data if note.firstChild is not None else ""

            # Create "ADVANCED"-element
            advanced = ET.SubElement(order, "ADVANCED")
            ET.SubElement(advanced, "REFERENCE_NUM").text = ""
            ET.SubElement(advanced, "IP_ADRESS").text = input_xml.getElementsByTagName('browser-ip')[0].firstChild.data
            ET.SubElement(advanced, "DISCOUNT").text = "0,00"
            ET.SubElement(advanced, "LBL_EXPORT_STATE").text = "0"

            # Create "PAY_METHOD"-element
            pay_method = ET.SubElement(order, "PAY_METHOD")
            ET.SubElement(pay_method, "PAY_METHOD_ID").text = "60"
            ET.SubElement(pay_method, "PAY_METHOD_NAME").text = "Faktura"
            ET.SubElement(pay_method, "PAY_METHOD_FEE").text = "0,00"
            ET.SubElement(pay_method, "PAY_METHOD_FEE_INCL_VAT").text = "False"

            # Create "SHIPPING_METHOD"-element
            shipping_method = ET.SubElement(order, "SHIPPING_METHOD")
            ET.SubElement(shipping_method, "SHIP_METHOD_ID").text = "58"
            ET.SubElement(shipping_method, "SHIP_METHOD_NAME").text = "GLS Pakkeshop - HENT SELV"
            ET.SubElement(shipping_method, "SHIP_METHOD_FEE").text = "37,50"
            ET.SubElement(shipping_method, "SHIP_METHOD_FEE_INCL_VAT").text = "True"

            # Create "CUSTOMER"-element
            customer = ET.SubElement(order, "CUSTOMER")
            ET.SubElement(customer, "CUST_NUM").text = "53794648"
            ET.SubElement(customer, "VAT_REG_NUM").text = ""

            [billing_adress] = [billing_address for billing_address in input_xml.getElementsByTagName('billing-address')]
            ET.SubElement(customer, "CUST_NAME").text = (
                    billing_adress.getElementsByTagName("first-name")[0].firstChild.data + " " +
                    billing_adress.getElementsByTagName("last-name")[0].firstChild.data + " " +
                    billing_adress.getElementsByTagName("phone")[0].firstChild.data.replace(" ", "")
            )
            ET.SubElement(customer, "CUST_COMPANY").text = "Cares ApS"
            ET.SubElement(customer, "CUST_ADDRESS").text = "Gammel Strandvej 193 a"
            ET.SubElement(customer, "CUST_ADDRESS_2").text = ""
            ET.SubElement(customer, "CUST_ZIP_CODE").text = "3060"
            ET.SubElement(customer, "CUST_CITY").text = "Espergærde"
            ET.SubElement(customer, "CUST_STATE").text = ""
            ET.SubElement(customer, "CUST_COUNTRY").text = "Danmark"
            ET.SubElement(customer, "CUST_COUNTRY_ISO").text = "DK"
            ET.SubElement(customer, "CUST_PHONE").text = "53794684"
            ET.SubElement(customer, "CUST_FAX").text = ""
            ET.SubElement(customer, "CUST_EMAIL").text = "info@cares.dk"
            ET.SubElement(customer, "CUST_EAN").text = ""

            # Create "B2B_GROUP"-element
            b2b_group = ET.SubElement(order, "B2B_GROUP")
            ET.SubElement(b2b_group, "CUST_B2B_ID").text = "1"
            ET.SubElement(b2b_group, "CUST_B2B_NAME").text = "02 - B2B kunder"

            # Create "DELIVERY_INFO"-element
            delivery_info = ET.SubElement(order, "DELIVERY_INFO")

            [shipping_line] = [shipping_line for shipping_line in input_xml.getElementsByTagName('shipping-line')]
            deliv_name = ""
            shipping_line_title = shipping_line.getElementsByTagName("title")[0].firstChild.data.split(" ")
            for i in range(len(shipping_line_title) - 2):
                if shipping_line_title[i] == "Din" and shipping_line_title[i + 1] == "Pakkeshop":
                    deliv_name = shipping_line_title[i] + " " + shipping_line_title[i + 1] + " " + shipping_line_title[i + 2]
                    break
            if deliv_name == "":
                deliv_name = " ".join(shipping_line_title)

            ET.SubElement(delivery_info, "DELIV_NAME").text = deliv_name
            ET.SubElement(delivery_info, "DELIV_COMPANY").text = ""
            ET.SubElement(delivery_info, "DELIV_ADDRESS").text = ""
            ET.SubElement(delivery_info, "DELIV_ADDRESS_2").text = "Pakkeshop: " + shipping_line.getElementsByTagName("code")[0].firstChild.data.split("_")[-1]
            ET.SubElement(delivery_info, "DELIV_ZIP_CODE").text = ""
            ET.SubElement(delivery_info, "DELIV_CITY").text = ""
            ET.SubElement(delivery_info, "DELIV_STATE").text = ""
            ET.SubElement(delivery_info, "DELIV_COUNTRY").text = "Danmark"
            ET.SubElement(delivery_info, "DELIV_COUNTRY_ISO").text = "DK"
            ET.SubElement(delivery_info, "DELIV_PHONE").text = ""
            ET.SubElement(delivery_info, "DELIV_FAX").text = ""
            ET.SubElement(delivery_info, "DELIV_EMAIL").text = ""
            ET.SubElement(delivery_info, "DELIV_EAN").text = ""
        except Exception as e:
            error = f"Filen '{file}' blev ikke konverteret. Kontroller, at der ikke er andre .xml-filer i mappen end dem, der skal konverteres. Fejlbesked: {e}\n"
            logging.error(error)
            raise e

        # Create "CUSTOM_FIELDS"-element
        custom_fields = ET.SubElement(order, "CUSTOM_FIELDS")
        ET.SubElement(custom_fields, "FIELD_1").text = ""
        ET.SubElement(custom_fields, "FIELD_2").text = ""
        ET.SubElement(custom_fields, "FIELD_3").text = "0"
        ET.SubElement(custom_fields, "FIELD_4").text = "1"
        ET.SubElement(custom_fields, "FIELD_5").text = ""

        # Create "GIFT_CERTIFICATES"-element
        gift_certificates = ET.SubElement(order, "GIFT_CERTIFICATES")
        ET.SubElement(gift_certificates, "GC_PURCHASE_AMOUNT").text = "0,00"

        order_lines = ET.SubElement(order, "ORDER_LINES")

        for line_item in input_xml.getElementsByTagName("line-items"):
            if line_item.parentNode.tagName != 'order':
                continue

            order_line = ET.SubElement(order_lines, "ORDERLINE")
            ET.SubElement(order_line, "PROD_NUM").text = line_item.getElementsByTagName("sku")[0].firstChild.data
            ET.SubElement(order_line, "PROD_NAME").text = line_item.getElementsByTagName("title")[0].firstChild.data
            ET.SubElement(order_line, "VENDOR_NUM").text = ""
            ET.SubElement(order_line, "VARIANT").text = ""
            ET.SubElement(order_line, "AMOUNT").text = line_item.getElementsByTagName("quantity")[0].firstChild.data
            ET.SubElement(order_line, "UNIT_PRICE").text = line_item.getElementsByTagName("price")[0].firstChild.data.replace(".", ",")
            ET.SubElement(order_line, "LINE_TOTAL_PRICE").text = f'{float(line_item.getElementsByTagName("quantity")[0].firstChild.data) * float(line_item.getElementsByTagName("price")[0].firstChild.data):.2f}'.replace(".", ",")
            ET.SubElement(order_line, "FILE_URL").text = ""
            ET.SubElement(order_line, "LINE_VAT").text = f'{float(line_item.getElementsByTagName("rate")[0].firstChild.data) * 100:.0f}'

        logging.info(f"Succes! '{file}' blev konverteret\n")

    logging.info(f"Skriver konverteret xml til '{output_file_name}'\n")
    xml_helper.prettify(order_export)
    tree = ET.ElementTree(order_export)
    tree.write(output_file_name, encoding='iso-8859-1', xml_declaration=True, short_empty_elements=False)


if __name__ == "__main__":
    initiate_logger()
    convert_xml_files()
