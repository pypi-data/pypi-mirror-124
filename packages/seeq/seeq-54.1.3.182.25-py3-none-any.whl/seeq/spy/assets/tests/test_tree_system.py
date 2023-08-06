import numpy as np
import pandas as pd
import pytest

from seeq import spy
from seeq.sdk import *
from seeq.spy import _common, _login
from seeq.spy.assets import Tree, _tree
from seeq.spy.tests import test_common


def assert_frame_equal(df1, df2):
    # noinspection PyProtectedMember
    return pd._testing.assert_frame_equal(df1.sort_index(axis=1),
                                          df2.sort_index(axis=1),
                                          check_dtype=False)


def setup_module():
    test_common.login()


start_cleanup_names = {'test_tree_system', 'test_tree_system2', 'Example', 'test_root', 'My Root', 'test_pull_calcs'}
end_cleanup_ids = set()


@pytest.mark.system
def test_create_tree_from_subtree_of_pushed_tree():
    workbook = 'test_create_tree_from_subtree_of_pushed_tree'

    tree1 = Tree('tree1', workbook=workbook)
    tree1.insert(spy.search({'Name': 'Cooling Tower 2', 'Path': 'Example', 'Datasource ID': 'Example Data'}))
    tree1.push()

    tree2 = Tree(spy.search({'Name': 'Cooling Tower 2', 'Path': 'tree1', 'Datasource ID': 'Seeq Data Lab'},
                            workbook=workbook),
                 workbook=workbook)
    tree2.push()

    df1 = tree1._dataframe
    df2 = tree2._dataframe
    assert len(df2) == len(df1) - 1
    assert not df2.ID.isin(df1.ID).any()
    assert list(df2['Referenced ID']) == list(df1.loc[1:, 'ID'])


@pytest.mark.system
def test_create_new_tree_then_repull_and_edit():
    workbook = 'test_create_new_tree_then_repull_and_edit'
    tree = Tree('test_tree_system', workbook=workbook)
    tree.insert(['Cooling Tower 1', 'Cooling Tower 2'])
    tree.insert(children=['Area A', 'Area B', 'Area C'], parent='Cooling Tower 1')
    tree.insert(children=['Area E', 'Area F', 'Area G', 'Area H'], parent='Cooling Tower 2')
    tree.insert(children=['Temperature', 'Optimizer', 'Compressor'], parent=3)

    tower1_areas = ['Area A', 'Area B', 'Area C']
    tower2_areas = ['Area E', 'Area F', 'Area G', 'Area H']
    leaves = ['Temperature', 'Optimizer', 'Compressor']

    expected = list()
    expected.append({
        'Name': 'test_tree_system',
        'Path': '',
        'Type': 'Asset'
    })
    expected.append({
        'Name': 'Cooling Tower 1',
        'Path': 'test_tree_system',
        'Type': 'Asset'
    })
    expected.append({
        'Name': 'Cooling Tower 2',
        'Path': 'test_tree_system',
        'Type': 'Asset'
    })
    for area in tower1_areas:
        expected.append({
            'Name': area,
            'Path': 'test_tree_system >> Cooling Tower 1',
            'Type': 'Asset'
        })
        for leaf in leaves:
            expected.append({
                'Name': leaf,
                'Path': f'test_tree_system >> Cooling Tower 1 >> {area}',
                'Type': 'Asset'
            })
    for area in tower2_areas:
        expected.append({
            'Name': area,
            'Path': 'test_tree_system >> Cooling Tower 2',
            'Type': 'Asset'
        })
        for leaf in leaves:
            expected.append({
                'Name': leaf,
                'Path': f'test_tree_system >> Cooling Tower 2 >> {area}',
                'Type': 'Asset'
            })
    assert_tree_equals_expected(tree, expected)

    tree.push()
    assert not tree._dataframe['ID'].isnull().values.any(), "Pushing should set the dataframe's ID for all items"
    assert not tree._dataframe['Type'].isnull().values.any(), "Pushing should set the dataframe's Type for all items"
    search_results_df = spy.search({
        'Path': 'test_tree_system'
    }, workbook=workbook)
    expected.pop(0)  # Since we're searching using Path, the root node won't be retrieved.
    assert_search_results_equals_expected(search_results_df, expected)

    # Pull in the previously-created test_tree_system by name
    tree = Tree('test_tree_system', workbook=workbook)
    original_root_id, original_root_referenced_id = get_root_node_ids(tree)
    assert _common.is_guid(original_root_id), \
        f'Pulled root ID should be a GUID: {original_root_id}'
    assert str(original_root_referenced_id) == str(np.nan), \
        f'Pulled root Reference ID should be {np.nan}: {original_root_referenced_id}'

    expected_existing_items = 1 + 2 + 3 + 4 + (3 * 3) + (4 * 3)
    assert len(tree._dataframe) == expected_existing_items, \
        f'Pulled tree items do not match count: Real={len(tree._dataframe)}, Expected={expected_existing_items}'
    expected_nodes = create_expected_list_from_tree(tree)

    # Add a single node
    tree.insert(children='Area I', parent='Cooling Tower 2')
    expected_nodes.append({
        'Name': 'Area I',
        'Path': 'test_tree_system >> Cooling Tower 2',
        'Type': 'Asset'
    })
    expected_existing_items += 1
    assert_tree_equals_expected(tree, expected_nodes)
    tree.push()
    # The ID column should be fully filled in when the push occurs
    assert not tree._dataframe['ID'].isnull().any()

    # Pull it again, but by ID
    tree2 = Tree(original_root_id, workbook=workbook)
    assert len(tree2._dataframe) == expected_existing_items, \
        f'Edited tree items do not match count: Real={len(tree2._dataframe)}, Expected={expected_existing_items}'
    updated_root_id, updated_root_referenced_id = get_root_node_ids(tree2)
    assert original_root_id == updated_root_id, \
        f'Pulled root ID should be the same as before: Original={original_root_id}, Updated={updated_root_id}'
    assert str(original_root_referenced_id) == str(np.nan), \
        f'Pulled root Reference ID should be the same as before: ' \
        f'Original={original_root_referenced_id}, Updated={updated_root_referenced_id}'
    assert_tree_equals_expected(tree2, expected_nodes)


