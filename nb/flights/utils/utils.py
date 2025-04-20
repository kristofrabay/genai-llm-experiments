from fast_flights import FlightData, Passengers, Result, get_flights
import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime


def parse_flight(flight):
    """
    Parse a Flight object and return a clean dictionary with parsed values.
    
    Args:
        flight: A Flight object
        
    Returns:
        dict: Clean dictionary with parsed values
    """
    clean_flight = {}
    
    # Extract price as number
    price_str = flight.price
    # Handle empty price strings
    price_digits = re.sub(r'[^\d]', '', price_str)
    clean_flight['price'] = int(price_digits) if price_digits else 0
    
    # Parse departure and arrival as datetime
    departure_str = flight.departure
    arrival_str = flight.arrival
    
    # Extract date and time from strings
    departure_match = re.search(r'(\d+:\d+ [AP]M) on ([A-Za-z]+), ([A-Za-z]+) (\d+)', departure_str)
    arrival_match = re.search(r'(\d+:\d+ [AP]M) on ([A-Za-z]+), ([A-Za-z]+) (\d+)', arrival_str)
    
    if departure_match:
        departure_datetime = datetime.strptime(f"{departure_match.group(3)} {departure_match.group(4)} 2025 {departure_match.group(1)}", "%b %d %Y %I:%M %p")
        clean_flight['departure_date'] = departure_datetime.strftime('%Y-%m-%d')
        clean_flight['departure_time'] = departure_datetime.strftime('%H:%M')
    
    if arrival_match:
        arrival_datetime = datetime.strptime(f"{arrival_match.group(3)} {arrival_match.group(4)} 2025 {arrival_match.group(1)}", "%b %d %Y %I:%M %p")
        clean_flight['arrival_date'] = arrival_datetime.strftime('%Y-%m-%d')
        clean_flight['arrival_time'] = arrival_datetime.strftime('%H:%M')
    
    # Extract duration as hours (float)
    duration_str = flight.duration
    duration_match = re.search(r'(\d+) hr (\d+) min', duration_str)
    if duration_match:
        hours = int(duration_match.group(1))
        minutes = int(duration_match.group(2))
        clean_flight['duration_hours'] = round(hours + minutes / 60, 3)
    
    # Add other relevant fields
    clean_flight['name'] = flight.name
    clean_flight['stops'] = flight.stops
    clean_flight['is_best'] = flight.is_best
    clean_flight['price_denomination'] = re.sub(r'[\d,]', '', price_str).strip()
    
    # Keep origin and destination airports
    #Not Implemented yet as response does not include this information
    #clean_flight['from_airport'] = flight.from_airport
    #clean_flight['to_airport'] = flight.to_airport
    
    return clean_flight


def plot_price_distribution(df, figsize=(7, 4), bins=20, color='skyblue', edgecolor='black', 
                           title='Flight Price Distribution', xlabel='Price (HUF)', ylabel='Frequency'):
    """
    Plot the distribution of flight prices.
    
    Args:
        df: DataFrame containing flight data with a 'price' column
        figsize: Tuple specifying figure dimensions (width, height)
        bins: Number of histogram bins
        color: Color of histogram bars
        edgecolor: Color of histogram bar edges
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
    
    Returns:
        matplotlib.figure.Figure: The created figure
    """
    
    fig = plt.figure(figsize=figsize)
    df['price'].hist(bins=bins, color=color, edgecolor=edgecolor)
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{int(x):,}'))
    
    return fig


def get_flights_to_destinations(
    date: str,
    from_airport: str,
    to_airports: list[str],
    max_stops: int = 0,
    #trip: str = "one-way",
    #passengers_adults: int = 2,
) -> pd.DataFrame:
    """
    Fetch flights to multiple destinations and return a combined DataFrame.
    
    Note: The fast_flights API doesn't support multiple destinations in a single call,
    so this function makes separate API calls for each destination and combines the results.
    
    Args:
        date: Flight date in YYYY-MM-DD format
        from_airport: Departure airport code in IATA format (3-letter codes), such as "BUD"
        to_airports: List of destination airport codes in IATA format (3-letter codes), such as ["CDG", "ORY", "BVA"]
        max_stops: Maximum number of stops (default: 0)
    
    Returns:
        pd.DataFrame: Combined DataFrame of all flights to the specified destinations
    """
    all_flights = []
    
    for to_airport in to_airports:
        try:
            result = get_flights(
                flight_data=[
                    FlightData(
                        date=date, 
                        from_airport=from_airport, 
                        to_airport=to_airport, 
                        max_stops=max_stops
                    ),
                ],
                trip='one-way',
                seat='economy',
                passengers=Passengers(adults=2),
                fetch_mode='local'
            )
        except Exception:
            continue

        #trip: Trip type, either "one-way" or "round-trip" (default: "one-way")
        #seat: Seat class (default: "economy")
        #passengers_adults: Number of adult passengers (default: 2)
        #fetch_mode: API fetch mode (default: "local")
        
        flights = [parse_flight(flight) for flight in result.flights]
        all_flights.extend(flights)
    
    df = pd.DataFrame(all_flights)
    return df[df['price'] > 0]
