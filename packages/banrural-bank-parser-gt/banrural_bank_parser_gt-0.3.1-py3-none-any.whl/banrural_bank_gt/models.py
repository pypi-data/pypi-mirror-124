from bank_base_gt import (
    AbstractBankAccount,
    BaseBank,
    Bank,
    InvalidCredentialsException,
    Movement,
    MovementPageNonAvailable,
)
from bank_base_gt.bank import ChangePasswordRequired
from bs4 import BeautifulSoup
from urllib.parse import parse_qs, quote_plus
import random
import string
from money import Money
import time
import datetime
import logging
import sys


BANRURAL_ERRORS = {
    "INVALID_CREDENTIALS": " Nombre de usuario o credenciales de autentificación inválidas",
    "CHANGE_PASSWORD": "CAMBIO DE CLAVE REQUERIDO, 90 DIAS DESDE LA ULTIMA MODIFICACION",
}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)


class BanruralBaseBank(BaseBank):
    def __init__(self):
        super().__init__(
            login_url="https://www.banrural.com.gt/corp/a/principal.asp",
            accounts_url="https://www.banrural.com.gt/corp/a/consulta_saldos.asp",
            movements_url="https://www.banrural.com.gt/corp/a/consulta_movimientos_resp.asp",
            logout_url="https://www.banrural.com.gt/corp/a/default.asp",
        )


class BanruralBank(Bank):
    def __init__(self, credentials):
        super().__init__("Banrural", BanruralBaseBank(), credentials)

    def login(self):
        r = self._fetch(
            self.login_url,
            {
                "UserName": self.credentials.username,
                "password": self.credentials.password,
            },
        )
        bs = BeautifulSoup(r, features="html.parser")
        error_fields = [
            bs.find("td", {"class": "txt_normal"}),
            bs.find("td", {"class": "txt_normal_bold"}),
        ]
        error_fields = error_fields[error_fields is not None]
        if error_fields:
            for field in error_fields:
                logger.error("TXT Field {0}".format(field.string))
                if field and BANRURAL_ERRORS["INVALID_CREDENTIALS"] in field.string:
                    logger.error("Invalid Credentials: {0}".format(field.string))
                    raise InvalidCredentialsException(field.string)
                elif field and BANRURAL_ERRORS["CHANGE_PASSWORD"] in field.string:
                    logger.error("Change of password required")
                    raise ChangePasswordRequired(field.string)
        logger.info("Log in finished succesfully")
        return True

    def fetch_accounts(self):
        accounts = []
        logger.info("Will start to fetch accounts")
        r = self._fetch(self.accounts_url)
        bs = BeautifulSoup(r, features="html.parser")
        account_table = bs.findAll("tr", {"class": "tabledata_gray"})
        for account_row in account_table:
            text_of_account = account_row.findAll("span")
            alias = text_of_account[0].string.strip()
            account_num = text_of_account[1].string.strip()
            account_type = text_of_account[2].string.strip()
            currency = text_of_account[3].string.strip()
            movements_link = account_row.findAll("a")[1]
            internal_reference = None
            if movements_link:
                link = movements_link["href"]
                internal_reference = self._build_internal_reference_account(link)

            account = BanruralBankAccount(
                self, account_num, alias, account_type, currency, internal_reference
            )
            logger.info("Found new account with number {0}".format(account_num))
            accounts.append(account)
        logger.info("Finish fetching accounts")

        return accounts

    def get_account(self, number):
        accounts = self.fetch_accounts()
        for account in accounts:
            if account.account_number == number:
                return account

        return None

    def logout(self):
        r = self._fetch(
            self.logout_url,
            headers={"Referer": "https://www.banrural.com.gt/corp/a/menu_nuevo.asp"},
        )
        logger.info("Did logout")

        return True

    def _build_internal_reference_account(self, url):
        query_params = parse_qs(url.split("?")[1], keep_blank_values=True)
        return "{0};{1};{2};{3};{4}".format(
            query_params["cta"][0],
            query_params["moneda"][0],
            query_params["producto"][0],
            quote_plus(query_params["alias"][0]),
            query_params["descmoneda"][0],
        )