@pytest.mark.system
def test_insert_referenced_single_item():
    # Setup: Find the IDs of actual Example Data items
    items_api = ItemsApi(test_common.get_client())
    result = items_api.search_items(filters=['Name==Area A && Datasource ID==Example Data'],
                                    types=['Asset'])  # type: ItemSearchPreviewPaginatedListV1
    assert len(result.items) >= 1, 'There should be at least one global Area A asset'
    area_a_asset = result.items[0].id
    result = items_api.search_items(filters=['Name==Temperature'], types=['StoredSignal'], asset=area_a_asset)
    assert len(result.items) >= 1, 'There should be at least one global Area A Temperature signal'
    area_a_temperature = result.items[0].id

    # Test inserting an item by ID. It should be made into a reference.
    workbook = 'test_insert_referenced_single_item'
    tree = Tree('test_tree_system2', workbook=workbook)
    tree.insert(area_a_temperature)
    expected = [{
        'Name': 'test_tree_system2',
        'Path': '',
        'Type': 'Asset'
    }, {
        'Referenced ID': area_a_temperature,
        'Name': 'Temperature',
        'Path': 'test_tree_system2',
        'Type': 'CalculatedSignal',
        'Formula Parameters': f'signal={area_a_temperature}'
    }]
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will result in no change
    tree.insert(area_a_temperature)
    assert_tree_equals_expected(tree, expected)

    # Test inserting a dataframe with a custom name and ID. It too should be made into a reference that is distinct
    # from the previous one.
    df = pd.DataFrame([{'Name': 'Temperature with new name', 'ID': area_a_temperature}])
    tree.insert(df)
    expected.append({
        'Referenced ID': area_a_temperature,
        'Name': 'Temperature with new name',
        'Path': 'test_tree_system2',
        'Type': 'CalculatedSignal',
        'Formula Parameters': f'signal={area_a_temperature}'
    })
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will still result in no change
    tree.insert(df)
    assert_tree_equals_expected(tree, expected)

    # 'Friendly Name' should work in the same way as above.
    df = pd.DataFrame([{'Friendly Name': 'Temperature with friendly name', 'ID': area_a_temperature}])
    tree.insert(df)
    expected.append({
        'Referenced ID': area_a_temperature,
        'Name': 'Temperature with friendly name',
        'Path': 'test_tree_system2',
        'Type': 'CalculatedSignal',
        'Formula Parameters': f'signal={area_a_temperature}'
    })
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will still result in no change
    tree.insert(df)
    assert_tree_equals_expected(tree, expected)


