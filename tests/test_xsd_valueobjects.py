import six

from zeep import xsd
from zeep.xsd import valueobjects


def test_simple_args():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]))
    args = tuple(['value-1', 'value-2'])
    kwargs = {}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        'item_1': 'value-1',
        'item_2': 'value-2',
    }


def test_simple_args_attributes():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]),
        [
            xsd.Attribute('attr_1', xsd.String())
        ]
    )
    args = tuple(['value-1', 'value-2'])
    kwargs = {'attr_1': 'bla'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        'item_1': 'value-1',
        'item_2': 'value-2',
        'attr_1': 'bla',
    }


def test_simple_args_too_many():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]))
    args = tuple(['value-1', 'value-2', 'value-3'])
    kwargs = {}

    try:
        valueobjects._process_signature(xsd_type, args, kwargs)
    except TypeError as exc:
        assert six.text_type(exc) == (
            '__init__() takes at most 2 positional arguments (3 given)')
    else:
        assert False, "TypeError not raised"


def test_simple_args_too_few():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]))
    args = tuple(['value-1'])
    kwargs = {}
    valueobjects._process_signature(xsd_type, args, kwargs)


def test_simple_kwargs():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]))
    args = tuple([])
    kwargs = {'item_1': 'value-1', 'item_2': 'value-2'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        'item_1': 'value-1',
        'item_2': 'value-2',
    }


def test_simple_mixed():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Element('item_1', xsd.String()),
            xsd.Element('item_2', xsd.String())
        ]))
    args = tuple(['value-1'])
    kwargs = {'item_2': 'value-2'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        'item_1': 'value-1',
        'item_2': 'value-2',
    }


def test_choice():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Element('item_1', xsd.String()),
                xsd.Element('item_2', xsd.String())
            ])
        ])
    )
    args = tuple([])
    kwargs = {'item_2': 'value-2'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': {'item_2': 'value-2'}
    }


def test_choice_max_occurs_simple_interface():
    fields = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Element('item_1', xsd.String()),
                xsd.Element('item_2', xsd.String())
            ], max_occurs=2)
        ])
    )
    args = tuple([])
    kwargs = {
        '_value_1': [{'item_1': 'foo'}, {'item_2': 'bar'}]
    }
    result = valueobjects._process_signature(fields, args, kwargs)
    assert result == {
        '_value_1': [
            {'item_1': 'foo'},
            {'item_2': 'bar'},
        ]
    }


def test_choice_max_occurs():
    fields = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Element('item_1', xsd.String()),
                xsd.Element('item_2', xsd.String())
            ], max_occurs=3)
        ])
    )
    args = tuple([])
    kwargs = {
        '_value_1': [
            {'item_1': 'foo'}, {'item_2': 'bar'}, {'item_1': 'bla'}
        ]
    }
    result = valueobjects._process_signature(fields, args, kwargs)
    assert result == {
        '_value_1': [
            {'item_1': 'foo'},
            {'item_2': 'bar'},
            {'item_1': 'bla'},
        ]
    }


def test_choice_max_occurs_on_choice():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Element('item_1', xsd.String(), max_occurs=2),
                xsd.Element('item_2', xsd.String())
            ], max_occurs=2)
        ])
    )
    args = tuple([])
    kwargs = {
        '_value_1': [
            {'item_1': ['foo', 'bar']},
            {'item_2': 'bla'},
        ]
    }
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': [
            {'item_1': ['foo', 'bar']},
            {'item_2': 'bla'}
        ]
    }


def test_choice_mixed():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Element('item_1', xsd.String()),
                xsd.Element('item_2', xsd.String()),
            ]),
            xsd.Element('item_2', xsd.String())
        ])
    )
    args = tuple([])
    kwargs = {'item_1': 'value-1', 'item_2': 'value-2'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        'item_2': 'value-2',
        '_value_1': {'item_1': 'value-1'}
    }


def test_choice_sequences_simple():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String())
                ]),
                xsd.Sequence([
                    xsd.Element('item_3', xsd.String()),
                    xsd.Element('item_4', xsd.String())
                ]),
            ])
        ])
    )
    args = tuple([])
    kwargs = {'item_1': 'value-1', 'item_2': 'value-2'}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': {'item_1': 'value-1', 'item_2': 'value-2'}
    }


def test_choice_sequences_no_match():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String())
                ]),
                xsd.Sequence([
                    xsd.Element('item_3', xsd.String()),
                    xsd.Element('item_4', xsd.String())
                ]),
            ])
        ])
    )
    args = tuple([])
    kwargs = {'item_1': 'value-1', 'item_3': 'value-3'}

    try:
        valueobjects._process_signature(xsd_type, args, kwargs)
    except TypeError as exc:
        assert six.text_type(exc) == (
            "__init__() got an unexpected keyword argument 'item_3'. " +
            "Signature: (_value_1: ({item_1: xsd:string, item_2: xsd:string} | {item_3: xsd:string, item_4: xsd:string}))"  # noqa
        )
    else:
        assert False, "TypeError not raised"


def test_choice_sequences_no_match_nested():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String())
                ]),
            ])
        ])
    )
    args = tuple([])
    kwargs = {'_value_1': {'item_1': 'value-1'}}
    try:
        valueobjects._process_signature(xsd_type, args, kwargs)
    except TypeError as exc:
        assert six.text_type(exc) == (
            "No complete xsd:Sequence found for the xsd:Choice '_value_1'.\n" +
            "The signature is: ({item_1: xsd:string, item_2: xsd:string})")
    else:
        assert False, "TypeError not raised"


def test_choice_sequences_optional_elms():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String(), min_occurs=0)
                ]),
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String()),
                    xsd.Element('item_3', xsd.String())
                ]),
            ])
        ])
    )
    args = tuple([])
    kwargs = {'_value_1': {'item_1': 'value-1'}}
    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': {'item_1': 'value-1'}
    }


def test_choice_sequences_max_occur():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String())
                ]),
                xsd.Sequence([
                    xsd.Element('item_2', xsd.String()),
                    xsd.Element('item_3', xsd.String()),
                ]),
            ], max_occurs=2)
        ]),
    )
    args = tuple([])
    kwargs = {
        '_value_1': [
            {'item_1': 'value-1', 'item_2': 'value-2'},
            {'item_2': 'value-2', 'item_3': 'value-3'},
        ]
    }

    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': [
            {'item_1': 'value-1', 'item_2': 'value-2'},
            {'item_2': 'value-2', 'item_3': 'value-3'},
        ]
    }


def test_choice_sequences_init_dict():
    xsd_type = xsd.ComplexType(
        xsd.Sequence([
            xsd.Choice([
                xsd.Sequence([
                    xsd.Element('item_1', xsd.String()),
                    xsd.Element('item_2', xsd.String())
                ]),
                xsd.Sequence([
                    xsd.Element('item_2', xsd.String()),
                    xsd.Element('item_3', xsd.String()),
                ]),
            ], max_occurs=2)
        ]),
    )
    args = tuple([])
    kwargs = {
        '_value_1': {'item_1': 'value-1', 'item_2': 'value-2'},
    }

    result = valueobjects._process_signature(xsd_type, args, kwargs)
    assert result == {
        '_value_1': [
            {'item_1': 'value-1', 'item_2': 'value-2'}
        ]
    }