#!/usr/bin/python3
# -*- coding: utf8 -*-

from miniirc import IRC
import requests
import xml.etree.ElementTree as et
import os


def pars_rss(xml_file):
    tree = et.parse(xml_file)
    root = tree.getroot()
    titles_links_dict = []
    for items in root.iter("item"):
        for titles in items.iter("title"):
            for links in items.iter("link"):
                titles_links_dict.append(titles.text + ' ' + links.text)

    return titles_links_dict


def w_file(filename, data):
    file = open(filename, 'w')
    file.write(data)
    file.close()


def irc_send(send_data):
    # Variables
    nick = 'Hata_Bot'
    ident = nick
    realname = 'Hata RSS Bot'
    identity = None
    channels = ['#hata_test']
    debug = False
    ip = '127.0.0.1'
    port = 6668

    irc = IRC(ip, port, nick, channels, ident=ident, realname=realname,
              ns_identity=identity, debug=debug, auto_connect=False)

    irc.connect()
    print('Connection established...')
    irc.send('PRIVMSG', '#hata_test', send_data)
    irc.disconnect()


def get_rss():
    s = requests.Session()
    s.proxies = {"http": "http://127.0.0.1:4444"}
    rss = s.get("http://hata.i2p/index.php?action=.xml;type=rss2")
    print('RSS received! ')
    print('')

    try:
        rssfile = open('rss.xml')
    except IOError as e:
        print('Could not open file! Create file!...')
        print('')
        w_file('rss.xml', rss.content.decode())
        return True

    else:
        print('Difference Check!')
        print('')
        w_file('rss_check.xml', rss.content.decode())

        if os.path.getsize('rss.xml') == os.path.getsize('rss_check.xml'):
            print('Files are identical -> Cancel operation -> Remove temp file')
            print('')
            os.remove('rss_check.xml')
            return False

        else:
            print('Files are not identical -> Go! ')
            print('')
            return True


def main():
    print('# Hata Botan RSS Bot #')
    print('')
    decision = get_rss()
    messages = pars_rss('rss.xml')

    if decision == True:
        for items in messages:
            irc_send(items)
            print(' Message ', items, ' sens...')
    else:
        exit(0)


if __name__ == "__main__":
    main()