@pytest.mark.system
def test_insert_referenced_tree_item():
    # Setup: Find the IDs of actual Example Data items
    items_api = ItemsApi(test_common.get_client())
    result = items_api.search_items(filters=['Name==Area A && Datasource ID==Example Data'], types=['Asset'])
    assert len(result.items) >= 1, 'There should be at least one global Area A asset'
    area_a_asset = result.items[0].id
    result = items_api.search_items(types=['StoredSignal'], asset=area_a_asset, order_by=['Name'])
    assert len(result.items) >= 5, 'There should be at least five global Area A signals'
    area_a_signals = list()
    for item in result.items:
        area_a_signals.append({'Name': item.name, 'ID': item.id})

    def create_expected_tuples(asset_name):
        expected_items = [{
            'Referenced ID': area_a_asset,
            'Name': asset_name,
            'Path': 'test_tree_system2',
            'Type': 'Asset'
        }]
        for signal in area_a_signals:
            expected_items.append({
                'Referenced ID': signal['ID'],
                'Name': signal['Name'],
                'Path': f'test_tree_system2 >> {asset_name}',
                'Type': 'CalculatedSignal',
                'Formula Parameters': f"signal={signal['ID']}"
            })
        return expected_items

    # Test inserting an asset by ID. It should be made into a reference and children pulled.
    tree = Tree('test_tree_system2', workbook='test_insert_referenced_single_item')
    tree.insert(area_a_asset)
    expected = [{
        'Name': 'test_tree_system2',
        'Path': '',
        'Type': 'Asset'
    }] + create_expected_tuples('Area A')
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will result in no change
    tree.insert(area_a_asset)
    assert_tree_equals_expected(tree, expected)

    # Test inserting a dataframe with a custom name and ID. It too should be made into a reference that is distinct
    # from the previous one.
    df = pd.DataFrame([{'Name': 'Area A with new name', 'ID': area_a_asset}])
    tree.insert(df)
    expected.extend(create_expected_tuples('Area A with new name'))
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will still result in no change
    tree.insert(df)
    assert_tree_equals_expected(tree, expected)

    # 'Friendly Name' should work in the same way as above.
    df = pd.DataFrame([{'Friendly Name': 'Area A with friendly name', 'ID': area_a_asset}])
    tree.insert(df)
    expected.extend(create_expected_tuples('Area A with friendly name'))
    assert_tree_equals_expected(tree, expected)
    # Inserting it again will still result in no change
    tree.insert(df)
    assert_tree_equals_expected(tree, expected)

    # Inserting a mix of names+IDs should automatically figure out which is which. In this case, insert only
    # existing items. The lack of new rows will prove the resolution was successful (although some of the properties
    # will be lost on 'Area A with new name' due to this call no longer being a reference).
    tree.insert(['Area A with new name', area_a_asset])
    assert len(tree._dataframe) == len(expected)


@pytest.mark.system
def test_remove_from_example_data():
    tree = spy.assets.Tree('Example', workbook='test_remove_from_example_data')
    tree.push()

    remove_df = tree.remove('Cooling Tower 1')
    assert len(remove_df) == 57

    df = tree._dataframe
    assert not ((df['Name'] == 'Cooling Tower 1') | (df['Path'].str.contains('Cooling Tower 1'))).any()

    tree.push()

    items_api = ItemsApi(test_common.get_client())
    for guid in remove_df.ID:
        item_output = items_api.get_item_and_all_properties(id=guid)
        assert item_output.is_archived is True
    for guid in remove_df['Referenced ID']:
        item_output = items_api.get_item_and_all_properties(id=guid)
        assert item_output.is_archived is False


