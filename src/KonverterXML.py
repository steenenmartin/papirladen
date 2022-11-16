import os
import xml.etree.ElementTree as ET
import logging

from datetime import datetime
from xml.dom import minidom

from utils.xml_helper import XmlHelper
from utils.logging_helper import initiate_logger


def convert_xml_files() -> ET.ElementTree:
    all_files = os.listdir("./Import")
    xml_files = [file for file in all_files if file.endswith('.xml')]

    if not xml_files:
        error_msg = "Der var ingen xml filer i 'Import'-mappen at konvertere. Programmet stopper."
        logging.error(error_msg)
        raise Exception(error_msg)

    # Create output XML tree structure
    order_export = ET.Element('ORDER_EXPORT')
    order_export.set("type", "ORDERS")
    elements = ET.SubElement(order_export, "ELEMENTS")

    for file in xml_files:
        logging.info(f"Konverterer '{file}'")
        # Read input XML:
        input_xml = XmlHelper(minidom.parse("./Import/" + file))
        order = ET.SubElement(elements, "ORDER")

        # Create "GENERAL"-element
        general = ET.SubElement(order, "GENERAL")
        try:
            ET.SubElement(general, "ORDER_ID").text = input_xml.get_element_by_tag_name('order-number')
            ET.SubElement(general, "LANGUAGE_ID").text = "26"

            created_at_element = input_xml.get_element_by_tag_name('created-at', lambda x: x.parentNode.tagName == "order")
            created_at = datetime.fromisoformat(created_at_element)
            ET.SubElement(general, "DATE").text = created_at.strftime("%d-%m-%Y %H:%M:%S")

            ET.SubElement(general, "CURRENCY_CODE").text = "DKK"
            ET.SubElement(general, "ORDER_TOTAL_PRICE").text = ""  # input_xml.getElementsByTagName('total-price')[0]
            ET.SubElement(general, "ORDER_VAT").text = "25"
            ET.SubElement(general, "TOTAL_WEIGHT").text = f"{float(input_xml.get_element_by_tag_name('total-weight')) / 1000}".replace(".", ",")
            ET.SubElement(general, "STATE_ID").text = "1"
            ET.SubElement(general, "REFERRER").text = "https://www.papirladen.dk/admin/Modules/Login/Login"
            ET.SubElement(general, "CUST_COMMENTS").text = input_xml.get_element_by_tag_name('note', lambda x: x.parentNode.tagName != "customer")

            # Create "ADVANCED"-element
            advanced = ET.SubElement(order, "ADVANCED")
            ET.SubElement(advanced, "REFERENCE_NUM").text = ""
            ET.SubElement(advanced, "IP_ADRESS").text = input_xml.get_element_by_tag_name('browser-ip', lambda x: x.parentNode.tagName == "order")
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
            pakkeshop_id = input_xml.get_element_by_tag_name("code", lambda x: x.parentNode.tagName == "shipping-line").split("_")[-1]
            ET.SubElement(shipping_method, "SHIP_METHOD_ID").text = "58" if pakkeshop_id.isdigit() else "55"
            ET.SubElement(shipping_method, "SHIP_METHOD_NAME").text = "GLS Pakkeshop - HENT SELV"
            ET.SubElement(shipping_method, "SHIP_METHOD_FEE").text = "37,50"
            ET.SubElement(shipping_method, "SHIP_METHOD_FEE_INCL_VAT").text = "True"

            # Create "CUSTOMER"-element
            customer = ET.SubElement(order, "CUSTOMER")
            ET.SubElement(customer, "CUST_NUM").text = "53794648"
            ET.SubElement(customer, "VAT_REG_NUM").text = ""

            ET.SubElement(customer, "CUST_NAME").text = (
                input_xml.get_element_by_tag_name("phone", lambda x: x.parentNode.tagName == "billing-address").replace(" ", "") + " " +
                input_xml.get_element_by_tag_name("first-name", lambda x: x.parentNode.tagName == "billing-address") + " " +
                input_xml.get_element_by_tag_name("last-name", lambda x: x.parentNode.tagName == "billing-address")
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

            shipping_line_title = input_xml.get_element_by_tag_name("title", lambda x: x.parentNode.tagName == "shipping-line").split(" ")
            deliv_name = " ".join(shipping_line_title)
            for i in range(len(shipping_line_title) - 2):
                if shipping_line_title[i] == "Din" and shipping_line_title[i + 1] == "Pakkeshop":
                    deliv_name = shipping_line_title[i] + " " + shipping_line_title[i + 1] + " " + shipping_line_title[i + 2]
                    break

            ET.SubElement(delivery_info, "DELIV_NAME").text = deliv_name
            ET.SubElement(delivery_info, "DELIV_COMPANY").text = ""
            ET.SubElement(delivery_info, "DELIV_ADDRESS").text = ""
            ET.SubElement(delivery_info, "DELIV_ADDRESS_2").text = "Pakkeshop: " + pakkeshop_id
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
            error_msg = f"Filen '{file}' blev ikke konverteret. Kontroller, at der ikke er andre .xml-filer i mappen end dem, der skal konverteres. Fejlbesked: '{e}'\n"
            logging.error(error_msg)
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

        for line_item in input_xml.get_elements_by_tag_name("line-item", lambda x: x.parentNode.tagName == "line-items"):
            if line_item.parentNode.parentNode.tagName != 'fulfillment':
                continue

            line_item = XmlHelper(line_item)

            def is_line_item_element(element):
                return element.parentNode.tagName == "line-item"

            order_line = ET.SubElement(order_lines, "ORDERLINE")
            ET.SubElement(order_line, "PROD_NUM").text = line_item.get_element_by_tag_name("sku", is_line_item_element)
            ET.SubElement(order_line, "PROD_NAME").text = line_item.get_element_by_tag_name("name", is_line_item_element)
            ET.SubElement(order_line, "VENDOR_NUM").text = ""
            ET.SubElement(order_line, "VARIANT").text = ""
            quantity = line_item.get_element_by_tag_name("quantity", is_line_item_element)
            ET.SubElement(order_line, "AMOUNT").text = quantity
            price = line_item.get_element_by_tag_name("price", is_line_item_element)
            ET.SubElement(order_line, "UNIT_PRICE").text = price.replace(".", ",")
            ET.SubElement(order_line, "LINE_TOTAL_PRICE").text = f'{float(quantity) * float(price):.2f}'.replace(".", ",")
            ET.SubElement(order_line, "FILE_URL").text = ""
            line_vat = "25"
            try:
                line_vat = f'{float(line_item.get_element_by_tag_name("rate")) * 100:.0f}'
            except:
                logging.error(f'Mangler tax-line på produktnummer {line_item.get_element_by_tag_name("sku")}. Defaulter til 25 %.')

            ET.SubElement(order_line, "LINE_VAT").text = line_vat

        logging.info(f"Succes! '{file}' blev konverteret\n")

    XmlHelper.prettify(order_export)

    return ET.ElementTree(order_export)


if __name__ == "__main__":
    output_folder_path = "./Output/"
    initiate_logger(output_folder_path)

    if not os.path.exists("./Import"):
        error = "Mappen 'Import' eksisterer ikke. Programmet stopper."
        logging.error(error)

    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)

    tree = convert_xml_files()

    out_file_name = "export-ORDERS.xml"
    logging.info(f"Skriver konverteret xml til '{output_folder_path + out_file_name}'\n")
    tree.write(
        output_folder_path + out_file_name,
        encoding='iso-8859-1',
        xml_declaration=True,
        short_empty_elements=False
    )

