import csv
#Search function for fields name, team, nationality, position, league, overall, and potential
#Can choose to search by multiple criteria at once

def matches_text(value, search_term):
    """Case-insensitive partial match."""
    return search_term.lower() in value.lower()


def matches_numeric(value, condition):
    """
    Supports numeric filters like:
    '90'    -> exact match
    '>=90'  -> greater than or equal
    '<25'   -> less than
    """
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False

    condition = condition.strip()

    operators = [">=", "<=", ">", "<", "="]

    for op in operators:
        if condition.startswith(op):
            try:
                target = int(condition[len(op):].strip())
            except ValueError:
                return False

            if op == ">=":
                return value >= target
            elif op == "<=":
                return value <= target
            elif op == ">":
                return value > target
            elif op == "<":
                return value < target
            elif op == "=":
                return value == target

    # No operator provided: exact match
    try:
        return value == int(condition)
    except ValueError:
        return False


def player_matches(row, filters):
    """
    Check if one player row matches all requested filters.
    Supported filter keys:
      name, team, nationality, position, league, overall, potential, age
    """
    for field, search_value in filters.items():
        if not search_value:
            continue

        if field == "name":
            short_name = row.get("short_name", "")
            long_name = row.get("long_name", "")
            if not (
                matches_text(short_name, search_value)
                or matches_text(long_name, search_value)
            ):
                return False

        elif field == "team":
            club_name = row.get("club_name", "")
            if not matches_text(club_name, search_value):
                return False

        elif field == "nationality":
            nationality = row.get("nationality_name", "")
            if not matches_text(nationality, search_value):
                return False

        elif field == "position":
            positions = row.get("player_positions", "")
            if not matches_text(positions, search_value):
                return False

        elif field == "league":
            league = row.get("league_name", "")
            if not matches_text(league, search_value):
                return False

        elif field == "overall":
            if not matches_numeric(row.get("overall", ""), search_value):
                return False

        elif field == "potential":
            if not matches_numeric(row.get("potential", ""), search_value):
                return False

        elif field == "age":
            if not matches_numeric(row.get("age", ""), search_value):
                return False

        else:
            # Ignore unsupported fields
            pass

    return True


def search_players(csv_file, filters):
    matches = []

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if player_matches(row, filters):
                matches.append(row)

    return matches


def print_results(results):
    if not results:
        print("\nNo players found.")
        return

    print(f"\nFound {len(results)} match(es):\n")
    for player in results:
        print(f"Short Name : {player.get('short_name', '')}")
        print(f"Long Name  : {player.get('long_name', '')}")
        print(f"Team       : {player.get('club_name', '')}")
        print(f"League     : {player.get('league_name', '')}")
        print(f"Nationality: {player.get('nationality_name', '')}")
        print(f"Positions  : {player.get('player_positions', '')}")
        print(f"Overall    : {player.get('overall', '')}")
        print(f"Potential  : {player.get('potential', '')}")
        print(f"Age        : {player.get('age', '')}")
        print("-" * 50)


def main():
    csv_file = "Fifa 2022 Full Player Database.csv"

    print("Enter search filters. Leave blank to skip a field.\n")
    print("For numeric fields, you can use:")
    print("  90   (exact match)")
    print("  >=90")
    print("  <25\n")

    filters = {
        "name": input("Player name: ").strip(),
        "team": input("Team/club: ").strip(),
        "nationality": input("Nationality: ").strip(),
        "position": input("Position: ").strip(),
        "league": input("League: ").strip(),
        "overall": input("Overall: ").strip(),
        "potential": input("Potential: ").strip(),
        "age": input("Age: ").strip(),
    }

    results = search_players(csv_file, filters)
    print_results(results)


if __name__ == "__main__":
    main()