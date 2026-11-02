from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 1000

markets = ["Whitefield", "Sarjapur Road", "Hebbal", "Yelahanka", "Electronic City", "Devanahalli"]
builders = ["Builder A", "Builder B", "Builder C", "Builder D", "Builder E"]
configs = ["2BHK", "3BHK", "4BHK", "5BHK"]
statuses = ["Booked", "Available", "Confirmed"]
quarters = ["Q1", "Q2", "Q3", "Q4"]
channels = ["Direct", "Broker", "Online", "Referral"]
buyers = ["End User", "Investor", "NRI"]

df = pd.DataFrame({
    "Project_ID": rng.choice([f"P{i:04d}" for i in range(1, 151)], n),
    "Micro_Market": rng.choice(markets, n),
    "Builder": rng.choice(builders, n),
    "Ticket_Price_Cr": np.round(rng.uniform(2.5, 25, n), 2),
    "Configuration": rng.choice(configs, n),
    "Possession_Status": rng.choice(["Ready", "Under Construction", "Pre-Launch"], n),
    "Amenity_Score": np.round(rng.uniform(30, 95, n), 1),
    "Booking_Status": rng.choice(statuses, n, p=[0.42, 0.45, 0.13]),
    "Purchase_Quarter": rng.choice(quarters, n),
    "Sales_Channel": rng.choice(channels, n),
    "Buyer_Type": rng.choice(buyers, n),
    "Buyer_Comments": rng.choice(["Good location", "Premium amenities", "Price is high", "Good investment"], n),
})

out = Path("data/raw/sample_luxury_housing_sales.csv")
out.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(out, index=False)
print(f"Wrote {len(df):,} sample rows to {out}")
