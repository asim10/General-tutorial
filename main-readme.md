---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
---

## Important Concept: if __name__ == "__main__" 

<!-- #region -->
### 1️⃣ What is __name__?
Every Python file (module) has a special built‑in variable called __name__.
- If the file is run directly, Python sets:
```python
__name__ = "__main__"
````
- If the file is imported into another file, Python sets:
```python
__name__ = "<file_name>"
```
<!-- #endregion -->

<!-- #region -->
### 2️⃣ What Does This Line Mean?
```python
if __name__ == "__main__":
```
if means
>“Run the code below only if this file is executed directly, not if it is imported.”
<!-- #endregion -->

<!-- #region -->
### 3️⃣ Simple Example
#### ✅ File: example.py
```python
print("This always runs")

if __name__ == "__main__":
    print("This runs only when file is executed directly")
```

#### ▶ Run directly
```python
python example.py
```
#### Output
```
This always runs
This runs only when file is executed directly
```
<!-- #endregion -->

<!-- #region -->
### 🔁 Import into another file
✅ File: main.py
```python
import example
```
Output
```
This always runs
```
❌ The if __name__ == "__main__": **block does NOT run**

<!-- #endregion -->

### 4️⃣ Why Is This Needed?
#### 👉 Without it:
- Code executes immediately when imported
- Bad for reusable modules
- Can cause unexpected behavior

#### 👉 With it:
- ✅ Clean imports
- ✅ Reusable code
- ✅ Safe execution
- ✅ Industry best practice

<!-- #region -->
### 5️⃣ Real‑World Example (Function Execution)
```python
def add(a, b):
    return a + b

if __name__ == "__main__":
    result = add(10, 20)
    print(result)
```
✅ Direct execution
```python
python math_utils.py

30
```
✅ Importing
```python
from math_utils import add
```
✅ Function is available

❌ Test code does not run

<!-- #endregion -->

### 6️⃣ Important Insight (Interview Favorite ⭐)

> Python files are both scripts AND modules

This line lets a file behave as:
- ✅ A script
- ✅ A reusable module

<!-- #region -->
### 7️⃣ Visual Summary

```bash
Run directly? ──YES──▶ __name__ == "__main__"
                             │
                             └──▶ Code executes

            Imported? ──NO──▶ __name__ != "__main__"
                             │
                             └──▶ Code skipped
```
<!-- #endregion -->


