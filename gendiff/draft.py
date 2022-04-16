import json
import yaml
import generator
import pprint
import os
import itertools
import copy


file_path_1 = 'file1.json'
file_1 = generator.load_file_by_path(file_path_1)
file_path_2 = 'file4.json'
file_2 = generator.load_file_by_path(file_path_2)
listed = list(file_1.items())
#print(file_1)
#print('aaa')
#print(listed)
def has_nesting(node):
    #print(f'node1: {node}')
    _, value = node #list(node.items())[0]
    return True if isinstance(value, dict) else False

def get_nesting(node):
    #print(f'node: {node}')
    #print(list(node.items())[0])
    result = []
    _, value = list(node.items())[0]
    #print(f'value: {value}')
    for key, value in value.items():
        result.append({key: value})
    #print(f'GGGGGG {result}')
    return result #if has_nesting(node) else None

def get_name(node):
    #print(f'node: {node}')
    #print(f'HHH {node[0]}')
    #print(list(node.items()))
    name = node[0]#list(node.items())[0]
    return name

def make_final_nesting(name, value, depth=0):
    final_nesting = {'name': name,
                     'value': value,
                     'type': 'final_nesting',
                     'depth': depth
                     }
    return final_nesting

def make_storing_nesting(name, nesting, depth=0):
    storing_nesting = {'name': name,
                       'nesting': nesting,
                       'type': 'storing_nesting',
                       'depth': depth
                       }
    return storing_nesting

json_ = {'JSON': file_1}
#print(json_)

def change_owner(file):

    if len(list(file.items())) > 1:
        file = {'file': file}

    def inner(normalized_tree, depth):
        name = get_name(normalized_tree)

    #print(f'name: {name}, value: {value}, meta: {meta}')
    #print(json_)
    #print(has_nesting(json_))
        if not has_nesting(normalized_tree):
            value = normalized_tree[name]
            return make_final_nesting(name, value, depth)
        children = get_nesting(normalized_tree)
    #print(f'children: {children}')
        new_children = list(map(lambda child: inner(child, depth + 1), children))
        new_tree = make_storing_nesting(name, new_children, depth)
        return new_tree
    return inner(file, 0)

#change_owner(file_1)
#pprint.pprint(change_owner(file_1))

def flatten(t):
    return [item for sublist in t for item in sublist]


#def find_files_by_name(tree):
    #def walk(node, ancestry='', depth=0):
        #print(f'node: {node}')
        #for elem in node.items():
            #print(f'elem: {elem}')
            #name = node[0]
            #name = get_name(elem)
            #print(f'name: {name}')
            #print(f'node: {node}')
            #print(f'Dir: {has_nesting(elem)}')
            #if not has_nesting(node):
            #    value = elem[1]
            #    print(f'value: {value}')
            #    #print(f'path: {os.path.join(ancestry, name, str(value))}')
            #    return {os.path.join(ancestry, name): {'name': get_name(elem),
            #                                           'depth': depth,
            #                                           'value': value,
            #                                           'type': 'final_nesting'


            #                                                       }}
            #children = get_nesting(elem)
            #print(f'children: {children}')
            #print(f'elem: {elem}')
            #dir_paths = list(map(
            #    lambda child: walk(child, os.path.join(ancestry, name), depth + 1), children
            #    ))
            #print(f'dir_paths: {dir_paths}')
            #return dir_paths#flatten(dir_paths)
    #return walk(tree)


def find_files_by_name(tree, base_tree_name='base_tree'):
    tree = {str(base_tree_name): tree}
    #parents = {}
    def walk(node, ancestry='', depth=-1, parents={}):
            #parents = {}
            #print(f'node: {node}')
        #for elem in node.items():
            #print(f'elem: {elem}')
            name = list(node.items())[0][0]
            #name = get_name(elem)
            #print(f'name: {name}')
            #print(f'node: {node}')
            #print(f'Dir: {has_nesting(elem)}')
            #print(list(node.items())[0][1])
            if not isinstance(list(node.items())[0][1], dict):
                value = list(node.items())[0][1]
                #print(f'value: {value}')
                #print(f'path: {os.path.join(ancestry, name, str(value))}')
                parents['parent_' + str(depth)] = ancestry.replace(base_tree_name + '/', '')
                return {os.path.join(ancestry, name): {'name': name,
                                                       'depth': depth,
                                                       'value': value,
                                                       'type': 'final_nesting',
                                                       'parents': parents

                                                       }}

            #print(f'CHIL: {get_nesting(node)}')
            children = get_nesting(node)
            parents['parent_' + str(depth)] = ancestry.replace(base_tree_name + '/', '')
            #print(f'children: {children}')
            #print(f'elem: {elem}')
            dir_paths = list(map(
                lambda child: walk(child, os.path.join(ancestry, name), depth + 1, parents), children
                ))

            dir_paths.append({os.path.join(ancestry, name): {'name': name,
                                                             'type': 'has_nesting',
                                                             'children': children,
                                                             'value': 'NO VALUE',
                                                             'parents': parents,
                                                             'depth': depth}})
            #print(f'dir_paths: {dir_paths}')
            return dir_paths
    result = {
        'base_tree': base_tree_name,
        'list_of_nodes': walk(tree)
    }
    return result

