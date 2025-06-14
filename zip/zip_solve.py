import sys
import json
from ortools.sat.python import cp_model


def main():
    # Load puzzle data from JSON
    json_path = sys.argv[1] if len(sys.argv) > 1 else 'zip.json'

    with open(json_path, 'r') as f:
        data = json.load(f)

    n_rows = data['nRows']
    n_cols = data['nCols']
    locked_cells = [
        cell["cellId"]
        for cell in sorted(
            data['lockedCells'],
            key=lambda cell: cell["cellNumber"]
        )
    ]
    wall_condition = data['wallCondition']

    # Helper variable
    n = n_rows * n_cols

    # Model setup
    model = cp_model.CpModel()

    # Create path variables that represents the order of traversal
    # Example (3x3 grid, spiral path):
    # 2 3 4     ┌─────┐
    # 1 0 5     └─ o  │
    # 8 7 6     x ────┘
    # path = [2, 3, 4, 1, 0, 5, 8, 7, 6]
    path = [model.NewIntVar(0, n-1, f'pos_{i}') for i in range(n)]

    # Rule: path is a permutation of [0, ..., n-1]
    model.AddAllDifferent(path)

    # Rule: first and last locked cells are start and end of the path
    model.Add(path[locked_cells[0]] == 0)
    model.Add(path[locked_cells[-1]] == n-1)

    # Rule: locked cells should be visited in the prespecified order
    for i in range(len(locked_cells) - 1):
        model.Add(path[locked_cells[i]] < path[locked_cells[i+1]])

    def neighbors(cell_id: int) -> list[int]:
        '''Returns the IDs of neighbouring cells while taking into account walls and grid boundaries.'''
        r, c = divmod(cell_id, n_cols)
        neighbor = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n_rows and 0 <= nc < n_cols:
                neighbor_cell_id = nr * n_cols + nc
                if [cell_id, neighbor_cell_id] in wall_condition or [neighbor_cell_id, cell_id] in wall_condition:
                    continue
                neighbor.append(neighbor_cell_id)
        return neighbor

    # Rule: Each cell, except for the final path cell, should have a exactly one successor cell within its neighbourhood.
    for i in range(n):
        if i == locked_cells[-1]:
            continue

        from_cell = path[i]
        # Create boolean literals for allowed moves
        allowed = []
        for j in neighbors(i):
            to_cell = path[j]

            b = model.NewBoolVar(f'move_{i}_{j}')
            model.Add(from_cell + 1 == to_cell).OnlyEnforceIf(b)
            allowed.append(b)

        model.AddExactlyOne(allowed)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    solution = [solver.Value(path[i]) for i in range(n)]

    def asciify(solution: list[int]) -> list[str]:
        '''Returns an ASCII representation of the solution.'''
        points: list[tuple[int, int, int]] = sorted(
            (
                (*reversed(divmod(i, n_cols)), sol)
                for i, sol in enumerate(solution)
            ),
            key=lambda x: x[-1]
        )

        directions_with_ids: list[tuple[str | None, int]] = []

        for i in range(len(points)):
            curr = points[i]

            if i in [0, len(points) - 1]:
                # No direction for first or last
                directions_with_ids.append([
                    ' o ' if i == 0 else ' x ',
                    curr[0] + curr[1] * n_cols
                ])
                continue

            prev = points[i - 1]
            next_ = points[i + 1]

            direction_map = {
                (0, -1): 'up',
                (-1,  0): 'left',
                (1,  0): 'right',
                (0,  1): 'down'
            }

            dx = curr[0] - prev[0]
            dy = curr[1] - prev[1]

            # Normalize the delta to -1, 0, or 1
            dx = max(min(dx, 1), -1)
            dy = max(min(dy, 1), -1)

            first_direction = direction_map.get((dx, dy), None)

            dx = next_[0] - curr[0]
            dy = next_[1] - curr[1]

            # Normalize the delta to -1, 0, or 1
            dx = max(min(dx, 1), -1)
            dy = max(min(dy, 1), -1)

            second_direction = direction_map.get((dx, dy), None)

            ascii_map = {
                'left-left': '───',
                'left-up': ' └─',
                'left-down': ' ┌─',
                'up-left': '─┐ ',
                'up-up': ' │ ',
                'up-right': ' ┌─',
                'right-up': '─┘ ',
                'right-right': '───',
                'right-down': '─┐ ',
                'down-left': '─┘ ',
                'down-right': ' └─',
                'down-down': ' │ ',
            }

            direction = ascii_map.get(
                f'{first_direction}-{second_direction}', None)
            directions_with_ids.append([direction, curr[0] + curr[1] * n_cols])

        return [
            direction
            for direction, _ in sorted(
                directions_with_ids,
                key=lambda d: d[1]
            )
        ]

    # Print solution
    ascii_solution = asciify(solution)

    if status in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        print("🧩 Puzzle Solved:\n")
        for r in range(n_rows):
            row = ''.join([
                ascii_solution[r * n_cols + c]
                for c in range(n_cols)
            ])
            print(row)
    else:
        print("❌ No solution found.")


if __name__ == '__main__':
    main()
