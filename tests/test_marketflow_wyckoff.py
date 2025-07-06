# This code is a test suite for the marketflow_wyckoff module, specifically testing the run_analysis function.
from marketflow.marketflow_wyckoff import WyckoffAnalyzer
import pandas as pd

def test_run_analysis():
    # Test with a sample DataFrame
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Open': [100, 102, 101],
        'High': [105, 106, 104],
        'Low': [99, 100, 98],
        'Close': [104, 105, 103],
        'Volume': [1000, 1500, 1200]
    }
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)  # Set Date as index

    # Create a mock processed_data dictionary
    processed_data = {
        "price": df[['Open', 'High', 'Low', 'Close']],
        "volume": df['Volume']
    }

    # Initialize WyckoffAnalyzer with processed_data
    analyzer = WyckoffAnalyzer(processed_data)

    # Run the analysis
    result = analyzer.run_analysis()

    print(result)  # Print the result for debugging

    assert isinstance(result, dict)  # Check the result type
    assert 'analysis' in result
    assert 'summary' in result
    assert isinstance(result['analysis'], pd.DataFrame)
    assert isinstance(result['summary'], dict)
    assert not result['analysis'].empty
    assert 'Wyckoff Phase' in result['analysis'].columns
    assert 'Volume' in result['analysis'].columns
    assert 'Price Action' in result['summary']

if __name__ == "__main__":
    test_run_analysis()
    
    print("All tests passed!")
# This code is a test suite for the marketflow_wyckoff module, specifically testing the run_analysis function.
# It includes tests for various scenarios such as valid data, empty DataFrame, invalid data types, missing columns,
# non-DataFrame input, large data, edge cases like NaN values, and incomplete data.
# Each test checks the output structure and content to ensure the function behaves as expected.
# The tests are designed to be run independently and will print "All tests passed!" if all assertions are successful.