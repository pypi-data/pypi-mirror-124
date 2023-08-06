import numpy as np
import pandas as pd
import pytest

from seeq import spy
from seeq.spy.assets import _tree, Tree


def assert_frame_equal(df1, df2):
    # noinspection PyProtectedMember
    return pd._testing.assert_frame_equal(df1.sort_index(axis=1),
                                          df2.sort_index(axis=1),
                                          check_dtype=False)


def _tree_from_nested_dict(d):
    if len(d) != 1:
        raise ValueError('Cannot have more than one root.')

    root_name, root_branches = [(k, v) for k, v in d.items()][0]
    tree = Tree(root_name)

    def _add_branches(parent_name, branches_dict):
        for branch_name, sub_branches in branches_dict.items():
            tree.insert(branch_name, parent_name)
            _add_branches(branch_name, sub_branches)

    _add_branches(root_name, root_branches)
    return tree


def _build_dataframe_from_path_name_depth_triples(data):
    df = pd.DataFrame(columns=_tree._dataframe_columns)
    return df.append([{
        'Type': 'Asset',
        'Path': path,
        'Depth': depth,
        'Name': name,
    } for path, name, depth in data])


@pytest.mark.unit
def test_constructor_invalid():
    # Basic property validation
    with pytest.raises(TypeError, match="Argument 'data' should be type DataFrame or str, but is type int"):
        Tree(0)
    with pytest.raises(TypeError, match="'data' must be a name, Seeq ID, or Metadata dataframe"):
        Tree('')
    with pytest.raises(TypeError, match="'data' must be a name, Seeq ID, or Metadata dataframe"):
        Tree(None)
    with pytest.raises(ValueError, match="DataFrame with no rows"):
        Tree(pd.DataFrame(columns=['Name']))
    with pytest.raises(TypeError, match="Argument 'description' should be type str"):
        Tree('name', description=0)
    with pytest.raises(TypeError, match="Argument 'workbook' should be type str"):
        Tree('name', workbook=0)
    with pytest.raises(TypeError, match="should be type DataFrame or str, but is type Tree"):
        Tree(Tree('Tree Inception'))

    df = pd.DataFrame([{'Name': 'root1', 'Type': 'Asset'}, {'Name': 'root2', 'Type': 'Asset'}])
    with pytest.raises(RuntimeError, match="A tree can only have one root"):
        Tree(df)

    with pytest.raises(RuntimeError, match="Not logged in"):
        Tree('8DEECF16-A500-4231-939D-6C24DD123A30')


@pytest.mark.unit
def test_constructor_name():
    # Valid constructor for a new root asset with all other properties default
    name = 'test name'
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'test name', 1)
    ])
    test_tree = Tree(name)
    assert test_tree._dataframe.columns.equals(expected.columns)
    assert test_tree._dataframe.iloc[0].equals(expected.iloc[0])
    assert test_tree._workbook == spy._common.DEFAULT_WORKBOOK_PATH

    # Valid constructor for a new root asset with all other properties assigned to non-defaults
    description = 'test description'
    workbook = 'test workbook'
    expected['Description'] = [description]
    test_tree = Tree(name, description=description, workbook=workbook)
    assert_frame_equal(test_tree._dataframe, expected)
    assert test_tree._workbook == workbook


