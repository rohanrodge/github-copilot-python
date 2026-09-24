// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const SCOREBOARD_KEY = 'sudoku-top-scores';
const THEME_KEY = 'sudoku-theme';

const gameState = {
  puzzle: [],
  difficulty: 'medium',
  completionLocked: false,
  timerId: null,
  elapsedSeconds: 0,
  startedAt: 0,
  hintsUsed: 0,
};

function applyTheme(theme) {
  const isDark = theme === 'dark';
  document.body.classList.toggle('dark-mode', isDark);
  localStorage.setItem(THEME_KEY, theme);

  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.textContent = isDark ? 'Light mode' : 'Dark mode';
    toggle.setAttribute('aria-pressed', String(isDark));
  }
}

function initializeTheme() {
  const savedTheme = localStorage.getItem(THEME_KEY);
  const preferredTheme = savedTheme === 'dark' ? 'dark' : 'light';
  applyTheme(preferredTheme);

  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const nextTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
      applyTheme(nextTheme);
    });
  }
}

function setMessage(text, type = 'error') {
  const msg = document.getElementById('message');
  msg.innerText = text;
  msg.className = type;
}

function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateTimerDisplay() {
  const timerDisplay = document.getElementById('timer-display');
  timerDisplay.textContent = formatTime(gameState.elapsedSeconds);
}

function stopTimer() {
  if (gameState.timerId) {
    clearInterval(gameState.timerId);
    gameState.timerId = null;
  }
}

function startTimer() {
  stopTimer();
  gameState.elapsedSeconds = 0;
  gameState.startedAt = Date.now();
  updateTimerDisplay();

  gameState.timerId = window.setInterval(() => {
    if (gameState.completionLocked) {
      stopTimer();
      return;
    }
    const elapsed = Math.floor((Date.now() - gameState.startedAt) / 1000);
    if (elapsed !== gameState.elapsedSeconds) {
      gameState.elapsedSeconds = elapsed;
      updateTimerDisplay();
    }
  }, 1000);
}

function getBoardFromInputs() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const value = inputs[idx].value;
      board[i][j] = value ? parseInt(value, 10) : 0;
    }
  }
  return { board, inputs };
}

