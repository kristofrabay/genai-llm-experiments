from agents import function_tool
import pandas as pd
from fast_flights import FlightData, Passengers, get_flights

try: #from ai script terminal run
    from utils import parse_flight
except: #from notebook
    from utils.utils import parse_flight

@function_tool
async def add_tool(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@function_tool
def get_flights_to_destinations_tool(
    date: str,
    from_airport: str,
    to_airports: list[str],
    max_stops: int,
) -> pd.DataFrame:
    """
    Fetch flights to multiple destinations and return a combined DataFrame.
    
    Args:
        date: Flight date in YYYY-MM-DD format
        from_airport: Departure airport code in IATA format (3-letter codes), such as "BUD"
        to_airports: List of destination airport codes in IATA format (3-letter codes), such as ["CDG", "ORY", "BVA"]
        max_stops: Maximum number of stops (default: 0)
    
    Returns:
        Combined DataFrame of all flights to the specified destinations
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
        
        flights = [parse_flight(flight) for flight in result.flights]
        all_flights.extend(flights)
    
    df = pd.DataFrame(all_flights)
    return df[df['price'] > 0]