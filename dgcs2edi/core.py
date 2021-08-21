import xml.etree.ElementTree as ET
from datetime import datetime
from decimal import Decimal
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import configparser


class XMLRead(object):
    """XML Reading class"""
    def __init__(self, file):
        self.tree = ET.parse(file)

    def read_file(self):
        attributes = {}
        items = []

        root = self.tree.getroot()

        for element in root:
            e = element.attrib

            if 'wartosc' in e:
                attributes[e['nazwa']] = e['wartosc']

            elif 'isNull' in e:
                if e['isNull'] == 'true':
                    attributes[e['nazwa']] = 'null'

                else:
                    attributes[e['nazwa']] = e['isNull']

            elif 'lp' in e:
                item = {}
                for detail in element:
                    d = detail.attrib

                    if 'wartosc' in d:
                        item[d['nazwa']] = d['wartosc']

                    elif 'isNull' in d:
                        if d['isNull'] == 'true':
                            item[d['nazwa']] = 'null'

                        else:
                            item[d['nazwa']] = d['isNull']

                items.append(item)

        del root

        return attributes, items

    def close(self):
        del self.tree


class XMLWrite(object):
    """XML Writing class"""
    def __init__(self, attributes, items):
        self.attributes = attributes
        self.items = items
        self.line_count = 0
        self.total_net = 0
        self.total_gross = 0
        self.total_tax = 0
        self.tax_rates = {}

        config = configparser.ConfigParser()
        config.read('./dgcs2edi/db.ini')

        self.iln = config['edi']['iln']
        self.bank = config['edi']['bank_number']
        self.country = config['edi']['country']
        self.bdo = config['edi']['bdo']
        self.krs = config['edi']['krs']

    def _create_file(self, number):
        number = number.replace('/', '-')
        filename = './' + number + '-EDI' + '.xml'
        self.outfile = open(filename, 'w')

        return filename

    def _close_file(self):
        self.outfile.close()

    def write_file(self, country):
        filename = self._create_file(self.attributes['NUMER'])
        self.outfile.writelines('<Document-Invoice>')
        self._write_header()
        self._write_parties(country)
        self._write_lines()
        self._write_summary()
        self.outfile.writelines('</Document-Invoice>')
        self._close_file()

        return filename

    def _write_header(self):
        self.outfile.writelines('<Invoice-Header>')

        self.outfile.writelines('<InvoiceNumber><![CDATA[' + self.attributes['NUMER'] + ']]></InvoiceNumber>')
        self.outfile.writelines('<InvoiceDate>' + self.attributes['DATA_WYSTAWIENIA'][0:10] + '</InvoiceDate>')
        self.outfile.writelines('<SalesDate>' + self.attributes['DATA'][0:10] + '</SalesDate>')
        self.outfile.writelines('<InvoiceCurrency>' + self.attributes['WALUTA'] + '</InvoiceCurrency>')
        self.outfile.writelines('<InvoicePaymentDueDate>' + self.attributes['TERMIN_PLATNOSCI'][0:10] +
                                '</InvoicePaymentDueDate>')

        a = datetime.strptime(self.attributes['DATA_WYSTAWIENIA'][0:10], '%Y-%m-%d')
        b = datetime.strptime(self.attributes['TERMIN_PLATNOSCI'][0:10], '%Y-%m-%d')
        payment_terms = b - a
        self.outfile.writelines('<InvoicePaymentTerms>' + str(payment_terms.days) + '</InvoicePaymentTerms>')

        if self.attributes['NAZWA_PLATNOSCI'] == 'gotówka':
            payment_means = '10'

        else:
            payment_means = '42'
        self.outfile.writelines('<InvoicePaymentMeans>' + payment_means + '</InvoicePaymentMeans>')

        self.outfile.writelines('<DocumentFunctionCode>O</DocumentFunctionCode>')
        self.outfile.writelines('<MessageType>INV</MessageType>')
        self.outfile.writelines('<Remarks>' + self.attributes['UWAGI'] + '</Remarks>')

        self.outfile.writelines('<Order><BuyerOrderNumber></BuyerOrderNumber><BuyerOrderDate></BuyerOrderDate></Order>')

        self.outfile.writelines('<Delivery>')

        self.outfile.writelines('<DeliveryLocationNumber></DeliveryLocationNumber>')
        self.outfile.writelines('<DeliveryDate>' + self.attributes['DATA'][0:10] + '</DeliveryDate>')
        self.outfile.writelines('<DespatchNumber><![CDATA[' + self.attributes['NUMER'] + ']]></DespatchNumber>')

        self.outfile.writelines('</Delivery>')

        self.outfile.writelines('</Invoice-Header>')

    def _write_parties(self, country):
        self.outfile.writelines('<Invoice-Parties>')

        self.outfile.writelines('<Buyer>')

        self.outfile.writelines('<ILN></ILN>')
        self.outfile.writelines('<TaxID>' + self.attributes['NIPKONTR'] + '</TaxID>')
        self.outfile.writelines('<Name><![CDATA[' + self.attributes['NAZWAKONTR'] + ']]></Name>')
        self.outfile.writelines('<StreetAndNumber><![CDATA[' + self.attributes['ADRESKONTR'] + ']]></StreetAndNumber>')
        self.outfile.writelines('<CityName><![CDATA[' + self.attributes['MIASTOKONTR'] + ']]></CityName>')
        self.outfile.writelines('<PostalCode>' + self.attributes['KODMIASTAKONTR'] + '</PostalCode>')
        self.outfile.writelines('<Country>' + country + '</Country>')

        self.outfile.writelines('</Buyer>')

        self.outfile.writelines('<Seller>')

        self.outfile.writelines('<ILN><![CDATA[' + self.iln + ']]></ILN>')
        self.outfile.writelines('<TaxID>' + self.attributes['NIPWYST'] + '</TaxID>')
        self.outfile.writelines('<AccountNumber><![CDATA[' + self.bank + ']]></AccountNumber>')
        self.outfile.writelines('<Name><![CDATA[' + self.attributes['NAZWAWYST'] + ']]></Name>')
        self.outfile.writelines('<StreetAndNumber><![CDATA[' + self.attributes['ADRESWYST'] + ']]></StreetAndNumber>')
        self.outfile.writelines('<CityName><![CDATA[' + self.attributes['MIASTOWYST'] + ']]></CityName>')
        self.outfile.writelines('<PostalCode>' + self.attributes['KODMIASTAWYST'] + '</PostalCode>')
        self.outfile.writelines('<Country>' + self.country + '</Country>')
        if self.bdo != '':
            self.outfile.writelines('<UtilizationRegisterNumber><![CDATA[' + self.bdo
                                    + ']]></UtilizationRegisterNumber>')
        if self.krs != '':
            self.outfile.writelines('<CourtAndCapitalInformation><![CDATA[' + self.krs
                                    + ']]></CourtAndCapitalInformation>')

        self.outfile.writelines('</Seller>')

        self.outfile.writelines('<SellerHeadquarters>')

        self.outfile.writelines('<ILN><![CDATA[' + self.iln + ']]></ILN>')
        self.outfile.writelines('<Name><![CDATA[' + self.attributes['NAZWAWYST'] + ']]></Name>')
        self.outfile.writelines('<StreetAndNumber><![CDATA[' + self.attributes['ADRESWYST'] + ']]></StreetAndNumber>')
        self.outfile.writelines('<CityName><![CDATA[' + self.attributes['MIASTOWYST'] + ']]></CityName>')
        self.outfile.writelines('<PostalCode>' + self.attributes['KODMIASTAWYST'] + '</PostalCode>')
        self.outfile.writelines('<Country>' + self.country + '</Country>')

        self.outfile.writelines('</SellerHeadquarters>')

        self.outfile.writelines('</Invoice-Parties>')

    def _write_lines(self):
        self.outfile.writelines('<Invoice-Lines>')

        for line in self.items:
            self.line_count += 1

            self.outfile.writelines('<Line>')

            self.outfile.writelines('<Line-Item>')

            self.outfile.writelines('<LineNumber>' + str(self.line_count) + '</LineNumber>')
            if line['SYMBOL'] == '':
                self.outfile.writelines('<EAN>' + line['INDEKS'] + '</EAN>')
            else:
                self.outfile.writelines('<EAN>' + line['SYMBOL'] + '</EAN>')
            self.outfile.writelines('<ItemDescription><![CDATA[' + line['NAZWAPRODUKTU'] + ']]></ItemDescription>')
            self.outfile.writelines('<ItemType>' + 'CU' + '</ItemType>')
            self.outfile.writelines('<InvoiceQuantity>' + str("{0:.3f}".format(Decimal(line['ILOSCWYDANA']))) +
                                    '</InvoiceQuantity>')

            if line['JEDNOSTKA'] == 'szt.':
                unit = 'PCE'

            elif line['JEDNOSTKA'] == 'm b.':
                unit = 'MTR'

            elif line['JEDNOSTKA'] == 'm kw.':
                unit = 'MTK'

            elif line['JEDNOSTKA'] == 'kg':
                unit = 'KGM'

            elif line['JEDNOSTKA'] == 'litr':
                unit = 'LTR'

            elif line['JEDNOSTKA'] == 'Tona':
                unit = 'TNE'

            else:
                unit = 'PCE'

            self.outfile.writelines('<UnitOfMeasure>' + unit + '</UnitOfMeasure>')

            self.outfile.writelines('<InvoiceUnitNetPrice>' + str("{0:.2f}".format(Decimal(line['NETTOWWALUCIE']))) +
                                    '</InvoiceUnitNetPrice>')
            self.outfile.writelines('<InvoiceUnitGrossPrice>' + str("{0:.2f}".format(Decimal(line['BRUTTOWWALUCIE']))) +
                                    '</InvoiceUnitGrossPrice>')

            tax_rate = "{0:.2f}".format((Decimal(line['STAWKAPODATKU'])) * 100)
            if tax_rate not in self.tax_rates:
                self.tax_rates[tax_rate] = [0, 0, 0]
            self.outfile.writelines('<TaxRate>' + str(tax_rate) + '</TaxRate>')
            self.outfile.writelines('<TaxCategoryCode>S</TaxCategoryCode>')

            net = (Decimal(line['NETTOWWALUCIE']) * Decimal(line['ILOSCWYDANA']))
            tax = net * Decimal(line['STAWKAPODATKU'])
            gross = net + tax

            self.total_gross += gross
            self.total_net += net
            self.total_tax += tax
            self.tax_rates[tax_rate][0] += tax
            self.tax_rates[tax_rate][1] += net
            self.tax_rates[tax_rate][2] += gross

            self.outfile.writelines('<TaxAmount>' + str("{0:.2f}".format(tax)) + '</TaxAmount>')
            self.outfile.writelines('<NetAmount>' + str("{0:.2f}".format(net)) + '</NetAmount>')

            self.outfile.writelines('</Line-Item>')

            self.outfile.writelines('</Line>')

        self.outfile.writelines('</Invoice-Lines>')

    def _write_summary(self):
        self.outfile.writelines('<Invoice-Summary>')

        self.outfile.writelines('<TotalLines>' + str(self.line_count) + '</TotalLines>')
        self.outfile.writelines('<TotalNetAmount>' + str("{0:.2f}".format(self.total_net)) + '</TotalNetAmount>')
        self.outfile.writelines('<TotalTaxableBasis>' + str("{0:.2f}".format(self.total_net)) + '</TotalTaxableBasis>')
        self.outfile.writelines('<TotalTaxAmount>' + str("{0:.2f}".format(self.total_tax)) + '</TotalTaxAmount>')
        self.outfile.writelines('<TotalGrossAmount>' + str("{0:.2f}".format(self.total_gross)) + '</TotalGrossAmount>')
        self.outfile.writelines('<Tax-Summary>')

        for tax_rate in self.tax_rates:
            self.outfile.writelines('<Tax-Summary-Line>')
            self.outfile.writelines('<TaxRate>' + str(tax_rate) + '</TaxRate>')
            self.outfile.writelines('<TaxCategoryCode>' + 'S' + '</TaxCategoryCode>')
            self.outfile.writelines('<TaxAmount>' + str("{0:.2f}".format(self.tax_rates[tax_rate][0])) + '</TaxAmount>')
            self.outfile.writelines('<TaxableBasis>' + str("{0:.2f}".format(self.tax_rates[tax_rate][1])) +
                                    '</TaxableBasis>')
            self.outfile.writelines('<TaxableAmount>' + str("{0:.2f}".format(self.tax_rates[tax_rate][1])) +
                                    '</TaxableAmount>')
            self.outfile.writelines('<GrossAmount>' + str("{0:.2f}".format(self.tax_rates[tax_rate][2])) +
                                    '</GrossAmount>')
            self.outfile.writelines('</Tax-Summary-Line>')

        self.outfile.writelines('</Tax-Summary>')

        self.outfile.writelines('</Invoice-Summary>')


class XMLSend(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./dgcs2edi/db.ini')

        self.user = config['email']['login']
        self.passwd = config['email']['passwd']
        self.server = config['email']['server']
        self.port = config['email']['port']
        self.content = config['email']['content'] + '\n\n\n'
        self.subject = config['email']['subject']

    def send_invoice(self, receiver, filename):

        message = MIMEMultipart()
        message["From"] = self.user
        message["To"] = receiver
        message["Subject"] = self.subject

        message.attach(MIMEText(self.content, "plain"))

        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        message.attach(part)
        text = message.as_string()

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.server, self.port, context=context) as server:
            server.login(self.user, self.passwd)
            server.sendmail(self.user, receiver, text)