function refreshCellClasses(inputs) {
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    const isPrefilled = inp.disabled;
    const isAltBox = Number(inp.dataset.box) % 2 === 1;
    inp.className = 'sudoku-cell';
    inp.classList.add(isAltBox ? 'box-alt' : 'box-primary');
    if (isPrefilled) {
      inp.classList.add('prefilled');
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      const boxIndex = Math.floor(i / 3) * 3 + Math.floor(j / 3);
      input.type = 'text';
      input.maxLength = 1;
      input.className = `sudoku-cell ${boxIndex % 2 === 1 ? 'box-alt' : 'box-primary'}`;
      input.dataset.row = i;
      input.dataset.col = j;
      input.dataset.box = boxIndex;
      input.addEventListener('input', (e) => {
        const cur = e.target;
        if (cur.disabled || gameState.completionLocked) return;
        const val = cur.value.replace(/[^1-9]/g, '');
        cur.value = val;
        if (val === '') {
          cur.classList.remove('invalid');
          return;
        }
        const row = Number(cur.dataset.row);
        const col = Number(cur.dataset.col);
        const existing = gameState.puzzle[row][col];
        if (existing !== 0 && existing !== Number(val)) {
          cur.classList.add('invalid');
          setMessage('Invalid move: this cell is locked or conflicts with the puzzle.', 'error');
          cur.value = '';
          return;
        }
        const board = getBoardFromInputs().board;
        const currentValue = Number(val);
        const safe = board[row][col] !== 0 && board[row][col] === currentValue;
        if (!safe) {
          let isValid = true;
          for (let r = 0; r < SIZE; r++) {
            if (r !== row && board[r][col] === currentValue) isValid = false;
          }
          for (let c = 0; c < SIZE; c++) {
            if (c !== col && board[row][c] === currentValue) isValid = false;
          }
          const startRow = Math.floor(row / 3) * 3;
          const startCol = Math.floor(col / 3) * 3;
          for (let r = startRow; r < startRow + 3; r++) {
            for (let c = startCol; c < startCol + 3; c++) {
              if ((r !== row || c !== col) && board[r][c] === currentValue) isValid = false;
            }
          }
          if (!isValid) {
            cur.classList.add('invalid');
            setMessage('Invalid move: value conflicts with Sudoku rules.', 'error');
            cur.value = '';
          } else {
            cur.classList.remove('invalid');
          }
        } else {
          cur.classList.remove('invalid');
        }
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  gameState.puzzle = puz;
  gameState.completionLocked = false;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const value = gameState.puzzle[i][j];
      const input = inputs[idx];
      if (value !== 0) {
        input.value = value;
        input.disabled = true;
        input.classList.add('prefilled');
      } else {
        input.value = '';
        input.disabled = false;
      }
    }
  }
}

function getStoredScores() {
  try {
    const scores = JSON.parse(localStorage.getItem(SCOREBOARD_KEY) || '[]');
    return Array.isArray(scores) ? scores : [];
  } catch (error) {
    return [];
  }
}

function renderScores() {
  const list = document.getElementById('scoreboard-list');
  const scores = getStoredScores();
  list.innerHTML = '';

  if (scores.length === 0) {
    const emptyItem = document.createElement('li');
    emptyItem.textContent = 'No scores yet.';
    list.appendChild(emptyItem);
    return;
  }

  scores.slice(0, 10).forEach((entry, index) => {
    const item = document.createElement('li');
    item.textContent = `${index + 1}. ${entry.name} — ${entry.difficulty} — ${formatTime(entry.time)} — ${entry.hints} hints`;
    list.appendChild(item);
  });
}

function saveScoreEntry(entry) {
  const scores = getStoredScores();
  const updatedScores = [...scores, entry]
    .sort((first, second) => {
      if (first.time !== second.time) return first.time - second.time;
      if (first.hints !== second.hints) return first.hints - second.hints;
      return first.name.localeCompare(second.name);
    })
    .slice(0, 10);

  localStorage.setItem(SCOREBOARD_KEY, JSON.stringify(updatedScores));
  renderScores();
}

function completeGame() {
  if (gameState.completionLocked) {
    return;
  }

  gameState.completionLocked = true;
  stopTimer();

  const playerName = document.getElementById('player-name').value.trim() || 'Player';
  saveScoreEntry({
    name: playerName,
    difficulty: gameState.difficulty,
    time: gameState.elapsedSeconds,
    hints: gameState.hintsUsed,
  });

  setMessage('Congratulations! You solved it!', 'success');
}

async function newGame() {
  const difficulty = document.getElementById('difficulty-select').value;
  gameState.difficulty = difficulty;
  try {
    const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
    const data = await res.json();
    renderPuzzle(data.puzzle);
    gameState.hintsUsed = Number(data.hints_used) || 0;
    setMessage('', 'info');
    startTimer();
  } catch (error) {
    setMessage('Unable to start a new game.', 'error');
  }
}

async function checkSolution() {
  const { board, inputs } = getBoardFromInputs();
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ board })
  });
  const data = await res.json();
  if (data.error) {
    setMessage(data.error, 'error');
    return;
  }

  refreshCellClasses(inputs);
  const incorrect = new Set(data.incorrect.map((entry) => entry[0] * SIZE + entry[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const input = inputs[idx];
    if (input.disabled) continue;
    if (incorrect.has(idx)) {
      input.classList.add('incorrect');
    }
  }

  if (data.complete) {
    completeGame();
    return;
  }

  if (incorrect.size === 0) {
    setMessage('No incorrect entries found.', 'success');
  } else {
    setMessage('Some cells are incorrect.', 'error');
  }
}

async function applyHint() {
  if (gameState.completionLocked) {
    setMessage('Puzzle already completed.', 'success');
    return;
  }

  const { board } = getBoardFromInputs();
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ board })
  });
  const data = await res.json();
  if (data.error) {
    setMessage(data.error, 'error');
    return;
  }

  gameState.hintsUsed = Number(data.hints_used) || 0;
  const boardDiv = document.getElementById('sudoku-board');
  const input = boardDiv.querySelector(`input[data-row="${data.row}"][data-col="${data.col}"]`);
  if (input) {
    input.value = data.value;
    input.disabled = true;
    input.classList.add('prefilled');
    input.classList.remove('incorrect', 'invalid');
  }

  if (data.complete) {
    completeGame();
    return;
  }

  setMessage(`Hint used: row ${data.row + 1}, col ${data.col + 1} filled with ${data.value}.`, 'info');
}

window.addEventListener('load', () => {
  initializeTheme();
  renderScores();
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  document.getElementById('hint-move').addEventListener('click', applyHint);
  document.getElementById('difficulty-select').addEventListener('change', () => {
    newGame();
  });
  updateTimerDisplay();
  newGame();
});