import pharmpy.workflows.client


def test_log():
    client = pharmpy.workflows.client.Client()
    client.log_error("help!")
    client.log_warning("an annoying warning")
    df = client.log_as_dataframe()
    assert list(df['category']) == ['ERROR', 'WARNING']
    assert list(df['message']) == ['help!', 'an annoying warning']
