# Test Suite for Kivi-Paperi-Sakset Web App

## Test Summary

**Total Tests: 23**
**Status: ✅ All Passed**

## Test Coverage

### 1. Index Route Tests (2 tests)
- ✅ Index page loads successfully
- ✅ Session is cleared when visiting index

### 2. Start Game Route Tests (3 tests)
- ✅ Starting player vs player game
- ✅ Starting game vs simple AI
- ✅ Starting game vs advanced AI

### 3. Play Route Tests (9 tests)
- ✅ Redirects to index without game mode
- ✅ Displays game page correctly
- ✅ Player vs player round works
- ✅ Tie rounds are handled correctly
- ✅ Multiple rounds can be played
- ✅ Invalid moves redirect to results
- ✅ Playing against simple AI works
- ✅ Playing against advanced AI works
- ✅ All 9 possible move combinations (k/p/s) work correctly

### 4. Results Route Tests (6 tests)
- ✅ Redirects to index without session
- ✅ Displays final score
- ✅ Shows player 1 victory
- ✅ Shows player 2 victory
- ✅ Shows tie result
- ✅ Includes game statistics

### 5. Integration Tests (3 tests)
- ✅ Complete game flow from start to finish
- ✅ Full game flow with AI opponent
- ✅ Restarting game flow

## Key Features Tested

### Game Logic
- All rock-paper-scissors rule combinations
- Score tracking (wins, losses, ties)
- Move history preservation
- Session management

### AI Functionality
- Simple AI move generation
- Advanced AI with memory
- AI memory persistence across rounds

### User Interface
- Page navigation and redirects
- Session state management
- Invalid input handling
- Game restart functionality

### Edge Cases
- Missing session data
- Invalid moves
- Multiple consecutive games
- Session clearing

## Running the Tests

```bash
cd src
poetry run pytest tests/ -v
```

## Test Files
- `src/tests/test_app.py` - Main test suite (350 lines)
- `src/tests/conftest.py` - Test configuration
- `src/tests/__init__.py` - Package marker

## Dependencies
- pytest 9.0.2
- pytest-flask 1.3.0
- Flask 3.1.2
