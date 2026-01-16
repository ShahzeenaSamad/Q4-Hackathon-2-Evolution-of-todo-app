# Console Todo App - Testing Guide

**Phase I Console App**
**Created**: January 16, 2026

---

## 🧪 How to Run and Test

### **Quick Start**

```powershell
# Navigate to phase-1-console
cd phase-1-console

# Run the app
python console-todo.py

# OR (if Python launcher)
py console-todo.py
```

---

## ✅ Test Cases

### **Test 1: Application Starts**

**Steps**:
1. Run: `python console-todo.py`
2. Check welcome message appears

**Expected**:
```
🚀 Todo App Starting...
📝 All tasks stored in memory (lost on exit)
💾 Save your work before exiting!

========================================
Welcome to Todo App
========================================
1. Add Todo
2. View Todos
3. Update Todo
4. Complete Todo
5. Delete Todo
6. Exit
========================================

Enter your choice (1-6):
```

**Status**: ✅ PASS if menu appears

---

### **Test 2: Add Todo**

**Steps**:
1. Select option `1`
2. Enter title: "Buy groceries"
3. Enter description: "Milk, eggs, bread"

**Expected**:
```
✅ Task added: [1] Buy groceries
```

**Status**: ✅ PASS if task added successfully

---

### **Test 3: View Todos**

**Steps**:
1. Add 2-3 tasks
2. Select option `2`

**Expected**:
```
Your Tasks:
----------------------------------------
[1]   Buy groceries
[2]   Call mom
[3]   Finish Python project
----------------------------------------

Total tasks: 3 (0 completed, 3 pending)
```

**Status**: ✅ PASS if all tasks displayed

---

### **Test 4: Update Todo**

**Steps**:
1. Select option `3`
2. Enter task ID: `1`
3. Enter new title: "Buy groceries and fruits"

**Expected**:
```
✅ Task 1 updated
```

**Status**: ✅ PASS if task updated

---

### **Test 5: Complete Todo**

**Steps**:
1. Select option `4`
2. Enter task ID: `1`

**Expected**:
```
✅ Task 1 marked as complete
```

**Status**: ✅ PASS if task marked complete

---

### **Test 6: Delete Todo**

**Steps**:
1. Select option `5`
2. Enter task ID: `2`

**Expected**:
```
✅ Task 2 deleted
```

**Status**: ✅ PASS if task deleted

---

### **Test 7: Exit Application**

**Steps**:
1. Select option `6`

**Expected**:
```
👋 Thank you for using Todo App!
💾 Remember: Your tasks are saved in memory only
    (Consider implementing file/database storage in Phase II)

Goodbye! 👋
```

**Status**: ✅ PASS if app exits cleanly

---

## ❌ Error Handling Tests

### **Test 8: Empty Title**

**Steps**:
1. Select option `1`
2. Enter title: (just press Enter, no text)

**Expected**:
```
❌ Title cannot be empty. Please try again.
Title:
```

**Status**: ✅ PASS if validation works

---

### **Test 9: Invalid Task ID**

**Steps**:
1. Select option `3` (Update)
2. Enter task ID: `999`

**Expected**:
```
❌ Task 999 not found
```

**Status**: ✅ PASS if error handled

---

### **Test 10: Non-Numeric Input**

**Steps**:
1. Select option `4`
2. Enter task ID: `abc`

**Expected**:
```
❌ Invalid input. Please enter a number.
Enter task ID:
```

**Status**: ✅ PASS if validation catches

---

### **Test 11: Empty List View**

**Steps**:
1. Don't add any tasks
2. Select option `2` (View)

**Expected**:
```
📝 No tasks yet. Add your first task!
```

**Status**: ✅ PASS if graceful message

---

## 📊 Performance Tests

### **Test 12: Add 100 Tasks**

**Steps**:
1. Write script to add 100 tasks
2. Check memory usage
3. Check speed

**Expected**:
- Should complete quickly
- Memory usage minimal
- No performance degradation

**Status**: ⏳ Manual test required

---

## ✅ Success Criteria Validation

