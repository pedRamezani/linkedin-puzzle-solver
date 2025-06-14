import sys
import json
from ortools.sat.python import cp_model


def main():
    # Load puzzle data from JSON
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'queens.json'

    with open(json_path, 'r') as f:
        data = json.load(f)

    n_rows = data['nRows']
    n_cols = data['nCols']
    cell_colors = [
        cell['cellType'] for cell in sorted(
            data['cellColors'],
            key=lambda x: x['cellId']
        )
    ]

    # Helper variable
    possible_colors = set(cell_colors)

    # Constant
    QUEEN = 1

    # Model setup
    model = cp_model.CpModel()

    # Create variables
    grid = {}

    # Create grid variables: grid[r, c] is 0 (Empty) or 1 (Queen)
    grid = {
        (r, c): model.NewBoolVar(f'cell_{r}_{c}')
        for c in range(n_cols)
        for r in range(n_rows)
    }

    # Rule: exactly one queen per row
    for r in range(n_rows):
        model.Add(sum(grid[r, c] for c in range(n_cols)) == 1)

    # Rule: exactly one queen per column
    for c in range(n_cols):
        model.Add(sum(grid[r, c] for r in range(n_rows)) == 1)

    # Rule: exactly one queen per color region
    for color in possible_colors:
        region_cells = [
            grid[divmod(i, n_cols)]
            for i, t in enumerate(cell_colors) if t == color
        ]
        model.Add(sum(region_cells) == 1)

    # Rule: no two queens can touch
    # NOTE: only diagonals need to be checked after applying the previous rules
    for r in range(n_rows):
        for c in range(n_cols):
            for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n_rows and 0 <= nc < n_cols:
                    model.AddBoolOr([grid[r, c].Not(), grid[nr, nc].Not()])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution
    ANSI_COLOR_TEMPLATE = "\033[48;5;{region}m"
    RESET = "\033[0m"

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        print("🧩 Puzzle Solved:\n")
        for r in range(n_rows):
            row_str = ""
            for c in range(n_cols):
                cell_id = r * n_cols + c
                region = cell_colors[cell_id]

                symbol = "♛" if solver.Value(grid[r, c]) == QUEEN else "x"
                color = ANSI_COLOR_TEMPLATE.format(region=region)

                row_str += f"{color} {symbol} {RESET}"
            print(row_str)
    else:
        print("❌ No solution found.")


if __name__ == '__main__':
    main()
