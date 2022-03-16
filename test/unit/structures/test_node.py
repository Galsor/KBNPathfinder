def test_hash(mock_node_pair):
    # Given
    node = mock_node_pair[0]
    expected_hash = 2225566097923666370
    # When
    hash_value = hash(node)
    # Then
    assert expected_hash == hash_value
