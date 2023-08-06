"""Storage module for classes RssParser and Printer"""

import json
import xmltodict
import logging
import config
from getter import GetterXml

logger = logging.getLogger('app.rss_parser')


class Printer:
    """Class for printing info"""

    def print_info(self, data_to_print: dict):
        """
        Print info in stdout
        :param data_to_print: data for printing
        """
        for item in data_to_print['item']:
            print('\n', "- " * 10, '\n')
            print(f'Title: {item.get("title")}\nData: {item.get("pubDate")}\nLink: {item.get("link")}')
            # if item.get("description"):
            #     print(f'\nDescription: {item.get("description")}')
            # print(f'\n\nLinks:\n[1]: {item.get("link")}\n[2]: {item.get("media:thumbnail").get("@url")}')

    def print_info_json(self, data_to_print: dict):
        """
        Print info in json format
        :param data_to_print: data for printing
        """
        for item in data_to_print['item']:
            item_in_json = json.dumps(item, ensure_ascii=False).encode('utf8')
            print('\n', "- " * 10, '\n')
            print(item_in_json.decode())


class RssParser:
    """Class for parsing response received by getter.py and printing result"""

    def parse_xml(self, args) -> dict:
        """
        Transform XML data to dict
        :arg args: set of arguments
        :return: dictionary with XLM data
        """
        data_dict_input = xmltodict.parse(GetterXml().get_response(args.source).text, encoding='utf-8')
        logger.debug(data_dict_input)
        data_dict_out = {"item": []}

        for item in data_dict_input['rss']['channel']['item'][:args.limit]:
            data_dict_out['item'].append(
                {"title": item.get("title"), "pubDate": item.get("pubDate"),
                 "link": item.get("link")})  # "description": item.get("description")
        logger.debug(f'Out dict - {data_dict_out}')
        return data_dict_out

    @staticmethod
    def start():
        """ Start work with rss_parser"""
        args = config.AppArgParser().get_args()

        if args.verbose:
            config.AppLogger.activate_verbose()
            logger.info(f'Verbose mode activated.')

        logger.debug(f'Argparse sent these arguments - {args.__dict__}')

        parser = RssParser()
        logger.info("Module rss_parser is starting.")

        if args.json:
            logger.info(f'Json mode activated.')
            Printer().print_info_json(parser.parse_xml(args))
        else:
            Printer().print_info(parser.parse_xml(args))