@pytest.mark.system
def test_comprehension_funcs_on_example_data():
    example = Tree('Example', workbook='test_comprehension_funcs_on_example_data')

    assert example.height == 4
    assert example.size == 76

    counts = example.count()
    expected_counts = {
        'Asset': 14,
        'Signal': 62
    }
    for key in ['Asset', 'Signal']:
        assert counts[key] == expected_counts[key]
        assert example.count(key) == expected_counts[key]
    for key in ['Condition', 'Scalar', 'Formula']:
        assert example.count(key) == 0

    missing_items_dict = example.missing_items('dict')
    area_f = 'Example >> Cooling Tower 2 >> Area F'
    expected_missing_names = ['Compressor Stage', 'Optimizer', 'Relative Humidity', 'Temperature', 'Wet Bulb']
    assert len(missing_items_dict) == 1
    assert area_f in missing_items_dict
    assert len(missing_items_dict[area_f]) == 5
    for name in expected_missing_names:
        assert name in missing_items_dict[area_f]


@pytest.mark.system
def test_constructor_and_insert_tree_dataframe():
    push_results = spy.push(metadata=pd.DataFrame([{
        'Name': 'My Root',
        'Type': 'Asset'
    }, {
        'Name': 'Leaf',
        'Type': 'Signal',
        'Path': 'My Root'
    }]))

    # The input properties (particularly the Referenced ID and Formula information) should come though
    root = {'Name': 'My Root',
            'Type': 'Asset',
            'Referenced ID': push_results.ID[0],
            'Path': '',
            'Depth': 1}
    signal = {'Name': 'Leaf',
              'Type': 'Signal',
              'Referenced ID': push_results.ID[1],
              'Formula': '$signal',
              'Formula Parameters': '$signal=Signal_ID',
              'Path': 'My Root',
              'Depth': 2,
              'Cache Enabled': False}
    expected = pd.DataFrame(columns=_tree._dataframe_columns)
    expected = expected.append([root, signal], ignore_index=True)
    tree = Tree(pd.DataFrame([root, signal]))
    assert_frame_equal(tree._dataframe, expected)


@pytest.mark.system
def test_root_only_asset_tree_visible():
    # Insert a Tree that has no children.
    tree = Tree('test_root')
    tree.push()
    trees_api = TreesApi(_login.client)
    roots = trees_api.get_tree_root_nodes()
    result = [x.name for x in roots.children if 'test_root' == x.name]
    assert len(result) == 1