#print(find_files_by_name(file_1))

dopustim_result = [[[{'common/setting6/key': {'depth': 3,
                            'name': 'key',
                            'type': 'final_nesting',
                            'value': 'value'}},
   [{'common/setting6/key777777777777777': {'childen': [],
                                            'depth': 3,
                                            'name': 'key777777777777777',
                                            'type': 'has_nesting'}}],
   [{'common/setting6/doge/wow': {'depth': 4,
                                  'name': 'wow',
                                  'type': 'final_nesting',
                                  'value': ''}},
    {'common/setting6/doge': {'childen': [{'wow': ''}],
                              'depth': 3,
                              'name': 'doge',
                              'type': 'has_nesting'}}],
   {'common/setting6': {'childen': [{'key': 'value'},
                                    {'key777777777777777': {}},
                                    {'doge': {'wow': ''}}],
                        'depth': 2,
                        'name': 'setting6',
                        'type': 'has_nesting'}}],
  {'common': {'childen': [{'setting6': {'doge': {'wow': ''},
                                        'key': 'value',
                                        'key777777777777777': {}}}],
              'depth': 1,
              'name': 'common',
              'type': 'has_nesting'}}],
 [{'group1/foo': {'depth': 2,
                  'name': 'foo',
                  'type': 'final_nesting',
                  'value': 'bar'}},
  [{'group1/nest/key': {'depth': 3,
                        'name': 'key',
                        'type': 'final_nesting',
                        'value': 'value'}},
   {'group1/nest': {'childen': [{'key': 'value'}],
                    'depth': 2,
                    'name': 'nest',
                    'type': 'has_nesting'}}],
  {'group1': {'childen': [{'foo': 'bar'}, {'nest': {'key': 'value'}}],
              'depth': 1,
              'name': 'group1',
              'type': 'has_nesting'}}],
 {'': {'childen': [{'common': {'setting6': {'doge': {'wow': ''},
                                            'key': 'value',
                                            'key777777777777777': {}}}},
                   {'group1': {'foo': 'bar', 'nest': {'key': 'value'}}}],
       'depth': 0,
       'name': '',
       'type': 'has_nesting'}}]
#print(len(dopustim_result[0]))
a = [[[''], ''], ['']]
#pprint.pprint(a)
#merged = list(itertools.chain.from_iterable(dopustim_result))
#pprint.pprint(merged)
#print.pprint(dopustim_result[0])

def make_flatten_list(standardized_list_of_nodes):
    list_of_nodes = standardized_list_of_nodes['list_of_nodes']
    base_tree_name = standardized_list_of_nodes['base_tree']

    result_list = []
    def inner(list_of_nodes):
        if isinstance(list_of_nodes, list):
            for elem in list_of_nodes:
                if not isinstance(elem, list):
                    key = list(elem.items())[0][0]
                    value = list(elem.items())[0][1]
                    if not key == base_tree_name:
                        result_list.append(dict(path=key.replace(base_tree_name + '/', ''), meta=value))

                inner(elem)
            return result_list
        else:
            return
    result_list = inner(list_of_nodes)
    return result_list

#pprint.pprint(make_flatten_list(find_files_by_name(file_1)))

def make_element_dict(key, value, source=None, status='unchanged'):
    value['source'] = source
    value['status'] = status
    return dict(path=key, meta=value)

def make_checking_list(dict1, dict2):

    elements_list = []
    #print([dict_['path'] for dict_ in dict1])
    for elem in dict1:
        path = elem['path']
        meta = elem['meta']

        if (path, meta['value']) in [(dict_['path'], dict_['meta']['value']) for dict_ in dict2]:
            element_dict = make_element_dict(path, meta, source='file_1')
            elements_list.append(element_dict.copy())

        else:
            element_dict = make_element_dict(path, meta, source='file_1', status='deleted')
            elements_list.append(element_dict.copy())


    for elem in dict2:
        path = elem['path']
        #print(path)
        meta = elem['meta']
        #print(sorted([dict_['path'] for dict_ in dict1]))
        #print(path)
        if (path, meta['value']) not in [(dict_['path'], dict_['meta']['value']) for dict_ in dict1]:
            element_dict = make_element_dict(path, meta, source='file_2', status='added')
            elements_list.append(element_dict.copy())

        #else:
         #   element_dict = make_element_dict(path, meta, source='file_2')
          #  elements_list.append(element_dict.copy())

    return elements_list
