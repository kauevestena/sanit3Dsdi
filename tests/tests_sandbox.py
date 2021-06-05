import json


test_dic = {'b':[23,312,312,321,321,3,123,213,21,3,5,435,4,45,6],'c':['dasda','fsdfdsf']}
print(test_dic)


filename = 'tests/json_test.json'

with open(filename,'w+') as handle:
    json.dump(test_dic,handle)

test_dic = None

print(test_dic)

with open(filename) as opener:
    test_dic = json.load(opener)


print(test_dic)