@pytest.mark.unit
def test_insert_by_name():
    tree_dict = {
        'Root Asset': {
            'L Asset': {
                'LL Asset': {},
                'LR Asset': {}
            },
            'R Asset': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'L Asset', 2),
        ('Root Asset >> L Asset', 'LL Asset', 3),
        ('Root Asset >> L Asset', 'LR Asset', 3),
        ('Root Asset', 'R Asset', 2),
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_by_name_list():
    tree_dict = {
        'Root Asset': {
            'Location A': {},
            'Location B': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    test_tree.insert([f'Equipment {n}' for n in range(1, 4)], parent='Location A')
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Location A', 2),
        ('Root Asset >> Location A', 'Equipment 1', 3),
        ('Root Asset >> Location A', 'Equipment 2', 3),
        ('Root Asset >> Location A', 'Equipment 3', 3),
        ('Root Asset', 'Location B', 2),
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_at_depth():
    tree_dict = {
        'Root Asset': {
            'Location A': {},
            'Location B': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    test_tree.insert([f'Equipment {n}' for n in range(1, 4)], parent=2)
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Location A', 2),
        ('Root Asset >> Location A', 'Equipment 1', 3),
        ('Root Asset >> Location A', 'Equipment 2', 3),
        ('Root Asset >> Location A', 'Equipment 3', 3),
        ('Root Asset', 'Location B', 2),
        ('Root Asset >> Location B', 'Equipment 1', 3),
        ('Root Asset >> Location B', 'Equipment 2', 3),
        ('Root Asset >> Location B', 'Equipment 3', 3),
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_at_path():
    tree_dict = {
        'Root Asset': {
            'Factory': {
                'Location A': {},
                'Location B': {}
            }
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    # Test partial path match with regex
    test_tree.insert('Equipment 1', parent='Factory >> Location [A-Z]')
    # Test full path match with case insensitivity
    test_tree.insert('Equipment 2', parent='rOoT aSsEt >> FaCtOrY >> lOcAtIoN b')
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Factory', 2),
        ('Root Asset >> Factory', 'Location A', 3),
        ('Root Asset >> Factory >> Location A', 'Equipment 1', 4),
        ('Root Asset >> Factory', 'Location B', 3),
        ('Root Asset >> Factory >> Location B', 'Equipment 1', 4),
        ('Root Asset >> Factory >> Location B', 'Equipment 2', 4),
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_at_root():
    tree_dict = {
        'Root Asset': {
            'Location A': {},
            'Location B': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    test_tree.insert('Location C')
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Location A', 2),
        ('Root Asset', 'Location B', 2),
        ('Root Asset', 'Location C', 2),
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_at_regex():
    tree_dict = {
        'Root Asset': {
            'Factory': {
                'Location Z': {}
            },
            'Area 51': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    test_tree.insert('Equipment 1', parent='Area [1-9][0-9]*|Location [A-Z]+')
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Area 51', 2),
        ('Root Asset >> Area 51', 'Equipment 1', 3),
        ('Root Asset', 'Factory', 2),
        ('Root Asset >> Factory', 'Location Z', 3),
        ('Root Asset >> Factory >> Location Z', 'Equipment 1', 4)
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_at_glob():
    tree_dict = {
        'Root Asset': {
            'Location A': {},
            'Location 1': {}
        }
    }
    test_tree = _tree_from_nested_dict(tree_dict)
    test_tree.insert('Equipment 1', parent='Location ?')
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root Asset', 1),
        ('Root Asset', 'Location 1', 2),
        ('Root Asset >> Location 1', 'Equipment 1', 3),
        ('Root Asset', 'Location A', 2),
        ('Root Asset >> Location A', 'Equipment 1', 3)
    ])
    assert_frame_equal(test_tree._dataframe, expected)


@pytest.mark.unit
def test_insert_preexisting_node():
    tree_dict = {
        'Root': {
            'Location A': {}
        }
    }
    tree = _tree_from_nested_dict(tree_dict)
    tree.insert('lOcAtIoN a')
    expected = _tree_from_nested_dict(tree_dict)
    assert_frame_equal(tree._dataframe, expected._dataframe)


@pytest.mark.unit
def test_insert_same_node_twice():
    tree_dict = {
        'Root': {}
    }
    tree = _tree_from_nested_dict(tree_dict)
    expected_dict = {
        'Root': {
            'Location A': {}
        }
    }
    expected = _tree_from_nested_dict(expected_dict)
    tree.insert(['Location A', 'Location A'])
    assert_frame_equal(tree._dataframe, expected._dataframe)


@pytest.mark.unit
def test_insert_no_parent_match():
    tree = Tree('Root')

    insert_results = tree.insert(children=['Child 1', 'Child 2'], parent=3)
    assert len(insert_results) == 2
    assert (insert_results['Result'] == 'Ignored: No matching parent found.').all()

    insert_results = tree.insert(children=['Child 1', 'Child 2'], parent='asdf')
    assert len(insert_results) == 2
    assert (insert_results['Result'] == 'Ignored: No matching parent found.').all()


@pytest.mark.unit
def test_constructor_dataframe_implied_and_leading_assets():
    # The constructor will imply assets and remove redundant leading assets.
    # Even though 'Root' and 'Location B' are not explicitly stated, they must exist for this to be a valid tree.
    insertions = _build_dataframe_from_path_name_depth_triples([
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root', 'Location A', 7),
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root >> Location A', 'Equipment 1', 8),
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root >> Location B', 'Equipment 2', 8),
    ])
    tree = Tree(insertions)
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Location A', 'Equipment 1', 3),
        ('Root', 'Location B', 2),
        ('Root >> Location B', 'Equipment 2', 3),
    ])
    assert_frame_equal(tree._dataframe, expected)

    # And try with Path+Asset columns
    insertions = _build_dataframe_from_path_name_depth_triples([
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root', 'Equipment 1', 8),
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root', 'Equipment 2', 8),
    ])
    insertions['Asset'] = ['Location A', 'Location B']
    tree = Tree(insertions)
    assert_frame_equal(tree._dataframe, expected)


@pytest.mark.unit
def test_insert_dataframe_implied_and_leading_assets():
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Location A', 'Equipment 1', 3),
        ('Root', 'Location B', 2),
        ('Root >> Location B', 'Equipment 2', 3),
    ])
    insertions = _build_dataframe_from_path_name_depth_triples([
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root >> Location A', 'Equipment 1', 8),
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root >> Location B', 'Equipment 2', 8),
    ])
    tree = Tree('Root')
    result_df = tree.insert(insertions)
    assert_frame_equal(tree._dataframe, expected)
    assert len(result_df) == 4  # 2 explicit insertions + 2 implied
    assert (result_df['Result'] == 'Success').all()

    # And try with Path+Asset columns
    insertions = _build_dataframe_from_path_name_depth_triples([
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root', 'Equipment 1', 8),
        ('Redundant >> Assets >> Will >> Be >> Removed >> Root', 'Equipment 2', 8),
    ])
    insertions['Asset'] = ['Location A', 'Location B']
    tree = Tree('Root')
    result_df = tree.insert(insertions)
    assert_frame_equal(tree._dataframe, expected)
    assert len(result_df) == 4  # 2 explicit insertions + 2 implied
    assert (result_df['Result'] == 'Success').all()


@pytest.mark.unit
def test_insert_dataframe_name_only():
    expected1 = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root', 'Location B', 2),
    ])
    insertions1 = pd.DataFrame([{'Name': 'Location A'}, {'Name': 'Location B'}])
    tree = Tree('Root')
    result_df1 = tree.insert(insertions1)
    assert_frame_equal(tree._dataframe, expected1)
    assert len(result_df1) == 2
    assert (result_df1['Result'] == 'Success').all()

    expected2 = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Location A', 'Equipment 1', 3),
        ('Root >> Location A', 'Equipment 2', 3),
        ('Root', 'Location B', 2),
        ('Root >> Location B', 'Equipment 1', 3),
        ('Root >> Location B', 'Equipment 2', 3),
    ])
    insertions2 = pd.DataFrame([{'Name': 'Equipment 1'}, {'Name': 'Equipment 2'}])
    result_df2 = tree.insert(insertions2, parent='location *')
    assert_frame_equal(tree._dataframe, expected2)
    assert len(result_df2) == 4
    assert (result_df2['Result'] == 'Success').all()


@pytest.mark.unit
def test_insert_dataframe_missing_name():
    insertions = pd.DataFrame([{'Formula': 'days()'}])
    tree = Tree('Root')
    with pytest.raises(RuntimeError, match="'Name' or 'Friendly Name' is required"):
        tree.insert(insertions)


@pytest.mark.unit
def test_insert_dataframe_metric():
    insertions = pd.DataFrame([{'Name': 'Location A', 'Type': 'Metric'}])
    tree = Tree('Root')
    result_df = tree.insert(insertions, errors='catalog')
    assert len(result_df) == 1
    assert 'Metrics are not yet supported' in result_df.loc[0, 'Result']


@pytest.mark.unit
def test_insert_dataframe_weird_index():
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Optimizer', 2),
        ('Root', 'Temperature', 2),
    ])
    insertions = pd.DataFrame([{'Name': 'Optimizer'}, {'Name': 'Temperature'}],
                              index=['some index', 'does not actually matter'])
    tree = Tree('Root')
    result_df = tree.insert(insertions)
    assert_frame_equal(tree._dataframe, expected)
    assert len(result_df) == 2
    assert (result_df['Result'] == 'Success').all()


