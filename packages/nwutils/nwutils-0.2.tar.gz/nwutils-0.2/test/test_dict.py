from nwutils.dict import mergeDict

class TestMergeDict:
    def test_mergeDict_1(self):
        a = {"a":10}
        b = {"b":5}
        expected = {"b":5, "a":10}
        c = mergeDict(a, b)
        assert c == expected

    def test_mergeDict_2(self):
        a = {"a":{"c":10}}
        b = {"b":{"c":5}}
        expected = {"b":{"c":5}, "a":{"c":10}}
        expected2 = {"a":{"c":10}, "b":{"c":5}}
        c = mergeDict(a, b)
        assert c == expected and c == expected2
    
    def test_mergeDict_3(self):
        a={"a":5}
        b={"a":10}
        try:
            c = mergeDict(a, b)
            assert False
        except:
            pass

    def test_mergeDict_4(self):
        a={"a":5, "b":100}
        b={"c":50, "a":[1,2,3]}
        try:
            c = mergeDict(a, b)
            assert False
        except:
            pass

    def test_mergeDict_5(self):
        a = {"a":{"c":10}}
        b = {"b":{"c":5}}
        expected = {"b":{"c":5}, "a":{"c":10}}
        expected2 = {"a":{"c":10}, "b":{"c":5}}
        c = mergeDict(a, b, createNew=False)
        assert id(a) == id(c)
        assert c == expected and c == expected2

    def test_mergeDict_6(self):
        a = {"a":{"c":10}}
        b = {"b":{"c":5}}
        expected_a = {"a":{"c":10}}
        expected = {"b":{"c":5}, "a":{"c":10}}
        expected2 = {"a":{"c":10}, "b":{"c":5}}
        c = mergeDict(a, b, createNew=True)
        assert id(a) != id(c)
        assert a == expected_a
        assert c == expected and c == expected2