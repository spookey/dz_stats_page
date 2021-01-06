from observatory.models.value import EnumBox


class TestValueEnumBox:
    @staticmethod
    def test_names():
        assert [elem.name for elem in EnumBox] == [
            'STRING',
            'NUMBER',
            'SWITCH',
        ]

    @staticmethod
    def test_values():
        assert [elem.value for elem in EnumBox] == [
            '_string',
            '_number',
            '_switch',
        ]

    @staticmethod
    def test_from_type():
        assert EnumBox.from_type(True) == EnumBox.SWITCH
        assert EnumBox.from_type(False) == EnumBox.SWITCH

        assert EnumBox.from_type(0) == EnumBox.NUMBER
        assert EnumBox.from_type(23.42) == EnumBox.NUMBER
        assert EnumBox.from_type(1337) == EnumBox.NUMBER

        assert EnumBox.from_type('') == EnumBox.STRING
        assert EnumBox.from_type('test') == EnumBox.STRING
        assert EnumBox.from_type('abc xyz') == EnumBox.STRING

        assert EnumBox.from_type(None) == EnumBox.STRING
        assert EnumBox.from_type(Exception) == EnumBox.STRING
