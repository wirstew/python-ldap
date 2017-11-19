# -*- coding: utf-8 -*-
"""
Automatic tests for python-ldap's module ldap.dn

See https://www.python-ldap.org/ for details.
"""

# from Python's standard lib
import unittest

# from python-ldap
import ldap.dn


class TestDN(unittest.TestCase):
    """
    test ldap.functions
    """

    def test_is_dn(self):
        """
        test function is_dn()
        """
        self.assertEqual(ldap.dn.is_dn('foobar,ou=ae-dir'), False)
        self.assertEqual(ldap.dn.is_dn('-cn=foobar,ou=ae-dir'), False)
        self.assertEqual(ldap.dn.is_dn(';cn=foobar,ou=ae-dir'), False)
        self.assertEqual(ldap.dn.is_dn(',cn=foobar,ou=ae-dir'), False)
        self.assertEqual(ldap.dn.is_dn('cn=foobar,ou=ae-dir,'), False)
        self.assertEqual(ldap.dn.is_dn('uid=xkcd,cn=foobar,ou=ae-dir'), True)
        self.assertEqual(
            ldap.dn.is_dn(
                'cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c.o=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f'
            ),
            True
        )

    def test_escape_dn_chars(self):
        """
        test function escape_dn_chars()
        """
        self.assertEqual(ldap.dn.escape_dn_chars('foobar'), 'foobar')
        self.assertEqual(ldap.dn.escape_dn_chars('foo,bar'), 'foo\\,bar')
        self.assertEqual(ldap.dn.escape_dn_chars('foo=bar'), 'foo\\=bar')
        self.assertEqual(ldap.dn.escape_dn_chars('foo#bar'), 'foo#bar')
        self.assertEqual(ldap.dn.escape_dn_chars('#foobar'), '\\#foobar')
        self.assertEqual(ldap.dn.escape_dn_chars('foo bar'), 'foo bar')
        self.assertEqual(ldap.dn.escape_dn_chars(' foobar'), '\\ foobar')

    def test_str2dn(self):
        """
        test function str2dn()
        """
        self.assertEqual(ldap.dn.str2dn(''), [])
        self.assertEqual(
            ldap.dn.str2dn('uid=test42,ou=Testing,dc=example,dc=com'),
            [
                [('uid', 'test42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )
        self.assertEqual(
            ldap.dn.str2dn('uid=test42+uidNumber=42,ou=Testing,dc=example,dc=com'),
            [
                [('uid', 'test42', 1), ('uidNumber', '42', 1) ],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )
        self.assertEqual(
            ldap.dn.str2dn('uid=test42,ou=Testing,dc=example,dc=com', flags=0),
            [
                [('uid', 'test42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )
        self.assertEqual(
            ldap.dn.str2dn('uid=test\\, 42,ou=Testing,dc=example,dc=com', flags=0),
            [
                [('uid', 'test, 42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )
        self.assertEqual(
            ldap.dn.str2dn('cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f,dc=example,dc=com', flags=0),
            [
                [('cn', '\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 4)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )
        self.assertEqual(
            ldap.dn.str2dn('cn=\\c3\\a4\\c3\\b6\\c3\\bc\\c3\\84\\c3\\96\\c3\\9c\\c3\\9f,dc=example,dc=com', flags=0),
            [
                [('cn', '\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 4)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]
        )

    def test_dn2str(self):
        """
        test function dn2str()
        """
        self.assertEqual(ldap.dn.str2dn(''), [])
        self.assertEqual(
            ldap.dn.dn2str([
                [('uid', 'test42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'uid=test42,ou=Testing,dc=example,dc=com',
        )
        self.assertEqual(
            ldap.dn.dn2str([
                [('uid', 'test42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'uid=test42,ou=Testing,dc=example,dc=com'
        )
        self.assertEqual(
            ldap.dn.dn2str([
                [('uid', 'test42', 1), ('uidNumber', '42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'uid=test42+uidNumber=42,ou=Testing,dc=example,dc=com'
        )
        self.assertEqual(
            ldap.dn.dn2str([
                [('uid', 'test, 42', 1)],
                [('ou', 'Testing', 1)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'uid=test\\, 42,ou=Testing,dc=example,dc=com'
        )
        self.assertEqual(
            ldap.dn.dn2str([
                [('cn', '\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 4)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f,dc=example,dc=com'
        )
        self.assertEqual(
            ldap.dn.dn2str([
                [('cn', '\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 4)],
                [('dc', 'example', 1)],
                [('dc', 'com', 1)]
            ]),
            'cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f,dc=example,dc=com'
        )

    def test_explode_dn(self):
        """
        test function explode_dn()
        """
        self.assertEqual(ldap.dn.explode_dn(''), [])
        self.assertEqual(
            ldap.dn.explode_dn('uid=test42,ou=Testing,dc=example,dc=com'),
            ['uid=test42', 'ou=Testing', 'dc=example', 'dc=com']
        )
        self.assertEqual(
            ldap.dn.explode_dn('uid=test42,ou=Testing,dc=example,dc=com', flags=0),
            ['uid=test42', 'ou=Testing', 'dc=example', 'dc=com']
        )
        self.assertEqual(
            ldap.dn.explode_dn('uid=test42,ou=Testing,dc=example,dc=com', notypes=True),
            ['test42', 'Testing', 'example', 'com']
        )
        self.assertEqual(
            ldap.dn.explode_dn('uid=test\\, 42,ou=Testing,dc=example,dc=com', flags=0),
            ['uid=test\\, 42', 'ou=Testing', 'dc=example', 'dc=com']
        )
        self.assertEqual(
            ldap.dn.explode_dn('cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f,dc=example,dc=com', flags=0),
            ['cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 'dc=example', 'dc=com']
        )
        self.assertEqual(
            ldap.dn.explode_dn('cn=\\c3\\a4\\c3\\b6\\c3\\bc\\c3\\84\\c3\\96\\c3\\9c\\c3\\9f,dc=example,dc=com', flags=0),
            ['cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', 'dc=example', 'dc=com']
        )

    def test_explode_rdn(self):
        """
        test function explode_rdn()
        """
        self.assertEqual(ldap.dn.explode_rdn(''), [])
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42'),
            ['uid=test42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42', notypes=False, flags=0),
            ['uid=test42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42', notypes=0, flags=0),
            ['uid=test42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42+uidNumber=42', flags=0),
            ['uid=test42', 'uidNumber=42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42', notypes=True),
            ['test42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test42', notypes=1),
            ['test42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('uid=test\\+ 42', flags=0),
            ['uid=test\\+ 42']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f', flags=0),
            ['cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f']
        )
        self.assertEqual(
            ldap.dn.explode_rdn('cn=\\c3\\a4\\c3\\b6\\c3\\bc\\c3\\84\\c3\\96\\c3\\9c\\c3\\9f', flags=0),
            ['cn=\xc3\xa4\xc3\xb6\xc3\xbc\xc3\x84\xc3\x96\xc3\x9c\xc3\x9f']
        )


if __name__ == '__main__':
    unittest.main()
