# Flask Sudoku Project — Copilot Instructions

## Project Goal

Refactor the existing Flask Sudoku application into a clean, maintainable Sudoku game with additional functionality while preserving working features.

The final application must include:

* Easy, Medium, and Hard difficulty levels
* Sudoku puzzles with exactly one unique solution
* Locked prefilled cells
* Immediate invalid-move feedback
* Hint functionality
* Check functionality
* Completion message
* Game timer
* Top 10 scoreboard
* Player name, time, difficulty, and hints in the scoreboard
* Local storage persistence for the Top 10 scores
* Light and dark modes
* Responsive desktop and mobile layouts
* Alternating styling for the 3×3 Sudoku boxes

## Code Quality

* Use modern Python practices and follow PEP 8.
* Keep functions small and focused on one responsibility.
* Use descriptive variable and function names.
* Add type hints where practical.
* Add comments only where they improve understanding.
* Avoid unnecessary dependencies.
* Avoid duplicated code.
* Preserve existing working functionality unless there is a clear reason to change it.
* Use modular and reusable components.

## Project Structure

Keep responsibilities separated:

* Flask routes and application configuration in the appropriate Python files.
* Sudoku generation, solving, and validation in dedicated game logic.
* HTML in templates.
* Styling in CSS.
* Browser interaction and local storage in JavaScript.
* Tests in the tests directory.

Do not put the entire application into one large file if the functionality can reasonably be separated.

## Sudoku Logic

The Sudoku board must follow standard Sudoku rules:

* 9 rows
* 9 columns
* Nine 3×3 boxes
* Numbers 1–9
* No duplicate number in a row, column, or 3×3 box

Every generated puzzle must have exactly one valid solution.

The implementation must verify uniqueness rather than assuming that a generated puzzle has one solution.

Difficulty levels should change the number of cells initially revealed.

Prefilled cells must not be editable by the player.

## Validation

Validate user input safely.

Invalid moves should provide immediate visual feedback.

The Check feature should identify incorrect entries without incorrectly marking valid entries.

A completed puzzle should only be considered solved when all cells contain the correct solution.

Do not rely only on client-side validation for important game logic.

## Testing

Use pytest for automated testing.

Tests should cover important Sudoku logic and Flask functionality.

Run the test suite after major changes.

Do not remove existing tests simply to make the test suite pass.

When a test fails, investigate and fix the underlying issue rather than bypassing the test.

## Frontend

Use HTML, CSS, and vanilla JavaScript unless an existing project dependency provides a clear reason to use something else.

The interface must:

* Work on desktop and mobile
* Support light and dark modes
* Keep text readable
* Keep controls accessible
* Avoid layout shifts
* Clearly distinguish editable and locked cells
* Use alternating visual styles for the 3×3 Sudoku boxes

Use semantic HTML and accessible labels where practical.

## Git and Development Workflow

Make focused changes and avoid unrelated modifications.

Before making large changes, inspect the existing code and understand how it currently works.

Use Copilot as an assistant rather than blindly accepting generated code.

Review generated code before accepting it.

If a Copilot suggestion is incorrect, reject or modify it and explain the reason when documenting the development process.

Run tests after refactoring or adding major functionality.

## Priority

Complete the required project rubric before attempting optional features.

Required functionality has priority over visual extras.

Do not add unnecessary libraries or complicated architecture.

The application should remain simple enough for a beginner developer to understand and explain during a project review.

## Required Development Milestones

Document and capture Copilot interactions for these milestones:

1. Testing framework setup
2. Sudoku unique-solution validation
3. Top 10 scoreboard and localStorage
4. 3×3 grid styling

Screenshots should include the prompt and Copilot's response and should be stored in the `Screenshots` folder.

## Important Rule

Do not claim that a feature works until it has been tested.

When implementing a feature, first understand the existing code, make the smallest appropriate change, test it, and then move to the next feature.