@pytest.mark.unit
def test_insert_dataframe_mixed_scope():
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Optimizer', 2),
        ('Root', 'Temperature', 2),
    ])
    insertions = pd.DataFrame([{'Name': 'Optimizer', 'Scoped To': np.nan},
                               {'Name': 'Temperature', 'Scoped To': '48C3002F-BBEA-4143-8765-D7DADD4E0CA2'}])
    tree = Tree('Root')
    result_df = tree.insert(insertions)
    assert_frame_equal(tree._dataframe, expected)
    assert len(result_df) == 2
    assert (result_df['Result'] == 'Success').all()


@pytest.mark.unit
def test_insert_dataframe_with_mixed_path_existence():
    expected = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Location A', 'Equipment 1', 3),
    ])
    # Inserting a NaN path implies that 'Location A' is the sub-root
    insertions = pd.DataFrame([{'Name': 'Location A', 'Path': np.nan},
                               {'Name': 'Equipment 1', 'Path': 'Location A'}])
    tree = Tree('Root')
    result_df1 = tree.insert(insertions)
    assert_frame_equal(tree._dataframe, expected)
    assert len(result_df1) == 2
    assert (result_df1['Result'] == 'Success').all()


@pytest.mark.unit
def test_validate_empty_df():
    df = pd.DataFrame(columns=['Any', 'Columns', 'You', 'Want'])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    assert 'Tree must be non-empty' in error_summaries[0]
    assert len(error_series) == 0