| Criterion | Test | Target | Result |
|-----------|------|--------|--------|
| SC-001 | App starts < 1s | < 1s | ⏳ Test manually |
| SC-002 | Add < 500ms | < 500ms | ⏳ Test manually |
| SC-003 | View 100 items < 1s | < 1s | ⏳ Test manually |
| SC-004 | All 5 options work | All work | ⏳ Test all |
| SC-005 | No crashes on bad input | Graceful | ⏳ Test errors |
| SC-006 | PEP 8 compliant | Pass style | ⏳ Run pylint |
| SC-007 | Has docstrings | All functions | ✅ Checked |
| SC-008 | Runs on Python 3.13+ | 3.13+ | ⏳ Check version |

---

## 🔧 Run Commands

```powershell
# Check Python version
python --version

# Run the app
python console-todo.py

# Run with Python launcher
py console-todo.py

# Check code style (if pylint installed)
pylint console-todo.py

# Count lines
wc -l console-todo.py
```

---

## 📝 Testing Checklist

Copy this checklist and mark as you test:

```
Pre-Test Setup:
[ ] Python 3.13+ installed
[ ] Navigate to phase-1-console
[ ] console-todo.py exists

Functional Tests:
[ ] App starts and shows menu
[ ] Can add task with title only
[ ] Can add task with title and description
[ ] Can view empty task list
[ ] Can view tasks with items
[ ] Can update existing task
[ ] Can complete task
[ ] Can delete task
[ ] Can exit cleanly

Error Handling:
[ ] Empty title rejected
[ ] Invalid task ID handled
[ ] Non-numeric input handled
[ ] Negative ID rejected
[ ] Empty list view handled

Code Quality:
[ ] Code has docstrings
[ ] Code has type hints
[ ] Code is PEP 8 compliant
[ ] No hardcoded values
[ ] Clean structure
```

---

## 🎯 Test Session Example

```
$ python console-todo.py

🚀 Todo App Starting...

========================================
Welcome to Todo App
========================================
1. Add Todo
2. View Todos
3. Update Todo
4. Complete Todo
5. Delete Todo
6. Exit
========================================

Enter your choice (1-6): 1

--- Add New Todo ---
Title: Buy groceries
Description: Milk, eggs, bread

✅ Task added: [1] Buy groceries

Enter your choice (1-6): 2

Your Tasks:
----------------------------------------
[1]   Buy groceries
----------------------------------------

Total tasks: 1 (0 completed, 1 pending)

Enter your choice (1-6): 4

--- Complete Todo ---
Enter task ID: 1

✅ Task 1 marked as complete

Enter your choice (1-6): 2

Your Tasks:
----------------------------------------
[1] ✓ Buy groceries
----------------------------------------

Total tasks: 1 (1 completed, 0 pending)

Enter your choice (1-6): 6

👋 Thank you for using Todo App!
💾 Remember: Your tasks are saved in memory only
    (Consider implementing file/database storage in Phase II)

Goodbye! 👋

$
```

---

## 📈 Test Results

**Date**: [Fill after testing]
**Tester**: [Your name]
**Python Version**: [Fill after testing]

| Test | Result | Notes |
|------|--------|-------|
| Test 1: App starts | ⏳ |  |
| Test 2: Add todo | ⏳ |  |
| Test 3: View todos | ⏳ |  |
| Test 4: Update todo | ⏳ |  |
| Test 5: Complete todo | ⏳ |  |
| Test 6: Delete todo | ⏳ |  |
| Test 7: Exit app | ⏳ |  |
| Test 8: Empty title | ⏳ |  |
| Test 9: Invalid ID | ⏳ |  |
| Test 10: Non-numeric input | ⏳ |  |
| Test 11: Empty list view | ⏳ |  |

**Overall Result**: _____ (PASS/FAIL)

---

## 🚀 Next Steps After Testing

If all tests pass:
- ✅ Phase I Todo App complete
- ✅ Ready for submission
- ✅ Can proceed to Phase II (Full-Stack Web App)

If tests fail:
- Document issues
- Fix bugs
- Retest until all pass

---

**Ready to Test**: ✅
**Now run**: `python console-todo.py`
