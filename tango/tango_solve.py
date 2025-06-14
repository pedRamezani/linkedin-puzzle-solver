import sys
import json
from ortools.sat.python import cp_model


def main():
    # Load puzzle data from JSON
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'tango.json'

    with open(json_path, 'r') as f:
        data = json.load(f)

    n_rows = data['nRows']
    n_cols = data['nCols']
    locked_cells = data['lockedCells']
    equal_condition = data['equalCondition']
    cross_condition = data['crossCondition']

    # Constant
    SUN = 1

    # Model setup
    model = cp_model.CpModel()

    # Create grid variables: grid[r, c] is 0 (MOON) or 1 (SUN)
    grid = {
        (r, c): model.NewBoolVar(f'cell_{r}_{c}')
        for c in range(n_cols)
        for r in range(n_rows)
    }

    # Apply locked cells
    for cell in locked_cells:
        idx = cell['cellId']
        model.Add(grid[divmod(idx, n_cols)] == cell['cellType'])

    # Rule: No more than two identical symbols in a row or column
    for r in range(n_rows):
        for c in range(n_cols - 2):
            # no three moons
            model.Add(grid[r, c] + grid[r, c+1] + grid[r, c+2] != 0)
            # no three suns
            model.Add(grid[r, c] + grid[r, c+1] + grid[r, c+2] != 3)

    for c in range(n_cols):
        for r in range(n_rows - 2):
            # no three moons
            model.Add(grid[r, c] + grid[r+1, c] + grid[r+2, c] != 0)
            # no three suns
            model.Add(grid[r, c] + grid[r+1, c] + grid[r+2, c] != 3)

    # Rule: Equal number of each symbol in every row and column
    half = n_cols // 2
    for r in range(n_rows):
        model.Add(sum(grid[r, c] for c in range(n_cols)) == half)

    for c in range(n_cols):
        model.Add(sum(grid[r, c] for r in range(n_rows)) == half)

    # Rule: Edge constraints (Equal)
    for start, end in equal_condition:
        model.Add(grid[divmod(start, n_cols)] == grid[divmod(end, n_cols)])

    # Rule: Cross constraints (Different)
    for start, end in cross_condition:
        model.Add(grid[divmod(start, n_cols)] != grid[divmod(end, n_cols)])

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Print solution
    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        print("🧩 Puzzle Solved:\n")
        for r in range(n_rows):
            row = ''.join([
                '🟠' if solver.Value(grid[r, c]) == SUN
                else '🌙' for c in range(n_cols)
            ])
            print(row)
    else:
        print("❌ No solution found.")


if __name__ == '__main__':
    main()