@pytest.mark.unit
def test_validate_bad_depth():
    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Location A', 'Equipment 1', 3),
        ('Root >> Location A', 'Equipment 2', 1),
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'Item\'s depth does not match its path'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[3]

    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 3)
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'Item\'s depth does not match its path'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[1]


@pytest.mark.unit
def test_validate_root():
    df = _build_dataframe_from_path_name_depth_triples([
        ('Super-root', 'Root', 2),
        ('Super-root >> Root', 'Item', 3)
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'The root of the tree cannot be assigned a path.'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[0]

    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Item', 2),
        ('', 'Another Root', 1)
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'A tree can only have one root'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[2]


@pytest.mark.unit
def test_validate_bad_path():
    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location A', 2),
        ('Root >> Locat--TYPO--ion A', 'Equipment 1', 3),
        ('Root >> Location A', 'Equipment 2', 3),
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'Item\'s position in tree does not match its path.'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[2]


@pytest.mark.unit
def test_validate_path_sort():
    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Location B', 2),
        ('Root >> Location B', 'Equipment 1', 3),
        ('Root', 'Location A', 2),
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'Item is not stored in proper position sorted by path.'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[3]


@pytest.mark.unit
def test_validate_all_assets_exist():
    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root >> Location A', 'Equipment 1', 3),
        ('Root', 'Location B', 2),
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 1
    error_msg = 'Item has an ancestor not stored in this tree.'
    assert error_msg in error_summaries[0]
    assert error_msg in error_series[1]


@pytest.mark.unit
def test_validate_invalid_parent():
    df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Bad Path', 'Location B', 2),
        ('Bad Path >> Location B', 'Area 1', 3),
        ('Bad Path', 'Location A', 2),
        ('Bad Path >> Location A', 'Area 2', 3),
    ])
    error_summaries, error_series = _tree._validate(df)
    assert len(error_summaries) == 2
    assert (error_series.loc[[2, 4]] == 'Item\'s parent is invalid.').all()


@pytest.mark.unit
def test_validate_column_dtypes():
    max_errors_displayed = _tree.MAX_ERRORS_DISPLAYED
    _tree.MAX_ERRORS_DISPLAYED = 999

    df = pd.DataFrame([{
        'ID': 3.14159,
        'Referenced ID': -163,
        'Type': pd.Series([1, 2, 3]),
        'Path': set(),
        'Depth': pd.to_datetime('2020'),
        'Name': list(),
        'Description': False,
        'Formula': (),
        'Formula Parameters': 0.577215,
        'Cache Enabled': 'Yes'
    }])
    error_summaries, error_series = _tree._validate(df)
    for column in _tree._dataframe_columns:
        error_msg = f"The property '{column}' must have one of the following types"
        assert any([error_msg in x for x in error_summaries])
        assert error_msg in error_series[0]

    _tree.MAX_ERRORS_DISPLAYED = max_errors_displayed