@pytest.mark.system
def test_modify_existing_spy_tree_with_constructor():
    workbook = 'test_modify_existing_spy_tree_with_constructor'
    tree1 = Tree(pd.DataFrame([{
        'Name': 'root'
    }, {
        'Name': 'leaf 1',
        'Path': 'root >> asset'
    }, {
        'Name': 'leaf 2',
        'Path': 'root >> asset'
    }, {
        'Name': 'leaf 3',
        'Path': 'root >> asset'
    }, {
        'Name': 'leaf 4',
        'Path': 'root >> asset >> asset to be modified'
    }]), workbook=workbook)
    tree1.push()

    # Because tree2 will be defined upon the items of tree1, it will pull and modify what we just pushed via tree1.
    # However, the dataframe input will include modifications that we expect to be reflected in the resulting tree
    #  object, so that spy.push doesn't fail to update pre-existing items in certain ways (changing name, path, or
    #  type).

    tree2_df = tree1._dataframe.copy()
    # Change the name of an existing item.
    # We expect the result to be a reference to the old item.
    tree2_df.at[tree2_df.Name == 'leaf 1', 'Name'] = 'new leaf 1 name'
    # Change the path of an existing item.
    # We expect the result to be a reference to the old item.
    tree2_df.at[tree2_df.Name == 'leaf 2', 'Path'] = 'root >> new leaf 2 path'
    # Change the type of an existing item.
    # We expect this to be a fresh item (not a reference) that overwrites the old item when pushed.
    tree2_df.at[tree2_df.Name == 'leaf 3', 'Type'] = 'CalculatedSignal'
    tree2_df.at[tree2_df.Name == 'leaf 3', 'Formula'] = 'sinusoid()'
    # Rename an asset with children.
    # We expect the result to be a reference to the old asset, and all of the new children to be references to old
    # children.
    tree2_df.at[tree2_df.Name == 'asset to be modified', 'Name'] = 'new asset name'
    tree2_df.at[tree2_df.Name == 'leaf 4', 'Path'] = 'root >> asset >> new asset name'
    # Add a new item. We expect the result to be a fresh item.
    tree2_df = tree2_df.append({'Name': 'additional leaf', 'Path': 'root >> asset'}, ignore_index=True)

    tree2 = Tree(tree2_df, workbook=workbook)

    def tree1_id(name):
        rows = tree1._dataframe[tree1._dataframe.Name == name]
        if len(rows) != 1:
            raise RuntimeError('tree1 did not push correctly')
        return rows.ID.iloc[0]

    expected_df = pd.DataFrame([
        ['', 'root', 'Asset', tree1_id('root'), np.nan],
        ['root', 'asset', 'Asset', tree1_id('asset'), np.nan],
        ['root >> asset', 'additional leaf', 'Asset', np.nan, np.nan],
        ['root >> asset', 'leaf 3', 'CalculatedSignal', np.nan, np.nan],
        ['root >> asset', 'new asset name', 'Asset', np.nan, tree1_id('asset to be modified')],
        ['root >> asset >> new asset name', 'leaf 4', 'Asset', np.nan, tree1_id('leaf 4')],
        ['root >> asset', 'new leaf 1 name', 'Asset', np.nan, tree1_id('leaf 1')],
        ['root', 'new leaf 2 path', 'Asset', np.nan, np.nan],
        ['root >> new leaf 2 path', 'leaf 2', 'Asset', np.nan, tree1_id('leaf 2')]
    ], columns=['Path', 'Name', 'Type', 'ID', 'Referenced ID'])

    assert_frame_equal(tree2._dataframe[expected_df.columns], expected_df)

    # Assert equal after push as well, except for new IDs
    tree2.push()
    assert list(tree2._dataframe.ID[expected_df.ID.notnull()]) == list(expected_df.ID[expected_df.ID.notnull()])
    columns_no_id = ['Path', 'Name', 'Type', 'Referenced ID']
    assert_frame_equal(tree2._dataframe[columns_no_id], expected_df[columns_no_id])


@pytest.mark.system
def test_pull_calculations():
    area_a_temp_search = spy.search({'Name': 'Area A_Temperature'})
    assert len(area_a_temp_search) > 0
    area_a_temp_id = area_a_temp_search.ID[0]

    orig_tree = Tree('test_pull_calcs')
    orig_tree.insert(pd.DataFrame([{
        'Name': 'Calc with Parameters',
        'Formula': '$x + $x',
        'Formula Parameters': [f'x={area_a_temp_id}']
    }, {
        'Name': 'Condition Calc',
        'Formula': 'days()'
    }, {
        'Name': 'Scalar Calc',
        'Formula': '1'
    }, {
        'Name': 'Signal Calc',
        'Formula': 'sinusoid()'
    }]))
    orig_tree.push()
    orig_root_id = orig_tree._dataframe.ID[0]

    expected_df = orig_tree._dataframe.copy()
    expected_df['Cache Enabled'] = False
    for i in (2, 3, 4):
        expected_df.at[i, 'Formula Parameters'] = list()

    # First pull the same tree without references
    tree1 = Tree(pd.DataFrame([{
        'ID': orig_root_id
    }]))
    assert_frame_equal(expected_df, tree1._dataframe)

    # Then pull the same tree, but rename the root node so it is forced to become a reference
    tree2 = Tree(pd.DataFrame([{
        'Name': 'New Root Name',
        'ID': orig_root_id
    }]))
    df = tree2._dataframe.copy()
    assert (df.Path.iloc[1:] == 'New Root Name').all()
    assert df.ID.isnull().all()
    assert list(df['Referenced ID']) == list(expected_df.ID)
    assert list(df['Formula'].iloc[1:]) == ['$signal', '$condition', '$scalar', '$signal']
    assert df['Formula Parameters'].iloc[1:].str.fullmatch(r'[a-z]+\=' + _common.GUID_REGEX).all()

    # Make sure that pulling the same tree but specifying the correct tree does not result in references
    tree3 = Tree(pd.DataFrame([{
        'Name': 'test_pull_calcs',
        'ID': orig_root_id
    }]))
    assert_frame_equal(expected_df, tree3._dataframe)

    # Pull as references using Referenced ID column
    tree4 = Tree(pd.DataFrame([{
        'Name': 'test_pull_calcs',
        'Referenced ID': orig_root_id
    }]))
    # Assert that this is equal to tree2 except for the root name change (and a Cache Enabled value)
    df = tree2._dataframe.copy()
    df['Name'] = df['Name'].str.replace('New Root Name', 'test_pull_calcs')
    df['Path'] = df['Path'].str.replace('New Root Name', 'test_pull_calcs')
    df.loc[0, 'Cache Enabled'] = np.nan
    assert_frame_equal(tree4._dataframe, df)


