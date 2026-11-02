import pandas as pd

from src.cleaning import clean_dataset, derive_booking_flag, derive_quarter_number


def test_booking_flag():
    result = derive_booking_flag(pd.Series(["Booked", "Available", "Confirmed", "No"]))
    assert result.tolist() == [1, 0, 1, 0]


def test_quarter_number():
    result = derive_quarter_number(pd.Series(["Q1", "FY25 Q3", "q4", None]))
    assert result.tolist() == [1, 3, 4, None]


def test_clean_dataset():
    raw = pd.DataFrame({
        "Project ID": ["P1", "P1"],
        "Micro Market": [" Whitefield ", " Whitefield "],
        "Builder": [" Builder A ", " Builder A "],
        "Ticket Price Cr": ["12.50", "12.50"],
        "Booking Status": ["Booked", "Booked"],
        "Purchase Quarter": ["Q1", "Q1"],
    })
    result = clean_dataset(raw)
    assert result["micro_market"].iloc[0] == "Whitefield"
    assert result["ticket_price_cr"].iloc[0] == 12.5
    assert result["booking_flag"].iloc[0] == 1
    assert len(result) == 1