@pytest.mark.unit
def test_validate_properties():
    df = pd.DataFrame([
        {},
        {'Name': 'My Condition', 'Type': 'Condition'},
        {'Name': 'My Formula', 'Formula': '$signal'},
        {'Name': 'My Metric', 'Type': 'Metric'},
        {'ID': '8DEECF16-A500-4231-939D-6C24DD123A30'},
        {'ID': 'bad-guid-format'},
        {'Referenced ID': 'bad-guid-format'},
        {'Name': 'Area A', 'Path': 'Example >> Cooling Tower 1 >> Cooling Tower 1'}
    ])
    error_summaries, error_series = _tree._validate(df, stage='input')
    for index, (_, error_msg) in enumerate(_tree._property_validations['input']):
        assert error_msg in error_series[index]

    df = pd.DataFrame([
        {'Name': 'My Asset', 'Path': '', 'Depth': 1},
        {'Name': 'My Condition', 'Type': 'Condition', 'Path': '', 'Depth': 1},
        {'Name': 'My Formula', 'Formula': '$signal', 'Path': '', 'Depth': 1},
        {'Name': 'My Metric', 'Type': 'Metric', 'Path': '', 'Depth': 1},
        {'Path': '', 'Depth': 1, 'Type': 'Asset'},
        {'Name': 'My Asset', 'Depth': 1, 'Type': 'Asset'},
        {'Name': 'My Asset', 'Path': '', 'Type': 'Asset'},
        {'Name': 'Cooling Tower 1', 'Path': 'Example >> Cooling Tower 1', 'Type': 'Asset', 'Depth': 4}
    ])
    df['Depth'] = df['Depth'].astype('Int64')
    error_summaries, error_series = _tree._validate(df, stage='final')
    for index, (_, error_msg) in enumerate(_tree._property_validations['final']):
        assert error_msg in error_series[index]


@pytest.mark.unit
def test_insert_other_tree():
    tree_to_insert = Tree('Area A')
    tree_to_insert.insert(['Optimizer', 'Temperature'])

    # Insert a tree directly below the root. The old 'Area A' root will not be transferred over.
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Area A', 2),
        ('Real Root >> Area A', 'Optimizer', 3),
        ('Real Root >> Area A', 'Temperature', 3),
        ('Real Root', 'Tower', 2),
    ])
    tree = Tree('Real Root')
    tree.insert('Tower')
    tree.insert(tree_to_insert)
    assert_frame_equal(tree._dataframe, expected_df)
    # Do it again to show it up-serts the nodes
    tree.insert(tree_to_insert)
    assert_frame_equal(tree._dataframe, expected_df)

    # Insert a tree below multiple parents
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Tower 1', 2),
        ('Real Root >> Tower 1', 'Area A', 3),
        ('Real Root >> Tower 1 >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower 1 >> Area A', 'Temperature', 4),
        ('Real Root', 'Tower 2', 2),
        ('Real Root >> Tower 2', 'Area A', 3),
        ('Real Root >> Tower 2 >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower 2 >> Area A', 'Temperature', 4),
    ])
    tree = Tree('Real Root')
    tree.insert(['Tower 1', 'Tower 2'])
    tree.insert(tree_to_insert, parent='Tower*')
    assert_frame_equal(tree._dataframe, expected_df)


@pytest.mark.unit
def test_trim_unneeded_paths_constructor():
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Tower', 2),
        ('Real Root >> Tower', 'Area A', 3),
        ('Real Root >> Tower >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower >> Area A', 'Temperature', 4),
    ])
    # Test three leading nodes to be removed
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2', 'Real Root', 4),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root', 'Tower', 5),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower', 'Area A', 6),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower >> Area A', 'Optimizer', 7),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower >> Area A', 'Temperature', 7),
    ])
    tree = Tree(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test one leading node to be removed
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Root', 'Real Root', 2),
        ('Dupe Root >> Real Root', 'Tower', 3),
        ('Dupe Root >> Real Root >> Tower', 'Area A', 4),
        ('Dupe Root >> Real Root >> Tower >> Area A', 'Temperature', 5),
        ('Dupe Root >> Real Root >> Tower >> Area A', 'Optimizer', 5),
    ])
    tree = Tree(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test no changes needed
    test_df = expected_df.copy()
    tree = Tree(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test with implied shared roots only
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Tower 1', 2),
        ('Real Root >> Tower 1', 'Area A', 3),
        ('Real Root >> Tower 1 >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower 1 >> Area A', 'Temperature', 4),
        ('Real Root', 'Tower 2', 2),
        ('Real Root >> Tower 2', 'Area A', 3),
        ('Real Root >> Tower 2 >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower 2 >> Area A', 'Temperature', 4),
    ])
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower 1 >> Area A', 'Temperature', 4),
        ('Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower 1 >> Area A', 'Optimizer', 4),
        ('Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower 2 >> Area A', 'Temperature', 4),
        ('Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower 2 >> Area A', 'Optimizer', 4),
    ])
    tree = Tree(test_df)
    assert_frame_equal(tree._dataframe, expected_df)