def assert_tree_equals_expected(tree, expected_nodes):
    pd.set_option('display.max_columns', None)  # Print all columns if something errors
    tree_dataframe = tree._dataframe
    for expected_node in expected_nodes:
        found_series = pd.Series(data=([True] * len(tree_dataframe)))
        for key, value in expected_node.items():
            found_series = found_series & (tree_dataframe[key] == value)

        assert found_series.sum() == 1, \
            f"Found item {expected_node}" \
            f"\n{found_series.sum()} times in Dataframe" \
            f"\n{tree_dataframe}"
    assert len(tree_dataframe) == len(expected_nodes), \
        f'Tree items do not match count: Real={len(tree_dataframe)}, Expected={len(expected_nodes)}'


def assert_search_results_equals_expected(search_results_df, expected_nodes):
    pd.set_option('display.max_columns', None)  # Print all columns if something errors

    for expected_node in expected_nodes:
        asset = np.nan
        # Extract the parent asset from that path
        if expected_node['Path'].count('>>') > 0:
            asset = expected_node['Path'].rpartition(' >> ')[2]
        elif expected_node['Path'] is not '':
            asset = expected_node['Path']

        node_df = search_results_df[
            (search_results_df['Name'] == expected_node['Name']) &
            (search_results_df['Asset'] == asset) &
            (search_results_df['Type'] == expected_node['Type'])]

        assert len(node_df) == 1, \
            f"Expected item ({expected_node['Name']}, {asset}, {expected_node['Type']})" \
            f"\n was not found in Dataframe" \
            f"\n{search_results_df}"
    assert len(search_results_df) == len(expected_nodes), \
        f'Search result items do not match count: Real={len(search_results_df)}, Expected={len(expected_nodes)}'


def create_expected_list_from_tree(tree):
    # Create a list of node dicts from an existing tree.
    tree_dataframe = tree._dataframe
    expected = list()
    for index, row in tree_dataframe.iterrows():
        expected.append({
            'Name': row['Name'],
            'Path': row['Path'],
            'Type': row['Type']
        })
    return expected


def get_root_node_ids(tree):
    # Get the ID and Reference ID from the tree's root
    tree_dataframe = tree._dataframe
    root_df = tree_dataframe[(tree_dataframe['Path'] == '')]
    assert len(root_df) == 1, \
        f"Exactly one root node was not found in Dataframe: \n{tree_dataframe}"
    id = root_df['ID'].values[0]
    referenced_id = root_df['Referenced ID'].values[0]
    return id, referenced_id


def add_all_pushed_ids_to_cleanup(dataframe):
    # Get all IDs from the tree and add it to the set of cleanup_ids.
    for index, row in dataframe.iterrows():
        end_cleanup_ids.add(row['ID'])


@pytest.fixture(autouse=True)
def setup_and_teardown():
    items_api = ItemsApi(test_common.get_client())
    # Setup: Make sure any previously-created versions of these trees are not present when beginning the test
    for cleanup_name in start_cleanup_names:
        cleanup_df = spy.search(query={'Name': cleanup_name,
                                       'Datasource Class': _common.DEFAULT_DATASOURCE_CLASS,
                                       'Datasource ID': _common.DEFAULT_DATASOURCE_ID}, workbook=None)
        for index, cleanup_row in cleanup_df.iterrows():
            items_api.archive_item(id=cleanup_row['ID'])
    yield None
    # Teardown: Trash any items that we created
    for cleanup_id in end_cleanup_ids:
        items_api.archive_item(id=cleanup_id)
