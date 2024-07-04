# Python Sandboxed - Code Interpreter

Verify will error when numpy not installed. Do this before verify will fail

```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "code": "import os\nimport numpy as np\na = int(os.getenv(\"VAR_A\"))\nb = int(os.getenv(\"VAR_B\"))\nc = int(os.getenv(\"VAR_C\"))\narray = np.array([a, b, c])\nresult = np.sum(array)\nprint(f\"Result of summing [{a}, {b}, {c}] is: {result}\")",
  "env": {
    "VAR_A": "10",
    "VAR_B": "20",
    "VAR_C": "30"
  }
}'
```

Run with it now installing numpy and see suceed. Run the previous command again to show that its been uninstalled.

```bash
curl -X POST http://localhost:8000/execute -H "Content-Type: application/json" -d '{
  "packages": ["numpy"],
  "code": "import os\nimport numpy as np\na = int(os.getenv(\"VAR_A\"))\nb = int(os.getenv(\"VAR_B\"))\nc = int(os.getenv(\"VAR_C\"))\narray = np.array([a, b, c])\nresult = np.sum(array)\nprint(f\"Result of summing [{a}, {b}, {c}] is: {result}\")",
  "env": {
    "VAR_A": "10",
    "VAR_B": "20",
    "VAR_C": "30"
  }
}'
```