#print(file_1)
#print(file_2)
one = make_flatten_list(find_files_by_name(file_1))
two = make_flatten_list(find_files_by_name(file_2))

#pprint.pprint(two)
#pprint.pprint(make_checking_list(one, two))

def sort_checking_list(checking_list):
    return list(checking_list.keys()).sort()

new1 = (make_checking_list(one, two))
new1.sort(key= lambda node: (node['path'], node['meta']['source']))
#pprint.pprint(new1)

#def SUPAPUPA(list):
    #print(list.items())
    #for key, value in list(list.items()).sort():
        #print(key)


#SUPAPUPA(new1)
def make_line(dict_, prev_depth):
    #print(f'prev_depth: {prev_depth}')
    status_interpretation = {
        'unchanged': '    ',
        'added': '  + ',
        'deleted': '  - ',
    }
    bool_normalization = {
        False: 'false',
        True: 'true',
        None: 'null',
    }
    depth = dict_['meta']['depth']
    #print(depth, prev_depth)

    result = ''
    if depth < prev_depth:
        result += ' ' * prev_depth * 4 + '}\n'

    if dict_['meta']['type'] == 'has_nesting':
        #print(' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': {')
        result += ' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': {\n'
        return result
    else:
        if dict_['meta']['value'] in bool_normalization.keys():
            #print(' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': ' + bool_normalization[dict_['meta']['value']])
            result += ' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': ' + bool_normalization[dict_['meta']['value']] + '\n'
            return result
        #print(' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': ' + str(dict_['meta']['value']))
        result += ' ' * depth * 4 + status_interpretation[dict_['meta']['status']] + dict_['meta']['name'] + ': ' + str(dict_['meta']['value']) + '\n'
        return result

def make_diff(list_):
    result = '{\n'
    for elem in list_:
        #print(list_.index(elem)-1)
        depth = list_[list_.index(elem)-1]['meta']['depth'] if not list_.index(elem)-1 < 0 else list_[list_.index(elem)]['meta']['depth']
        #print(f'depth: {depth}')
        result += make_line(elem, depth)
    result += '}'
    return result


#iii = make_diff(new1)
aaa = """{
    common: {
      + follow: false
        setting1: Value 1
      - setting2: 200
      - setting3: true
      + setting3: null
      + setting4: blah blah
      + setting5: {
            key5: value5
        }
        setting6: {
            doge: {
              - wow: 
              + wow: so much
            }
            key: value
          + ops: vops
        }
    }
    group1: {
      - baz: bas
      + baz: bars
        foo: bar
      - nest: {
            key: value
        }
      + nest: str
    }
  - group2: {
        abc: 12345
        deep: {
            id: 45
        }
    }
  + group3: {
        deep: {
            id: {
                number: 45
            }
        }
        fee: 100500
    }
}"""
#print(iii)
#print(iii == aaa)

file1={"setting1": "Value 1","setting2": {"KEYYY": {"TUT KEY": 10}},"setting3": True,"setting6": {'a': 'b'},"setting10": True,"setting66": "POOK"}
file2={"setting1": "Value 1","setting2": {"KEYYY": {"TUT KEY": 100}},"setting3": False,"setting6": None,"setting50": True,"setting66": {'a': 'b'}}

#################################################################ver_1

def sort_checking_list(checking_list):
    return checking_list['key'], checking_list['source']


def make_normalization(function):
    bool_normalization_dict = {
        False: 'false',
        True: 'true',
        None: 'null',
    }

    def inner(*args, **kwargs):
        result = function(*args, **kwargs)
        result.sort(key=sort_checking_list)
        for elem in result:
            if elem['value'] in bool_normalization_dict:
                elem['value'] = bool_normalization_dict[elem['value']]
        return result
    return inner


def make_element_dict(key, value, source=None, status=' '):
    element_dict = {}

    element_dict['key'] = key
    element_dict['value'] = value
    element_dict['source'] = source
    element_dict['status'] = status

    return element_dict

@make_normalization
def make_checking_list(dict1, dict2):

    checking_list = []

    for key, value in dict1.items():

        if dict2.get(key) == value:
            element_dict = make_element_dict(key, value, source='file_1')
            checking_list.append(element_dict.copy())

        else:
            element_dict = make_element_dict(key, value,
                                             source='file_1', status='-')
            checking_list.append(element_dict.copy())

    for key, value in dict2.items():
        if dict1.get(key) != value:
            element_dict = make_element_dict(key, value,
                                             source='file_2', status='+')
            checking_list.append(element_dict.copy())

    return checking_list


def make_formatted_diff(checking_list):
    diff = "{"
    for elem in checking_list:
        diff += '\n  {} {}: {}'.format(elem['status'],
                                       elem['key'],
                                       elem['value'])
    diff += '\n}'
    return diff

#################################################################ver_1////////////////////

#################################################################ver_2

def normalize_value(value):
    bool_normalization = {
        False: 'false',
        True: 'true',
        None: 'null',
    }
    if isinstance(value, dict):
        return value
    else:
        if value in bool_normalization:
            return bool_normalization[value]
        return str(value)


def make_diff(file_1, file_2):
    diff = []
    for key, value in file_1.items():
        value_file_1 = normalize_value(value)

        if key in file_2.keys():
            value_file_2 = normalize_value(file_2[key])

            if not isinstance(value_file_1, dict):
                if isinstance(value_file_2, dict):
                    diff.append({'name': key, 'status': 'updated',
                                 'value': (value_file_1, value_file_2)})
                else:
                    if value_file_1 == value_file_2:
                        diff.append({'name': key, 'status': 'unchanged', 'value': value_file_1})
                    else:
                        diff.append({'name': key, 'status': 'updated', 'value': (value_file_1, value_file_2)})
            else:
                if not isinstance(file_2[key], dict):
                    diff.append({'name': key, 'status': 'updated', 'value': (value_file_1, value_file_2)})
                else:
                    diff.append(
                        {'name': key, 'status': 'updated, needs DFS', 'value': make_diff(value_file_1, value_file_2)})
        else:

            diff.append({'name': key, 'status': 'deleted', 'value': value_file_1})


    for key, value in file_2.items():
        value_file_2 = normalize_value(value)
        if key not in file_1.keys():
            diff.append({'name': key, 'status': 'added', 'value': value_file_2})

    diff.sort(key=lambda node: node['name'])
    return diff


def print_value(key, value, depth=0, status='unchanged'):
    initial_depth = depth
    def inner(key, value,depth=0, status='unchanged'):
        status_interpretation = {
            'unchanged': '    ',
            'deleted': '  - ',
            'added': '  + ',
        }
        status = status_interpretation[status]
        result = ''

        if not isinstance(value, dict):
            result += ('{}{}{}: {}{}'.format(' ' * 4 * depth, status, str(key), str(value), '\n'))
        else:
            result += ('{}{}{}{}'.format(' ' * 4 * depth, status, str(key), ': {\n'))
            for inner_key, inner_value in list(value.items()):
                if not isinstance(inner_value, dict):
                    result += ('{}{}: {}{}'.format(' ' * 4 * (depth + 2), str(inner_key), str(inner_value), '\n'))
                else:
                    result += inner(inner_key, inner_value, depth + 1)

            result += ('{}{}'.format(' ' * 4 * (depth + 1), '}'))
            result += '\n' if depth >= initial_depth else ''

        return result
    return inner(key, value, depth, status)


def make_node_visualization(node, depth=0):
    initial_depth = depth
    def inner(node, depth=0, result=''):
        if node['status'] == 'updated, needs DFS':
            result += "{}{}: {}".format(' ' * 4 * max(depth, depth + 1), node['name'], '{\n')
            for elem in node['value']:
                result += inner(elem, depth + 1)

            result += '{}{}'.format(' ' * 4 * max(depth, depth + 1), '}')
            result += '\n' if depth >= initial_depth else ''


        if node['status'] == 'updated':
            result += print_value(node['name'], node['value'][0], depth, status='deleted')
            result += print_value(node['name'], node['value'][1], depth, status='added')
            return result

        if node['status'] == 'deleted':
            result += print_value(node['name'], node['value'], depth, status='deleted')
            return result

        if node['status'] == 'added':
            result += print_value(node['name'], node['value'], depth, status='added')
            return result

        if node['status'] == 'unchanged':
            result += print_value(node['name'], node['value'], depth)
            return result

        return result
    return inner(node)

#################################################################ver_2////////////////////


try1 = {'meta': {'status': 'updated, need_rec'},
  'name': 'setting2',
  'value': [{'meta': {'status': 'updated, need_rec'},
             'name': 'KEYYY',
             'value': [{'meta': {'status': 'updated, val-val'},
                        'name': 'TUT KEY',
                        'value': (10, 100)}]}]}
def make_stylish_diff(list_of_nodes):
    stylish_diff = '{\n'
    for elem in list_of_nodes:
        stylish_diff += make_node_visualization(elem)
    stylish_diff += '}'
    return stylish_diff

#print_tree(try1)
#pprint.pprint(make_diff(file_1,file_2))
#print(AAA(make_diff(file_1,file_2)))

bbb = make_stylish_diff(make_diff(file_1,file_2))
print(bbb)
#g = make_diff(file_1,file_2)
#n = list(map(print_value, g))
#make_node_visualization()


#i = print_value('a',{'b':{'c': 'd', 'e': 'j'}}, status='added')
#i = print_value('j', status='added')
#print(i)