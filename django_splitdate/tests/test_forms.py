# -*- coding: utf-8 -*-
from datetime import date
import logging
from django.test import TestCase, override_settings
from django.utils import translation
from django.utils.translation import ugettext_lazy
from ..forms import SplitDateWidget, get_placeholder
from ..app_settings import Settings
__author__ = 'Tim Schneider <tim.schneider@northbridge-development.de>'
__copyright__ = "Copyright 2015, Northbridge Development Konrad & Schneider GbR"
__credits__ = ["Tim Schneider", ]
__maintainer__ = "Tim Schneider"
__email__ = "mail@northbridge-development.de"
__status__ = "Development"

logger = logging.getLogger(__name__)

class GetPlaceholderTestCase(TestCase):
    def test_day(self):
        placeholder = get_placeholder(0, 'dmy', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        self.assertEqual(placeholder, 'Day')

    def test_month(self):
        placeholder = get_placeholder(1, 'dmy', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        self.assertEqual(placeholder, 'Month')

    def test_year(self):
        placeholder = get_placeholder(2, 'dmy', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        self.assertEqual(placeholder, 'Year')

    def test_errors(self):
        #too long
        self.assertRaises(ValueError, get_placeholder, 0, 'dmya', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        #too short
        self.assertRaises(ValueError, get_placeholder, 0, 'dm', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        # no day
        self.assertRaises(ValueError, get_placeholder, 0, 'amy', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        # no month
        self.assertRaises(ValueError, get_placeholder, 0, 'day', {'d': 'Day', 'm': 'Month', 'y': 'Year'})
        #no year
        self.assertRaises(ValueError, get_placeholder, 0, 'dma', {'d': 'Day', 'm': 'Month', 'y': 'Year'})

class SplitDateWidgetTestCase(TestCase):

    def setUp(self):
        Settings._SPLITDATE_ORDER = None
        Settings._SPLITDATE_PLACEHOLDER_DAY = None
        Settings._SPLITDATE_PLACEHOLDER_MONTH = None
        Settings._SPLITDATE_PLACEHOLDER_YEAR = None

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmy',
    )
    def test___init___global_config(self):
        widget = SplitDateWidget()
        self.assertEqual(len(widget.widgets), 3)
        self.assertEqual(unicode(widget.widgets[0].attrs['placeholder']), 'DAY')
        self.assertEqual(unicode(widget.widgets[1].attrs['placeholder']), 'MONTH')
        self.assertEqual(unicode(widget.widgets[2].attrs['placeholder']), 'YEAR')
        self.assertEqual(unicode(widget.ordering), 'dmy')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmy',
    )
    def test___init___local_config(self):
        widget = SplitDateWidget(
            field_ordering='ymd',
            placeholder_day='day',
            placeholder_month='month',
            placeholder_year='year',
        )
        self.assertEqual(len(widget.widgets), 3)
        self.assertEqual(unicode(widget.widgets[0].attrs['placeholder']), 'year')
        self.assertEqual(unicode(widget.widgets[1].attrs['placeholder']), 'month')
        self.assertEqual(unicode(widget.widgets[2].attrs['placeholder']), 'day')
        self.assertEqual(unicode(widget.ordering), 'ymd')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='DMY',
    )
    def test___init___to_order_lowercase(self):
        widget = SplitDateWidget()
        self.assertEqual(unicode(widget.ordering), 'DMY')

    def test_get_ordering_string_by_language(self):
        widget = SplitDateWidget()
        translation.activate('de_DE')
        # Test language directly included
        ret = widget.get_ordering_string_by_language({'en': 'en', 'de_DE': 'de_DE'})
        self.assertEqual(ret, 'de_DE')

        # Test only starts with
        ret = widget.get_ordering_string_by_language({'en': 'en', 'de': 'de'})
        self.assertEqual(ret, 'de')

        # Test not included
        ret = widget.get_ordering_string_by_language({'en': 'en', })
        self.assertEqual(ret, 'en')

        # test none at all
        ret = widget.get_ordering_string_by_language({})
        self.assertEqual(ret, 'dmy')

        translation.activate('en')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmy',
    )
    def test_get_ordering_ok(self):
        widget = SplitDateWidget()
        self.assertEqual('dmy', widget.get_ordering())

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER={'en': 'mdy', 'de':'dmy'},
    )
    def test_get_ordering_translation(self):
        widget = SplitDateWidget()
        translation.activate('de')
        self.assertEqual('dmy', widget.get_ordering())
        translation.activate('en')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='DMY',
    )
    def test_get_ordering_ok_upper(self):
        widget = SplitDateWidget()
        self.assertEqual('dmy', widget.get_ordering())

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmyy',
    )
    def test_get_ordering_ordererror_length(self):
        widget = SplitDateWidget()
        self.assertRaises(ValueError, widget.get_ordering)

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='mmy',
    )
    def test_get_ordering_ordererror_day_missing(self):
        widget = SplitDateWidget()
        self.assertRaises(ValueError, widget.get_ordering)

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='ddy',
    )
    def test_get_ordering_ordererror_month_missing(self):
        widget = SplitDateWidget()
        self.assertRaises(ValueError, widget.get_ordering)

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmm',
    )
    def test_get_ordering_ordererror_year_missing(self):
        widget = SplitDateWidget()
        self.assertRaises(ValueError, widget.get_ordering)

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER=ugettext_lazy('mdy'),
    )
    def test_get_ordering_two_languages(self):
        widget = SplitDateWidget()
        translation.activate('en')
        self.assertEqual(widget.get_ordering(), 'mdy')
        translation.activate('de')
        self.assertEqual(widget.get_ordering(), 'dmy')
        translation.activate('en')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmy',
    )
    def test_decompress(self):
        widget = SplitDateWidget()

        ret = widget.decompress(None)
        self.assertListEqual(ret, [None, None, None])

        ret = widget.decompress(date(2000, 02, 01))
        self.assertListEqual(ret, ['01', '02', '2000'])

        ret = widget.decompress('01.02.2000')
        self.assertListEqual(ret, ['01', '02', '2000'])

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='mdy',
    )
    def test_decompress_second_ordering(self):
        widget = SplitDateWidget()

        ret = widget.decompress('01.02.2000')
        self.assertListEqual(ret, ['02', '01', '2000'])

        ret = widget.decompress(date(2000, 02, 01))
        self.assertListEqual(ret, ['02', '01', '2000'])

    def test_decompress_wrong_date_format(self):
        widget = SplitDateWidget()

        self.assertRaises(ValueError, widget.decompress, '02/01/2000')

    @override_settings(
        SPLITDATE_PLACEHOLDER_DAY='DAY',
        SPLITDATE_PLACEHOLDER_MONTH='MONTH',
        SPLITDATE_PLACEHOLDER_YEAR='YEAR',
        SPLITDATE_ORDER='dmy',
    )
    def test_value_from_datadict_ok_value(self):
        widget = SplitDateWidget()

        ret = widget.value_from_datadict({'test_0': '01', 'test_1': '02', 'test_2': '2000'}, None, 'test')
        self.assertEqual(ret, '01.02.2000')

    def test_value_from_datadict_missing_value(self):
        widget = SplitDateWidget()

        ret = widget.value_from_datadict({'test_0': '01', 'test_2': '2000'}, None, 'test')
        self.assertIsNone(ret)