@pytest.mark.unit
def test_trim_unneeded_paths_insert():
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Tower', 2),
        ('Real Root >> Tower', 'Area A', 3),
        ('Real Root >> Tower >> Area A', 'Optimizer', 4),
        ('Real Root >> Tower >> Area A', 'Temperature', 4),
    ])
    # Test three leading nodes to be removed with the same root as parent
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2', 'Real Root', 4),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root', 'Tower', 5),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower', 'Area A', 6),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower >> Area A', 'Temperature', 7),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Real Root >> Tower >> Area A', 'Optimizer', 7),
    ])
    tree = Tree('Real Root')
    tree.insert(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test one leading node to be removed
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Root', 'Real Root', 2),
        ('Dupe Root >> Real Root', 'Tower', 3),
        ('Dupe Root >> Real Root >> Tower', 'Area A', 4),
        ('Dupe Root >> Real Root >> Tower >> Area A', 'Temperature', 5),
        ('Dupe Root >> Real Root >> Tower >> Area A', 'Optimizer', 5),
    ])
    tree = Tree('Real Root')
    tree.insert(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test no changes needed
    tree = Tree('Real Root')
    tree.insert(expected_df.copy())
    assert_frame_equal(tree._dataframe, expected_df)

    # Test three leading nodes to be removed with a different root as parent
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Sub Root', 2),
        ('Real Root >> Sub Root', 'Tower', 3),
        ('Real Root >> Sub Root >> Tower', 'Area A', 4),
        ('Real Root >> Sub Root >> Tower >> Area A', 'Optimizer', 5),
        ('Real Root >> Sub Root >> Tower >> Area A', 'Temperature', 5),
    ])
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2', 'Sub Root', 4),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Sub Root', 'Tower', 5),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Sub Root >> Tower', 'Area A', 6),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Sub Root >> Tower >> Area A', 'Temperature', 7),
        ('Dupe Root >> Dupe Path 1 >> Dupe Path 2 >> Sub Root >> Tower >> Area A', 'Optimizer', 7),
    ])
    tree = Tree('Real Root')
    tree.insert(test_df)
    assert_frame_equal(tree._dataframe, expected_df)

    # Test with implied shared roots only
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Real Root', 1),
        ('Real Root', 'Sub Root', 2),
        ('Real Root >> Sub Root', 'Tower 1', 3),
        ('Real Root >> Sub Root >> Tower 1', 'Area A', 4),
        ('Real Root >> Sub Root >> Tower 1 >> Area A', 'Optimizer', 5),
        ('Real Root >> Sub Root >> Tower 1 >> Area A', 'Temperature', 5),
        ('Real Root >> Sub Root', 'Tower 2', 3),
        ('Real Root >> Sub Root >> Tower 2', 'Area A', 4),
        ('Real Root >> Sub Root >> Tower 2 >> Area A', 'Optimizer', 5),
        ('Real Root >> Sub Root >> Tower 2 >> Area A', 'Temperature', 5),
    ])
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Dupe Path >> Sub Root >> Tower 1 >> Area A', 'Temperature', 5),
        ('Dupe Path >> Sub Root >> Tower 1 >> Area A', 'Optimizer', 5),
        ('Dupe Path >> Sub Root >> Tower 2 >> Area A', 'Temperature', 5),
        ('Dupe Path >> Sub Root >> Tower 2 >> Area A', 'Optimizer', 5),
    ])
    tree = Tree('Real Root')
    tree.insert(test_df)
    assert_frame_equal(tree._dataframe, expected_df)
    # Inserting that same thing again should be idempotent.
    tree.insert(test_df)
    assert_frame_equal(tree._dataframe, expected_df)