class BanruralBankAccount(AbstractBankAccount):
    _FILE_NAME = "".join(random.choices(string.digits, k=8))
    _DEFAULT_HEADERS = {
        "Referer": "https://www.banrural.com.gt/corp/a/consulta_movimientos.asp"
    }

    def _convert_date_format(self, date_string):
        first_two = date_string[0:2]
        second_two = date_string[3:5]
        return "{0}/{1}/{2}".format(second_two, first_two, date_string[6:])

    def process_mov_line(self, line):
        splitted = line.split(";")
        if len(splitted) <= 6:
            return None
        date = datetime.datetime.strptime(splitted[0], "%d/%m/%Y")
        description = splitted[2]
        document_number = splitted[3]
        ammount = splitted[5].replace(",", "")
        is_credit = splitted[4] == "C"
        alternative_transaction_id = splitted[10]
        m = Money(amount=ammount, currency="GTQ")
        if not is_credit:
            m = -1 * m
        return Movement(
            self,
            document_number,
            date,
            description,
            m,
            alternative_transaction_id=alternative_transaction_id,
        )

    def _convert_date_to_txt_format(self, date):
        return date.strftime("%d/%m/%Y")

    def _get_initial_dict(self, start_date, end_date):
        date_query_start = self._convert_date_to_txt_format(start_date)
        date_query_end = self._convert_date_to_txt_format(end_date)
        datehd_query_start = self._convert_date_format(date_query_start)
        datehd_query_end = self._convert_date_format(date_query_end)
        form_data = {
            "ddmCuentas": self.account_bank_reference,
            "txtfechainicial": date_query_start,
            "txtfechafinal": date_query_end,
            "transmitir": "TRANSMITIR",
            "HSec": 40,
            "HSecAlt": 3000,
            "hdFechaInicial": datehd_query_start,
            "hdFechaFinal": datehd_query_end,
            "hdArchivo": type(self)._FILE_NAME,
        }
        logger.info(
            "Will request MOVEMENTS with this initial data {0}".format(form_data)
        )
        return form_data

    def _iterate_all_pages(
        self, start_date, end_date, form_data=None, previous_page=None
    ):
        if form_data is None:
            form_data = self._get_initial_dict(start_date, end_date)
        headers = type(self)._DEFAULT_HEADERS
        bs = BeautifulSoup(
            self.bank._fetch(self.bank.movements_url, form_data, headers),
            features="html.parser",
        )
        submit = bs.findAll("input", {"value": "SIGUIENTE"})
        form = bs.findAll("form")
        needs_to_exit = False
        if len(form) == 0 and previous_page:
            bs = previous_page
            submit = bs.findAll("input", {"value": "SIGUIENTE"})
            form = bs.findAll("form")
            needs_to_exit = True

        fields = form[0].findAll("input")
        form_data = dict((field.get("name"), field.get("value")) for field in fields)
        logger.info(
            "Will request MOVEMENTS with this initial data {0}".format(form_data)
        )

        if submit and not needs_to_exit:
            logger.info("Downloading next movement page")
            self._iterate_all_pages(start_date, end_date, form_data, previous_page=bs)

        file_name = bs.findAll("input")[-1]["onclick"].split("/")[-1][0:-1]
        return file_name

    def fetch_movements(self, start_date, end_date):
        file_name = self._iterate_all_pages(start_date, end_date)
        logger.info("Finished fetching all pages")
        txt_file = self.bank._fetch("https://www.banrural.com.gt/corp/ofc/" + file_name)
        logger.info("Downloaded TXT file with movements")
        lines = txt_file.decode("utf-8").split("\r\n")
        movements = []
        for line in lines:
            movement = self.process_mov_line(line)
            if movement:
                movements.append(movement)
        logger.info("Finished processing all movements")
        return movements