@pytest.mark.unit
def test_reify_missing_assets():
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root', 'Tower', 2),
        ('Root >> Tower', 'Region 1', 3),
        ('Root >> Tower >> Region 1', 'Area A', 4),
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1', 'Area B', 4),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower', 'Region 2', 3),
        ('Root >> Tower >> Region 2', 'Area C', 4),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    # Test everything missing except the leaf nodes
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    result_df = _tree._reify_missing_assets(test_df)
    _tree._sort_by_node_path(result_df)
    assert_frame_equal(result_df, expected_df)

    # Test everything missing between the root and the leaves
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('', 'Root', 1),
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    result_df = _tree._reify_missing_assets(test_df)
    _tree._sort_by_node_path(result_df)
    assert_frame_equal(result_df, expected_df)

    # Test missing the root-most two levels
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Root >> Tower', 'Region 1', 3),
        ('Root >> Tower >> Region 1', 'Area A', 4),
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1', 'Area B', 4),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower', 'Region 2', 3),
        ('Root >> Tower >> Region 2', 'Area C', 4),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    result_df = _tree._reify_missing_assets(test_df)
    _tree._sort_by_node_path(result_df)
    assert_frame_equal(result_df, expected_df)

    # Test no changes needed
    test_df = expected_df.copy()
    result_df = _tree._reify_missing_assets(test_df)
    _tree._sort_by_node_path(result_df)
    assert_frame_equal(result_df, expected_df)

    # Test where the first two levels should not be reified.
    expected_df = _build_dataframe_from_path_name_depth_triples([
        ('Root >> Tower', 'Region 1', 3),
        ('Root >> Tower >> Region 1', 'Area A', 4),
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1', 'Area B', 4),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower', 'Region 2', 3),
        ('Root >> Tower >> Region 2', 'Area C', 4),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    test_df = _build_dataframe_from_path_name_depth_triples([
        ('Root >> Tower >> Region 1 >> Area A', 'Optimizer', 5),
        ('Root >> Tower >> Region 1 >> Area A', 'Temperature', 5),
        ('Root >> Tower >> Region 1 >> Area B', 'Optimizer', 5),
        ('Root >> Tower >> Region 2 >> Area C', 'Temperature', 5),
    ])
    result_df = _tree._reify_missing_assets(test_df, 'Root >> Tower')
    _tree._sort_by_node_path(result_df)
    assert_frame_equal(result_df, expected_df)


@pytest.mark.unit
def test_upsert():
    df1 = pd.DataFrame([{
        'Path': 'Root',
        'Name': 'Area A',
        'Property': 'Anything',
        'Numerical': 123
    }, {
        'Path': 'Root >> Area A',
        'Name': 'Temperature',
        'Property': 'Old Value',
        'Numerical': 1,
        'Extra Old Column': 'Anything'
    }])
    df2 = pd.DataFrame([{
        'Path': 'Root >> Area A',
        'Name': 'Optimizer',
        'Property': 'Anything',
        'Numerical': 2,
        'Extra New Column': 'Something Unexpected'
    }, {
        'Path': 'root >> area A',
        'Name': 'temperature',
        'Property': 'New Value',
        'Numerical': np.nan,
        'Extra New Column': 'Something Unexpected'
    }])

    expected_df = pd.DataFrame([{
        'Path': 'Root',
        'Name': 'Area A',
        'Property': 'Anything',
        'Numerical': 123
    }, {
        'Path': 'Root >> Area A',
        'Name': 'Temperature',
        'Property': 'New Value',
        'Numerical': 1,
        'Extra Old Column': 'Anything'
    }, {
        'Path': 'Root >> Area A',
        'Name': 'Optimizer',
        'Property': 'Anything',
        'Numerical': 2
    }])

    upsert_df = _tree._upsert(df1, df2)
    assert_frame_equal(upsert_df, expected_df)
    assert upsert_df['Numerical'].dtype in [np.int32, np.int64]

    expected_df.loc[1, 'Property'] = 'Old Value'
    upsert_df = _tree._upsert(df1, df2, prefer_right=False)
    assert_frame_equal(upsert_df, expected_df)
